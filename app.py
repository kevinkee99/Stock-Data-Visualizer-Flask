from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import pygal
from datetime import datetime
from lxml import etree
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# API
API_KEY = 'JGSKV0LY50824HYL'
BASE_URL = 'https://www.alphavantage.co/query'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        function = request.form['function']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        data = None  # API logic here

        if not data:
            flash(f"No data found for symbol: {symbol}", "error")
            return redirect(url_for('index'))

        chart = None  # Chart gen logic here

        return render_template('chart_display.html', chart=chart)

    return render_template('index.html')

def get_data(symbol, function, start_date, end_date):
    """
    placeholder function to query the Alpha Vantage API.
    """
    return None


def generate_line_chart(data):
    """
    placeholder function to generate a line chart, use pygal
    """
    return None


def generate_bar_chart(data):
    """
    placeholder function to generate a bar chart, use pygal
    """
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5019)