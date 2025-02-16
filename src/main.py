from utils.csv_utility import CSVUtility
import sys
import os

def print_menu():
    """Display the main menu options."""
    print("\nCSV Utility Menu:")
    print("1. Display first N rows")
    print("2. Filter rows")
    print("3. Sort rows")
    print("4. Aggregate data")
    print("5. Count palindromes")
    print("6. Save to new CSV file")
    print("7. Display available columns")
    print("8. Reset to original data")
    print("9. Exit")
    print("\nEnter your choice (1-9): ")

def get_column_choice(csv_util):
    """Display and get column choice from user."""
    print("\nAvailable columns:")
    for idx, column in enumerate(csv_util.headers, 1):
        print(f"{idx}. {column}")
    while True:
        try:
            choice = int(input("\nEnter column number: ")) - 1
            if 0 <= choice < len(csv_util.headers):
                return csv_util.headers[choice]
            print("Invalid column number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Get input file name
    while True:
        input_file = input("Enter the CSV file name (or path): ").strip()
        try:
            # Check if file exists
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"File '{input_file}' not found")
            
            # Check if file is empty
            if os.path.getsize(input_file) == 0:
                raise ValueError("File is empty")
            
            csv_util = CSVUtility(input_file)
            print(f"\nSuccessfully loaded CSV file with {len(csv_util.data)} rows")
            break
        except Exception as e:
            print(f"\nError: {e}")
            retry = input("Would you like to try again? (y/n): ").lower()
            if retry != 'y':
                sys.exit()

    while True:
        try:
            print_menu()
            choice = input().strip()

            if choice == '1':
                while True:
                    try:
                        n = int(input("Enter number of rows to display: "))
                        if n > 0:
                            csv_util.display_head(n)
                            break
                        print("Please enter a positive number")
                    except ValueError:
                        print("Please enter a valid number")

            elif choice == '2':
                print("\nFilter options:")
                print("1. Greater than (>)")
                print("2. Less than (<)")
                print("3. Equal to (==)")
                print("4. Contains (string)")
                
                filter_choice = input("Enter filter option (1-4): ")
                column = get_column_choice(csv_util)
                
                condition_map = {
                    '1': '>', 
                    '2': '<',
                    '3': '==',
                    '4': 'contains'
                }
                
                if filter_choice in condition_map:
                    value = input("Enter value to compare: ")
                    if filter_choice in ['1', '2']:
                        try:
                            value = float(value)
                        except ValueError:
                            print("Error: Please enter a numeric value")
                            continue
                    
                    filtered_data = csv_util.filter_rows(
                        column, 
                        condition_map[filter_choice], 
                        value
                    )
                    print(f"\nFiltered results ({len(filtered_data)} rows):")
                    csv_util.display_head(len(filtered_data))
                else:
                    print("Invalid filter option!")

            elif choice == '3':
                column = get_column_choice(csv_util)
                order = input("Sort ascending? (y/n): ").lower()
                ascending = order == 'y'
                sorted_data = csv_util.sort_rows(column, ascending)
                print(f"\nSorted results ({len(sorted_data)} rows):")
                csv_util.display_head(min(5, len(sorted_data)))  # Show first 5 rows only
                if len(sorted_data) > 5:
                    print("... (showing first 5 rows)")

            elif choice == '4':
                print("\nAggregation options:")
                print("1. Sum")
                print("2. Mean (Average)")
                print("3. Minimum")
                print("4. Maximum")
                
                agg_choice = input("Enter aggregation option (1-4): ")
                column = get_column_choice(csv_util)
                
                operation_map = {
                    '1': 'sum',
                    '2': 'mean',
                    '3': 'min',
                    '4': 'max'
                }
                
                if agg_choice in operation_map:
                    try:
                        result = csv_util.aggregate_data(column, operation_map[agg_choice])
                        print(f"\nResult for {operation_map[agg_choice]} of '{column}': {result:.2f}")
                    except ValueError as ve:
                        print(f"\nError: {str(ve)}")
                        print("\nNote: Aggregation operations can only be performed on numeric columns.")
                else:
                    print("Invalid aggregation option!")

            elif choice == '5':
                count = csv_util.count_palindromes()
                print(f"\nTotal palindromes found: {count}")

            elif choice == '6':
                output_file = input("Enter name for the output CSV file: ").strip()
                if not output_file.endswith('.csv'):
                    output_file += '.csv'
                
                # Check if file exists
                if os.path.exists(output_file):
                    overwrite = input(f"File '{output_file}' already exists. Overwrite? (y/n): ").lower()
                    if overwrite != 'y':
                        continue
                
                csv_util.write_to_csv(output_file)

            elif choice == '7':
                print("\nAvailable columns:")
                for idx, column in enumerate(csv_util.headers, 1):
                    print(f"{idx}. {column}")

            elif choice == '8':
                csv_util.reset_data()
                print("\nData reset to original state.")
                csv_util.display_head(min(5, len(csv_util.data)))

            elif choice == '9':
                print("\nThank you for using CSV Utility!")
                break

            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print(f"\nError: {e}")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
