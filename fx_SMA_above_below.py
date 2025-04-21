import os
import pandas as pd
import numpy as np
from fx_select_csv_and_column import select_csv_and_column


def compare_close_to_sma():
    # Script location
    script_location = os.path.dirname(os.path.abspath(__file__))

    # Select columns from CSV files
    print('Enter the close price')
    df_raw, close = select_csv_and_column()
    if df_raw is None or close is None:
        print('Invalid selection for close price.')
        return

    # Dynamically select SMA CSV file
    print('Enter the SMA value (e.g., 20, 100, 200)')
    df_SMA, SMA_value = select_csv_and_column()
    if df_SMA is None or SMA_value is None:
        print('Invalid selection for SMA value.')
        return

    # Extract the numerical value from the selected SMA file name (assuming it's part of the file name)
    SMA_number = ''.join(filter(str.isdigit, SMA_value))  # Extract numbers from the SMA column name or file name

    # Extract relevant columns
    data_set_1 = df_raw[[close]]
    data_set_2 = df_SMA[[SMA_value]]

    # Assuming date is always selected from df_raw
    print('Enter the date')
    df_raw_date, date = select_csv_and_column()
    if df_raw_date is None or date is None:
        print('Invalid selection for date.')
        return
    data_set_date = df_raw[[date]]

    # Combine into one DataFrame
    combined_data = pd.concat([data_set_date, data_set_1, data_set_2], axis=1)
    combined_data.columns = ['date', 'close', f'SMA {SMA_number}']  # Dynamically name the SMA column

    # Dynamically set the column header for the comparison
    close_vs_sma_column = f'close_vs_sma_{SMA_number}'  # Changed to close_vs_sma_{SMA_number}

    # Add a column showing whether close is higher or lower than SMA
    combined_data[close_vs_sma_column] = np.where(
        combined_data['close'] > combined_data[f'SMA {SMA_number}'],
        'higher',
        'lower'
    )

    # Dynamically update output file name to include the extracted SMA number
    output_filename = f'compare_close_to_SMA_{SMA_number}.csv'  # Corrected the file name format
    output_path = os.path.join(script_location, output_filename)

    # Save to CSV
    combined_data.to_csv(output_path, index=False)
    print(f'Saved as {output_filename}')

    return combined_data


compare_close_to_sma()
