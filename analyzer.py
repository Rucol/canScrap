import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY)

def analyze_with_gemini(profile_data: dict) -> str:
    """Analiza profilu GitHub z użyciem modelu Gemini."""
    
    #  Walidacja danych wejściowych (sprawdzenie, czy to słownik)
    if not isinstance(profile_data, dict):
        return "Błąd: Nieprawidłowy format danych wejściowych."

    #  Obsługa błędów zwróconych w profile_data
    if "error" in profile_data:
        return profile_data["error"]

    #  Pobieranie danych z profile_data z domyślnymi wartościami, aby uniknąć KeyError
    username = profile_data.get("username", "Nieznany użytkownik")
    followers = profile_data.get("followers", "Brak danych")
    total_repos = profile_data.get("total_repos", "Brak danych")
    achievements = profile_data.get("achievements", "Brak danych")
    languages = profile_data.get("languages", "Brak danych")
    bio = profile_data.get("bio", "Brak danych")

    prompt = f"""
Przeanalizuj profil GitHub użytkownika {username} i przedstaw wnioski na podstawie podanych danych. 
Nie powtarzaj podstawowych informacji takich jak bio, followers, liczba repozytoriów, osiągnięcia czy języki programowania. 
Zamiast tego, zaproponuj ocenę umiejętności, mocne strony oraz ewentualne sugestie rozwoju dla tego użytkownika.

Dane profilu:
- Followers: {followers}
- Liczba repozytoriów: {total_repos}
- Osiągnięcia: {achievements}
- Używane języki: {languages}
- Bio: {bio}

Analiza AI:
"""

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        #  Obsługa błędu, gdy API nie zwraca poprawnej odpowiedzi
        return response.text.strip() if response and response.text else "Błąd: Brak analizy z modelu AI."
    
    except Exception as e:
        #  Obsługa błędów podczas komunikacji z API
        return f"Błąd podczas generowania analizy: {e}"
