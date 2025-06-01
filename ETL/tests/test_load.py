import unittest
from unittest.mock import patch, Mock, MagicMock
import pandas as pd
from utils.load import save_to_postgre, save_to_csv, save_to_google_sheets

class TestSaveFunctions(unittest.TestCase):

    def setUp(self):
        """Menyiapkan DataFrame mock untuk pengujian"""
        # Data mock untuk pengujian
        self.mock_data = {
            'Title': ['T-shirt 1', 'T-shirt 2'],
            'Price': ['$123.45', '$150.00'],
            'Rating': ['4.5', '4.7'],
            'Colors': ['3', '2'],
            'Size': ['M', 'L'],
            'Gender': ['Men', 'Women'],
            'Timestamp': ['2025-04-01 12:00', '2025-04-02 12:00']
        }
        self.df = pd.DataFrame(self.mock_data)  # Membuat DataFrame untuk pengujian

    # Test untuk menyimpan data ke Postgre
    @patch("utils.load.create_engine")
    def test_store_to_postgre(self, mock_create_engine):
        """Menguji apakah save_to_postgre berhasil menyimpan data ke PostgreSQL"""
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value._enter_.return_value = mock_conn
        mock_create_engine.return_value = mock_engine

        save_to_postgre(self.df, "postgresql://dummy")
        self.assertTrue(mock_create_engine.called)
    
    @patch('utils.load.create_engine')
    def test_save_to_postgre_error(self, mock_create_engine):
        """Menguji apakah save_to_postgre menangani error dengan benar"""
        # Simulasikan error koneksi
        mock_create_engine.side_effect = Exception("Database connection error")
        
        with self.assertRaises(Exception):  # Memastikan exception ditangani dengan benar
            save_to_postgre(self.df, 'postgresql://dummy')
        
    # Test untuk menyimpan data ke CSV
    @patch('utils.load.pd.DataFrame.to_csv')  # Memmock pd.DataFrame.to_csv
    def test_save_to_csv(self, mock_to_csv):
        """Menguji apakah fungsi save_to_csv berhasil menyimpan data ke file CSV"""
        # Menjalankan fungsi
        save_to_csv(self.df, "products.csv")

        # Memastikan bahwa to_csv dipanggil dengan benar
        mock_to_csv.assert_called_once_with("products.csv", index=False, encoding='utf-8')
        print("Test save_to_csv berhasil.")
    
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv_error(self, mock_to_csv):
        """Menguji apakah save_to_csv menangani error dengan benar"""
        mock_to_csv.side_effect = Exception("File saving error")

        with self.assertRaises(Exception):  # Memastikan exception ditangani dengan benar
            save_to_csv(self.df, "products.csv")

    # Test untuk menyimpan data ke Google Sheets
    @patch('utils.load.build')  # Memmock googleapiclient.discovery.build
    @patch('utils.load.Credentials.from_service_account_file')  # Memmock Credentials
    def test_save_to_google_sheets(self, mock_credentials, mock_build):
        """Menguji apakah fungsi save_to_google_sheets berhasil mengirim data ke Google Sheets"""
        # Membuat mock credentials dan service
        mock_service = Mock()
        mock_build.return_value = mock_service

        # Menyiapkan data mock untuk update ke Google Sheets
        spreadsheet_id = 'mock_spreadsheet_id'
        service_account_file = 'mock_service_account.json'

        # Menjalankan fungsi
        save_to_google_sheets(self.df, service_account_file, spreadsheet_id)

        # Memastikan service.spreadsheets().values().update dipanggil dengan benar
        mock_service.spreadsheets().values().update.assert_called_once()
        print("Test save_to_google_sheets berhasil.")

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets_error(self, mock_credentials, mock_build):
        """Menguji apakah save_to_google_sheets menangani error dengan benar"""
        mock_build.side_effect = Exception("Google Sheets API error")

        with self.assertRaises(Exception):  # Memastikan exception ditangani dengan benar
            save_to_google_sheets(self.df, 'mock_service_account.json', 'mock_spreadsheet_id')

if __name__ == '__main__':
    unittest.main()
