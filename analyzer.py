import requests
import json
import time

# Adres API serwera FastAPI
API_URL = "http://localhost:8000/generate/"

def remove_duplicates(text: str) -> str:
    """Usuwa powtarzające się linie w tekście."""
    lines = text.split("\n")
    seen = set()
    filtered_lines = []
    for line in lines:
        if line.strip() not in seen:
            seen.add(line.strip())
            filtered_lines.append(line)
    return "\n".join(filtered_lines)

def clean_response(response_text: str, prompt: str) -> str:
    """Usuwa fragmenty promptu z odpowiedzi modelu."""
    if prompt in response_text:
        response_text = response_text.split(prompt)[-1].strip()
    return response_text

def analyze_with_mistral(profile_data: dict) -> str:
    """
    Analizuje profil GitHub z użyciem lokalnego modelu Mistral-7B.

    Args:
        profile_data (dict): Dane pobrane z GitHub (nazwa użytkownika, repozytoria, języki itp.).

    Returns:
        str: Podsumowanie wygenerowane przez model AI.
    """

    if not isinstance(profile_data, dict):
        return "Błąd: Nieprawidłowy format danych wejściowych."

    if "error" in profile_data:
        return profile_data["error"]

    # Pobranie danych z profilu użytkownika
    username = profile_data.get("username", "Nieznany użytkownik")
    followers = profile_data.get("followers", "Brak danych")
    total_repos = profile_data.get("total_repos", "Brak danych")
    languages = profile_data.get("languages", {})
    achievements = profile_data.get("achievements", {})
    bio = profile_data.get("bio", "Brak opisu")

    # Formatowanie listy języków programowania
    languages_str = ", ".join(languages.keys())

    # Tworzenie promptu
       # Tworzenie zoptymalizowanego promptu
    prompt = f"""
Przeanalizuj profil GitHub użytkownika {username} i przygotuj profesjonalne podsumowanie w języku polskim. W oparciu o następujące informacje, przygotuj krótkie podsumowanie tego profilu:
- Liczba followersów: {followers}
- Liczba repozytoriów: {total_repos}
- Główne języki programowania: {languages_str}
- Bio: {bio}
- Osiągnięcia: {len(achievements)}

Podsumowanie nie powinno powtarzać tych danych, a jedynie na ich podstawie wygeneruj ocenę użytkownika, oceń jego profil oraz umiejętności i główne języki programowania.
Zrób to krótko, opisz użytkownika pod kątem programowania w maksymalnie 5 zdaniach. 
"""
    prompt += "\n### Odpowiedź AI:\n"





    payload = {
        "model": "mistral",
        "prompt": prompt,
        "max_tokens": 200,  # Więcej miejsca na pełne podsumowanie
        "temperature": 0.3,  # Mniejsza losowość
        "top_p": 0.6,
        "repetition_penalty": 1.2,  # Mniej powtórzeń
        "do_sample": True,  # Wymusza losowe generowanie
        "top_k": 50,  # Zmniejsza ryzyko powtarzania promptu

    }

    print("Wysyłany payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and "response" in result:
                response_text = clean_response(result["response"].strip(), prompt)
                response_text = remove_duplicates(response_text)
                
                end_time = time.time()
                print(f"Czas generowania: {end_time - start_time:.2f} sekund")
                
                return response_text
            else:
                return f"Błąd: Nieprawidłowa odpowiedź modelu: {result}"
        else:
            return f"Błąd API: {response.status_code} - {response.text}"

    except requests.RequestException as e:
        return f"Błąd połączenia z modelem: {e}"
