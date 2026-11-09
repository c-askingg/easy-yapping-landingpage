"""Erzeugt das A4-PDF der Tagesaufgaben für Woche 2 ohne Textänderungen."""
from pathlib import Path
import html
import json

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/woche-2.json").read_text())
OUT = ROOT / "assets/easy-yapping_Woche-2_Tagesaufgaben.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 34
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)
PINK = HexColor("#AB2E6C")
INK = HexColor("#141414")

STYLES = {
    "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=12, leading=15.5, textColor=PINK),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.2, leading=13.1, textColor=INK),
    "example": ParagraphStyle("example", fontName="Helvetica", fontSize=10.2, leading=13.1, textColor=INK),
}


def make_block(task):
    items = [("heading", f"Tag {task['day']} · {task['title']}")]
    items.extend(("body", paragraph) for paragraph in task["paragraphs"])
    if task.get("example"):
        items.append(("example", f"Beispiel: {task['example']}"))
    block = []
    for kind, text in items:
        paragraph = Paragraph(html.escape(text), STYLES[kind])
        _, height = paragraph.wrap(CONTENT_WIDTH, 1000)
        block.append((paragraph, height))
    return block


def footer(pdf, page_number):
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(MARGIN, 19, "© ONE LIFE GMBH | EXPERTENBUCH AKADEMIE")
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 19, f"Woche 2 · {page_number}")


def page_header(pdf, include_title):
    pdf.setFillColor(PINK)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 32, "easy yapping  /  WOCHE 2")
    if not include_title:
        return PAGE_HEIGHT - 57
    pdf.setFont("Helvetica-Bold", 22)
    y = PAGE_HEIGHT - 68
    for line in ("Dich als Mensch ganz natürlich", "mit deinem Business", "verschmelzen lassen"):
        pdf.drawString(MARGIN, y, line)
        y -= 27
    return y - 8


pdf = canvas.Canvas(str(OUT), pagesize=A4)
pdf.setTitle("easy yapping | Woche 2 | Tagesaufgaben")
pdf.setAuthor("EXPERTENBUCH Akademie")
page = 1
y = page_header(pdf, include_title=True)
bottom = 39

for task in DATA["tasks"]:
    block = make_block(task)
    height = sum(item[1] for item in block) + 3 * (len(block) - 1) + 11
    # Tag 8-12 und Tag 13-14 bilden zwei sinnvoll lesbare Seiten.
    if task["day"] == 13 or y - height < bottom:
        footer(pdf, page)
        pdf.showPage()
        page += 1
        y = page_header(pdf, include_title=False)
    for paragraph, height in block:
        paragraph.drawOn(pdf, MARGIN, y - height)
        y -= height + 3
    y += 3
    y -= 11

footer(pdf, page)
pdf.showPage()
pdf.save()
print(f"Erstellt: {OUT} ({page} Seiten)")
