import requests
import pygal
import webbrowser
import os

# fx that handles user input, returns ticker, chart type, time start/end
def get_user_input():
    print("Welcome to the Alphavantage Stock Data Visualizer\n")

    while True:
        ticker = input("Enter the stock symbol you are looking for: ").strip()
        
        if ticker:
            break
        else:
            print("Ticker cannot be empty. Please enter a valid stock symbol.")
    
    while True:
        print("Chart Types")
        print("---------")
        print("1. Bar")
        print("2. Line")
        chart_type = input("Enter the chart type you want (1, 2): ")
        
        if chart_type in ["1", "2"]:
            break
        else:
            print("Invalid input. Please enter 1 for Bar or 2 for Line.")

    while True:
        print("\nSelect the time series of the chart you want to generate")
        print("---------------------------------------")
        print("1. intraday")
        print("2. daily")
        print("3. weekly")
        print("4. monthly")
        time_series = input("Enter the time series option (1, 2, 3, 4): ")
        
        if time_series in ["1", "2", "3", "4"]:
            break
        else:
            print("Invalid input. Please select 1, 2, 3, or 4 for time series.")
    
    while True:
        start_date = input("\nEnter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        try:
            from datetime import datetime
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start_date_obj <= end_date_obj:
                break
            else:
                print("End date must be after start date. Please try again.")
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
    
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

# Bar Chart (Option 1)
def create_chart(ticker, chart_type, filtered_data, start_date, end_date):
    if not filtered_data:
        print("No data available for the selected date range.")
        return

    # Chart title
    title = f"{ticker} Stock Prices ({start_date} to {end_date})"

    # Extract dates and values
    dates = sorted(filtered_data.keys())  # Sorting ensures chronological order
    values = [float(filtered_data[date]["1. open"]) for date in dates if start_date <= date <= end_date]

    if chart_type == "1":  # Bar chart
        bar_chart = pygal.Bar()
        bar_chart.title = title
        bar_chart.x_labels = map(str, dates)
        bar_chart.add('Opening Price', values)

        # Save and open the chart
        chart_file = f"{ticker}_chart.svg"
        bar_chart.render_to_file(chart_file)

        file_path = os.path.abspath(chart_file)
        webbrowser.open('file://' + file_path)
        
        print(f"Bar chart generated and saved as {chart_file}")

    elif chart_type == "2":  # Line chart - needs to be fixed
        line_chart = pygal.Line()
        line_chart.title = title
        line_chart.x_labels = map(str, dates)
        line_chart.add('Opening Price', values)

        # Save and open the chart
        chart_file = f"{ticker}_chart.svg"
        line_chart.render_to_file(chart_file)

        file_path = os.path.abspath(chart_file)
        webbrowser.open('file://' + file_path)

        print(f"Line chart generated and saved as {chart_file}")

    else:
        print("Invalid chart type selected. Please choose 1 for Bar Chart or 2 for Line Chart.")

    # and if chart type is 2 then = line 

    # create the chart using pygal. seek pygal docs for how to do this. 
        # needs to take a title, start/end, filtered data as a dict, and more
    # will prob need timeseries ref from above too


    # will need to use something like this V at the end of the code.
        # renders as svg that saves locally then opens in browser. this is how Culmer does it
    ####chart_file = f"{ticker}_chart.svg"
    #chart.render_to_file(chart_file)

    #file_path = os.path.abspath(chart_file)
    #webbrowser.open('file://' + file_path)
    
    #print("chart fx not yet implemented")

# this is the main function that runs the program
def main():
    ticker, chart_type, time_series, start_date, end_date = get_user_input()
    data, time_key = get_stock_data(ticker, time_series)
    filtered_data = filter_data_by_date(data, time_key, time_series, start_date, end_date)
    create_chart(ticker, chart_type, filtered_data, start_date, end_date)

if __name__ == "__main__":
    main()