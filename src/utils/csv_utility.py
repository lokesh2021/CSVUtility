import csv
from typing import List, Union, Optional
import copy
import pandas as pd

class CSVUtility:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.original_data = []
        self.data = []
        self.headers = []
        self._load_data()

    def _load_data(self):
        """Load data from CSV file"""
        try:
            # Use pandas for efficient reading of large files
            df = pd.read_csv(self.file_path, na_filter=True)
            self.headers = list(df.columns)
            
            # Convert DataFrame to list for consistent processing
            self.original_data = df.fillna('').values.tolist()
            self.data = copy.deepcopy(self.original_data)
            
            if not self.headers:
                raise ValueError("CSV file must have headers")
                
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

    def display_head(self, n: int = 3) -> None:
        """Display first n rows of the CSV data"""
        try:
            col_widths = [len(str(header)) for header in self.headers]
            for row in self.data:
                for i, val in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(val)))

            # Print headers
            header_format = " | ".join(f"{header:<{width}}" for header, width in zip(self.headers, col_widths))
            print("\n" + header_format)
            print("-" * len(header_format))

            # Print rows
            for row in self.data[:n]:
                row_format = " | ".join(f"{str(val):<{width}}" for val, width in zip(row, col_widths))
                print(row_format)
            
            print(f"\nShowing {min(n, len(self.data))} of {len(self.data)} rows")
        except Exception as e:
            raise Exception(f"Error displaying data: {str(e)}")

    def filter_rows(self, column: str, condition: str, value: Union[str, int, float]) -> List[List[str]]:
        """Filter rows based on condition"""
        try:
            col_index = self.headers.index(column)
            filtered_data = []
            
            for row in self.data:
                # Handle missing or empty values
                if col_index >= len(row) or not row[col_index]:
                    continue
                
                cell_value = row[col_index]
                
                try:
                    if condition == 'contains':
                        if str(value).lower() in str(cell_value).lower():
                            filtered_data.append(row)
                    elif condition in ['>', '<', '==']:
                        # Convert to float only for numeric comparisons
                        if condition in ['>', '<']:
                            cell_num = float(cell_value)
                            value_num = float(value)
                            if (condition == '>' and cell_num > value_num) or \
                               (condition == '<' and cell_num < value_num):
                                filtered_data.append(row)
                        elif condition == '==' and str(cell_value) == str(value):
                            filtered_data.append(row)
                except ValueError:
                    # Skip rows where numeric conversion fails
                    continue
            
            self.data = filtered_data
            return filtered_data
        except Exception as e:
            raise Exception(f"Error filtering rows: {str(e)}")

    def sort_rows(self, column: str, ascending: bool = True) -> List[List[str]]:
        """Sort rows by specified column"""
        try:
            col_index = self.headers.index(column)
            
            def sort_key(row):
                if col_index >= len(row):
                    return '' if ascending else float('inf')
                value = row[col_index]
                if not value:
                    return '' if ascending else float('inf')
                try:
                    return float(value)
                except ValueError:
                    return str(value)
            
            self.data.sort(key=sort_key, reverse=not ascending)
            return self.data
        except Exception as e:
            raise Exception(f"Error sorting rows: {str(e)}")

    def aggregate_data(self, column: str, operation: str) -> float:
        """Perform aggregation on numeric column"""
        try:
            col_index = self.headers.index(column)
            values = []
            
            for row in self.data:
                if col_index < len(row) and row[col_index]:
                    try:
                        values.append(float(row[col_index]))
                    except ValueError:
                        continue
            
            if not values:
                raise ValueError(f"No valid numeric values found in column '{column}'")
            
            if operation == 'sum':
                result = sum(values)
            elif operation == 'mean':
                result = sum(values) / len(values)
            elif operation == 'min':
                result = min(values)
            elif operation == 'max':
                result = max(values)
            else:
                raise ValueError("Invalid operation")
            
            return result
        except Exception as e:
            raise Exception(f"Error performing aggregation: {str(e)}")

    def write_to_csv(self, output_file: str) -> None:
        """Write data to new CSV file"""
        try:
            # Convert to pandas DataFrame for efficient writing
            df = pd.DataFrame(self.data, columns=self.headers)
            df.to_csv(output_file, index=False)
            print(f"\nSuccessfully wrote {len(self.data)} rows to {output_file}")
        except Exception as e:
            raise Exception(f"Error writing to CSV: {str(e)}")

    def count_palindromes(self) -> int:
        """Count palindromes containing only A, D, V, B, N"""
        def is_valid_palindrome(s: str) -> bool:
            if not isinstance(s, str):
                return False
            s = str(s).upper()
            if not all(c in 'ADVBN' for c in s):
                return False
            return s == s[::-1]

        palindromes_found = []
        palindrome_count = 0
        
        for row in self.data:
            for value in row:
                if is_valid_palindrome(str(value)):
                    palindrome_count += 1
                    palindromes_found.append(value)
        
        # Display results
        if palindrome_count > 0:
            print("\nPalindromes found:")
            for p in palindromes_found:
                print(f"- {p}")
        else:
            print("\nNo palindromes found matching the criteria")
            
        return palindrome_count
    
    def reset_data(self):
        """Reset working data to its original"""
        self.data = copy.deepcopy(self.original_data)