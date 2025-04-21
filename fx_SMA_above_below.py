import os
import pandas as pd
import numpy as np
from fx_select_csv_and_column import select_csv_and_column

# Script location
script_location = os.path.dirname(os.path.abspath(__file__))

# Select columns from CSV files
df_raw, close = select_csv_and_column()
df_SMA_100, SMA_100 = select_csv_and_column()
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
output_path = os.path.join(script_location, 'test.csv')
combined_data.to_csv(output_path, index=False)
