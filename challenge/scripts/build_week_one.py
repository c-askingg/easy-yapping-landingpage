"""Ein gemeinsamer Textstand für HTML und Tagesaufgaben-PDF.

python build_week_one.py [--font-dir PFAD]
Ohne Schriftverzeichnis werden die eingebauten Helvetica-Schriften verwendet.
"""
from pathlib import Path
import argparse, json, html, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font-dir',type=Path);args=parser.parse_args()
data=json.loads((root/'content/woche-1.json').read_text())
regular,bold='Helvetica','Helvetica-Bold'
if args.font_dir:
    for name in ['Montserrat-Bold-Full','Raleway-Regular-Full']:
        pdfmetrics.registerFont(TTFont(name,str(args.font_dir/(name+'.ttf'))))
    regular,bold='Raleway-Regular-Full','Montserrat-Bold-Full'

# HTML aus denselben unveränderten Absätzen und Beispielen erzeugen.
rows=[]
for task in data['tasks']:
    parts=['<p>'+html.escape(p)+'</p>' for p in task['paragraphs']]
    if task.get('example'):
        parts.append('<p><strong>Beispiel:</strong> '+html.escape(task['example'])+'</p>')
    rows.append(f'        <details id="{task["id"]}"><summary><span>{task["day"]:02}</span><h3>{html.escape(task["title"])}</h3><i aria-hidden="true">+</i></summary><div class="impulse-answer">'+''.join(parts)+'</div></details>')
f=root/'index.html';source=f.read_text()
pattern=r'(<div class="impulse-list" aria-label="Sprechimpulse der ersten Woche">).*?(\n      </div></div></section>)'
source,count=re.subn(pattern,lambda m:m[1]+'\n'+'\n'.join(rows)+m[2],source,flags=re.S)
assert count==1,'Aufgabenbereich nicht eindeutig gefunden'
f.write_text(source)

# Eine gut lesbare A4-Übersicht im vorhandenen Serienraster.
w,h=A4;x=34;width=w-68;pink=HexColor('#AB2E6C');ink=HexColor('#141414')
styles={
 'heading':ParagraphStyle('heading',fontName=bold,fontSize=12,leading=15.5,textColor=pink),
 'body':ParagraphStyle('body',fontName=regular,fontSize=11,leading=14.3,textColor=ink),
 'example':ParagraphStyle('example',fontName=regular,fontSize=11,leading=14.3,textColor=ink),
}
blocks=[]
for task in data['tasks']:
    bits=[('heading',f'Tag {task["day"]} · '+task['title'])]
    bits += [('body',p) for p in task['paragraphs']]
    if task.get('example'):bits.append(('example','Beispiel: '+task['example']))
    elements=[]
    for kind,txt in bits:
        para=Paragraph(html.escape(txt),styles[kind]);_,height=para.wrap(width,1000)
        elements.append((kind,para,height))
    blocks.append(elements)
content_height=sum(sum(v[2] for v in block)+3*(len(block)-1)+9 for block in blocks)-9
# Zwei Titelzeilen erhalten; 706 pt stehen für die vollständigen Aufgaben zur Verfügung.
start=h-122;bottom=35
assert content_height<=start-bottom, f'Inhalt passt nicht lesbar auf eine Seite: {content_height:.1f} pt'
out=root/'assets/easy-yapping_Woche-1_Tagesaufgaben.pdf'
c=canvas.Canvas(str(out),pagesize=A4)
c.setTitle('easy yapping | Woche 1 | Tagesaufgaben');c.setAuthor('EXPERTENBUCH Akademie')
c.setFillColor(pink);c.setFont(bold,10);c.drawString(x,h-32,'easy yapping  /  WOCHE 1')
c.setFont(bold,26);c.drawString(x,h-69,'Dich als Unternehmerin');c.drawString(x,h-100,'warmsprechen')
y=start
for block in blocks:
    for kind,para,height in block:
        para.drawOn(c,x,y-height);y-=height+3
    y+=3;y-=9
c.setFont(regular,7.5);c.setFillColor(ink)
c.drawString(x,19,'© ONE LIFE GMBH | EXPERTENBUCH AKADEMIE');c.drawRightString(w-x,19,'Woche 1')
c.showPage();c.save()
print(f'HTML und einseitige A4-PDF erzeugt. Letzte Inhaltszeile bei {y+9:.1f} pt über dem unteren Rand.')
