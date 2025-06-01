import unittest
from unittest.mock import patch, Mock
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Mengimpor fungsi yang diuji
from utils.extract import extract_product_details, get_page_content, scrape_product_data

class TestDataExtract(unittest.TestCase):

    def setUp(self):
        """Menyiapkan HTML untuk pengujian."""
        self.html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 1</h3>
                <span class="price">$100.00</span>
                <p>Rating: ⭐ Invalid Rating / 5</p>
                <p>5 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </div>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.details = self.soup.find('div', class_='product-details')

    # Test untuk get_page_content
    def test_get_page_content_success(self):
        """Mengujikan fungsi get_page_content untuk memastikan bisa mengambil konten halaman dengan benar."""
        url = 'https://fashion-studio.dicoding.dev/'
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '<html><body>Mocked Page Content</body></html>'
            
            content = get_page_content(url)
            
            # Memastikan fungsi mengembalikan konten halaman
            self.assertIsNotNone(content)
            self.assertIn('Mocked Page Content', content)
            mock_get.assert_called_once_with(url)

    def test_get_page_content_failure(self):
        """Mengujikan fungsi get_page_content jika gagal mengambil halaman."""
        url = 'https://fashion-studio.dicoding.dev/'
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404  # Simulasi halaman tidak ditemukan
            
            content = get_page_content(url)
            
            # Memastikan bahwa tidak ada konten yang dikembalikan
            self.assertIsNone(content)
            mock_get.assert_called_once_with(url)

    @patch('requests.get')
    def test_get_page_content_timeout(self, mock_get):
        """Mengujikan get_page_content saat terjadi timeout."""
        mock_get.side_effect = requests.exceptions.Timeout  # Simulasi timeout

        url = 'https://fashion-studio.dicoding.dev/'
        content = get_page_content(url)  # Fungsi yang sedang diuji

        self.assertIsNone(content)  # Mengharapkan None karena ada timeout

    @patch('requests.get')
    def test_get_page_content_invalid_url(self, mock_get):
        """Mengujikan get_page_content dengan URL yang tidak valid."""
        mock_get.return_value.status_code = 404  # Simulasi halaman tidak ditemukan
        
        url = 'https://fashion-studio.dicoding.dev/nonexistent-page'
        content = get_page_content(url)  # Fungsi yang sedang diuji

        self.assertIsNone(content)  # Mengharapkan None karena halaman tidak ditemukan

    # Test untuk extract_product_details
    def test_extract_product_details(self):
        """Mengujikan fungsi extract_product_details"""
        # Mengambil detail produk menggunakan fungsi yang diuji
        product_data = extract_product_details(self.details)

        # Mengecek apakah data yang diambil sesuai dengan yang diharapkan
        self.assertEqual(product_data['Title'], 'T-shirt 1')
        self.assertEqual(product_data['Price'], '$100.00')
        self.assertEqual(product_data['Rating'], 'Rating: ⭐ Invalid Rating / 5')  # Rating yang tidak valid
        self.assertEqual(product_data['Colors'], '5 Colors')
        self.assertEqual(product_data['Size'], 'Size: M')
        self.assertEqual(product_data['Gender'], 'Gender: Men')
        self.assertTrue('Timestamp' in product_data)  # Memastikan timestamp ada dalam hasil
    
    def test_extract_product_details_missing_price(self):
        """Mengujikan fungsi extract_product_details tetap bekerja saat harga hilang."""
        html_missing_price = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 2</h3>
                <p>Rating: ⭐ 4.0 / 5</p>
                <p>4 Colors</p>
                <p>Size: L</p>
                <p>Gender: Women</p>
            </div>
        </div>
        """
        soup_missing_price = BeautifulSoup(html_missing_price, 'html.parser')
        details_missing_price = soup_missing_price.find('div', class_='product-details')

        product_data_missing_price = extract_product_details(details_missing_price)

        self.assertEqual(product_data_missing_price['Title'], 'T-shirt 2')
        self.assertIsNone(product_data_missing_price['Price'])  # Harga hilang
        self.assertEqual(product_data_missing_price['Rating'], 'Rating: ⭐ 4.0 / 5')
        self.assertEqual(product_data_missing_price['Colors'], '4 Colors')
        self.assertEqual(product_data_missing_price['Size'], 'Size: L')
        self.assertEqual(product_data_missing_price['Gender'], 'Gender: Women')
        self.assertTrue('Timestamp' in product_data_missing_price)

    def test_extract_product_details_missing_title(self):
        """Mengujikan fungsi extract_product_details tetap bekerja saat title hilang."""
        html_missing_title = """
        <div class="collection-card">
            <div class="product-details">
                <span class="price">$50.00</span>
                <p>Rating: ⭐ 3.9 / 5</p>
                <p>3 Colors</p>
                <p>Size: S</p>
                <p>Gender: Unisex</p>
            </div>
        </div>
        """
        soup_missing_title = BeautifulSoup(html_missing_title, 'html.parser')
        details_missing_title = soup_missing_title.find('div', class_='product-details')

        product_data_missing_title = extract_product_details(details_missing_title)

        self.assertIsNone(product_data_missing_title['Title'])  # Judul hilang
        self.assertEqual(product_data_missing_title['Price'], '$50.00')
        self.assertEqual(product_data_missing_title['Rating'], 'Rating: ⭐ 3.9 / 5')
        self.assertEqual(product_data_missing_title['Colors'], '3 Colors')
        self.assertEqual(product_data_missing_title['Size'], 'Size: S')
        self.assertEqual(product_data_missing_title['Gender'], 'Gender: Unisex')
        self.assertTrue('Timestamp' in product_data_missing_title)

    def test_extract_product_details_missing_metadata(self):
        """Mengujikan fungsi extract_product_details tetap bekerja saat metadata hilang."""
        html_missing_metadata = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 3</h3>
                <span class="price">$75.00</span>
            </div>
        </div>
        """
        soup_missing_metadata = BeautifulSoup(html_missing_metadata, 'html.parser')
        details_missing_metadata = soup_missing_metadata.find('div', class_='product-details')

        product_data_missing_metadata = extract_product_details(details_missing_metadata)

        self.assertEqual(product_data_missing_metadata['Title'], 'T-shirt 3')
        self.assertEqual(product_data_missing_metadata['Price'], '$75.00')
        self.assertIsNone(product_data_missing_metadata['Rating'])  # Rating hilang
        self.assertIsNone(product_data_missing_metadata['Colors'])  # Warna hilang
        self.assertIsNone(product_data_missing_metadata['Size'])    # Ukuran hilang
        self.assertIsNone(product_data_missing_metadata['Gender'])  # Gender hilang
        self.assertTrue('Timestamp' in product_data_missing_metadata)

    # Test untuk scrape_product_data
    def test_scrape_product_data(self):
        """Mengujikan apakah fungsi scrape_product_data berhasil mengambil data produk dari halaman."""
        url = 'https://fashion-studio.dicoding.dev/'
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = self.html  # Menggunakan HTML contoh yang sudah disiapkan
            
            # Memanggil fungsi scrape_product_data untuk mengambil data produk
            all_products = scrape_product_data(url, max_pages=1)
            
            # Memastikan data produk berhasil diambil
            self.assertEqual(len(all_products), 1)
            self.assertEqual(all_products[0]['Title'], 'T-shirt 1')
            self.assertEqual(all_products[0]['Price'], '$100.00')
            self.assertEqual(all_products[0]['Rating'], 'Rating: ⭐ Invalid Rating / 5')
            self.assertEqual(all_products[0]['Colors'], '5 Colors')
            self.assertEqual(all_products[0]['Size'], 'Size: M')
            self.assertEqual(all_products[0]['Gender'], 'Gender: Men')

    def test_scrape_product_data_empty_page(self):
        """Mengujikan fungsi scrape_product_data jika halaman tidak berisi produk."""
        
        # Simulasi halaman kosong
        html_empty = "<html><body>No products available</body></html>"

        url = 'https://fashion-studio.dicoding.dev/empty'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = html_empty  # Menggunakan HTML kosong untuk simulasi

            # Memanggil fungsi scrape_product_data untuk mengambil data produk
            all_products = scrape_product_data(url, max_pages=1)
            
            # Memastikan tidak ada produk yang diambil
            self.assertEqual(len(all_products), 0)  # Tidak ada produk yang diambil

    @patch('utils.extract.get_page_content')
    def test_scrape_product_data_no_products(self, mock_get_page_content):
        """Mengujikan fungsi scrape_product_data saat halaman tidak ada produk."""
        # Mock halaman tanpa produk
        mock_get_page_content.return_value = "<html><body>No products found</body></html>"

        # Memanggil scrape_product_data
        all_products = scrape_product_data('https://example.com', max_pages=1)

        # Memastikan bahwa tidak ada produk yang diambil
        self.assertEqual(len(all_products), 0)

    @patch('utils.extract.get_page_content')
    def test_scrape_product_data_page_error(self, mock_get_page_content):
        """Mengujikan fungsi scrape_product_data saat terjadi error pada pengambilan halaman."""
        # Mock gagal mengambil halaman
        mock_get_page_content.return_value = None

        # Memanggil scrape_product_data
        all_products = scrape_product_data('https://example.com', max_pages=1)

        # Memastikan bahwa tidak ada produk yang diambil karena halaman gagal diambil
        self.assertEqual(len(all_products), 0)

    @patch('utils.extract.get_page_content')
    @patch('utils.extract.extract_product_details')
    def test_scrape_product_data_invalid_extract(self, mock_extract_product_details, mock_get_page_content):
        """Mengujikan fungsi scrape_product_data saat extract_product_details gagal memproses produk."""
        # Mock halaman dengan produk yang valid
        mock_get_page_content.return_value = """
        <html><body>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">T-shirt 1</h3>
                    <span class="price">$100.00</span>
                </div>
            </div>
        </body></html>
        """
        
        # Mock extract_product_details untuk melempar pengecualian
        mock_extract_product_details.side_effect = Exception("Error parsing product")

        # Memanggil scrape_product_data dan memverifikasi bahwa produk gagal diproses
        all_products = scrape_product_data('https://example.com', max_pages=1)

        # Memastikan bahwa tidak ada produk yang berhasil diproses karena terjadi pengecualian
        self.assertEqual(len(all_products), 0)

if __name__ == "__main__":
    unittest.main()