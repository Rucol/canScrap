# 🚀 canScrap

canScrap to zaawansowany scraper profili GitHub, który wykorzystuje AI do generowania profesjonalnych analiz na podstawie danych użytkownika. Aplikacja obsługuje interfejs w Gradio i pozwala na eksportowanie wyników w formacie PDF.

## 🛠 Funkcjonalności
- 📌 Pobieranie danych profilu GitHub (bio, followers, liczba repozytoriów, osiągnięcia itp.).
- 📊 Analiza profilu przy użyciu AI (Lokalny model Mistral-7B).
- 📜 Generowanie raportu w formacie PDF.
- 🎨 Interfejs użytkownika oparty na Gradio.

## 🔧 Technologie
- **Python** 🐍
- **BeautifulSoup** – scraping stron internetowych 🌍
- **Requests** – pobieranie danych HTTP
- **Gradio** – interfejs użytkownika 🎨
- **ReportLab** – generowanie raportów PDF 📄
- **Mistral-7B** – analiza danych przy użyciu AI 🤖
- **FastApi** - Stawianie serwera do lokalnego hostowania modelu

## 📦 Instalacja
1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/Rucol/canScrap.git
   cd canScrap
   ```
2. **Utwórz i aktywuj wirtualne środowisko (opcjonalnie, ale zalecane):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```
3. **Zainstaluj wymagane pakiety:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Pobierz model mistral-7b:**
   
   https://huggingface.co/mistralai/Mistral-7B-v0.1
5. **Zmień MODEL_PATH w pliku server.py:**

   ```
   MODEL_PATH = "D:/Mistral/mistral-7B-v0.1"
   ```

## 🚀 Uruchomienie
```bash
python main.py
```
oraz serwer w osobnej konsoli:
```
py server.py

```
## 📄 Przykładowe użycie
1. Uruchom aplikację.
2. Wklej link do profilu GitHub w interfejsie Gradio.
3. Poczekaj na analizę.
4. Pobierz gotowy raport PDF!


## 🏗 TODO / Możliwe ulepszenia
- [ ] Obsługa API GitHub do bardziej precyzyjnego pobierania danych.
- [ ] Rozszerzenie o dodatkowe witryny takie jak LinkedIn
- [ ] Możliwość wyboru różnych formatów raportów.

## 🤝 Współtworzenie
Jeśli chcesz dodać coś od siebie, śmiało otwórz **issue** lub stwórz **pull request**! 💡



---

🎉 **Dziękuję za zainteresowanie canScrap!**
## Twórca: Rucol
