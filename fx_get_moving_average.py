import pandas as pd
import os

def get_moving_average():
    # Script location
    script_location = os.path.dirname(os.path.abspath(__file__))

    # List CSV files
    csv_files = [f for f in os.listdir(script_location) if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in this directory.")
        return

    print("\nAvailable CSV files:")
    for i, file in enumerate(csv_files, start=1):
        print(f"{i}. {file}")

    try:
        file_choice = int(input("\nEnter the number of the CSV file you want to use: "))
        if not 1 <= file_choice <= len(csv_files):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_file = csv_files[file_choice - 1]
    file_path = os.path.join(script_location, selected_file)

    # Read CSV
    df = pd.read_csv(file_path)
    list_column_headers = df.columns.to_list()

    print("\nAvailable columns:")
    for i, col in enumerate(list_column_headers, start=1):
        print(f"{i}. {col}")

    try:
        column_choice = int(input("Enter the number of the column to gather SMA: "))
        if not 1 <= column_choice <= len(list_column_headers):
            print("Invalid selection.")
            return
        user_column_header_select = list_column_headers[column_choice - 1]
    except ValueError:
        print("Please enter a valid number.")
        return

    try:
        input_from_user = int(input('Enter day count for SMA: '))
    except ValueError:
        print("Invalid number. Exiting.")
        return

    df[user_column_header_select] = pd.to_numeric(df[user_column_header_select], errors='coerce')

    # Generate a dynamic column name
    sma_column_name = f'SMA_{input_from_user}_{user_column_header_select}'

    df[sma_column_name] = df[user_column_header_select].rolling(window=input_from_user).mean()
    df[sma_column_name] = df[sma_column_name].round(2)

    # Remove the old generic 'SMA' column if it exists
    if 'SMA' in df.columns:
        df = df.drop(columns=['SMA'])

    # Save to new file
    new_filename = f"{sma_column_name}.csv"
    new_file_path = os.path.join(script_location, new_filename)
    df.to_csv(new_file_path, index=False)

    print(f"\n{sma_column_name} column added and saved to '{new_filename}'.")


get_moving_average()
