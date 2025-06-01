import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data
from unittest.mock import patch

class TestDataTransformation(unittest.TestCase):

    def setUp(self):
        """Setup data untuk pengujian"""
        # Data mock untuk pengujian
        self.mock_data = [
            {"Title": "T-shirt 1", "Price": "$123.45", "Rating": "4.4 / 5", "Colors": "3", "Size": "Size: M", "Gender": "Gender: Men"},
            {"Title": "T-shirt 2", "Price": "$150.00", "Rating": "Not Rated", "Colors": "2", "Size": "Size: L", "Gender": "Gender: Women"},
            {"Title": "Unknown Product", "Price": "Price Unavailable", "Rating": "Invalid Rating / 5", "Colors": "5", "Size": "Size: S", "Gender": "Gender: Unisex"},
        ]
        self.df = transform_to_DataFrame(self.mock_data)  # Mengubah mock data menjadi DataFrame
    
    # Test untuk transform_to_DataFrame
    def test_transform_to_DataFrame(self):
        """Menguji apakah data bisa diubah menjadi DataFrame dengan benar"""
        self.assertIsInstance(self.df, pd.DataFrame, "Data harus menjadi DataFrame.")
        self.assertEqual(self.df.shape[0], 3, "Jumlah baris pada DataFrame tidak sesuai.")  # Memastikan ada 3 baris
        self.assertEqual(self.df.shape[1], 6, "Jumlah kolom pada DataFrame tidak sesuai.")  # Memastikan ada 6 kolom
    
    @patch('builtins.print')
    def test_transform_to_DataFrame_empty_data(self, mock_print):
        """Mengujinya jika data kosong dikembalikan None dan mencetak pesan kesalahan"""
        invalid_data = []  # Data kosong (list kosong)
        result = transform_to_DataFrame(invalid_data)
        
        # Memastikan hasil adalah None
        self.assertIsNone(result, "Data kosong harus mengembalikan None.")
        
        # Memastikan print dipanggil dengan pesan kesalahan yang benar
        mock_print.assert_called_once_with("Data kosong, tidak dapat diubah menjadi DataFrame.")
    
    # Test untuk transform_data
    def test_transform_data(self):
        """Menguji transformasi data"""
        transformed_data = transform_data(self.df)
        
        # Memastikan kolom 'Title' tidak mengandung 'Unknown Product' setelah transformasi
        self.assertNotIn("Unknown Product", transformed_data['Title'].values, "Data yang tidak valid tidak terhapus.")

        # Memastikan kolom 'Price' diubah menjadi format rupiah dan dikalikan dengan exchange rate
        self.assertEqual(transformed_data['Price'].iloc[0], 1975200.0, "Harga produk tidak dikonversi dengan benar.")

        # Memastikan rating diubah menjadi angka float (hanya angka rating tanpa '/5')
        self.assertEqual(transformed_data['Rating'].iloc[0], 4.4, "Rating produk tidak diproses dengan benar.")

        # Memastikan kolom 'Colors' diubah menjadi integer
        self.assertEqual(transformed_data['Colors'].iloc[0], 3, "Warna produk tidak diproses dengan benar.")

        # Memastikan kolom 'Size' sudah tidak mengandung teks 'Size: '
        self.assertEqual(transformed_data['Size'].iloc[0], "M", "Ukuran produk tidak diproses dengan benar.")

        # Memastikan kolom 'Gender' sudah tidak mengandung teks 'Gender: '
        self.assertEqual(transformed_data['Gender'].iloc[0], "Men", "Gender produk tidak diproses dengan benar.")

        # Memastikan tidak ada nilai NaN atau duplikat setelah transformasi
        self.assertFalse(transformed_data.isna().any().any(), "Terdapat nilai NaN setelah transformasi data.")
        self.assertEqual(transformed_data.duplicated().sum(), 0, "Terdapat duplikat setelah transformasi data.")

    def test_transform_invalid_data(self):
        """Menguji transformasi data jika data kosong atau tidak valid dikembalikan None"""
        invalid_data = None
        result = transform_data(invalid_data)
        self.assertIsNone(result, "Data tidak valid harus mengembalikan None.")

if __name__ == '__main__':
    unittest.main()