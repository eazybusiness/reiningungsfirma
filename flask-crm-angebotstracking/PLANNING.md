# Flask CRM Angebots-Tracking – Projektplanung

## Projektbeschreibung

Bid auf freelancer.de für ein internes CRM-System mit EML-Monitoring aus David InfoCenter, automatischen Erinnerungsmails, externem Feedback-Webservice und Statistik-Dashboard.

## Eigene Referenz

- Selbst entwickeltes Flask-CRM mit WhatsApp Business API
- Produktiv im Einsatz für eigenes Unternehmen
- Architektur: Token-basierte Links, DB-Anbindung, Dashboard, automatisierte Kommunikation

## Differenzierung im Bid

- WhatsApp-Integration ist technisch komplexer als Email → zeigt Kompetenz-Overhead
- Konkreter Umsetzungsvorschlag mit Architektur-Diagramm (nicht nur Text)
- Prototyp-Angebot vor Beauftragung → minimiert Risiko für den Kunden
- Kein generischer Bid → spezifisch auf David InfoCenter und EML-Workflow zugeschnitten

## Deliverables

1. **Bid-Text** (`BID-TEXT-DE.txt`) – für freelancer.de
2. **Umsetzungsvorschlag** (`UMSETZUNGSVORSCHLAG.md`) – teilbar via GitHub-Link, enthält Architektur, Module, Zeitplan, Sicherheitskonzept

## Tech Stack des Projekts

- Python 3.x, Flask, SQLAlchemy
- PostgreSQL / SQLite
- Chart.js, Bootstrap 5
- smtplib / Flask-Mail
- Gunicorn + Nginx (Linux VPS)
- Windows Task Scheduler (intern, David InfoCenter)
