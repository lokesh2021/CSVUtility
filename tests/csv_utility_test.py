import pytest
import os, sys
import pandas as pd
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from src.utils.csv_utility import CSVUtility

@pytest.fixture
def setup_test_csv():
    """Create a test CSV file with sample data."""
    test_data = {
        'Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
        'Product': ['Apple', 'Banana', 'ADA', 'Orange', 'ANNA'],
        'Quantity': [10, 5, 15, 8, 12],
        'Price': [1.2, 0.8, 1.3, 1.5, 0.7]
    }
    df = pd.DataFrame(test_data)
    test_file = 'test_data.csv'
    df.to_csv(test_file, index=False)
    yield test_file
    # Cleanup after tests
    if os.path.exists(test_file):
        os.remove(test_file)

@pytest.fixture
def csv_util(setup_test_csv):
    """Create CSVUtility instance with test data."""
    return CSVUtility(setup_test_csv)

class TestCSVUtility:
    """Test cases for CSVUtility class."""

    def test_file_loading(self, csv_util):
        """Test if file is loaded correctly."""
        assert len(csv_util.headers) == 4
        assert csv_util.headers == ['Date', 'Product', 'Quantity', 'Price']
        assert len(csv_util.data) == 5

    def test_display_head(self, csv_util, capsys):
        """Test display_head functionality."""
        csv_util.display_head(2)
        captured = capsys.readouterr()
        assert 'Date' in captured.out
        assert 'Product' in captured.out
        assert 'Apple' in captured.out
        assert 'Banana' in captured.out

    def test_filter_rows_numeric(self, csv_util):
        """Test filtering rows with numeric condition."""
        filtered = csv_util.filter_rows('Quantity', '>', '7')
        assert len(filtered) == 4
        assert all(float(row[2]) > 7 for row in filtered)

    def test_filter_rows_string(self, csv_util):
        """Test filtering rows with string condition."""
        filtered = csv_util.filter_rows('Product', 'contains', 'an')
        assert len(filtered) == 3
        assert all('an' in row[1].lower() for row in filtered)


    def test_sort_rows_numeric(self, csv_util):
        """Test sorting rows by numeric column."""
        sorted_data = csv_util.sort_rows('Quantity', ascending=True)
        quantities = [float(row[2]) for row in sorted_data]
        assert quantities == sorted(quantities)

    def test_sort_rows_string(self, csv_util):
        """Test sorting rows by string column."""
        sorted_data = csv_util.sort_rows('Product', ascending=True)
        products = [row[1] for row in sorted_data]
        assert products == sorted(products)

    def test_sort_rows_date(self, csv_util):
        """Test sorting rows by date column."""
        sorted_data = csv_util.sort_rows('Date', ascending=True)
        dates = [row[0] for row in sorted_data]
        assert dates == sorted(dates)

    def test_aggregate_data(self, csv_util):
        """Test aggregation functions."""
        # Test sum
        sum_result = csv_util.aggregate_data('Quantity', 'sum')
        assert sum_result == 50

        # Test mean
        mean_result = csv_util.aggregate_data('Quantity', 'mean')
        assert mean_result == 10.0

        # Test min
        min_result = csv_util.aggregate_data('Quantity', 'min')
        assert min_result == 5

        # Test max
        max_result = csv_util.aggregate_data('Quantity', 'max')
        assert max_result == 15

    def test_write_to_csv(self, csv_util, tmp_path):
        """Test writing data to new CSV file."""
        output_file = tmp_path / "output.csv"
        csv_util.write_to_csv(str(output_file))
        assert os.path.exists(output_file)
        
        # Verify content
        df = pd.read_csv(output_file)
        assert len(df) == 5
        assert list(df.columns) == csv_util.headers

    def test_count_palindromes(self, csv_util):
        """Test palindrome counting."""
        count = csv_util.count_palindromes()
        assert count == 2  # ADA and ANNA are palindromes

    def test_reset_data(self, csv_util):
        """Test data reset functionality."""
        original_data = csv_util.data.copy()
        csv_util.filter_rows('Quantity', '>', '7')
        assert len(csv_util.data) < len(original_data)
        csv_util.reset_data()
        assert len(csv_util.data) == len(original_data)

    def test_invalid_column(self, csv_util):
        """Test handling of invalid column name."""
        with pytest.raises(Exception):
            csv_util.filter_rows('InvalidColumn', '>', '5')

    def test_invalid_operation(self, csv_util):
        """Test handling of invalid aggregation operation."""
        with pytest.raises(Exception):
            csv_util.aggregate_data('Quantity', 'invalid_op')

    def test_empty_filter_result(self, csv_util):
        """Test filtering that results in no matches."""
        filtered = csv_util.filter_rows('Quantity', '>', '1000')
        assert len(filtered) == 0

    def test_non_numeric_aggregation(self, csv_util):
        """Test aggregation on non-numeric column."""
        with pytest.raises(Exception):
            csv_util.aggregate_data('Product', 'sum')

    def test_large_dataset(self, tmp_path):
        """Test handling of large dataset."""
        # Create large test file
        large_data = {
            'Date': ['2025-01-01'] * 10000,
            'Product': ['Test'] * 10000,
            'Quantity': list(range(10000)),
            'Price': [1.0] * 10000
        }
        large_file = tmp_path / "large_test.csv"
        pd.DataFrame(large_data).to_csv(large_file, index=False)
        
        # Test performance
        csv_util = CSVUtility(str(large_file))
        assert len(csv_util.data) == 10000
        
        # Test filtering
        filtered = csv_util.filter_rows('Quantity', '>', '9000')
        assert len(filtered) == 999  # 9001-9999

