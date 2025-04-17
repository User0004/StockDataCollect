import pandas as pd
import os

def get_higher_lower():

    print('Get Higher and Lower counts')

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
        column_choice = int(input("Enter the number of the column to calculate Higher/Lower: "))
        if not 1 <= column_choice <= len(list_column_headers):
            print("Invalid selection.")
            return
        selected_column = list_column_headers[column_choice - 1]
    except ValueError:
        print("Please enter a valid number.")
        return

    # Ensure column is numeric
    df[selected_column] = pd.to_numeric(df[selected_column], errors='coerce')

    # Generate Movement column (Higher/Lower/Same)
    movement_col = 'Movement'
    df[movement_col] = df[selected_column].diff().apply(
        lambda x: 'Higher' if x > 0 else 'Lower' if x < 0 else 'Same'
    )

    # Calculate streaks
    streak_col = 'Streak'
    streaks = []
    current_streak = 0
    previous_result = None

    for result in df[movement_col]:
        if result == previous_result:
            current_streak += 1
        else:
            current_streak = 1
        streaks.append(current_streak)
        previous_result = result

    df[streak_col] = streaks

    # Only keep selected columns
    if 'date' not in df.columns:
        print("\nWarning: No 'date' column found — it won't be included in output.")
        final_df = df[[selected_column, movement_col, streak_col]]
    else:
        final_df = df[['date', selected_column, movement_col, streak_col]]

    # Save to new file
    new_filename = f"Higher Lower {selected_column}.csv"
    new_file_path = os.path.join(script_location, new_filename)
    final_df.to_csv(new_file_path, index=False)

    print(f"\nOutput saved to '{new_filename}' with columns: {', '.join(final_df.columns)}.")
