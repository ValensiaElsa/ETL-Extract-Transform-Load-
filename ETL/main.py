from utils.extract import scrape_product_data
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import save_to_postgre, save_to_csv, save_to_google_sheets

# Ganti dengan Google API Anda
SERVICE_ACCOUNT_FILE = 'google-sheets-api.json'

SPREADSHEET_ID = '1RDjBajEFmnvDPbiPeIcyLRjtuVBwEs3EEU908DHVou8'

# Ganti dengan database URL PostgreSQL Anda
POSTGRESQL_URL = 'postgresql://username:password@localhost:5432/fashionstudio'

def main():
    """Fungsi utama untuk keseluruhan proses ETL."""
    # Extract
    print("Memulai Scraping")
    url = 'https://fashion-studio.dicoding.dev/'
    all_products_data = scrape_product_data(url)
    ## Menampilkan jumlah total produk yang berhasil di-scrape
    print(f"Total produk yang berhasil di-scrape: {len(all_products_data)}")

    # Transform
    print("\nMemulai Transform")
    if all_products_data:
        # Transformasi data menjadi DataFrame
        df = transform_to_DataFrame(all_products_data)
        
        # Mentransformasikan data sesuai dengan aturan yang ditentukan
        data_clean = transform_data(df)
        
        # Tampilkan hasil akhir
        print(data_clean)
        print(data_clean.info())
    else:
        print("Tidak ada data yang ditemukan.")
    
    #Load
    print("\nMemulai Load")
    save_to_csv(data_clean)
    save_to_google_sheets(data_clean, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID)
    save_to_postgre(data_clean, POSTGRESQL_URL)

    print("Proses ETL Selesai")

if __name__ == '__main__':
    main()