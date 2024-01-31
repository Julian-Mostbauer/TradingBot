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

    plot(json_obj)



def table(json_obj):
    for stock in json_obj['json']:
        table_data = [(key, value) for key, value in stock.items()]
        table = tabulate(table_data, headers=["Attribute", "Value"], tablefmt="fancy_grid")
        print(table)


def plot(json_obj):
    if "json" not in json_obj:
        raise ValueError("Key 'json' not found in the JSON object.")

    arr = json_obj["json"]
    tickers = []  # List to store all tickers
    max_forecasts = {"one_month": [], "two_weeks": [], "one_week": [], "three_days": []}
    min_forecasts = {"one_month": [], "two_weeks": [], "one_week": [], "three_days": []}

    for stock in arr:
        tickers.append(stock["signal_ticker"])
        max_forecasts["one_month"].append(stock["signal_one_month_forecast_max"])
        min_forecasts["one_month"].append(stock["signal_one_month_forecast_min"])
        max_forecasts["two_weeks"].append(stock["signal_two_weeks_forecast_max"])
        min_forecasts["two_weeks"].append(stock["signal_two_weeks_forecast_min"])
        max_forecasts["one_week"].append(stock["signal_one_week_forecast_max"])
        min_forecasts["one_week"].append(stock["signal_one_week_forecast_min"])
        max_forecasts["three_days"].append(stock["signal_three_days_forecast_max"])
        min_forecasts["three_days"].append(stock["signal_three_days_forecast_min"])

    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    bar_width = 0.35
    index = range(len(arr))

    # Plot for One Month Forecast
    ax1 = axs[0, 0]
    ax1.bar(index, max_forecasts["one_month"], bar_width, label='Max Forecast')
    ax1.bar([i + bar_width for i in index], min_forecasts["one_month"], bar_width, label='Min Forecast')
    ax1.set_title('One Month Forecast')
    ax1.set_xticks([i + bar_width / 2 for i in index])
    ax1.set_xticklabels(tickers)
    ax1.legend()

    # Plot for Two Weeks Forecast
    ax2 = axs[0, 1]
    ax2.bar(index, max_forecasts["two_weeks"], bar_width, label='Max Forecast')
    ax2.bar([i + bar_width for i in index], min_forecasts["two_weeks"], bar_width, label='Min Forecast')
    ax2.set_title('Two Weeks Forecast')
    ax2.set_xticks([i + bar_width / 2 for i in index])
    ax2.set_xticklabels(tickers)
    ax2.legend()

    # Plot for One Week Forecast
    ax3 = axs[1, 0]
    ax3.bar(index, max_forecasts["one_week"], bar_width, label='Max Forecast')
    ax3.bar([i + bar_width for i in index], min_forecasts["one_week"], bar_width, label='Min Forecast')
    ax3.set_title('One Week Forecast')
    ax3.set_xticks([i + bar_width / 2 for i in index])
    ax3.set_xticklabels(tickers)
    ax3.legend()

    # Plot for Three Days Forecast
    ax4 = axs[1, 1]
    ax4.bar(index, max_forecasts["three_days"], bar_width, label='Max Forecast')
    ax4.bar([i + bar_width for i in index], min_forecasts["three_days"], bar_width, label='Min Forecast')
    ax4.set_title('Three Days Forecast')
    ax4.set_xticks([i + bar_width / 2 for i in index])
    ax4.set_xticklabels(tickers)
    ax4.legend()

    plt.show()

if __name__ == "__main__":
    main()
