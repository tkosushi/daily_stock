import csv
import pandas as pd
import finance_api_wrapper as faw

base_dir = "/Users/takumi-mac/PyProject/system_trade/daily_stock/app/data/"

def get_stock_data(ticker: str, start_date: str, end_date: str):
    api = faw.YahooFinanceAPIWrapper()
    data = api.get_stock_data(ticker, start_date, end_date)
    return data

def list_tokyo_stock_ticker_and_scale():
    path = base_dir + "tosho_stocks/data_j.csv"
    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        # (ticker, scale)
        tickers = [(row[1], row[8]) for row in reader]
    return tickers

def get_30percentup_stock_data_smallscale_topix(tickers: list, start_date: str, end_date: str):
    data_30percentup = []
    for i, t in enumerate(tickers):
        print(f"{i+1}/{len(tickers)}")
        ticker, scale = t
        if scale != "-" and int(scale) > 5:
            data = get_stock_data(ticker + ".T", start_date, end_date)
            if data.empty:
                continue
            min_price = data["Close"].min()
            min_price_date = data["Close"].idxmin()
            max_price = data["Close"].max()
            max_price_date = data["Close"].idxmax()
            # 最小値の日付が最大値の日付より後なら無視する
            if min_price_date > max_price_date:
                continue
            # 最小値から最大値までの上昇率が30%以上ならリストに追加する
            if (max_price - min_price) / min_price > 0.3:
                data["Ticker"] = ticker
                data_30percentup.append(data)
    return data_30percentup

if __name__ == "__main__":
    tickers = list_tokyo_stock_ticker_and_scale()
    data_30percentup = get_30percentup_stock_data_smallscale_topix(tickers, "2022-10-01", "2022-12-31")
    for i, d in enumerate(data_30percentup):
        print(f"{i+1}/{len(data_30percentup)}")
        ticker = d["Ticker"][0]
        d.to_csv(base_dir + "30percentup/" + str(ticker) + ".csv")