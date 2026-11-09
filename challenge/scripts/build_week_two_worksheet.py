"""Erzeugt das freigabefähige, digital ausfüllbare Woche-2-Worksheet."""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/worksheet-woche-2.pdf"
ILLUSTRATION = ROOT / "assets/images/worksheet-woche-2-bio-illustration.png"
W, H = A4
X = 38
WIDTH = W - 2 * X
PINK = HexColor("#AB2E6C")
PINK_LIGHT = HexColor("#FCEBF2")
INK = HexColor("#171717")
LINE = HexColor("#E8B7CD")
FIELD = HexColor("#FFF8FB")

TEMPLATES = [
    {
        "title": "Bio für Veränderung",
        "formula": ["Für [konkrete Person]", "[Klares Ergebnis, das du ermöglichst]", "[Zusätzliche Ebene: Lebensstil, Werte oder Methode]", "[Dein nächster Schritt]"],
        "example": ["Für Frauen, die sich in ihrem Körper wieder wohlfühlen möchten", "Individuelles Training für mehr Kraft und Energie", "Ohne Druck, dafür mit einem Plan, der zu deinem Alltag passt", "Starte hier ↓"],
    },
    {
        "title": "Bio: Problem und Lösung",
        "formula": ["Mach [konkrete Sache] leichter", "Für [wen]", "[Was du anbietest]", "[Dein nächster Schritt]"],
        "example": ["Mach deinen Hochzeitsmorgen entspannt", "Für Bräute, die sich natürlich schön fühlen möchten", "Individuelles Brautstyling und persönliche Begleitung", "Termin anfragen ↓"],
    },
    {
        "title": "Bio: Hier bist du richtig",
        "formula": ["Du bist hier richtig, wenn du …", "[Wiederkehrende Wünsche oder Verhaltensweisen]", "[Was du teilst]", "[Dein nächster Schritt]"],
        "example": ["Du bist hier richtig, wenn du …", "dein Business sichtbar machen möchtest, ohne dich zu verbiegen", "Reel-Ideen, klare Worte und ehrlicher Content", "Komm mit ↓"],
    },
    {
        "title": "Bio aus Erfahrung",
        "formula": ["[Was du Menschen ermöglichst]", "[Konkrete Angebote oder Inhalte]", "[Deine persönliche Perspektive oder Besonderheit]", "[Dein nächster Schritt]"],
        "example": ["Erinnerungen festhalten, die sich nach euch anfühlen", "Hochzeiten, Familien und besondere Lebensmomente", "Unaufgeregt, persönlich und mit Blick für die kleinen Dinge", "Mehr erfahren ↓"],
    },
    {
        "title": "Bio, die Nähe schafft",
        "formula": ["Stell dir vor: [nahbare Haltung oder Gedanke]", "[Was du teilst / dein inhaltlicher Blickwinkel]", "Für [wen]", "[Dein nächster Schritt]"],
        "example": ["Stell dir vor: Du musst nicht immer alles allein schaffen", "Impulse für mehr Klarheit im Familienalltag", "Für Mütter, die sich selbst nicht verlieren möchten", "Hier entlang ↓"],
    },
    {
        "title": "Persönliche Bio",
        "formula": ["[Was du machst]", "[Wer du außerhalb deiner Arbeit bist]", "[Wofür du stehst oder was dich qualifiziert]", "[Dein nächster Schritt]"],
        "example": ["Ernährungsberaterin für Frauen mit wenig Zeit", "Mama, Kaffeeliebhaberin und Fan von einfachen Rezepten", "Für alltagstaugliche Ernährung ohne Verbote", "Starte hier ↓"],
    },
    {
        "title": "Komm für … bleib für …",
        "formula": ["Komm für [erster Anknüpfungspunkt]", "… bleib für [tieferen Wert]", "[Was du regelmäßig teilst]", "[Dein nächster Schritt]"],
        "example": ["Komm für Tipps rund um deinen Garten", "… bleib für ein Zuhause, das dich täglich auftanken lässt", "Ideen, Pflanzenwissen und Freude am Draußensein", "Mehr entdecken ↓"],
    },
]


def footer(pdf, page):
    pdf.setStrokeColor(LINE); pdf.setLineWidth(.5); pdf.line(X, 31, W - X, 31)
    pdf.setFillColor(INK); pdf.setFont("Helvetica", 7.5)
    pdf.drawString(X, 18, "© ONE LIFE GMBH | EXPERTENBUCH AKADEMIE")
    pdf.drawRightString(W - X, 18, f"Woche 2 · {page}")


def header(pdf):
    pdf.setFillColor(PINK); pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(X, H - 32, "easy yapping  /  WOCHE 2")


def paragraph(pdf, text, style, top, width=WIDTH, x=X):
    item = Paragraph(text, style); _, height = item.wrap(width, 1000); item.drawOn(pdf, x, top - height)
    return top - height


def field(pdf, name, x, top, width, height):
    pdf.acroForm.textfield(name=name, tooltip="Hier kannst du direkt schreiben.", x=x, y=top - height, width=width, height=height, borderWidth=.8, borderColor=LINE, fillColor=FIELD, textColor=INK, forceBorder=True, fontName="Helvetica", fontSize=10, fieldFlags=8392704)


def template(pdf, item, number, top):
    pdf.setFillColor(PINK); pdf.circle(X + 11, top - 11, 11, fill=1, stroke=0)
    pdf.setFillColor(white); pdf.setFont("Helvetica-Bold", 10); pdf.drawCentredString(X + 11, top - 14.5, str(number))
    pdf.setFillColor(INK); pdf.setFont("Helvetica-Bold", 14.5); pdf.drawString(X + 31, top - 15, item["title"])
    box_top = top - 31
    pdf.setFillColor(PINK_LIGHT); pdf.roundRect(X, box_top - 56, WIDTH, 56, 7, fill=1, stroke=0)
    pdf.setFillColor(INK); pdf.setFont("Helvetica", 8.7)
    for index, line in enumerate(item["formula"]): pdf.drawString(X + 11, box_top - 13 - index * 12.2, line)
    example_top = box_top - 70
    pdf.setFillColor(PINK); pdf.setFont("Helvetica-Bold", 8.8); pdf.drawString(X, example_top, "BEISPIEL:")
    pdf.setFillColor(INK); pdf.setFont("Helvetica", 8.7)
    for index, line in enumerate(item["example"]): pdf.drawString(X, example_top - 14 - index * 12.2, line)
    input_top = example_top - 67
    pdf.setFillColor(PINK); pdf.setFont("Helvetica-Bold", 8.8); pdf.drawString(X, input_top, "MEINE VERSION:")
    field(pdf, f"vorlage_{number}_eingabe", X, input_top - 20, WIDTH, 48)
    return input_top - 88


body = ParagraphStyle("body", fontName="Helvetica", fontSize=11.7, leading=16.3, textColor=INK)
pdf = canvas.Canvas(str(OUT), pagesize=A4)
pdf.setTitle("easy yapping | Woche 2 | Deine Instagram-Bio"); pdf.setAuthor("EXPERTENBUCH Akademie")

# Seite 1: finaler Einstieg, ergänzt nur um die gewünschte Illustration.
header(pdf)
pdf.setFillColor(PINK); pdf.setFont("Helvetica-Bold", 29); pdf.drawString(X, H - 76, "Deine Instagram-Bio")
pdf.setStrokeColor(PINK); pdf.setLineWidth(1.8); pdf.line(X, H - 91, X + 275, H - 91)
pdf.drawImage(ImageReader(str(ILLUSTRATION)), 334, H - 207, width=194, height=130, mask="auto", preserveAspectRatio=True, anchor="c")
y = H - 142
for text in (
    "Deine Bio zeigt auf einen Blick, was Menschen bei dir finden, für wen du da bist und warum sie bleiben sollten.",
    "Du musst nicht alles unterbringen. Entscheide dich für eine Richtung, die sich nach dir und deinem Business anfühlt.",
    "Wähle eine Vorlage, die zu dir passt. Du musst sie nicht Wort für Wort übernehmen: Nutze sie als Ausgangspunkt und fülle sie mit deinen eigenen Worten.",
):
    y = paragraph(pdf, text, body, y, width=300); y -= 16
footer(pdf, 1); pdf.showPage()

# Seiten 2 bis 4: jeweils zwei Vorlagen mit digitalen Eingabefeldern.
page = 2
for start in range(0, 6, 2):
    header(pdf); y = H - 63
    y = template(pdf, TEMPLATES[start], start + 1, y) - 19
    template(pdf, TEMPLATES[start + 1], start + 2, y)
    footer(pdf, page); pdf.showPage(); page += 1

# Seite 5: siebte Vorlage und der finale Bio-Entwurf.
header(pdf); y = template(pdf, TEMPLATES[6], 7, H - 63) - 12
pdf.setFillColor(PINK); pdf.setFont("Helvetica-Bold", 18); pdf.drawString(X, y, "Meine Bio")
y -= 27; pdf.setFillColor(INK); pdf.setFont("Helvetica", 10.5); pdf.drawString(X, y, "Welche Vorlage fühlt sich nach dir an?")
y -= 22; pdf.setFont("Helvetica-Bold", 10); pdf.drawString(X, y, "Meine gewählte Vorlage:")
field(pdf, "gewaehlte_vorlage", X, y - 8, WIDTH, 25)
y -= 49; pdf.setFont("Helvetica-Bold", 10); pdf.drawString(X, y, "Mein erster Bio-Entwurf:")
field(pdf, "bio_entwurf", X, y - 8, WIDTH, 94)
y -= 122; pdf.setFont("Helvetica", 10.2); pdf.drawString(X, y, "Lies deine Bio einmal laut vor.")
y -= 24; paragraph(pdf, "Klingt sie nach dir? Versteht eine neue Person sofort, was sie bei dir findet? Dann darfst du sie ausprobieren.", body, y)
footer(pdf, 5); pdf.showPage(); pdf.save()
print(f"Erstellt: {OUT}")
