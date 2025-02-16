import os
from dotenv import load_dotenv

#  Bezpieczne wczytanie zmiennych środowiskowych
dotenv_path = ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f"Brak pliku {dotenv_path}! Upewnij się, że plik istnieje.")

#  Pobranie klucza API z domyślną wartością None
API_KEY = os.getenv("GOOGLE_API_KEY")

#  Obsługa błędu braku klucza API
if not API_KEY:
    raise ValueError("Brak klucza API! Sprawdź plik .env lub zmienne środowiskowe.")
