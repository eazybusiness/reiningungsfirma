# NetLogo Demo Project - Plan

## Ziel
Ein einfaches, aber professionelles NetLogo-Modell als Proof-of-Concept erstellen, um dem Client zu zeigen:
1. Wir können NetLogo-Modelle entwickeln (mit AI-Unterstützung)
2. Python-Integration funktioniert einwandfrei
3. Dokumentation ist wissenschaftlich und auf Deutsch
4. Git-Struktur ist sauber und nachvollziehbar

---

## Demo-Modell: Epidemie-Simulation (SIR-Modell)

### Warum dieses Modell?
- ✅ **Klassisches ABM** - jeder Forscher kennt es
- ✅ **Einfach genug** - in 2-3 Stunden umsetzbar
- ✅ **Wissenschaftlich relevant** - zeigt Forschungskompetenz
- ✅ **Gut dokumentiert** - viele Referenzen verfügbar
- ✅ **Visually impressive** - schöne Animation

### Was ist ein SIR-Modell?
**S**usceptible (anfällig) → **I**nfected (infiziert) → **R**ecovered (genesen)

Agenten bewegen sich zufällig, Infizierte können Anfällige anstecken, nach Zeit genesen sie.

---

## Modell-Features

### NetLogo-Komponenten
1. **Agenten (Turtles)**
   - 3 Zustände: Susceptible (grün), Infected (rot), Recovered (grau)
   - Zufällige Bewegung
   - Infektionslogik bei Kontakt

2. **Parameter (Interface-Slider)**
   - `population` - Anzahl Agenten (100-1000)
   - `infection-rate` - Ansteckungswahrscheinlichkeit (0-100%)
   - `recovery-time` - Dauer bis Genesung (Ticks)
   - `initial-infected` - Startanzahl Infizierte (1-10)
   - `movement-speed` - Geschwindigkeit der Agenten

3. **Visualisierung**
   - Farbcodierung der Agenten
   - Echtzeit-Plots: S/I/R über Zeit
   - Counter für aktuelle Zahlen

4. **Datenexport**
   - CSV-Export der Zeitreihen
   - Konfigurierbar per BehaviorSpace

### Python-Komponenten

1. **Batch-Run-Skript** (`run_experiments.py`)
   - Automatisierte Versuchsreihen
   - Parameter-Sweeps
   - Parallele Ausführung (optional)

2. **Datenauswertung** (`analyze_results.py`)
   - CSV-Import
   - Statistische Auswertung
   - Plots mit Matplotlib/Seaborn

3. **Visualisierung** (`plot_results.py`)
   - Zeitreihen-Plots
   - Heatmaps für Parameter-Sensitivität
   - Exportierbare Grafiken (PNG/PDF)

---

## Repository-Struktur

```
netlogo-sir-demo/
├── README.md                    # Deutsch, ausführlich
├── .gitignore
├── netlogo/
│   ├── sir_model.nlogo         # Hauptmodell
│   └── experiments.xml         # BehaviorSpace-Konfiguration
├── python/
│   ├── requirements.txt        # Dependencies
│   ├── run_experiments.py      # Batch-Runs
│   ├── analyze_results.py      # Datenauswertung
│   └── plot_results.py         # Visualisierung
├── data/
│   ├── raw/                    # CSV-Exports von NetLogo
│   └── processed/              # Verarbeitete Daten
├── results/
│   ├── plots/                  # Generierte Grafiken
│   └── reports/                # Zusammenfassungen
└── docs/
    └── model_documentation.pdf # Wissenschaftliche Dokumentation
```

---

## Implementierungs-Schritte

### Phase 1: NetLogo-Modell (2-3 Stunden)
1. ✅ Grundgerüst erstellen
2. ✅ Agenten-Logik implementieren
3. ✅ Interface-Slider hinzufügen
4. ✅ Plots einrichten
5. ✅ CSV-Export konfigurieren
6. ✅ BehaviorSpace-Experimente definieren

### Phase 2: Python-Integration (2 Stunden)
1. ✅ `requirements.txt` erstellen
2. ✅ Batch-Run-Skript schreiben
3. ✅ Datenauswertung implementieren
4. ✅ Plotting-Funktionen erstellen
5. ✅ Testen mit Beispieldaten

### Phase 3: Dokumentation (1-2 Stunden)
1. ✅ README.md (Deutsch)
   - Projektbeschreibung
   - Installation
   - Nutzung
   - Beispiele
2. ✅ Code-Kommentare (Deutsch)
3. ✅ Model Documentation PDF
   - Modellbeschreibung
   - Parameter-Erklärungen
   - Validierung
   - Beispiel-Ergebnisse

### Phase 4: Git & GitHub (30 Min)
1. ✅ Repository initialisieren
2. ✅ `.gitignore` konfigurieren
3. ✅ Commits mit aussagekräftigen Messages
4. ✅ Auf GitHub pushen
5. ✅ README mit Badges verschönern

---

## Keine Kundendaten nötig!

**Vorteil:** Wir brauchen KEINE Daten vom Kunden für dieses Demo!

- ✅ SIR-Modell ist generisch
- ✅ Synthetische Daten werden im Modell generiert
- ✅ Zeigt alle relevanten Skills
- ✅ Kann sofort erstellt werden

**Wenn Client interessiert ist:**
- Dann können wir sein spezifisches Modell besprechen
- Demo zeigt, dass wir liefern können
- Reduziert sein Risiko massiv

---

## Zeitaufwand

**Gesamt: 5-7 Stunden**
- NetLogo-Modell: 2-3h
- Python-Skripte: 2h
- Dokumentation: 1-2h
- Git/GitHub: 0.5h

**Dein Investment:** 1 Tag Arbeit
**Potentieller Gewinn:** Projekt-Zusage + Lernerfahrung

---

## Was das Demo zeigt

### Technische Kompetenz
- ✅ Funktionierendes NetLogo-Modell
- ✅ Saubere Python-Integration
- ✅ Professionelle Git-Struktur
- ✅ Wissenschaftliche Dokumentation

### Arbeitsweise
- ✅ Strukturiertes Vorgehen
- ✅ Reproduzierbare Ergebnisse
- ✅ Klare Dokumentation
- ✅ Best Practices

### Kommunikation
- ✅ Fließend Deutsch
- ✅ Wissenschaftlicher Standard
- ✅ Verständliche Erklärungen

---

## Nächste Schritte

### 1. Bid senden
- Ehrlicher Ansatz
- Demo-Angebot erwähnen
- Auf GitHub-Link verweisen (nach Erstellung)

### 2. Demo erstellen (falls Client interessiert)
- 1 Tag intensive Arbeit
- Mit meiner (Cascade) Hilfe
- Auf GitHub veröffentlichen

### 3. Client-Gespräch
- Demo zeigen
- Spezifische Anforderungen besprechen
- Entscheiden, ob Projekt passt

---

## Risiko-Minimierung

**Für den Client:**
- ✅ Sieht konkrete Arbeitsprobe
- ✅ Kann Code reviewen
- ✅ Kein finanzielles Risiko
- ✅ Kann informiert entscheiden

**Für dich:**
- ✅ Lernst NetLogo (nützlich für Zukunft)
- ✅ Hast Referenz-Projekt
- ✅ Nur 1 Tag Investment
- ✅ Kein Commitment ohne Zusage

---

## Alternativen zum SIR-Modell

Falls Client ein anderes Demo bevorzugt:

### 1. Schelling's Segregation Model
- Soziale Dynamiken
- Sehr visuell
- Klassisches ABM

### 2. Predator-Prey (Wolf-Sheep)
- Ökosystem-Simulation
- Gut dokumentiert
- Eindrucksvolle Animation

### 3. Traffic Simulation
- Verkehrsfluss
- Praktische Anwendung
- Emergente Staus

**Empfehlung:** SIR-Modell - am relevantesten für Forschung

---

## Erfolgswahrscheinlichkeit

**Mit Demo:** 60-70%
- Client sieht konkrete Kompetenz
- Ehrlichkeit schafft Vertrauen
- Moderner AI-Ansatz ist akzeptabel

**Ohne Demo:** 10-20%
- "Noch nie NetLogo genutzt" ist Ausschlusskriterium
- Keine Arbeitsprobe

**Fazit:** Demo lohnt sich absolut! 🚀
