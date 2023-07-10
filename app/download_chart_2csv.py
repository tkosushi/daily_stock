import sys
import finance_api_wrapper as faw

base_dir = "/Users/takumi-mac/PyProject/system_trade/daily_stock/app/data/"

# Download chart data for a single stock
# Usage: python download_chart_2csv.py [ticker] [start_date] [end_date] [filename]
# Example: python download_chart_2csv.py 7203.T 2020-01-01 2020-12-31 7203.T.csv
def download_chart_2csv(ticker: str, start_date: str, end_date: str, filename: str):
    api = faw.YahooFinanceAPIWrapper()
    data = api.get_stock_data(ticker, start_date, end_date)
    data.to_csv(base_dir + filename)

if __name__ == "__main__":
    args = sys.argv
    download_chart_2csv(args[1], args[2], args[3], args[4])
    print("Done")
