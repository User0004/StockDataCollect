import os
import pandas as pd
import matplotlib.pyplot as plt

def streak_histogram():

    print('Map Higher Lower movement streaks')

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

    # Load CSV
    df = pd.read_csv(file_path)
    print('\nAvailable columns:', df.columns.to_list())

    # Ensure 'Movement' and 'Streak' columns are available
    if 'Movement' not in df.columns or 'Streak' not in df.columns:
        print("Missing required columns: 'Movement' or 'Streak'.")
        return

    # Separate the DataFrame into 'Higher' and 'Lower' movements
    higher_df = df[df['Movement'] == 'Higher']
    lower_df = df[df['Movement'] == 'Lower']

    # Count the frequency of each streak length for 'Higher' movements
    higher_streak_counts = higher_df['Streak'].value_counts().sort_index()
    lower_streak_counts = lower_df['Streak'].value_counts().sort_index()

    # Create dataframes for the streak frequencies
    higher_result_df = pd.DataFrame({
        'Streak': higher_streak_counts.index,
        'Frequency': higher_streak_counts.values,
        'Movement': 'Higher'
    })

    lower_result_df = pd.DataFrame({
        'Streak': lower_streak_counts.index,
        'Frequency': lower_streak_counts.values,
        'Movement': 'Lower'
    })

    # Combine both DataFrames into one
    result_df = pd.concat([higher_result_df, lower_result_df], ignore_index=True)

    # Save the results to CSV
    safe_col_name = "higher_lower_streaks"
    output_file = os.path.join(script_location, f"{safe_col_name}_histogram_table.csv")
    result_df.to_csv(output_file, index=False)

    print(f"\n✅ Frequency table saved to: {output_file}")

    # Plot the histograms for 'Higher' and 'Lower' movements
    plt.figure(figsize=(12, 6))

    # Plot for 'Higher' movements
    plt.subplot(1, 2, 1)
    bars = plt.bar(higher_result_df['Streak'], higher_result_df['Frequency'], color='lightgreen', edgecolor='black')
    plt.title("Higher Movement Streaks")
    plt.xlabel("Streak Length")
    plt.xticks(higher_result_df['Streak'])
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 10, str(int(height)), ha='center', va='bottom')
    plt.gca().get_yaxis().set_visible(False)  # Hide y-axis

    # Plot for 'Lower' movements
    plt.subplot(1, 2, 2)
    bars = plt.bar(lower_result_df['Streak'], lower_result_df['Frequency'], color='lightcoral', edgecolor='black')
    plt.title("Lower Movement Streaks")
    plt.xlabel("Streak Length")
    plt.xticks(lower_result_df['Streak'])
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 10, str(int(height)), ha='center', va='bottom')
    plt.gca().get_yaxis().set_visible(False)  # Hide y-axis

    # Add a title for the entire chart based on the selected file
    plt.suptitle(f"{selected_file} - Higher Lower Streaks", fontsize=16)

    plt.tight_layout()
    plt.show()

streak_histogram()