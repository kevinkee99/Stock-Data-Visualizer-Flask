import requests
import pygal
import webbrowser
import os

# fx that handles user input, returns ticker, chart type, time start/end
def get_user_input():
    print("\nWelcome to the Alphavantage Stock Data Visualizer\n")
    ticker = input("Enter stock ticker: ")
    
    print("\Enter chart type: ")
    print("1. Bar")
    print("2. Line")
    chart_type = input("Enter type of chart you want, 1 or 2: ")
    
    print("\nSelect the time series you want")
    print("1. intraday")
    print("2. daily")
    print("3. weekly")
    print("4. monthly")
    time_series = input("Enter the time series option, 1,2,3,4: ")
    
    start_date = input("\nEnter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    return ticker, chart_type, time_series, start_date, end_date

# fx that accesses the api. time series is tricky here
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
    else:  # time_series = 4
        function = "TIME_SERIES_MONTHLY"
        time_key = "Monthly Time Series"
        params = {
            "function": function,
            "symbol": ticker,
            "apikey": api_key
        }
    
    # THis is the part that actually gets the data
    response = requests.get(url, params=params)
    data = response.json()
    
    return data, time_key

# fx to handle the data by the date and series
def filter_data_by_date(data, time_key, time_series, start_date, end_date):
    filtered_data = {}
    
    for date in data[time_key]:
        if time_series == "1":
            date_only = date.split()[0]
            
            if date_only >= start_date and date_only <= end_date:
                filtered_data[date] = data[time_key][date]
        
        else:
            if date >= start_date and date <= end_date:
                filtered_data[date] = data[time_key][date]
    
    return filtered_data

# fx that renders out chart. will handle both bar and line charts. 
    # i outlines what all it should take and a general format. 
def create_chart(ticker, chart_type, filtered_data, time_series, start_date, end_date):

    # here, you will put something like if chart type 1 then = bar
    # and if chart type is 2 then = line 

    # create the chart using pygal. seek pygal docs for how to do this. 
        # needs to take a title, start/end, filtered data as a dict, and more
    # will prob need timeseries ref from above too


    # will need to use something like this V at the end of the code.
        # renders as svg that saves locally then opens in browser. this is how Culmer does it
    chart_file = f"{ticker}_chart.svg"
    chart.render_to_file(chart_file)

    file_path = os.path.abspath(chart_file)
    webbrowser.open('file://' + file_path)
    
    print("chart fx not yet implemented")

# this is the main function that runs the program
def main():
    ticker, chart_type, time_series, start_date, end_date = get_user_input()
    data, time_key = get_stock_data(ticker, time_series)
    filtered_data = filter_data_by_date(data, time_key, time_series, start_date, end_date)
    create_chart(ticker, chart_type, filtered_data, time_series, start_date, end_date)

if __name__ == "__main__":
    main()