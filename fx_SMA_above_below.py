import os
import pandas as pd
import numpy as np
from fx_select_csv_and_column import select_csv_and_column

def compare_close_to_sma():
    # Script location
    script_location = os.path.dirname(os.path.abspath(__file__))
    output_filename = 'compare_close_to_sma.csv'
    output_path = os.path.join(script_location, output_filename)

    # Select columns from CSV files
    print('Enter the close price')
    df_raw, close = select_csv_and_column()
    print('Enter the SMA value')
    df_SMA_100, SMA_100 = select_csv_and_column()
    print('Enter the date')
    df_raw_date, date = select_csv_and_column()

    # Extract relevant columns
    data_set_1 = df_raw[[close]]
    data_set_2 = df_SMA_100[[SMA_100]]
    data_set_date = df_raw[[date]]

    # Combine into one DataFrame
    combined_data = pd.concat([data_set_date, data_set_1, data_set_2], axis=1)
    combined_data.columns = ['date', 'close', 'SMA 100']

    # Add a column showing whether close is higher or lower than SMA 100
    combined_data['close_vs_sma'] = np.where(
        combined_data['close'] > combined_data['SMA 100'],
        'higher',
        'lower'
    )

    # Save to CSV
    combined_data.to_csv(output_path, index=False)
    print(f'Saved as {output_filename}')

    return combined_data


compare_close_to_sma()
