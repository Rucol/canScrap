import gradio as gr
from scraper import GitHubScraper
from analyzer import analyze_with_mistral
from report_generator import generate_pdf
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(urls: str):
    """Główna funkcja aplikacji"""
    
    scraper = GitHubScraper()
    results = []
    pdf_files = []
    
    for url in urls.split("\n"):
        url = url.strip()
        if not url:
            continue
        
        try:
            logger.info(f"Przetwarzanie URL: {url}")
            profile_data = scraper.scrape_github_profile(url)
            if "error" in profile_data:
                results.append(f" {profile_data['error']}")
                continue
            
            analysis = analyze_with_mistral(profile_data)
            pdf_file = generate_pdf(profile_data, analysis)
            pdf_files.append(pdf_file)
        
            achievements_text = "\n".join([f"- {achievement}: {count}" for achievement, count in profile_data.get("achievements", {}).items()])
            languages_text = "\n".join([f"- {lang}: {count}" for lang, count in profile_data.get("languages", {}).items()])

            summary_text = f"""
### Profil GitHub: [{profile_data.get('username', 'Nieznany użytkownik')}](https://github.com/{profile_data.get('username', '')})

👥 **Followers:**  
{profile_data.get('followers', 'Brak danych')}

📝 **Bio:**  
{profile_data.get('bio', 'Brak opisu')}

📂 **Liczba repozytoriów:**  
{profile_data.get('total_repos', 'Brak danych')}

🏆 **Osiągnięcia:**  
{achievements_text if achievements_text else 'Brak osiągnięć'}

🛠️ **Używane języki:**  
{languages_text if languages_text else 'Brak danych'}

📊 **Analiza AI:**  
{analysis}
"""
            results.append(summary_text)
        except Exception as e:
            logger.error(f"Błąd dla {url}: {e}")
            results.append(f" Błąd dla {url}: {e}")
    
    return "\n\n---\n\n".join(results), pdf_files

# Obsługa błędów uruchamiania aplikacji
try:
    demo = gr.Interface(
        fn=main, 
        inputs=gr.Textbox(placeholder="Podaj linki do profili GitHub, każdy w nowej linii", lines=5), 
        outputs=["markdown", "file"],
        title="GitHub Profile Analyzer",
        description="Podaj linki do profili GitHub (każdy w nowej linii), aby uzyskać analizy oraz pobrać raporty PDF."
    )
    demo.launch()
except Exception as e:
    logger.error(f"Błąd podczas uruchamiania aplikacji: {e}")