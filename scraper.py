import requests
import time
import re
import logging
from bs4 import BeautifulSoup
from collections import defaultdict

class GitHubScraper:
    """Klasa do pobierania danych profilu GitHub."""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    def __init__(self):
        """Inicjalizacja klasy, ustawienie logowania."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")  # logowanie

    @staticmethod
    def extract_username(url: str) -> str:
        """Ekstrakcja username z linku GitHub."""
        match = re.search(r"github\.com/([^/?#]+)", url)
        return match.group(1) if match else None

    def get_soup(self, url: str):
        """Pobranie i sparsowanie strony, obsługa błędów HTTP."""
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10)  #  obsługa timeout
            response.raise_for_status()  #  Obsługa błędów HTTP
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logging.error(f"Błąd podczas pobierania strony: {url} - {e}")  #  Obsługa błędów za pomocą logging
            return None

    def scrape_github_profile(self, url: str) -> dict:
        """Pobranie danych z profilu GitHub."""
        username = self.extract_username(url)
        if not username:
            return {"error": "Nieprawidłowy link GitHub!"}

        logging.info(f"Pobieranie danych dla użytkownika: {username}")  #  Logowanie rozpoczęcia pobierania danych
        
        profile_url = f"https://github.com/{username}"
        repo_url = f"{profile_url}?tab=repositories"

        soup = self.get_soup(profile_url)
        if not soup:
            return {"error": "Nie udało się pobrać strony profilu!"}  #  Obsługa błędu braku danych

        # Pobieranie podstawowych informacji o użytkowniku
        followers = soup.select_one('a[href*="?tab=followers"] span.text-bold')
        about = soup.select_one('div.user-profile-bio')
        repositories = soup.select_one('a[href*="?tab=repositories"] span.Counter')
        achievements = soup.select('a[href*="achievement="]')

        achievement_counts = defaultdict(int)
        for achievement in achievements:
            href = achievement.get("href")
            if href:
                name = href.split("achievement=")[-1].split("&")[0].replace("-", " ").title()
                achievement_counts[name] += 1

        total_repos = int(repositories.text.strip().replace(",", "")) if repositories else 0

        # Pobieranie języków repozytoriów
        repo_languages = self.scrape_languages(repo_url)  #  Przeniesiono logikę do osobnej funkcji

        profile_data = {
            "username": username,
            "followers": int(followers.text.strip()) if followers else 0,
            "bio": about.text.strip() if about else "Brak informacji",
            "total_repos": total_repos,
            "achievements": dict(achievement_counts),
            "languages": dict(repo_languages),
        }
        return profile_data

    def scrape_languages(self, repo_url: str) -> dict:
        """Pobieranie języków programowania używanych w repozytoriach użytkownika."""
        repo_languages = defaultdict(int)
        page = 1

        while True:
            url = f"{repo_url}&page={page}"
            soup = self.get_soup(url)
            if not soup:
                break

            repo_links = soup.select('a[itemprop="name codeRepository"]')
            if not repo_links:
                break  #  Obsługa końca listy repozytoriów

            for repo in repo_links:
                repo_path = repo['href']
                full_repo_url = f"https://github.com{repo_path}"
                repo_soup = self.get_soup(full_repo_url)
                if not repo_soup:
                    continue

                language = repo_soup.select_one('span.color-fg-default.text-bold.mr-1')
                lang = language.text.strip() if language else "Brak informacji"
                repo_languages[lang] += 1
                
                time.sleep(0.5)  # ograniczenie zapytań do GitHub

            page += 1

        return repo_languages
