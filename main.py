import gradio as gr
from scraper import GitHubScraper
from analyzer import analyze_with_gemini
from report_generator import generate_pdf

def main(url: str):
    """Główna funkcja aplikacji przetwarzająca profil GitHub i generująca raport PDF."""

    scraper = GitHubScraper()
    
    # ✅ Obsługa błędów podczas scrapowania
    try:
        profile_data = scraper.scrape_github_profile(url)
    except Exception as e:
        return f"❌ Błąd podczas pobierania danych: {e}", None

    if "error" in profile_data:
        return f"❌ {profile_data['error']}", None

    # ✅ Obsługa błędów analizy AI
    try:
        analysis = analyze_with_gemini(profile_data)
    except Exception as e:
        return f"❌ Błąd podczas analizy AI: {e}", None

    # ✅ Obsługa błędów generowania PDF
    try:
        pdf_file = generate_pdf(profile_data, analysis)
    except Exception as e:
        return f"❌ Błąd podczas generowania PDF: {e}", None

    # ✅ Bezpieczna konwersja danych do Markdown (zapobieganie błędom formatowania)
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

    return summary_text, pdf_file

# ✅ Obsługa błędów uruchamiania aplikacji
try:
    demo = gr.Interface(
        fn=main, 
        inputs="text", 
        outputs=["markdown", "file"],
        title="GitHub Profile Analyzer",
        description="Podaj link do profilu GitHub, aby uzyskać analizę oraz możliwość pobrania raportu w PDF."
    )
    demo.launch()
except Exception as e:
    print(f"❌ Błąd podczas uruchamiania aplikacji: {e}")
