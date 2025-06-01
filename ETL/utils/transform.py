import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    try:
        if data:
            df = pd.DataFrame(data)
            return df
        else:
            print("Data kosong, tidak dapat diubah menjadi DataFrame.")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan saat mengubah data menjadi DataFrame: {e}")
        return None

def transform_data(data, exchange_rate=16000):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    try:
        # Dirty patterns untuk penggantian dan penghapusan
        dirty_patterns = {
            "Title": ["Unknown Product"],
            "Rating": ["Invalid Rating / 5", "Not Rated"],
            "Price": ["Price Unavailable", None]
        }

        # Menghapus baris yang memiliki nilai invalid pada kolom 'Title', 'Rating', dan 'Price'
        data = data[~data['Title'].isin(dirty_patterns['Title'])]
        data = data[~data['Rating'].isin(dirty_patterns['Rating'])]
        data = data[~data['Price'].isin(dirty_patterns['Price'])]

        # Menangani format rating seperti "4.8 / 5" dengan mengambil angka pertama sebelum '/'
        data['Rating'] = data['Rating'].str.extract(r'([0-9.]+)')

        # Mengkonversi kolom 'Price' ke rupiah dengan menangani nilai yang mungkin NaN atau None
        data['Price'] = data['Price'].replace({r'\$': '', r',': ''}, regex=True)
        data['Price'] = pd.to_numeric(data['Price'], errors='coerce')  # Mengubah menjadi numeric dan mengganti nilai error menjadi NaN
        data['Price'] = (data['Price'] * exchange_rate)

        # Mengubah kolom 'Colors' menjadi hanya angka
        data['Colors'] = data['Colors'].replace(r'\D+', '', regex=True)
        data['Colors'] = pd.to_numeric(data['Colors'], errors='coerce')  # Pastikan semua nilai adalah numerik

        # Menghapus teks 'Size: ' pada kolom 'Size'
        data['Size'] = data['Size'].replace(r'Size: ', '', regex=True)

        # Menghapus teks 'Gender: ' pada kolom 'Gender'
        data['Gender'] = data['Gender'].replace(r'Gender: ', '', regex=True)

        # Menghapus baris yang mengandung nilai NaN atau null pada kolom lainnya
        data = data.dropna()

        # Menghapus duplikat
        data = data.drop_duplicates()

        # Memastikan tipe data sesuai dengan yang diinginkan
        data['Title'] = data['Title'].astype('object')
        data['Size'] = data['Size'].astype('object')
        data['Gender'] = data['Gender'].astype('object')
        data['Rating'] = data['Rating'].astype('float64')
        data['Price'] = data['Price'].astype('float64')
        data['Colors'] = data['Colors'].astype('int64')

        return data

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi data: {e}")
        return None
