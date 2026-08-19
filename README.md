# StraightAds Performance Marketing | Sales Intelligence & Marketing Brain Hub v11.3

> **Agentur-Kontext:** Performance-Marketing-Agentur **StraightAds Marketing GmbH** (Mainz)  
> **Kernversprechen:** *„Klarheit. Geschwindigkeit. Ergebnisse. | Go-Live in 14 Tagen“*  
> **Entwickler:** Eeraj Jan  

---

## 🎯 Überblick

Der **StraightAds Technical SEO & Conversion Intelligence Hub** ist eine High-End B2B Sales Intelligence Anwendung für die gezielte Vorbereitung und Durchführung von Conversion-Sales-Calls. 

Durch die nahtlose Verknüpfung von technischem On-Page-Scraping (Google PageSpeed Vitals, Serper.dev Google-Live-Index, ScreenshotAPI.to Full-Page Screenshots) mit den 23 Fachmodulen des **StraightAds Marketing Brain** liefert das Tool in Sekunden maßgeschneiderte Hebel, fundierte psychologische Optimierungen und praxiserprobte Vertriebs-Assets für jeden Interessenten.

---

## 🏛️ Die 7 Analyse-Reiter im Überblick

| Reiter | Fokus & Nutzen |
| :--- | :--- |
| **1. SEO & DOM-Strukturanalyse** | 3 Kern-Signale, Google SERP Simulator (Desktop/Mobile), H1-Hierarchie, Formularhürden & isolierte CTAs. |
| **2. Keyword & Live-Ranking** | Echte Google-Position via Serper.dev, Top-5 Themenrelevanz & Google Ads 14-Tage Speed-Hebel. |
| **3. Design, Farben & UI/UX** | First-Fold Preview, 5 CI-Farbfelder mit Hex-Codes, Typografie-Erkennung & Gemini Vision Audit. |
| **4. Verkaufspsychologie (BJ-Fogg)** | Radial Health Score (Grade A-D), $B = M \times A \times T$ Analyse, Vorher-Nachher CTA-Tabelle & 4 angewandte Neuro-Hebel. |
| **5. ROI- & Hebel-Rechner** | Interaktives Cockpit (4 Regler) zur Bezifferung des zusätzlichen Jahresertrags bei 0 € Werbekosten. |
| **6. Vertriebs-Pitches & Outreach** | 3 Copywriting-Frameworks (PAS, BAB, Hook-Story-Offer), Kaltakquise-Leitfaden & 1-Klick E-Mail-Vorlage. |
| **7. JSON-Export & Onboarding** | Strukturierter Datensatz-Export für CRM-Übergabe (HubSpot / Pipedrive) & 14-Tage Go-Live Qualitätscheck. |

---

## 🚀 Wie teile ich die App mit anderen? (Deployment-Guide)

### Option 1: Streamlit Community Cloud (Empfohlen & am einfachsten ⭐)

Streamlit-Apps benötigen einen dauerhaften Python-Prozess mit Websocket-Verbindung. Der schnellste und kostenlose Weg ist **Streamlit Community Cloud**:

1. **Code auf GitHub hochladen:**
   ```powershell
   git init
   git add .
   git commit -m "feat: StraightAds Sales Intelligence Hub v11.3"
   git branch -M main
   git remote add origin https://github.com/<DEIN-USERNAME>/<REPO-NAME>.git
   git push -u origin main
   ```
2. **Mit Streamlit Cloud verbinden:**
   - Gehe auf [share.streamlit.io](https://share.streamlit.io) und melde dich mit deinem GitHub-Account an.
   - Klicke auf **„New app“**.
   - Wähle dein Repository, den Branch `main` und die Hauptdatei `app.py` aus.
3. **Fertig:**  
   Nach ca. 1 Minute erhältst du eine permanente Web-URL (z. B. `https://straightads-hub.streamlit.app`), die du direkt an dein Team oder Kunden schicken kannst.

---

### Option 2: Warum nicht Vercel?

* **Vercel** ist primär für statische Websites und Node.js / Next.js Serverless Functions optimiert.
* Da Streamlit eine dauerhafte Websocket-Verbindung zu einem Python-Backend benötigt, funktionieren Streamlit-Apps auf Vercel nicht nativ (Serverless Functions brechen nach wenigen Sekunden ab).
* Für Python/Streamlit sind **Streamlit Community Cloud**, **Render.com**, **Railway** oder ein eigener Docker-Server auf Hetzner/DigitalOcean die idealen Plattformen.

---

## 🛠️ Lokaler Schnellstart

```powershell
python -m streamlit run app.py
```
*(Oder per Doppelklick auf `run_app.bat`)*
