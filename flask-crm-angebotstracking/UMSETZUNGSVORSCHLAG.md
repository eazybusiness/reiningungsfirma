# Umsetzungsvorschlag – Angebots-Tracking mit Feedback- & Statistik-Dashboard

> **Projekt:** Internes CRM-System mit EML-Monitoring, Feedback-Webservice und Dashboard
> **Stack:** Python 3.x, Flask, PostgreSQL, Chart.js, SMTP, Cronjobs
> **Zeitrahmen:** 2–3 Wochen

---

## Warum ich

Ich habe ein vergleichbares Flask-basiertes CRM-System für mein eigenes Unternehmen entwickelt und betreibe es produktiv. Die Architektur umfasst automatisierte Kundenkommunikation, Token-basierte Interaktionslinks, Datenbankanbindung und ein internes Dashboard mit Statistiken.

Der Unterschied: Mein System nutzt die WhatsApp Business API statt SMTP — technisch aufwendiger als E-Mail-Verarbeitung, da es Webhook-Handling, Session-Management und Medienverarbeitung erfordert. Die hier geforderte EML-basierte Lösung ist architektonisch schlanker und liegt vollständig in meinem Kompetenzbereich.

---

## Architektur-Überblick

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNES NETZWERK                     │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │ David Info-  │    │  EML-Parser  │    │ Reminder  │  │
│  │ Center       │───▶│  (Cronjob)   │───▶│ Service   │  │
│  │ (.eml Export)│    │              │    │ (SMTP)    │  │
│  └──────────────┘    └──────┬───────┘    └─────┬─────┘  │
│                             │                  │        │
│                             ▼                  │        │
│                      ┌──────────────┐          │        │
│                      │  PostgreSQL  │◀─────────┘        │
│                      │  / SQLite    │                   │
│                      └──────┬───────┘                   │
│                             │                           │
│                             ▼                           │
│                      ┌──────────────┐                   │
│                      │  Dashboard   │                   │
│                      │  (Flask +    │                   │
│                      │   Chart.js)  │                   │
│                      └──────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
                              │
                              │ API (REST, API-Key Auth)
                              ▼
┌─────────────────────────────────────────────────────────┐
│                   EXTERNER VPS (HTTPS)                   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Feedback-Webservice                  │   │
│  │                                                  │   │
│  │  • Token-basierte Feedback-Links                 │   │
│  │  • Formular: Interesse / Absage / Grund          │   │
│  │  • Rate Limiting + Token-Expiry                  │   │
│  │  • REST-API für internen Datenabruf              │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Modulstruktur

### Modul 1: EML-Parser & Datenspeicherung

| Aspekt | Detail |
|---|---|
| **Trigger** | Cronjob / Watchdog überwacht Ausgangsordner von David |
| **Parsing** | Python `email`-Bibliothek extrahiert Empfänger, Betreff, Datum, Angebotsnummer |
| **Speicherung** | SQLAlchemy-Modell: `Angebot(id, kunde, email, betreff, angebotsnr, datum, status, token)` |
| **Token** | UUID4-basierter Einmal-Token pro Angebot für Feedback-Link |
| **Duplikat-Check** | Hash über Empfänger + Betreff + Datum verhindert Mehrfacherfassung |

### Modul 2: Reminder-Service

| Aspekt | Detail |
|---|---|
| **Logik** | Konfigurierbare Intervalle (z.B. 3, 7, 14 Tage nach Angebot) |
| **Versand** | SMTP via `smtplib` oder Flask-Mail |
| **Inhalt** | Erinnerungsmail mit eingebettetem Feedback-Link |
| **Tracking** | Reminder-Zähler und Zeitstempel pro Angebot |
| **Abbruch** | Automatischer Stopp nach Feedback oder max. Erinnerungen |

### Modul 3: Feedback-Webservice (extern)

| Aspekt | Detail |
|---|---|
| **Hosting** | Flask auf Linux VPS, HTTPS via Let's Encrypt / Certbot |
| **Endpunkt** | `GET /feedback/<token>` → Formular |
| **Optionen** | Interesse bestätigen / Absage mit Grund (Dropdown + Freitext) |
| **Sicherheit** | Token-Expiry (konfigurierbar), Rate Limiting (Flask-Limiter), kein Login nötig für Kunden |
| **API** | `GET /api/feedbacks` (API-Key Auth) für internen Abruf |

### Modul 4: Dashboard

| Aspekt | Detail |
|---|---|
| **Auth** | Basic Auth oder Flask-Login (konfigurierbar) |
| **KPIs** | Gesamtanzahl Angebote, Rückmeldungsquote, Ø Reaktionszeit |
| **Charts** | Chart.js – Ablehnungsgründe (Pie), Zeitverlauf (Line), Statusverteilung (Bar) |
| **Filter** | Zeitraum, Status, Kunde |
| **Export** | CSV-Download der gefilterten Daten |

---

## Sicherheitskonzept

| Massnahme | Umsetzung |
|---|---|
| **Feedback-Links** | UUID4-Token, einmalig gültig, konfigurierbare Ablaufzeit |
| **API-Zugriff** | API-Key im Header, IP-Whitelist optional |
| **HTTPS** | Let's Encrypt + Certbot Auto-Renewal |
| **Dashboard** | Basic Auth oder Session-basierter Login |
| **Datenbank** | Prepared Statements via SQLAlchemy (SQL-Injection-Schutz) |
| **Rate Limiting** | Flask-Limiter auf Feedback- und API-Endpunkte |

---

## Technologie-Stack

| Komponente | Technologie |
|---|---|
| Backend | Python 3.11+, Flask |
| ORM | SQLAlchemy / Flask-SQLAlchemy |
| Datenbank | PostgreSQL (Produktion) / SQLite (Entwicklung) |
| E-Mail-Parsing | Python `email`, `mailparser` |
| E-Mail-Versand | `smtplib` / Flask-Mail |
| Frontend | Jinja2-Templates, Chart.js, Bootstrap 5 |
| Scheduling | APScheduler oder systemd-Timer / Cron |
| Sicherheit | Flask-Limiter, Flask-Login, `secrets`-Modul |
| Deployment | Gunicorn + Nginx (VPS), Windows Task Scheduler (intern) |

---

## Zeitplan

| Woche | Meilenstein |
|---|---|
| **Woche 1** | EML-Parser, Datenmodell, Reminder-Service, erste Tests |
| **Woche 2** | Feedback-Webservice, Token-Logik, API, VPS-Deployment |
| **Woche 3** | Dashboard, Chart.js-Integration, Sicherheits-Hardening, Dokumentation |

---

## Prototyp-Angebot

Ich biete an, vor Beauftragung einen **funktionsfähigen Prototypen** zu erstellen, der folgendes demonstriert:

- EML-Parsing einer Beispieldatei
- Token-Generierung und Feedback-Formular
- Einfaches Dashboard mit Dummy-Daten

Damit können Sie die Qualität meiner Arbeit bewerten, bevor das Projekt startet.

---

*Erstellt am 26. Februar 2026*
