import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def get_page_content(url: str):
    """Mengambil konten HTML dari URL dan menangani kesalahan."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Gagal memuat halaman. Status: {response.status_code}")
            return None
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengambil halaman {url}: {e}")
        return None

def extract_product_details(details):
    """Ekstrak detail produk dari elemen produk."""
    try:
        title_tag = details.find('h3', class_='product-title')
        title = title_tag.text.strip() if title_tag else None

        price_tag = details.find('span', class_='price')
        if price_tag:
            price = price_tag.text.strip()
        else:
            p_price_tag = details.find('p', class_='price')
            price = p_price_tag.text.strip() if p_price_tag else None

        all_p = details.find_all('p')
        meta = []

        for p in all_p:
            if 'price' in p.get('class', []):
                continue
            meta.append(p.text.strip())

        rating = meta[0] if len(meta) > 0 else None
        colors = meta[1] if len(meta) > 1 else None
        size = meta[2] if len(meta) > 2 else None
        gender = meta[3] if len(meta) > 3 else None

        product = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": datetime.now().isoformat()
        }

        return product
    except Exception as e:
        print(f"Error parsing product: {e}")
        return None

def scrape_product_data(base_url: str, max_pages: int = 50):
    """Fungsi untuk menjalankan proses scraping produk dari halaman 1 hingga max_pages."""
    all_products = []

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}/page{page}"
        print(f"Scraping halaman {page}")
        
        # Mengambil konten halaman
        content = get_page_content(url)
        if not content:
            continue

        soup = BeautifulSoup(content, 'html.parser')
        product_cards = soup.find_all('div', class_='collection-card')

        if not product_cards:
            print(f"Tidak ada produk di halaman {page}. Berhenti.")
            break

        # Memproses produk-produk di halaman
        for card in product_cards:
            try:
                details = card.find('div', class_='product-details')
                if details is None:
                    print("Tidak ada detail produk, dilewati.")
                    continue

                # Mengambil detail produk menggunakan fungsi terpisah
                product_data = extract_product_details(details)
                if product_data:
                    all_products.append(product_data)

            except Exception as e:
                print(f"Error parsing product: {e}")

    return all_products