"""Build the one-page guide from content/guide.json with embedded brand fonts."""
from pathlib import Path
from html import escape
import json, argparse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Einseitigen Guide mit den Brand-Schriften erzeugen.')
parser.add_argument('--font-dir',type=Path,required=True,help='Verzeichnis mit Raleway-Regular-Full.ttf und Montserrat-Bold-Full.ttf')
FONTS=parser.parse_args().font_dir
pdfmetrics.registerFont(TTFont('Raleway', str(FONTS/'Raleway-Regular-Full.ttf')))
pdfmetrics.registerFont(TTFont('RalewayBold', str(FONTS/'Montserrat-Bold-Full.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat', str(FONTS/'Montserrat-Bold-Full.ttf')))
pdfmetrics.registerFontFamily('Raleway', normal='Raleway', bold='RalewayBold')
PINK = HexColor('#AB2E6C'); INK = HexColor('#171717')
styles = {
    'head': ParagraphStyle('head', fontName='Montserrat', fontSize=14, leading=16, textColor=PINK, spaceAfter=7),
    'body': ParagraphStyle('body', fontName='Raleway', fontSize=8.8, leading=11, textColor=INK, spaceAfter=3),
    'accent': ParagraphStyle('accent', fontName='RalewayBold', fontSize=9.5, leading=12, textColor=PINK, spaceAfter=4),
}
data=json.loads((ROOT/'content/guide.json').read_text())
cards=[[(part['style'],Paragraph(part['html'],styles[part['style']])) for part in card] for card in data]
w,h=A4; margin=31;gap=14;padding=10;cw=(w-2*margin-gap)/2; inner=cw-2*padding
heights=[]
for parts in cards:
    heights.append(sum(p.wrap(inner,1000)[1]+styles[k].spaceAfter for k,p in parts)+2*padding-5)
rows=[max(heights[i:i+2]) for i in (0,2,4)]
start=h-100
assert start-sum(rows)-2*gap>43,(rows,start-sum(rows)-2*gap)
out=ROOT/'assets/so-gehts-easy-yapping.pdf'
c=canvas.Canvas(str(out),pagesize=A4)
c.setTitle('easy yapping Guide'); c.setAuthor('EXPERTENBUCH Akademie')
c.setFillColor(PINK);c.setFont('Montserrat',27);c.drawCentredString(w/2,h-48,'easy yapping Guide')
c.setStrokeColor(PINK);c.setLineWidth(1.3);c.line(w/2-94,h-60,w/2+94,h-60)
c.setFillColor(INK);c.setFont('RalewayBold',10);c.drawCentredString(w/2,h-78,'Dein Überblick für 30 Tage Sprechen und Veröffentlichen')
y=start
for ri,rh in enumerate(rows):
    for ci in (0,1):
        x=margin+ci*(cw+gap)
        c.setStrokeColor(HexColor('#D1D3D6'));c.setLineWidth(.7);c.rect(x,y-rh,cw,rh)
        py=y-padding
        for kind,p in cards[ri*2+ci]:
            _,ph=p.wrap(inner,1000);p.drawOn(c,x+padding,py-ph);py-=ph+styles[kind].spaceAfter
        assert py>=y-rh+padding-5
    y-=rh+gap
c.setFillColor(INK);c.setFont('Raleway',8);c.drawCentredString(w/2,19,'Copyright 2026 | EXPERTENBUCH Akademie')
c.showPage();c.save()
print('One A4 page; row heights:', rows)
