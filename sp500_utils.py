import os
import pandas as pd
import time
from sp500_utils import get_price_from_alpha_vantage

def download_multiple_prices(ticker_list, api_key, save_dir="prices", sleep_sec=12):
    """
    批量下载多个股票的历史日线价格，并保存为CSV文件。

    参数：
        ticker_list: 股票代码列表
        api_key: Alpha Vantage 的 API Key
        save_dir: 保存CSV的目录（默认 "prices" 文件夹）
        sleep_sec: 每个请求之间的等待时间（防止触发API限流）

    返回：
        下载成功的股票列表
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    success = []
    for i, ticker in enumerate(ticker_list):
        print(f"[{i+1}/{len(ticker_list)}] Downloading {ticker}...")
        df = get_price_from_alpha_vantage(ticker, api_key)
        if not df.empty:
            file_path = os.path.join(save_dir, f"{ticker}.csv")
            df.to_csv(file_path)
            print(f"✅ Saved: {file_path}")
            success.append(ticker)
        else:
            print(f"⚠️ Skipped {ticker} (empty or failed)")
        time.sleep(sleep_sec)  # 防止请求过快被限流

    print(f"\n🎉 Done! {len(success)}/{len(ticker_list)} tickers downloaded.")
    return success