from flask import Flask, render_template, request
import requests
import pygal
import os
import csv
from datetime import datetime

app = Flask(__name__)
CHART_FOLDER = os.path.join('static', 'charts')
os.makedirs(CHART_FOLDER, exist_ok=True)

def load_ticker_symbols(filename='stocks.csv'):
    tickers = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tickers.append({"symbol": row["Symbol"], "name": row["Name"]})
    except Exception as e:
        print(f"Error loading ticker symbols: {e}")
    return sorted(tickers, key=lambda x: x["symbol"])

def get_stock_data(ticker, time_series):
    api_key = "JGSKV0LY50824HYL"
    url = "https://www.alphavantage.co/query"
    
    if time_series == "1":
        function = "TIME_SERIES_INTRADAY"
        time_key = "Time Series (60min)"
        params = {
            "function": function,
            "symbol": ticker,
            "interval": "60min",
            "apikey": api_key
        }
    elif time_series == "2":
        function = "TIME_SERIES_DAILY" 
        time_key = "Time Series (Daily)"
        params = {
            "function": function,
            "symbol": ticker,
            "apikey": api_key
        }
    elif time_series == "3":
        function = "TIME_SERIES_WEEKLY"
        time_key = "Weekly Time Series"
        params = {
            "function": function,
            "symbol": ticker,
            "apikey": api_key
        }
    else:
        function = "TIME_SERIES_MONTHLY"
        time_key = "Monthly Time Series"
        params = {
            "function": function,
            "symbol": ticker,
            "apikey": api_key
        }
    
    response = requests.get(url, params=params)
    data = response.json()

    return data, time_key

def filter_data_by_date(data, time_key, time_series, start_date, end_date):
    filtered_data = {}

    for date in data.get(time_key, {}):
        if time_series == "1":
            date_only = date.split()[0]
            if start_date <= date_only <= end_date:
                filtered_data[date] = data[time_key][date]
        else:
            if start_date <= date <= end_date:
                filtered_data[date] = data[time_key][date]

    return filtered_data

def create_chart(ticker, chart_type, filtered_data, start_date, end_date, output_path):
    if not filtered_data:
        return None

    dates = sorted(filtered_data.keys())
    closing_prices = []

    for date in dates:
        close_key = "4. close"
        if close_key not in filtered_data[date]:
            close_key = "4. Close"
        closing_prices.append(float(filtered_data[date][close_key]))

    chart = pygal.Bar(x_label_rotation=45) if chart_type == "1" else pygal.Line(x_label_rotation=45)
    chart.title = f"{ticker} Stock Prices ({start_date} to {end_date})"
    chart.x_labels = dates
    chart.add('Closing Price', closing_prices)
    chart.render_to_file(output_path)

    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    tickers = load_ticker_symbols()
    chart_file = None
    error = None

    if request.method == 'POST':
        try:
            ticker = request.form['ticker']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

            data, time_key = get_stock_data(ticker, time_series)
            filtered_data = filter_data_by_date(data, time_key, time_series, start_date, end_date)

            filename = f"{ticker}_chart.svg"
            output_path = os.path.join(CHART_FOLDER, filename)
            chart_file = create_chart(ticker, chart_type, filtered_data, start_date, end_date, output_path)
            if chart_file:
                chart_file = chart_file.replace("static/", "")

        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template("index.html", tickers=tickers, chart_file=chart_file, error=error)

if __name__ == '__main__':
    app.run(host="0.0.0.0")