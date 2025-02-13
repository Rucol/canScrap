import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time

username = "Zciwolvo"
base_url = f"https://github.com/{username}?tab=repositories"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Pobieranie podstawowych danych o profilu
response = requests.get(f"https://github.com/{username}", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

followers = soup.select_one('a[href*="?tab=followers"] span.text-bold')
about = soup.select_one('div.user-profile-bio')
repositories = soup.select_one('a[href*="?tab=repositories"] span.Counter')
website = soup.select_one('li[data-test-selector="profile-website-url"] a')
social_links = soup.select('li[itemprop="social"] a')


if followers:
    print(f"{username} ma {followers.text.strip()} followersów.")
else:
    print("Nie znaleziono followersów!")

if about:
    print(f"Bio: {about.text.strip()}")
else:
    print("Nie znaleziono bio!")
    
if repositories:
    total_repos = int(repositories.text.strip().replace(",", ""))
    print(f"Repositories: {total_repos}")
else:
    total_repos = 0
    print("Nie znaleziono liczby repozytoriów!")

if social_links:
    print("🔗 Linki do profili społecznościowych:")
    for link in social_links:
        print(f" - {link['href']}")
else:
    print("Brak linków społecznościowych!")
     
if website:
    print(f"Strona osobista: {website['href']}")
else:
    print("Brak strony osobistej!")

# Pobieranie języków programowania z repozytoriów
repo_languages = defaultdict(int)
page = 1

while True:
    url = f"{base_url}&page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Pobieranie repozytoriów na danej stronie
    repo_links = soup.select('a[itemprop="name codeRepository"]')
    if not repo_links:
        break  # Koniec repozytoriów
    
    for repo in repo_links:
        repo_name = repo.text.strip()
        repo_url = f"https://github.com{repo['href']}"
        
        # Pobieranie strony repozytorium
        repo_response = requests.get(repo_url, headers=headers)
        repo_soup = BeautifulSoup(repo_response.text, "html.parser")
        
        # Pobieranie języka z sekcji "Languages"
        language = repo_soup.select_one('span.color-fg-default.text-bold.mr-1')
        lang = language.text.strip() if language else "Brak informacji"
        repo_languages[lang] += 1

        print(f"Repo: {repo_name}, Język: {lang}")  # Debugowanie

        time.sleep(0.5)  # Unikanie blokady IP przez GitHub

    page += 1

# Wyświetlanie procentowego udziału języków
print("\nProcentowy udział języków w repozytoriach:")
if total_repos > 0:
    for lang, count in repo_languages.items():
        percentage = (count / total_repos) * 100
        print(f"{lang}: {percentage:.2f}% ({count}/{total_repos})")
else:
    print("Brak repozytoriów do analizy.")
