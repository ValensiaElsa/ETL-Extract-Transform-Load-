# Membuat dan mengaktifkan virtual environment
python -m venv .env 
.env\Scripts\Activate.ps1

# Menginstall requirements
pip install -r requirements.txt

# Menjalankan skrip main.py
python main.py
# Harap ubah db url sesuai dengan db url Anda pada bagian berikut di main.py (harap membuat db dengan nama fashionstudio jika memungkinkan)
POSTGRESQL_URL = 'postgresql://username:password@localhost:5432/fashionstudio'

# Menjalankan unit test pada folder tests
python -m pytest tests

# Menjalankan test coverage pada folder tests
coverage run -m pytest tests
coverage report

# Url Google Sheets:
https://docs.google.com/spreadsheets/d/1RDjBajEFmnvDPbiPeIcyLRjtuVBwEs3EEU908DHVou8/edit?usp=sharing
