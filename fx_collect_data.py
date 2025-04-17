import yfinance as yf
import os

# Script location
script_location = os.path.dirname(os.path.abspath(__file__))

def collect_data(ticker_input=None, start_date=None, end_date=None):
    # If parameters are not provided, ask for user input
    if ticker_input is None:
        ticker_input = input('Enter ticker: ')
    if start_date is None:
        start_date = input('Enter start date (YYYY-MM-DD): ')
    if end_date is None:
        end_date = input('Enter end date (YYYY-MM-DD): ')

    # Download data
    data = yf.download(ticker_input, start=start_date, end=end_date)

    # Reset index and select columns
    data = data.reset_index()[['Date', 'Open', 'Close']]

    # Rename columns
    data.columns = ['date', 'open', 'close']

    # Format date and round numeric values
    data['date'] = data['date'].dt.strftime('%d-%m-%Y')
    data = data.round(2)  # Rounds all numeric columns to 2 decimal places

    # Generate file name based on ticker
    file_path = os.path.join(script_location, f"raw_data_out_{ticker_input}.csv")

    # Export data to CSV
    data.to_csv(file_path, index=False)

    print(f"Data saved to {file_path}")
