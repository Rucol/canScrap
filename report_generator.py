from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

#  Bezpieczne wczytywanie czcionki
try:
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Nie znaleziono pliku czcionki: {font_path} pobierz czcionke lub zmien")
    pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
except Exception as e:
    print(f"❌ Błąd podczas ładowania czcionki: {e}")
    exit(1)

def generate_pdf(profile_data: dict, analysis: str) -> str:
    """Generowanie raportu PDF z danymi profilu GitHub i analizą AI."""

    #  Sprawdzanie poprawności danych wejściowych
    if not isinstance(profile_data, dict):
        raise ValueError("❌ profile_data musi być słownikiem")
    if not isinstance(analysis, str):
        raise ValueError("❌ analysis musi być tekstem")

    #  Bezpieczne generowanie nazwy pliku
    try:
        username = profile_data.get("username", "unknown_user").replace(" ", "_")
        filename = f"{username}_github_summary.pdf"
    except Exception as e:
        print(f"❌ Błąd przy generowaniu nazwy pliku: {e}")
        return None

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    #  Bezpieczne przetwarzanie bio
    bio_text = profile_data.get("bio", "Brak informacji")
    try:
        bio_text = bio_text.encode("utf-8").decode("utf-8")
    except Exception as e:
        print(f"❌ Błąd przy kodowaniu tekstu bio: {e}")
        bio_text = "Błąd kodowania tekstu"

    #  Definicja stylów
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=16, spaceAfter=20, fontName="DejaVuSans")
    content_style = ParagraphStyle("Content", parent=styles["Normal"], fontSize=12, fontName="DejaVuSans")
    bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"], fontSize=12, fontName="DejaVuSans", leftIndent=20)

    #  Tworzenie zawartości PDF
    elements = [
        Paragraph(f"📄 <b>Podsumowanie profilu GitHub:</b> {profile_data.get('username', 'unknown_user')}", title_style),
        Spacer(1, 10),
        Paragraph(f"👥 <b>Followers:</b> {profile_data.get('followers', 'Brak danych')}", content_style),
        Paragraph(f"📝 <b>Bio:</b> {bio_text}", content_style),
        Paragraph(f"📂 <b>Liczba repozytoriów:</b> {profile_data.get('total_repos', 'Brak danych')}", content_style),
        Spacer(1, 15),
        Paragraph("📊 <b>Analiza AI:</b>", title_style),
        Spacer(1, 10),
    ]

    #  Obsługa listy punktowanej w analizie
    analysis_lines = analysis.split("\n")
    for line in analysis_lines:
        if line.strip():
            paragraph_style = bullet_style if line.startswith("*") else content_style
            elements.append(Paragraph(line, paragraph_style))
        elements.append(Spacer(1, 5))

    #  Generowanie PDF z obsługą błędów
    try:
        doc.build(elements)
    except Exception as e:
        print(f"❌ Błąd podczas generowania pliku PDF: {e}")
        return None

    return filename
