import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def load_strategy_results():
    """加载之前生成的策略结果"""
    return pd.read_csv('portfolio_values.csv')

def get_sp500_performance(start_date, initial_capital=1000000.00):
    """获取S&P 500指数的表现"""
    # 下载S&P 500指数数据 (使用SPY ETF作为代理)
    spy = yf.download('^GSPC', start=start_date, auto_adjust=True)
    
    # 计算投资组合价值
    initial_spy_price = spy['Close'].iloc[0]
    shares = initial_capital / initial_spy_price
    spy['Portfolio_Value'] = spy['Close'] * shares
    spy['Date'] = spy.index
    
    return spy[['Date', 'Portfolio_Value']]

def plot_comparison(strategy_data, sp500_data):
    """Write Picture"""
    plt.figure(figsize=(12, 6))
    
    # 将日期转换为datetime格式
    strategy_data['Date'] = pd.to_datetime(strategy_data['Date'])
    sp500_data['Date'] = pd.to_datetime(sp500_data['Date'])
    
    # 绘制两条线
    plt.plot(strategy_data['Date'], strategy_data['Portfolio_Value'], 
             label='My Own Strategy', linewidth=2)
    plt.plot(sp500_data['Date'], sp500_data['Portfolio_Value'], 
             label='S&P 500', linewidth=2)
    
    # 设置图表格式
    plt.title('My Own Strategy vs S&P 500', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # 格式化y轴为货币格式
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # 旋转x轴日期标签
    plt.xticks(rotation=45)
    
    # 自动调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('strategy_comparison.png')
    plt.close()

def calculate_performance_metrics(strategy_data, sp500_data):
    """计算性能指标"""
    # 计算总收益率
    strategy_return = (strategy_data['Portfolio_Value'].iloc[-1] / 1000000.0 - 1) * 100
    sp500_return = (sp500_data['Portfolio_Value'].iloc[-1] / 1000000.0 - 1) * 100
    
    # 计算每日收益率
    strategy_daily_returns = strategy_data['Portfolio_Value'].pct_change()
    sp500_daily_returns = sp500_data['Portfolio_Value'].pct_change()
    
    # 计算年化波动率
    strategy_volatility = strategy_daily_returns.std() * np.sqrt(252) * 100
    sp500_volatility = sp500_daily_returns.std() * np.sqrt(252) * 100
    
    # 计算夏普比率（假设无风险利率为2%）
    risk_free_rate = 0.02
    strategy_sharpe = (strategy_daily_returns.mean() * 252 - risk_free_rate) / (strategy_daily_returns.std() * np.sqrt(252))
    sp500_sharpe = (sp500_daily_returns.mean() * 252 - risk_free_rate) / (sp500_daily_returns.std() * np.sqrt(252))
    
    return {
        '策略': {
            '总收益率': f'{strategy_return:.2f}%',
            '年化波动率': f'{strategy_volatility:.2f}%',
            '夏普比率': f'{strategy_sharpe:.2f}'
        },
        'S&P 500': {
            '总收益率': f'{sp500_return:.2f}%',
            '年化波动率': f'{sp500_volatility:.2f}%',
            '夏普比率': f'{sp500_sharpe:.2f}'
        }
    }

def main():
    # 加载策略结果
    strategy_data = load_strategy_results()
    
    # 获取开始日期
    start_date = pd.to_datetime(strategy_data['Date'].iloc[0])
    
    # 获取S&P 500数据
    sp500_data = get_sp500_performance(start_date)
    
    # 绘制对比图
    plot_comparison(strategy_data, sp500_data)
    
    # 计算并打印性能指标
    metrics = calculate_performance_metrics(strategy_data, sp500_data)
    
    print("\n性能指标对比:")
    print("-" * 50)
    for strategy_name, metrics_dict in metrics.items():
        print(f"\n{strategy_name}:")
        for metric_name, value in metrics_dict.items():
            print(f"{metric_name}: {value}")

if __name__ == "__main__":
    main() 