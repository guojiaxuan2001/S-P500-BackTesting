import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data():
    # 读取S&P 500成分股数据
    df = pd.read_csv('spx-companies.csv')
    df['Symbol'] = df['Symbol'].replace({'BRK.B': 'BRK-B', 'BF.B': 'BF-B'})
    tickers = df['Symbol'].dropna().unique().tolist()
    
    # 下载历史数据
    data = yf.download(tickers, period="2y", group_by='ticker', auto_adjust=True, threads=True)
    
    # 整理数据格式
    all_data = []
    for ticker in tickers:
        if ticker in data.columns.levels[0]:
            df = data[ticker].copy()
            df['Symbol'] = ticker
            df['Date'] = df.index
            all_data.append(df.reset_index(drop=True))
    
    result_df = pd.concat(all_data, ignore_index=True)
    result_df = result_df.sort_values(by=['Date', 'Symbol'])
    
    # 计算日收益率
    result_df['Return'] = result_df.groupby('Symbol')['Close'].pct_change()
    
    return result_df

def get_daily_worst_performers(df, n=10):
    # 获取每天表现最差的n只股票
    daily_worst = df.groupby('Date').apply(
        lambda x: x.nsmallest(n, 'Return')[['Symbol', 'Close', 'Return']]
    ).reset_index(level=1, drop=True).reset_index()
    return daily_worst

def simulate_strategy(df, initial_capital=1000000.00):
    # 按日期排序
    df = df.sort_values('Date')
    unique_dates = df['Date'].unique()
    
    # 创建交易记录和组合价值DataFrame
    trades = []
    portfolio_values = []
    current_capital = initial_capital
    
    for i in range(len(unique_dates)-1):
        current_date = unique_dates[i]
        next_date = unique_dates[i+1]
        
        # 获取当天最差表现的10只股票
        daily_stocks = df[df['Date'] == current_date]
        worst_10 = daily_stocks.nsmallest(10, 'Return')
        
        # 计算每只股票的投资金额
        amount_per_stock = current_capital / 10
        
        # 记录交易
        for _, stock in worst_10.iterrows():
            shares = amount_per_stock / stock['Close']
            trades.append({
                'Date': current_date,
                'Symbol': stock['Symbol'],
                'Close': stock['Close'],
                'Shares': shares,
                'Investment': amount_per_stock
            })
        
        # 计算下一天的组合价值
        next_day_prices = df[
            (df['Date'] == next_date) & 
            (df['Symbol'].isin(worst_10['Symbol']))
        ].set_index('Symbol')['Close']
        
        portfolio_value = sum(
            shares * next_day_prices[symbol] 
            for shares, symbol in zip(
                [amount_per_stock/price for price in worst_10['Close']], 
                worst_10['Symbol']
            )
        )
        
        portfolio_values.append({
            'Date': next_date,
            'Portfolio_Value': portfolio_value
        })
        
        current_capital = portfolio_value
    
    trades_df = pd.DataFrame(trades)
    portfolio_values_df = pd.DataFrame(portfolio_values)
    
    return trades_df, portfolio_values_df

def main():
    # 获取股票数据
    stock_data = get_stock_data()
    
    # 运行策略模拟
    trades_df, portfolio_values_df = simulate_strategy(stock_data)
    
    # 保存结果
    trades_df.to_csv('trading_records.csv', index=False)
    portfolio_values_df.to_csv('portfolio_values.csv', index=False)
    
    # 打印策略表现
    initial_value = 1000000.00
    final_value = portfolio_values_df['Portfolio_Value'].iloc[-1]
    total_return = (final_value - initial_value) / initial_value * 100
    
    print(f"策略表现摘要:")
    print(f"初始资金: ${initial_value:,.2f}")
    print(f"最终资金: ${final_value:,.2f}")
    print(f"总收益率: {total_return:.2f}%")

if __name__ == "__main__":
    main() 