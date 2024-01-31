import requests
import json
from tabulate import tabulate
from Secretes import key
import matplotlib.pyplot as plt


def main():
    url = f"https://www.aistockfinder.com/api/forecasts/{key}/LATEST"

    mode = "file"

    if mode == "site":
        res = requests.get(url)
        json_str = "{\"json\":" + str(res.json()).replace("\'", "\"") + "}"
    elif mode == "file":
        with open("example.json", "r") as f:
            json_str = f.read().strip()

    json_obj = json.loads(json_str)
    table(json_obj)



def table(json_obj):
    for stock in json_obj['json']:
        table_data = [(key, value) for key, value in stock.items()]
        table = tabulate(table_data, headers=["Attribute", "Value"], tablefmt="fancy_grid")
        print(table)


def plot(json_obj):
    arr = json_obj["json"]
    tickers = []  # List to store all tickers
    max_forecasts = []
    min_forecasts = []

    for stock in arr:
        tickers.append(stock["signal_ticker"])
        max_forecasts.append(stock["signal_one_month_forecast_max"])
        min_forecasts.append(stock["signal_one_month_forecast_min"])

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(arr))

    bar1 = ax.bar(index, max_forecasts, bar_width, label='Max Forecast')
    bar2 = ax.bar([i + bar_width for i in index], min_forecasts, bar_width, label='Min Forecast')

    ax.set_xlabel('Stock Tickers')
    ax.set_ylabel('Forecast Values')

    ax.set_title('Max and Min Forecasts for Each Stock')
    ax.set_xticks([i + bar_width / 2 for i in index])

    ax.set_xticklabels(tickers)  # Pass the list of tickers here
    ax.legend()

    plt.show()


if __name__ == "__main__":
    main()
