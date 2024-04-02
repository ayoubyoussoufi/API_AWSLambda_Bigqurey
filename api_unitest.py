import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from api_test import fetch_data, calculate_kpi


class TestYourApp(unittest.TestCase):

    @patch('api_test.requests.get')
    def test_fetch_data(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"amount": 100}, {"amount": 200}]  # Sample data
        mock_get.return_value = mock_response

        result = fetch_data("sales", "2023-03-01")
        self.assertEqual(result, [{"amount": 100}, {"amount": 200}])

    def test_calculate_kpi(self):
        sales_data = [[{"amount": 100}, {"amount": 200}], None, None]  # Sample sales data
        result = calculate_kpi(sales_data)
        expected_result = [
            {"day": "2023-03-01", "kpi_value": 300},
            {"day": "2023-03-02", "kpi_value": None},
            {"day": "2023-03-03", "kpi_value": None}
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
