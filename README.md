# CSV Data Processor

A Python utility for processing CSV files with various operations including filtering, sorting, and data aggregation. This project was developed to meet Redhat Assignment requirements for CSV file processing and manipulation.

## Project Structure
```
csv-data-processor/
├── README.md               # Project documentation
├── data/                  # Data directory
│   └── fruits_sales_data.csv  # Sample CSV file
├── requirements.txt       # Project dependencies
├── setup.py              # Package installation configuration
├── src/                  # Source code directory
│   ├── main.py          # Main execution script
│   └── utils/           # Utility functions
│       └── csv_utility.py  # Core CSV processing functionality
└── tests/               # Test directory
    └── csv_utility_test.py    # Test cases
```

## Features Implemented

### 1. CSV File Operations
- Read and display CSV data with headers
- Display configurable number of rows (e.g., first 3 rows)
- Handle large CSV files efficiently

### 2. Data Filtering
- Filter rows based on various conditions:
  - Greater than (>)
  - Less than (<)
  - Equal to (==)
  - Contains (string)
- Support for different data types:
  - Numeric values
  - Text strings
  - Dates

### 3. Sorting Capabilities
- Sort data by any column
- Support for ascending and descending order
- Handle different data types appropriately

### 4. Data Aggregation
- Calculate various statistics:
  - Sum
  - Average (Mean)
  - Minimum
  - Maximum
- Support for numeric columns

### 5. Special Features
- Palindrome detection for specific characters (A, D, V, B, N)
- Data persistence between operations
- Reset capability to original data

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd csv-data-processor
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/Mac
# or
venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Program
```bash
python src/main.py
```

### Running Tests
```bash
pytest tests/csv_utility_test.py
```

## Sample Data Format
The utility expects CSV files with headers. Example format:
```csv
Date,Product,Quantity,Price
2025-01-01,Apple,10,1.2
2025-01-02,Banana,5,0.8
2025-01-03,ADA,15,1.3
```

## Requirements Met

1. **File Operations**
   - Efficient CSV file reading and writing
   - Header detection and processing
   - Display functionality

2. **Data Processing**
   - Flexible filtering system
   - Multi-column sorting
   - Comprehensive aggregation functions

3. **Error Handling**
   - Proper error messages
   - Edge case handling
   - Data validation

4. **User Interface**
   - Interactive menu system
   - Clear operation feedback
   - User-friendly prompts

5. **Code Quality**
   - Modular design
   - Well-documented functions
   - Comprehensive test coverage

## Dependencies
- pandas: Data processing and analysis
- pytest: Testing framework

## Testing
The project includes comprehensive tests covering:
- File loading
- Data filtering
- Sorting operations
- Aggregation functions
- Palindrome detection
- Error handling

## Author
Lokesh B M [http://lokesh2021.github.io/]

## Acknowledgments
- Project requirements and specifications
- Testing data and scenarios