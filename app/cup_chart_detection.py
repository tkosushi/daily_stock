import pandas as pd
import os
import csv
import finance_api_wrapper as faw
from datetime import datetime
base_dir = "/Users/takumi-mac/PyProject/system_trade/daily_stock/app/data/"

# 東証グロース　スタンダード　プライム市場の銘柄のみ取得
path = base_dir + "tosho_stocks/data_j.csv"
tickers = None
with open(path, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    # (ticker, scale)
    tickers = [row[1] for row in reader if row[3] == "グロース（内国株式）" or row[3] == "スタンダード（内国株式）" or row[3] == "プライム（内国株式）"]

for i, p in enumerate(stock_data_path_list):
    print(f"{i+1}/{len(stock_data_path_list)}")
    data = pd.read_csv(p, index_col=0)
    max_price_date = datetime.strptime(data["Close"].idxmax(), "%Y-%m-%d")

    api = faw.YahooFinanceAPIWrapper()
    # amd (after max data)
    amd = api.get_stock_data(
        str(data["Ticker"][0]) + ".T",
        max_price_date.strftime("%Y-%m-%d"),
        (max_price_date + pd.Timedelta(days=180)).strftime("%Y-%m-%d")
    )
    if amd.empty:
        continue
    # 7日移動平均を追加
    amd["MA"] = amd["Close"].rolling(7).mean()

    # 1~3ヶ月前と比べて30%以上上昇しているか
    for i in range(30, 90):
        amd["UP_flag_" + str(i)] = amd["Close"].pct_change(periods=i) > 0.3
    amd["UP"] = amd.filter(like="UP_flag_").any(axis=1)

    # 30%上昇後に急落フェーズを迎えたか判定
    amd["Drop"] = amd["MA"].pct_change(periods=7) < -0.1 & amd["UP"].shift(7)
    # 停滞フェーズを定義
    for i in range(7, 31):
        amd["Stagnation_flag_" + str(i)] = amd["Drop"].shift(i)
    amd["Stagnation"] = amd["MA"].pct_change(periods=7).between(-0.02, 0.02) & amd.filter(like="Stagnation_flag").any(axis=1)
    # 回復フェーズを定義
    for i in range(7, 31):
        amd["Recovery_flag_" + str(i)] = amd["Stagnation"].shift(i)
    amd["Recovery"] = (amd["MA"].pct_change(periods=7) > 0.1) & amd.filter(like="Recovery_flag").any(axis=1)

    amd = amd.drop(columns=amd.filter(like="flag").columns)
    
    # Recovery列にTrueがあれば保存する
    if amd["Recovery"].any():
        amd.to_csv(base_dir + "cup_pattern/" + str(data["Ticker"][0]) + ".csv")