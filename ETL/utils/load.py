from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
 
def save_to_postgre(data, db_url):
    """Menyimpan data ke dalam PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        
        # Menyimpan data ke tabel 'products' jika tabel sudah ada, data akan di replace
        data.to_sql('products', engine, if_exists='replace', index=False)
        print("Data berhasil disimpan ke PostgreSQL.")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        raise

def save_to_csv(data, filename="products.csv"):
    """Menyimpan data ke dalam file CSV."""
    try:
        # Menyimpan DataFrame ke dalam file CSV
        data.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke {filename}: {e}")
        raise

def save_to_google_sheets(df, service_account_file, spreadsheet_id):
    """Menyimpan DataFrame ke Google Sheets menggunakan google-api-python-client."""
    try:
        # Autentikasi dengan Google Sheets API menggunakan file service account
        credentials = Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )

        # Membuat service client untuk mengakses Google Sheets API
        service = build('sheets', 'v4', credentials=credentials)

        # Pastikan Timestamp dikonversi ke string sebelum disimpan ke Google Sheets
        if 'Timestamp' in df.columns:
            df['Timestamp'] = df['Timestamp'].astype(str)  # Mengonversi Timestamp ke string
        
        # Membuka spreadsheet dan sheet yang dimaksud
        range_name = 'Sheet1!A1'  # Tentukan range di mana data akan dimulai
        values = [df.columns.values.tolist()] + df.values.tolist()

        # Menulis data ke Google Sheets
        body = {
            'values': values
        }

        # Memperbarui nilai di Google Sheets
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body=body,
            valueInputOption="RAW"
        ).execute()

        print("Data berhasil disimpan ke Google Sheets.")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Sheets: {e}")
        raise