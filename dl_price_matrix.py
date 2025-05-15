def dl_price_matrix(tickers, start_date, end_date):
    import pandas as pd
    import yfinance as yf
    import time

    data_list = []

    for ticker in tickers:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            continue
        df = df.reset_index()
        df['Ticker'] = ticker
        data_list.append(df)
        time.sleep(1)

    all_data = pd.concat(data_list, ignore_index=True)
    price_matrix = all_data.pivot(index='Date', columns='Ticker', values='Close')
    return price_matrix