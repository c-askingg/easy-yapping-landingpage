from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
OUT=Path(__file__).resolve().parents[1]/'assets/so-gehts-easy-yapping.pdf'
PINK=colors.HexColor('#AB2E6C'); INK=colors.HexColor('#111111')
W,H=A4; M=17*mm

def text(c,s,x,y,width,size=10,leading=14,bold=False,color=INK):
    p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=leading,textColor=color))
    _,h=p.wrap(width,1000);p.drawOn(c,x,y-h);return y-h

def block(c,title,body,y):
    y=text(c,title,M,y,W-2*M,13,17,True,PINK)-3*mm
    for s in body:y=text(c,s,M,y,W-2*M,10,14)-2*mm
    return y-4*mm

def main():
    c=canvas.Canvas(str(OUT),pagesize=A4);c.setTitle('Easy Yapping Guide');c.setAuthor('EXPERTENBUCH Akademie')
    c.setFillColor(PINK);c.setFont('Helvetica-Bold',22);c.drawString(M,H-M-5*mm,'easy yapping')
    y=text(c,'Dein Easy Yapping Guide',M,H-39*mm,W-2*M,25,29,True)-4*mm
    y=text(c,'30 Tage. 30 Sprechreels. Deine Themen, deine Stimme und ein täglicher Schritt nach draußen.',M,y,W-2*M,11,15)-7*mm
    y=block(c,'Deine tägliche Routine',[
        '<b>1.</b> Öffne die Challenge-Seite und wähle einen Tagesimpuls der aktuellen Woche.',
        '<b>2.</b> Nimm dein kurzes Sprechreel auf und veröffentliche es. Zeitrahmen: <b>10-20 Minuten</b>.',
        '<b>3.</b> Öffne das <b>Daily-Tracking</b>: Datum und Reel-Link eintragen, dein Gefühl auf der Skala festhalten und die Wochenfrage beantworten. Anschließend etwa <b>zwei Minuten</b> Mini-Reflexion; weitere Gedanken kannst du freiwillig ergänzen.'
    ],y)
    y=block(c,'Eine Woche nach der anderen',[
        'Woche 1 ist im Starter-Call zugänglich. Weitere Wochen werden nacheinander freigeschaltet. Innerhalb deiner freigeschalteten Woche kannst du die Aufgaben frei wählen.',
        'Die tägliche E-Mail führt dich oben auf die Challenge-Seite. Dort findest du Tagesimpulse, Material und Call-Zugänge.'
    ],y)
    y=block(c,'Deine Live-Termine',[
        '<b>Montag, 2. November 2026, 15 Uhr:</b> Starter-Call.',
        '<b>9., 16. und 23. November, jeweils 15 Uhr:</b> Fragen, Erfahrungen und ein Impuls von Gela. <b>30. November, 15 Uhr:</b> Abschlusscall.',
        'Die tägliche Challenge beginnt am <b>3. November</b> und läuft 30 Tage. Die Zeitzone der Call-Termine und die Zugangslinks werden auf der Seite ergänzt.'
    ],y)
    y=block(c,'Material und Begleitung',[
        'Dieser Guide bündelt die Organisation. Zu jeder Woche gibt es ein A4-Worksheet zum Ausdrucken und digitalen Ausfüllen. Woche 1: <b>Dein Coffeedate</b>. Aufzeichnungen findest du nach Bereitstellung auf der Challenge-Seite.',
        'Gela macht selbst mit und teilt ihre Beispielvideos in der eigenen WhatsApp-Gruppe. Dort ist Raum für Austausch und gegenseitige Unterstützung. Deine Reels kannst du freiwillig teilen.'
    ],y)
    if y<20*mm:raise ValueError('Inhalt reicht über den vorgesehenen Seitenraum hinaus')
    c.setStrokeColor(colors.HexColor('#D9D3D5'));c.line(M,18*mm,W-M,18*mm)
    text(c,'Easy Yapping | Organisatorischer Begleiter | Prüfstand 1. November 2026',M,15*mm,W-2*M,8,10)
    c.save()
if __name__=='__main__':main()
