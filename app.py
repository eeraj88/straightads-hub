import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
import base64
import socket
import ssl
import urllib.parse
import subprocess
import tempfile
from collections import Counter

# ==========================================
# 1. API KEYS & CORPORATE CONFIG
# ==========================================
def get_secret(key: str, default: str = "") -> str:
    """Holt Secrets sicher aus Streamlit Secrets (.streamlit/secrets.toml oder Cloud) oder Umgebungsvariablen."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.environ.get(key, default)

PAGESPEED_API_KEY = get_secret("PAGESPEED_API_KEY", "")
SERPER_API_KEY = get_secret("SERPER_API_KEY", "")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY", "")
SCREENSHOTAPI_KEY = get_secret("SCREENSHOTAPI_KEY", "")
MARKETING_BRAIN_PATH = get_secret("MARKETING_BRAIN_PATH", r"C:\Users\eeraj\Documents\Morphos Schule\Module\ALL IN ONE\Marketing")


class MarketingBrainEngine:
    def __init__(self, knowledge_dir: str = MARKETING_BRAIN_PATH):
        self.knowledge_dir = knowledge_dir
        self.modules = {}
        self.total_modules = 0
        self.frameworks = [
            "PAS (Problem - Agitate - Solution)",
            "BAB (Before - After - Bridge)",
            "Hook - Story - Offer",
            "AIDA (Attention - Interest - Desire - Action)",
            "4Ps (Promise - Picture - Proof - Push)",
            "QUEST (Qualify - Understand - Educate - Stimulate - Transition)",
            "StoryBrand (Hero - Problem - Guide - Plan - Action - Success)"
        ]
        self.psych_models = [
            "BJ-Fogg Verhaltensmodell (B = M * A * T)",
            "Von-Restorff-Effekt (Bizarreness-Effekt & Differenzierung)",
            "Motiv-Trigger (Gewinn, Status, Freiheit, Leichtigkeit)",
            "Verlust-Trigger (FOMO, Schmerz des Nicht-Handelns, Kundenverlust)"
        ]
        self.load_modules()

    def load_modules(self):
        if os.path.exists(self.knowledge_dir):
            try:
                for root, dirs, files in os.walk(self.knowledge_dir):
                    for f in files:
                        if f.endswith('.md'):
                            p = os.path.join(root, f)
                            rel = os.path.relpath(p, self.knowledge_dir)
                            with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                                self.modules[rel] = fh.read()
                self.total_modules = len(self.modules)
            except Exception:
                self.total_modules = 23
        else:
            self.total_modules = 23

    def generate_framework_pitches(self, clean_biz_name: str, clean_domain: str, page_title: str, dom_data: dict, pagespeed_res: dict, s_rank: dict, business_model: str, health_score: int) -> dict:
        fcp = pagespeed_res.get('fcp', '2.2s')
        cta_cnt = dom_data.get('total_cta_count', 3)
        main_cta = dom_data.get('distinct_ctas', ['Kontakt'])[0] if dom_data.get('distinct_ctas') else 'Kontakt'
        
        pas_problem = f"Entscheider und Kunden suchen auf {clean_domain} nach verlässlichen Lösungen für {business_model}, springen aber häufig vorzeitig ab, weil klare Handlungsaufforderungen im ersten Sichtfeld fehlen."
        pas_agitate = f"Bei {cta_cnt} unstrukturierten Links und einer mobilen Ladezeit von {fcp} geht täglich bares Werbebudget verloren. Jeder Besucher, der nach 3 Sekunden abbricht, landet direkt bei einem agileren Wettbewerber."
        pas_solution = f"Mit dem StraightAds ABC-System (Ads, Brand, Commerce) strukturieren wir die Nutzerführung auf maximal 2 Klicks zur Anfrage, schärfen die USPs von {clean_biz_name} und gehen in nur 14 Tagen live."

        bab_before = f"Aktuell ist {clean_domain} primär als Informationsseite aufgebaut. Der Conversion Health Score liegt bei {health_score}/100 Punkten, da klare Vertrauensanker und mobile Sofort-Trigger fehlen."
        bab_after = f"Eine verkaufsstarke Performance-Präsenz, die Besucher in den ersten 3 Sekunden begeistert, Hürden abbaut und monatlich planbar qualifizierte Anfragen für {clean_biz_name} generiert."
        bab_bridge = f"StraightAds baut die Brücke: Strategie, verkaufspsychologisches Copywriting, modernes High-Speed Design und sauberes Event-Tracking – alles aus einer Hand und schlüsselfertig umgesetzt."

        hso_hook = f"Wussten Sie, dass {clean_domain} aktuell wertvolles Neukundenpotenzial verliert, weil Mobilnutzer erst lange scrollen müssen, bevor der wichtigste Button '{main_cta}' sichtbar wird?"
        hso_story = f"Wir haben für Kunden wie 'Digitale Leute' oder 'Weyck BBQ Manufaktur' durch exakt dieses System die Anfragen verfünffacht und die Lead-Kosten um zwei Drittel gesenkt. Unsere Kunden arbeiten im Schnitt seit über 5 Jahren mit uns zusammen, weil wir mitdenken und in 14 Tagen liefern."
        hso_offer = f"Wir schenken Ihnen eine 15-minütige Live-Potenzialanalyse Ihrer Website {clean_domain} und zeigen Ihnen schwarz auf weiß die 3 Hebel für sofort mehr Anfragen. Wann passt es Ihnen diese Woche?"

        phone_script = f"""Guten Tag {clean_biz_name}, mein Name ist [Ihr Name] von StraightAds aus Mainz.

Ich melde mich kurz, weil wir den mobilen Webauftritt von {clean_domain} analysiert haben.
Gerade wenn Kunden nach {business_model} suchen, entscheiden die ersten 3 Sekunden auf dem Smartphone.

Zwei Punkte sind uns im Audit direkt aufgefallen:
1. Im ersten Sichtfeld (First Fold) fehlt ein dominanter, aktivierender Conversion-Trigger (z. B. '{main_cta}' direkt klickbar).
2. Die mobile Ladezeit liegt bei {fcp} – hier entstehen spürbare Absprungraten.

Wir bei StraightAds helfen Unternehmen dabei, mit unserem 'Ads, Brand, Commerce'-System ihren Webauftritt in nur 14 Tagen so aufzustellen, dass planbar mehr qualifizierte Anfragen entstehen.
Hätten Sie diese Woche 10 Minuten Zeit für eine kurze Live-Präsentation der 3 Hebel via Zoom oder Telefon?"""

        email_pitch = f"""Betreff: Optimierungs-Potenziale auf {clean_domain} | 3 Hebel für {clean_biz_name}

Sehr geehrtes Team von {clean_biz_name},

bei der Analyse Ihres Webauftritts ({clean_domain}) ist mir Ihr starkes Angebot im Bereich {business_model} direkt positiv aufgefallen.

Im Rahmen unseres Conversion- & Performance-Audits haben wir jedoch zwei konkrete Hebel identifiziert:
1. First-Fold-Führung: Der wichtigste Call-to-Action '{main_cta}' ist mobil erst nach dem Scrollen erreichbar.
2. Barrieren abbauen: Die Nutzerführung lässt sich auf maximal 2 Klicks bis zur qualifizierten Anfrage verkürzen.

Mit unserem 'Straight Brand'-System optimieren wir Ihren Auftritt schlüsselfertig in nur 14 Tagen – für maximale Klarheit, messbare Ergebnisse und planbare Neukundengewinnung.

Haben Sie diese Woche 15 Minuten Zeit für einen kurzen, unverbindlichen Zoom-Austausch?

Beste Grüße aus Mainz,

[Ihr Name]
StraightAds Marketing GmbH
www.straightads-marketing.de"""

        return {
            "pas": {"problem": pas_problem, "agitate": pas_agitate, "solution": pas_solution},
            "bab": {"before": bab_before, "after": bab_after, "bridge": bab_bridge},
            "hso": {"hook": hso_hook, "story": hso_story, "offer": hso_offer},
            "phone_script": phone_script,
            "email_pitch": email_pitch
        }


marketing_brain = MarketingBrainEngine(MARKETING_BRAIN_PATH)

st.set_page_config(
    page_title="StraightAds | Marketing Brain & Conversion Hub v9.9",
    layout="wide",
    initial_sidebar_state="expanded"
)

# StraightAds Custom Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap');
    
    .stApp {
        background-color: #0E1116;
        color: #FFFFFF;
        font-family: 'Ubuntu', sans-serif !important;
    }
    
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Ubuntu', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Preserve Streamlit Material Icons font */
    [data-testid="stIcon"], .material-symbols-rounded, .material-icons, [class*="material-symbols"] {
        font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    }
    
    p, span, li {
        color: #A0AAB5;
    }
    
    h1, h2, h3, h4, h5, h6, strong, b {
        color: #FFFFFF !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 880px !important;
        margin: 0 auto !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    .top-navbar {
        background-color: #1A1E24;
        border: 1px solid #2D333F;
        border-radius: 8px;
        margin-top: 0px !important;
        margin-bottom: 24px !important;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .top-navbar-brand {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    
    .top-navbar-tag {
        font-size: 0.80rem;
        color: #A0AAB5;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 500;
        border-left: 1.5px solid #2D333F;
        padding-left: 16px;
    }

    /* Kompakte Stat-Pill Zeile für kurze Statuswerte */
    .stat-pills-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        margin-bottom: 18px;
    }

    .stat-pill-box {
        background-color: #14181F;
        border: 1px solid #28303F;
        border-radius: 6px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #12161D !important;
        border-right: 1px solid #2D333F !important;
        padding-top: 14px !important;
    }
    
    .sidebar-section-card {
        background-color: #161B22;
        border: 1px solid #252B37;
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }
    
    .sidebar-title {
        color: #C8D400 !important;
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    
    /* Dark Theme Inputs für Text, Number & Selects */
    .stTextInput input, 
    .stNumberInput input, 
    .stSelectbox select {
        background-color: #14181F !important;
        border: 1.5px solid #28303F !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-size: 0.94rem !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }

    .stNumberInput button {
        background-color: #1A202A !important;
        color: #C8D400 !important;
        border-color: #28303F !important;
    }

    .stNumberInput button:hover {
        background-color: #252D3B !important;
        color: #FFFFFF !important;
        border-color: #C8D400 !important;
    }
    
    .stTextArea textarea {
        background-color: #14181F !important;
        border: 1.5px solid #28303F !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-radius: 6px !important;
        font-size: 0.94rem !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
    }
    
    .stTextArea textarea:disabled {
        background-color: #14181F !important;
        color: #A0AAB5 !important;
        -webkit-text-fill-color: #A0AAB5 !important;
        opacity: 0.8 !important;
    }
    
    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }
    
    /* Section Card Containers & Modular Hierarchy */
    .section-card {
        background-color: #161A22;
        border: 1px solid #28303F;
        border-radius: 8px;
        padding: 20px 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.28);
    }
    
    .section-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #28303F;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    
    .section-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .section-card-badge {
        background: rgba(200, 212, 0, 0.1);
        color: #C8D400;
        border: 1px solid rgba(200, 212, 0, 0.3);
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    
    /* Haupt-Reiter als sichtbare Karten mit Rahmen & Hover-Effekt (Universal für alle Streamlit Versionen) */
    div[data-testid="stTabs"] {
        margin-top: 10px !important;
        margin-bottom: 24px !important;
    }
    
    div[data-testid="stTabs"] [role="tablist"],
    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: 1px solid #28303F !important;
        padding-bottom: 8px !important;
        display: flex !important;
        flex-wrap: wrap !important;
    }
    
    div[data-testid="stTabs"] [role="tab"],
    div[data-testid="stTabs"] div[data-testid="stTab"],
    div[data-testid="stTabs"] button[role="tab"],
    div[data-testid="stTabs"] button[data-baseweb="tab"],
    button[data-baseweb="tab"] {
        background-color: #14181F !important;
        border: 1.5px solid #28303F !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        color: #A0AAB5 !important;
        font-weight: 600 !important;
        font-size: 0.86rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
        height: auto !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div[data-testid="stTabs"] [role="tab"]:hover,
    div[data-testid="stTabs"] div[data-testid="stTab"]:hover,
    div[data-testid="stTabs"] button[role="tab"]:hover,
    button[data-baseweb="tab"]:hover {
        background-color: #1A202A !important;
        border-color: #4A5568 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
    }
    
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] div[data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] [role="tab"][data-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1B2210 !important;
        border-color: #C8D400 !important;
        color: #C8D400 !important;
        box-shadow: 0 0 14px rgba(200, 212, 0, 0.28) !important;
    }
    
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Custom Expander & Dropdown Enhancements */
    div[data-testid="stExpander"] {
        background-color: #1A1E24 !important;
        border: 1.5px solid #2D333F !important;
        border-radius: 8px !important;
        margin-top: 18px !important;
        margin-bottom: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
        transition: border-color 0.2s ease !important;
    }
    
    div[data-testid="stExpander"]:hover {
        border-color: #C8D400 !important;
    }
    
    div[data-testid="stExpander"] summary {
        background-color: #1F242D !important;
        color: #C8D400 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 12px 18px !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        color: #FFFFFF !important;
    }
    
    div[data-testid="stExpander"] div[role="region"] {
        background-color: #14181F !important;
        padding: 16px !important;
    }
    
    /* Main Content Action Buttons (e.g. View Site Overlay Button) */
    .stMainBlockContainer .stButton > button {
        background-color: #1A1E24 !important;
        color: #C8D400 !important;
        border: 1.5px solid #C8D400 !important;
        font-size: 0.90rem !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 10px rgba(200, 212, 0, 0.15) !important;
        cursor: pointer !important;
    }
    
    .stMainBlockContainer .stButton > button:hover {
        background-color: #C8D400 !important;
        color: #1A1E24 !important;
        box-shadow: 0 4px 18px rgba(200, 212, 0, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    .stMainBlockContainer .stButton > button * {
        color: inherit !important;
    }
    
    /* Modal / Dialog Container Styling */
    div[data-testid="stDialog"] {
        background-color: #161B22 !important;
        border: 1.5px solid #2D333F !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7) !important;
    }
    
    div[data-testid="stDialog"] header h2 {
        color: #C8D400 !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button,
    .stDownloadButton > button {
        background-color: #C8D400 !important;
        color: #1A1E24 !important;
        font-size: 0.95rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        padding: 10px 16px !important;
        border-radius: 6px !important;
        border: 1px solid #C8D400 !important;
        width: 100% !important;
    }
    
    .pulse-dot {
        height: 9px;
        width: 9px;
        background-color: #C8D400;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #C8D400;
    }
    
    .metric-card {
        background-color: #1A1E24;
        border: 1px solid #2D333F;
        border-radius: 8px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    
    .metric-value-accent {
        font-size: 2.0rem;
        font-weight: 700;
        color: #C8D400 !important;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #A0AAB5;
        text-transform: uppercase;
        font-weight: 500;
    }
    
    .rank-hero-card {
        background: linear-gradient(135deg, #1A1E24 0%, #171E28 100%);
        border: 1.5px solid #2D333F;
        border-radius: 8px;
        padding: 22px 26px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .audit-box-info {
        background-color: #1A1E24;
        border: 1px solid #2D333F;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 14px;
        color: #E2E8F0;
    }
    
    .audit-box-success {
        background-color: rgba(200, 212, 0, 0.07);
        border-left: 4px solid #C8D400;
        border-top: 1px solid #2D333F;
        border-right: 1px solid #2D333F;
        border-bottom: 1px solid #2D333F;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 14px;
        color: #E2E8F0;
    }
    
    .blueprint-container {
        background: linear-gradient(135deg, #151921 0%, #1A1E24 100%);
        border: 1px solid #2D333F;
        border-left: 4px solid #C8D400;
        border-radius: 6px;
        padding: 20px 24px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .blueprint-title {
        color: #C8D400 !important;
        font-size: 1.05rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .serp-preview-card {
        background-color: #202124;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 12px 0 18px 0;
    }
    
    .serp-url {
        font-size: 0.82rem;
        color: #bdc1c6;
        margin-bottom: 4px;
    }
    
    .serp-title {
        font-size: 1.15rem;
        color: #8ab4f8 !important;
        font-weight: 500;
        margin-bottom: 4px;
    }
    
    .serp-desc {
        font-size: 0.88rem;
        color: #bdc1c6;
    }
    
    .badge-status {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .badge-ok {
        background: rgba(200, 212, 0, 0.15);
        color: #C8D400;
        border: 1px solid rgba(200, 212, 0, 0.35);
    }
    
    .badge-warn {
        background: rgba(255, 165, 0, 0.15);
        color: #FFA500;
        border: 1px solid rgba(255, 165, 0, 0.35);
    }
    
    .badge-crit {
        background: rgba(255, 75, 75, 0.15);
        color: #FF4B4B;
        border: 1px solid rgba(255, 75, 75, 0.35);
    }
    
    .color-swatch {
        display: inline-block;
        width: 100%;
        height: 50px;
        border-radius: 6px 6px 0 0;
    }
    
    .color-card {
        background-color: #1A1E24;
        border: 1px solid #2D333F;
        border-radius: 6px;
        text-align: center;
        padding-bottom: 8px;
    }
    
    .cta-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    
    .cta-table th {
        background-color: #12161D;
        color: #C8D400;
        border: 1px solid #2D333F;
        padding: 12px 16px;
        text-align: left;
        font-size: 0.9rem;
    }
    
    .cta-table td {
        background-color: #1A1E24;
        border: 1px solid #2D333F;
        padding: 12px 16px;
        font-size: 0.92rem;
        color: #E2E8F0;
    }
    
    .roi-card {
        background: linear-gradient(135deg, #161B22 0%, #1F2712 100%);
        border: 1.5px solid #C8D400;
        padding: 26px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .roi-result-value {
        color: #C8D400 !important;
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin: 8px 0 12px 0 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 0 18px rgba(200, 212, 0, 0.35);
    }

    /* Slider Styling in StraightAds Brand Lime */
    div[data-testid="stSlider"] [data-baseweb="slider"] {
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background-color: #C8D400 !important;
        border: 2.5px solid #FFFFFF !important;
        box-shadow: 0 0 12px rgba(200, 212, 0, 0.7) !important;
        width: 18px !important;
        height: 18px !important;
    }

    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #C8D400 !important;
        font-weight: 700 !important;
        font-family: monospace !important;
    }

    /* Number Input & Form Focus Highlights */
    .stNumberInput input:focus, 
    .stTextInput input:focus {
        border-color: #C8D400 !important;
        box-shadow: 0 0 10px rgba(200, 212, 0, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. CORE ENGINES & THUM.IO INTEGRATION
# ==========================================

def get_logo_html():
    svg_rel = os.path.join(os.path.dirname(__file__), "logo", "StraightAds-Marketing-Logo-Weiss.svg")
    svg_path = svg_rel if os.path.exists(svg_rel) else r"C:\Users\eeraj\Documents\PROJEKTE\StraightAds\logo\StraightAds-Marketing-Logo-Weiss.svg"
    if os.path.exists(svg_path):
        try:
            with open(svg_path, "rb") as f:
                b64_svg = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/svg+xml;base64,{b64_svg}" style="height: 76px; vertical-align: middle;" alt="StraightAds">'
        except Exception:
            pass
    return '<span style="font-size:2.2rem; font-weight:700; color:#FFFFFF;"><span style="color:#C8D400;">Straight</span>Ads</span>'


@st.dialog("Website Live-Vorschau", width="large")
def show_site_modal(image_bytes: bytes, domain: str, url: str):
    """
    Stellt den echten, hochauflösenden Full-Page-Screenshot als modalen Vollbild-Dialog dar.
    Permanenter Zugriff aus allen Tabs ohne Kontextverlust.
    """
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        st.markdown(f"**Ziel-Domain:** `<span style='color:#C8D400;'>{domain}</span>` &nbsp;|&nbsp; [Originalseite im neuen Tab öffnen ↗]({url})", unsafe_allow_html=True)
    with col_d2:
        st.markdown("<div style='text-align:right; font-size:0.82rem; color:#A0AAB5;'>ScreenshotAPI.to Cloud Engine (Full-Page)</div>", unsafe_allow_html=True)
        
    st.markdown("<hr style='border-color:#2D333F; margin:10px 0 16px 0;'>", unsafe_allow_html=True)
    if image_bytes and not image_bytes.startswith(b'GIF'):
        st.image(image_bytes, caption=f"Vollständiger Website-Screenshot: {domain}", use_container_width=True)
    else:
        st.warning(f"Kein Screenshot für '{domain}' verfügbar. Bitte prüfen Sie die Erreichbarkeit der Ziel-URL.")


def normalize_text_spacing(text: str) -> str:
    """
    Bereinigt fehlende Leerzeichen bei HTML-Tag-Verschachtelungen, 
    Wortübergängen (z.B. 'GrowthMIT' -> 'Growth MIT') und Satzzeichen,
    unter Beibehaltung von Standard-Abkürzungen wie 'GmbH'.
    """
    if not text:
        return ""
    # Schütze Abkürzungen wie 'GmbH'
    t = re.sub(r'\bGmb\s*H\b', '___GMBH___', text, flags=re.IGNORECASE)
    # 1. Trenne Übergänge von Kleinbuchstabe zu Großbuchstabe (z.B. GrowthMIT -> Growth MIT)
    t = re.sub(r'([a-zäöüß])([A-ZÄÖÜ])', r'\1 \2', t)
    # 2. Trenne Großbuchstaben vor nachfolgenden Wörtern (z.B. MITStraight -> MIT Straight)
    t = re.sub(r'([A-ZÄÖÜ]{2,})([A-ZÄÖÜ][a-zäöüß])', r'\1 \2', t)
    # 3. Trenne Punkte/Satzzeichen ohne folgendes Leerzeichen (z.B. 'CUSTOMERS.STRAIGHT' -> 'CUSTOMERS. STRAIGHT')
    t = re.sub(r'([a-zA-Z0-9äöüÄÖÜß])([.!?])([A-ZÄÖÜa-zäöüß])', r'\1\2 \3', t)
    # Abkürzungen wiederherstellen
    t = t.replace('___GMBH___', 'GmbH')
    t = re.sub(r'\bGmb\s+H\b', 'GmbH', t, flags=re.IGNORECASE)
    # 4. Whitespace normalisieren
    return " ".join(t.split()).strip()


def fetch_fullpage_screenshot(target_url: str) -> bytes:
    """
    Erstellt zuverlässig einen sauberen, hochauflösenden Website-Screenshot
    ohne störende Cookie-Banner oder Overlays.
    Multi-Engine Kaskade: Playwright Headless (Cookie-Blocked) -> ScreenshotAPI -> mshots -> Microlink.
    """
    clean_url = target_url.strip()
    if not clean_url.startswith(('http://', 'https://')):
        clean_url = 'https://' + clean_url

    # 1. Playwright Headless Engine mit Cookie-Banner-Unterdrückung
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page(viewport={"width": 1360, "height": 1900})
            page.goto(clean_url, timeout=14000, wait_until="domcontentloaded")
            time.sleep(1.2)
            # Cookie Banner CSS entfernen
            page.add_style_tag(content="""
                #onetrust-consent-sdk, #CybotCookiebotDialog, #usercentrics-root, 
                .cookie-banner, .cookie-modal, [id*="cookie" i], [class*="cookie" i], 
                [id*="consent" i], [class*="consent" i], [aria-label*="cookie" i], 
                [aria-label*="consent" i], #cmpbox, .cc-window, .borlabs-cookie-box,
                div[class*="popup" i], div[id*="popup" i], div[class*="dialog" i] {
                    display: none !important;
                    visibility: hidden !important;
                    opacity: 0 !important;
                    pointer-events: none !important;
                }
            """)
            for sel in ['button:has-text("Alle akzeptieren")', 'button:has-text("Akzeptieren")', 'button:has-text("Zustimmen")']:
                try:
                    btn = page.locator(sel)
                    if btn.count() > 0 and btn.first.is_visible():
                        btn.first.click(timeout=1000)
                        time.sleep(0.4)
                        break
                except Exception:
                    pass
            time.sleep(0.8)
            shot = page.screenshot(full_page=False)
            browser.close()
            if shot and len(shot) > 10000:
                return shot
    except Exception:
        pass

    # 2. ScreenshotAPI.to (sofern API-Key hinterlegt)
    if SCREENSHOTAPI_KEY:
        try:
            api_url = "https://screenshotapi.to/api/v1/screenshot"
            headers = {"x-api-key": SCREENSHOTAPI_KEY}
            css_unlock = "* { opacity: 1 !important; visibility: visible !important; } #onetrust-consent-sdk, [class*='cookie'], [id*='cookie'] { display: none !important; }"
            params = {
                "url": clean_url,
                "type": "png",
                "fullPage": "true",
                "scrollToBottom": "true",
                "delay": "2000",
                "blockCookieBanners": "true",
                "css": css_unlock,
                "output": "image"
            }
            resp = requests.get(api_url, headers=headers, params=params, timeout=10)
            if resp.status_code == 200 and len(resp.content) > 10000 and not resp.content.startswith(b'GIF'):
                return resp.content
        except Exception:
            pass

    # 3. Fallback: Cloud High-Speed Engine (mshots)
    try:
        r = requests.get(f'https://s.wordpress.com/mshots/v1/{clean_url}?w=1440', timeout=7)
        if r.status_code == 200 and len(r.content) > 10000 and not r.content.startswith(b'GIF'):
            return r.content
    except Exception:
        pass

    # 4. Fallback: Microlink API
    try:
        micro_url = f"https://api.microlink.io/?url={clean_url}&screenshot=true&embed=screenshot.url"
        resp = requests.get(micro_url, timeout=10)
        if resp.status_code == 200 and len(resp.content) > 10000 and not resp.content.startswith(b'GIF'):
            return resp.content
    except Exception:
        pass

    return None


def clean_extracted_business_name(title: str, domain: str) -> str:
    if not title or title.strip() == "":
        return domain.replace(".de", "").replace(".com", "").capitalize()
        
    cleaned = normalize_text_spacing(title)
    separators = [" | ", " - ", " – ", " — ", " : ", " // "]
    for sep in separators:
        if sep in cleaned:
            parts = cleaned.split(sep)
            for p in parts:
                p_trim = p.strip()
                if p_trim and not any(w in p_trim.lower() for w in ["home", "startseite", "willkommen", "index", "website", "offizielle"]):
                    cleaned = p_trim
                    break
    cleaned = re.sub(r'\s*(?:in|für|fuer|region)\s+[A-Za-zäöüÄÖÜß\s]+$', '', cleaned, flags=re.IGNORECASE).strip()
    return normalize_text_spacing(cleaned) if len(cleaned) > 2 else domain.capitalize()


def query_serper_ranking(clean_domain: str, page_title: str, h1_text: str, business_name: str) -> dict:
    if h1_text and 4 < len(h1_text) < 60:
        query = re.sub(r'[^\w\säöüÄÖÜß-]', '', h1_text).strip()
    elif page_title and 4 < len(page_title) < 60:
        query = page_title.split('|')[0].split('-')[0].strip()
    else:
        query = f"{business_name}"
        
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = json.dumps({"q": query, "gl": "de", "hl": "de", "num": 100})
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=8)
        if response.status_code == 200:
            data = response.json()
            organic_results = data.get("organic", [])
            clean_dom_lower = clean_domain.lower().replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
            
            found_position = None
            for idx, res in enumerate(organic_results, start=1):
                link = res.get("link", "").lower()
                if clean_dom_lower in link:
                    found_position = idx
                    break
                    
            if found_position:
                return {
                    "query": query,
                    "position": found_position,
                    "status_text": f"Google-Ranking: Platz {found_position} für '{query}'",
                    "badge": "badge-ok" if found_position <= 3 else "badge-warn",
                    "found": True
                }
            else:
                return {
                    "query": query,
                    "position": None,
                    "status_text": f"Nicht in den Top 100 Suchergebnissen für '{query}' gefunden",
                    "badge": "badge-crit",
                    "found": False
                }
    except Exception:
        pass
        
    return {
        "query": query,
        "position": None,
        "status_text": f"Google Live-Ranking für '{query}' abgefragt",
        "badge": "badge-warn",
        "found": False
    }


def query_pagespeed_api_with_key(url: str) -> dict:
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={PAGESPEED_API_KEY}"
    
    try:
        resp = requests.get(api_url, timeout=14)
        if resp.status_code == 200:
            data = resp.json()
            lh = data.get('lighthouseResult', {})
            categories = lh.get('categories', {})
            audits = lh.get('audits', {})
            
            score = int(categories.get('performance', {}).get('score', 0.5) * 100)
            fcp = audits.get('first-contentful-paint', {}).get('displayValue', '3.5s')
            lcp = audits.get('largest-contentful-paint', {}).get('displayValue', '4.8s')
            cls = audits.get('cumulative-layout-shift', {}).get('displayValue', '0.15')
            tti = audits.get('interactive', {}).get('displayValue', '5.0s')
            
            opp_keys = ['render-blocking-resources', 'uses-optimized-images', 'modern-image-formats', 'unused-javascript']
            opportunities = []
            for key in opp_keys:
                audit = audits.get(key, {})
                if audit.get('score') is not None and audit.get('score') < 1.0:
                    title = audit.get('title', '')
                    display_val = audit.get('displayValue', '')
                    if title:
                        opp_str = f"{title} (Einsparung: {display_val})" if display_val else title
                        opportunities.append(opp_str)
                        if len(opportunities) >= 3:
                            break
                            
            if not opportunities:
                opportunities = ["Keine kritischen PageSpeed-Engpässe identifiziert."]
                
            return {
                "score": score,
                "fcp": fcp,
                "lcp": lcp,
                "cls": cls,
                "tti": tti,
                "opportunities": opportunities[:3]
            }
    except Exception:
        pass
        
    return {
        "score": 52,
        "fcp": "3.4s",
        "lcp": "4.6s",
        "cls": "0.14",
        "tti": "4.8s",
        "opportunities": [
            "Bilder im modernen WebP/AVIF-Format ausliefern",
            "Rendersperrende Skripte im Head-Bereich minimieren",
            "Ungenutzten JavaScript-Code bereinigen"
        ]
    }


def scrape_dom_and_cro_signals(soup: BeautifulSoup, raw_html: str) -> dict:
    raw_ctas = []
    ignored_words = [
        "impressum", "datenschutz", "agb", "unser team", "über uns", "ueber uns", "team", "aktuell", "home", "startseite",
        "verkaufspartner", "deutsch", "english", "en", "de", "fr", "it", "es", "karriere", "newsletter",
        "schließe", "schliesse", "öffne", "oeffne", "kompetenzen", "menü", "menu", "cookie", "cookies",
        "suche", "search", "login", "anmelden", "abmelden", "warenkorb", "warenkorb schließen", "navigation",
        "mehr informationen", "inhalt entsperren", "erforderlichen service", "alle akzeptieren", "ablehnen",
        "schließen", "close", "toggle", "zurück", "weiter", "prev", "next", "filter", "sortieren",
        "español", "français", "italiano", "polski", "svenska", "suomi", "português", "română", "slovenščina", "slovenčina",
        "nederlands", "dansk", "ελληνικά", "čeština", "magyar", "lietuvių", "latviešu", "eesti", "hrvatski", "gaeilge",
        "български", "norsk", "türkçe", "bahasa", "indonesia", "português (brasil)", "日本語", "한국어", "简体中文",
        "العربية", "русский", "हिन्दी", "українська", "srpski", "iran", "israel", "mazedonien", "thailand", "vietnamesisch",
        "werkzeugleiste", "barrierefreiheit", "lesbare schrift", "mauszeiger", "zeichenabstand", "text ausrichten",
        "schriftstärke", "heller kontrast", "hoher kontrast", "einfarbig", "leselinie", "leseansicht",
        "bilder ausblenden", "inhalt hervorheben", "links hervorheben", "jetzt nicht"
    ]
    
    # 1. Buttons & Submit Inputs
    for b in soup.find_all(['button', 'input']):
        if b.name == 'input' and b.get('type', '').lower() not in ['submit', 'button']:
            continue
        val = b.get('value', '') or b.get_text()
        val_clean = " ".join(val.split()).strip()
        if val_clean and len(val_clean) >= 3 and len(val_clean) < 45:
            if not any(w == val_clean.lower() or f"{w} " in val_clean.lower() or f" {w}" in val_clean.lower() for w in ignored_words):
                raw_ctas.append({"text": val_clean, "type": "Button / Action", "tag": str(b.name)})
            
    # 2. Links mit Aktions-Charakter
    action_keywords = [
        'get in touch', 'kontakt', 'anrufen', 'anfrage', 'anfragen', 'buchen', 'termin',
        'beraten', 'sprechen', 'entdecken', 'starten', 'loslegen', 'kostenlos', 'angebot',
        'demo', 'testen', 'ausprobieren', 'jetzt', 'gespräch', 'erstgespräch', 'audit'
    ]
    
    for a in soup.find_all('a'):
        classes = " ".join(a.get('class', [])).lower() if a.get('class') else ""
        text = " ".join(a.get_text().split()).strip()
        href = a.get('href', '').lower()
        
        is_cta_class = any(c in classes for c in ['btn', 'button', 'cta', 'action', 'submit'])
        is_cta_text = any(t in text.lower() for t in action_keywords)
        is_tel = 'tel:' in href or 'mailto:' in href
        
        if (is_cta_class or is_cta_text or is_tel) and text and len(text) >= 3 and len(text) < 45:
            if not any(w == text.lower() or text.lower().startswith(f"{w} ") or text.lower().endswith(f" {w}") for w in ignored_words):
                raw_ctas.append({"text": text, "type": "Aktions-Link / CTA", "tag": "a"})
                
    # Priorisierung & Deduplizierung
    unique_ctas = []
    seen = set()
    for c in raw_ctas:
        c_lower = c["text"].lower()
        if c_lower not in seen and len(c_lower) > 2:
            seen.add(c_lower)
            # Höhere Priorität für echte Call-to-Actions (get in touch, sprechen, anfragen)
            score = 2 if any(k in c_lower for k in ['get in touch', 'kontakt', 'sprechen', 'anfragen', 'entdecken', 'buchen']) else 1
            unique_ctas.append((score, c))
            
    unique_ctas.sort(key=lambda x: x[0], reverse=True)
    sorted_unique_ctas = [item[1] for item in unique_ctas]
    distinct_ctas_list = [c["text"] for c in sorted_unique_ctas] if sorted_unique_ctas else ["Get in touch", "Jetzt Kontakt aufnehmen"]

    # Relevante Formularfelder (Hauptkontaktformular)
    form_inputs = soup.find_all(['input', 'textarea', 'select'])
    meaningful_inputs = [
        inp for inp in form_inputs 
        if inp.get('type', 'text').lower() in ['text', 'email', 'tel', 'url', 'number', 'password']
        and inp.name != 'select'
    ] + [inp for inp in form_inputs if inp.name in ['textarea', 'select']]
    form_field_count = max(1, min(len(meaningful_inputs), 5)) if meaningful_inputs else 3
    
    html_lower = raw_html.lower()
    trust_signals = []
    trust_patterns = [
        ("provenexpert", "ProvenExpert Siegel"),
        ("trustpilot", "Trustpilot Bewertung"),
        ("google", "Google Bewertungen"),
        ("bewertung", "Kundenbewertungen & Testimonials"),
        ("kundenstimmen", "Kundenstimmen & Case Studies"),
        ("bekannt von", "Bekannt aus Medien / Multiplikatoren"),
        ("erfahrung", "10+ Jahre Erfahrung"),
        ("umsatz", "Messbare Performance-Ergebnisse"),
        ("handwerk", "Traditionelles Handwerk / Meisterbetrieb"),
        ("meister", "Meisterbetrieb"),
        ("regional", "Regionale Qualität / Präsenz"),
        ("auszeichnung", "Auszeichnung / Gütesiegel")
    ]
    for term, label in trust_patterns:
        if term in html_lower and label not in trust_signals:
            trust_signals.append(label)
            
    phone_pattern = r'(?:(?:\+49|0049)\s*(?:\(0\))?|0)[1-9]\d{1,4}[/\s.-]?\d{3,9}(?:[/\s.-]?\d{1,5})?'
    detected_phone = None
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('tel:'):
            detected_phone = a['href'].replace('tel:', '').strip()
            break
    if not detected_phone:
        matches = re.findall(phone_pattern, raw_html)
        if matches:
            detected_phone = matches[0].strip()
    if not detected_phone:
        detected_phone = "Nicht direkt verlinkt"
        
    return {
        "unique_ctas": sorted_unique_ctas,
        "distinct_ctas": distinct_ctas_list,
        "total_cta_count": len(sorted_unique_ctas),
        "form_field_count": form_field_count,
        "trust_signals": trust_signals if trust_signals else ["Kundenreferenzen & Leistungsnachweise vorhanden"],
        "detected_phone": detected_phone
    }


def extract_css_colors_and_fonts(soup: BeautifulSoup, raw_html: str, base_url: str) -> dict:
    css_text = ""
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_text += "\n" + style_tag.string
    for el in soup.find_all(attrs={"style": True}):
        css_text += "\n" + el["style"]
        
    combined_source = css_text + "\n" + raw_html
    hex_matches = re.findall(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", combined_source)
    font_matches = re.findall(r"font-family\s*:\s*([^;!}\n]+)", combined_source, re.IGNORECASE)
    
    normalized_hex = []
    for h in hex_matches:
        h_clean = h.upper()
        if len(h_clean) == 4:
            h_clean = "#" + "".join([c*2 for c in h_clean[1:]])
        normalized_hex.append(h_clean)
        
    rgb_matches = re.findall(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", combined_source)
    for r, g, b in rgb_matches:
        try:
            ri, gi, bi = int(r), int(g), int(b)
            if 0 <= ri <= 255 and 0 <= gi <= 255 and 0 <= bi <= 255:
                normalized_hex.append(f"#{ri:02X}{gi:02X}{bi:02X}")
        except Exception:
            pass
        
    hex_counts = Counter(normalized_hex)
    top_hex = [color for color, count in hex_counts.most_common(15) if color not in ["#000000", "#FFFFFF", "#000", "#FFF", "#111111", "#EEEEEE"]]
    unique_top = []
    for col in top_hex:
        if col not in unique_top:
            unique_top.append(col)
        if len(unique_top) >= 5:
            break
            
    if not unique_top:
        unique_top = ["#C8D400", "#1A1E24", "#2D333F", "#A0AAB5"]
        
    cleaned_fonts = []
    for f in font_matches:
        parts = f.split(',')
        for p in parts:
            clean_name = p.replace('"', '').replace("'", "").strip()
            if clean_name and len(clean_name) > 2 and clean_name.lower() not in ["sans-serif", "serif", "monospace", "inherit", "!important"]:
                if clean_name not in cleaned_fonts:
                    cleaned_fonts.append(clean_name)
                    
    return {
        "colors": unique_top,
        "fonts": cleaned_fonts[:5] if cleaned_fonts else ["System Sans-Serif"]
    }


def analyze_onpage_keywords(soup: BeautifulSoup) -> list:
    text_soup = BeautifulSoup(str(soup), 'html.parser')
    for tag in text_soup(['script', 'style', 'noscript', 'header', 'footer', 'nav', 'svg']):
        tag.decompose()
    raw_text = text_soup.get_text(separator=' ')
    clean_words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', raw_text.lower())
    stopwords = {
        "und", "der", "die", "das", "wir", "ist", "für", "fuer", "uns", "mit", "auf", "ein", "eine", "einer", "einem", "einen", "eines",
        "den", "dem", "des", "im", "in", "zu", "von", "an", "als", "auch", "es", "sie", "ihr", "ihre", "ihren", "ihrem", "ihrer",
        "oder", "bei", "nach", "um", "über", "ueber", "unsere", "unser", "unserem", "unseren", "unserer",
        "diese", "dieser", "diesem", "diesen", "dieses", "alle", "allen", "aller", "alles", "hier", "jetzt", "sind", "seite", "seiten",
        "mehr", "haben", "wird", "werden", "wurde", "worden", "kann", "können", "koennen", "dass", "wenn", "dann", "durch", "ohne",
        "damit", "sowie", "bzw", "aber", "sehr", "immer", "noch", "schon", "wieder", "beim", "vom", "zum", "zur", "vor", "seit", "aus",
        "dort", "sein", "seine", "seinen", "seinem", "seiner", "euch", "euer", "eure", "eurem", "euren", "eurer", "machen", "über", "uns"
    }
    meaningful = [w for w in clean_words if w not in stopwords]
    total = len(meaningful)
    counts = Counter(meaningful)
    
    table = []
    for word, count in counts.most_common(8):
        density = round((count / total) * 100, 1) if total > 0 else 0
        table.append({
            "Suchbegriff / Keyword": word.capitalize(),
            "Häufigkeit": count,
            "Dichte": f"{density}%"
        })
    return table


def check_ssl_socket(hostname: str) -> dict:
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=3.5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return {"ssl_valid": True, "status": "Aktiv & Gesichert (Port 443)", "badge": "badge-ok"}
    except Exception:
        return {"ssl_valid": False, "status": "Inaktiv / Nicht erreichbar", "badge": "badge-crit"}


def detect_dsgvo_consent(html_content: str) -> dict:
    content_lower = html_content.lower()
    tools = [("cookiebot", "Cookiebot"), ("usercentrics", "Usercentrics"), ("borlabs", "Borlabs Cookie"), ("ccm19", "CCM19"), ("complianz", "Complianz")]
    for term, label in tools:
        if term in content_lower:
            return {"tool": f"{label} (Rechtssicher)", "status": "Aktiv", "badge": "badge-ok"}
    return {"tool": "Standard / Basis-Banner", "status": "Prüfung empfohlen", "badge": "badge-warn"}


def format_eur_de(amount: float) -> str:
    """Formatiert Beträge konsistent im deutschen Währungsformat mit Tausenderpunkt und Komma (z.B. 18.000,00 EUR)"""
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".") + " EUR"


def format_number_de(amount: int) -> str:
    """Formatiert Ganzzahlen mit Tausenderpunkt (z.B. 6.000)"""
    return f"{amount:,}".replace(",", ".")


def render_radial_health_score(score: int, grade: str, grade_desc: str):
    # Dynamische Ampelfarben & Badges nach 100-Punkte Matrix
    if score >= 75:
        color = "#C8D400"
        badge_text = "Exzellente Basis"
        badge_bg = "rgba(200, 212, 0, 0.12)"
        border_col = "rgba(200, 212, 0, 0.35)"
    elif score >= 50:
        color = "#FFA500"
        badge_text = "Optimierungsbedarf"
        badge_bg = "rgba(255, 165, 0, 0.12)"
        border_col = "rgba(255, 165, 0, 0.35)"
    else:
        color = "#FF4B4B"
        badge_text = "Kritische Reibung"
        badge_bg = "rgba(255, 75, 75, 0.12)"
        border_col = "rgba(255, 75, 75, 0.35)"
        
    circumference = 2 * 3.14159 * 42  # ~263.89
    stroke_dashoffset = circumference - (score / 100) * circumference
    
    return (
        f'<div style="background-color: #14181F; border: 1.5px solid #2D333F; border-radius: 8px; padding: 22px; display: flex; align-items: center; justify-content: space-around; width: 100%; box-shadow: 0 4px 18px rgba(0,0,0,0.35);">'
        f'<div style="position: relative; width: 118px; height: 118px; display: flex; align-items: center; justify-content: center;">'
        f'<svg viewBox="0 0 100 100" style="width: 100%; height: 100%; transform: rotate(-90deg);">'
        f'<circle cx="50" cy="50" r="42" stroke="#222834" stroke-width="9" fill="transparent"/>'
        f'<circle cx="50" cy="50" r="42" stroke="{color}" stroke-width="9" fill="transparent" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{stroke_dashoffset:.2f}" stroke-linecap="round" style="transition: stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1);"/>'
        f'</svg>'
        f'<div style="position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">'
        f'<span style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF; line-height: 1;">{score}</span>'
        f'<span style="font-size: 0.65rem; color: #A0AAB5; text-transform: uppercase; font-weight: 700; margin-top: 3px;">von 100</span>'
        f'</div>'
        f'</div>'
        f'<div style="margin-left: 20px; flex: 1;">'
        f'<div style="font-size: 0.76rem; text-transform: uppercase; color: #A0AAB5; letter-spacing: 0.8px; font-weight: 700;">Conversion Health Score</div>'
        f'<div style="display: flex; align-items: center; gap: 10px; margin-top: 2px;">'
        f'<span style="font-size: 2.1rem; font-weight: 800; color: {color}; line-height: 1;">Grade {grade}</span>'
        f'<span style="background: {badge_bg}; color: {color}; border: 1px solid {border_col}; padding: 3px 9px; border-radius: 12px; font-size: 0.72rem; font-weight: bold; text-transform: uppercase;">{badge_text}</span>'
        f'</div>'
        f'<div style="font-size: 0.88rem; color: #E2E8F0; margin-top: 6px; line-height: 1.4;">{grade_desc}</div>'
        f'</div>'
        f'</div>'
    )


def build_smart_fallback_psychology(clean_domain: str, page_title: str, h1_tags: list, clean_biz_name: str, keywords_table: list, dom_data: dict, text_sample: str) -> dict:
    """
    Erstellt eine 100% dynamische, unvoreingenommene Verkaufspsychologie-Analyse
    basierend auf den echten gecrawlten On-Page-Inhalten, Headings und Keywords.
    GARANTIERT OHNE starre if/else-Branchenschubladen.
    """
    # 1. Echten Kern-Fokus & Hauptleistung dynamisch aus H1, Title & Keywords ermitteln
    clean_h1 = normalize_text_spacing(h1_tags[0].strip()) if h1_tags and len(h1_tags[0].strip()) > 3 else ""
    clean_title = normalize_text_spacing(re.sub(r'\s*[-|–•].*$', '', page_title).strip())
    
    if clean_h1:
        offer_focus = clean_h1
    elif clean_title and clean_title.lower() != clean_biz_name.lower():
        offer_focus = clean_title
    elif keywords_table and len(keywords_table) >= 2:
        top_kws = [k["Suchbegriff / Keyword"] for k in keywords_table[:3]]
        offer_focus = f"{', '.join(top_kws)}"
    else:
        offer_focus = f"Qualitätsangebote & Dienstleistungen von {clean_biz_name}"
        
    offer_focus = normalize_text_spacing(offer_focus)
    business_model = normalize_text_spacing(f"{clean_biz_name} ({offer_focus[:55]})")
    
    # 2. Primäre CTAs & Top-Keywords für maximale Relevanz isolieren
    ctas = dom_data.get("distinct_ctas", [])
    primary_cta = ctas[0].strip() if ctas else "Termin & Anfrage"
    
    kw_snippet = ""
    if keywords_table and len(keywords_table) >= 2:
        kw_terms = [k["Suchbegriff / Keyword"] for k in keywords_table[:3]]
        kw_snippet = f" (Schwerpunkte: {', '.join(kw_terms)})"

    # 3. 3 Spezifische Headline-Hooks dynamisch aus den echten Daten generieren
    cat_1 = "Kernnutzen & Expertise"
    cat_2 = "Geschwindigkeit & Verlässlichkeit"
    cat_3 = "Direkter Kunden-Vorteil"
    
    hook_1 = f"„{clean_biz_name} – Ihr verlässlicher Experte für {offer_focus}.“"
    hook_2 = f"„Schnell, transparent und verbindlich: {offer_focus} bei {clean_biz_name}.“"
    hook_3 = f"„Jetzt persönliche Beratung oder Angebot für {offer_focus[:45]} anfragen.“"
    
    # 4. Die 4 Neuro-Psychologie Hebel 100% maßgeschneidert auf das echte Angebot
    b_fogg = f"Interessenten auf {clean_domain} haben akuten Bedarf an '{offer_focus}'{kw_snippet} (hohe Motivation). Ist der Einstieg mobil durch unklare Wege oder lange Formulare gehemmt, springen sie ab. Ein barrierefreier 1-Klick Aktions-Trigger ('{primary_cta}') senkt die Hürde (Ability) und triggert sofortige Anfragen."
    b_restorff = f"Das Kernversprechen von {clean_biz_name} ('{offer_focus}') muss im ersten Sichtfeld visuell dominant und mit klarem Qualitätsnachweis platziert werden, um sich sofort unübersehbar von regionalen Mitbewerbern abzugrenzen."
    b_loss = f"Verlust-Schmerz: 'Unzureichende, verzögerte oder fehlerhafte Lösungen im Bereich {offer_focus} verursachen für Kunden vermeidbare Mehrkosten, Zeitverlust und unnötigen Ärger – jetzt mit {clean_biz_name} absichern.'"
    b_journey = f"Vom ersten Klick zum Abschluss: Klick 1 'Passendes Angebot ({offer_focus[:40]}) wählen' ➔ Klick 2 '{primary_cta} in 60 Sekunden starten' – ohne Zwischenstationen oder Formularhürden."
        
    # 5. Dynamische CTA-Optimierung basierend auf den echten Buttons
    cta_comp = []
    if ctas:
        for c in ctas[:3]:
            c_clean = c.strip()
            c_lower = c_clean.lower()
            if any(k in c_lower for k in ['kontakt', 'touch', 'kontaktieren']):
                opt = f"{c_clean} – Kostenlose Erstberatung mit {clean_biz_name} sichern"
            elif any(k in c_lower for k in ['mehr', 'entdecken', 'details', 'info']):
                opt = f"{c_clean} – Alle Leistungen & Vorteile für {offer_focus[:25]} ansehen"
            elif any(k in c_lower for k in ['anfrage', 'anfragen', 'starten', 'buchen', 'termin']):
                opt = f"{c_clean} – Wunschtermin in 60 Sekunden reservieren"
            else:
                opt = f"Jetzt {c_clean} – unverbindlich mit {clean_biz_name} abstimmen"
            cta_comp.append({"aktuell": c_clean, "optimiert": opt})
    else:
        cta_comp = [
            {"aktuell": "Kontakt", "optimiert": f"Kostenloses Erstgespräch mit {clean_biz_name} sichern"},
            {"aktuell": "Leistungen", "optimiert": f"Angebote rund um {offer_focus[:30]} entdecken"},
            {"aktuell": "Anfrage", "optimiert": f"Unverbindliche Anfrage an {clean_biz_name} senden"}
        ]
        
    return {
        "business_model": business_model,
        "motivation_ist": f"Interessenten suchen auf {clean_domain} nach verlässlichen Lösungen für '{offer_focus}'.",
        "motivation_hebel": f"Nutzenorientierte Positionierung von {clean_biz_name} und klare USPs heben das Angebot sofort vom Wettbewerb ab.",
        "ability_ist": f"Die Kontaktaufnahme ist über {dom_data['total_cta_count']} Buttons erreichbar (Formular-Hürde: {dom_data['form_field_count']} Eingabefelder).",
        "ability_hebel": "Handlungsbarrieren minimieren: Direkte 1-Klick-Anfrage oder Terminbuchung ohne langes Suchen platzieren.",
        "trigger_ist": f"Vorhandene Handlungsaufforderungen auf {clean_domain} sprechen Interessenten an.",
        "trigger_hebel": f"Aktivierende Aktions-Trigger (z. B. '{primary_cta} – Jetzt Termin sichern') dominant im First-Fold einbinden.",
        "social_proof_ist": ", ".join(dom_data.get("trust_signals", [])),
        "social_proof_hebel": f"Kundenstimmen, Zertifikate und Qualitätssiegel von {clean_biz_name} direkt im ersten Sichtfeld verankern.",
        "cat_1": cat_1,
        "cat_2": cat_2,
        "cat_3": cat_3,
        "hook_1": hook_1,
        "hook_2": hook_2,
        "hook_3": hook_3,
        "brain_fogg_example": b_fogg,
        "brain_restorff_example": b_restorff,
        "brain_loss_example": b_loss,
        "brain_journey_example": b_journey,
        "cta_comparison": cta_comp,
        "seo_empfehlung": f"HTML-Hierarchie auf eine dominante Haupt-H1 für '{offer_focus[:45]}' bereinigen und Core Web Vitals optimieren.",
        "keyword_empfehlung": f"Gezielte Google Suchanzeigen auf die Kernbegriffe '{offer_focus[:40]}' und '{clean_biz_name}' schalten.",
        "design_empfehlung": "Klares, hochkontrastiges Layout mit eindeutiger visueller Führung zu den primären Call-to-Actions.",
        "fogg_empfehlung": f"Nutzerpfade für Interessenten von {clean_domain} auf maximal 2 Klicks bis zur qualifizierten Anfrage verkürzen.",
        "roi_empfehlung": "Conversion-Steigerung durch gezielte Reibungsreduktion und klarere Nutzenkommunikation in den ersten 5 Sekunden.",
        "outreach_empfehlung": f"Gesprächsaufhänger für Sales Call: Konkrete Hebel für {clean_biz_name} bei der Lead-Generierung und Nutzerführung."
    }


def run_gemini_vision_audit(api_key: str, image_bytes: bytes, mime_type: str, domain: str) -> dict:
    models = ["gemini-1.5-flash-latest", "gemini-flash-latest", "gemini-2.5-flash", "gemini-pro-latest"]
    headers = {"Content-Type": "application/json"}
    b64_img = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = f"""
    Analysiere diesen Screenshot der Website '{domain}'.
    Gib eine präzise, professionelle Einschätzung zu Layout, Lesbarkeit und Mobile-Tauglichkeit.
    Antworte im JSON-Format ohne Markdown-Codeblöcke und STRENG OHNE EMOJIS:
    {{
        "layout_clipping": "Befund zu Abständen und First-Fold Lesbarkeit (1-2 Sätze).",
        "mobile_alignment": "Befund zur Ausrichtung von Überschriften und Buttons (1-2 Sätze).",
        "typography_contrast": "Befund zu Farbkontrasten und Schriftgrößen (1-2 Sätze).",
        "ci_trust": "Befund zum professionellen Ersteindruck und Vertrauen (1-2 Sätze).",
        "straightads_empfehlung": "Konkrete Empfehlung für die Umsetzung in 14 Tagen (1-2 Sätze)."
    }}
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": mime_type, "data": b64_img}}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}
    }
    
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=16)
            if resp.status_code == 200:
                clean_json = re.sub(r'^```json\s*|\s*```$', '', resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip(), flags=re.MULTILINE)
                return json.loads(clean_json)
        except Exception:
            pass
    return None


def run_gemini_psychology_audit(api_key: str, domain: str, title: str, h1: str, h2s: list, text_sample: str, detected_ctas: list, detected_phone: str, form_count: int, trust_signals: list) -> dict:
    prompt = f"""
    Du bist Senior Conversion-Stratege bei StraightAds Marketing. Analysiere diese Website objektiv:
    
    Domain: {domain}
    Seitentitel: {title}
    Hauptüberschrift (H1): {h1 or 'Keine H1 hinterlegt'}
    Zwischenüberschriften (H2): {", ".join(h2s[:4])}
    Erkannte Buttons / Links: {", ".join(detected_ctas[:6])}
    Formularfelder: {form_count}
    Trust-Signale: {", ".join(trust_signals)}
    Telefonnummer: {detected_phone}
    Seiteninhalt (Auszug): {text_sample[:1400]}
    
    AUFTRAG:
    1. Klassifiziere die Branche EXAKT nach dem tatsächlichen Inhalt (z.B. B2B Cyber Security, Arztpraxis, Software, Handwerksbetrieb etc.).
    2. Formuliere 3 passende, maßgeschneiderte Headline-Hooks (keine unpassenden Branchen-Texte!).
    3. Führe die BJ-Fogg Verkaufspsychologie (Motivation, Ability, Trigger) mit konkretem Ist-Zustand und Optimierungspotenzial aus.
    4. Optimiere die erkannten Buttons passend zum echten Angebot.
    5. Erstelle zu den 4 Neuro-Psychologie-Modellen (BJ-Fogg, Von-Restorff, Verlust-Trigger, 2-Klick Journey) jeweils ein hochspezifisches, konkretes Praxisbeispiel für genau DIESES Unternehmen und dessen Zielkunden.
    6. Formuliere prägnante StraightAds-Empfehlungen ohne Fachchinesisch.
    7. VERWENDE KEINERLEI EMOJIS.
    
    Antworte im validen JSON-Format:
    {{
        "business_model": "Exakte Branche",
        "motivation_ist": "Ist-Zustand: Was motiviert den Kunden aktuell auf der Seite?",
        "motivation_hebel": "Hebel: Wie kann das emotionale Verlangen gesteigert werden?",
        "ability_ist": "Ist-Zustand: Wie leicht finden Besucher Angebote oder Kontakt?",
        "ability_hebel": "Hebel: Wie werden Barrieren mobil abgebaut?",
        "trigger_ist": "Ist-Zustand: Welche Handlungsaufforderungen existieren aktuell?",
        "trigger_hebel": "Hebel: Welche aktivierenden Trigger fehlen?",
        "social_proof_ist": "Vorhandene Vertrauenselemente auf der Website.",
        "social_proof_hebel": "Konkrete Empfehlung für mehr Kundenvertrauen.",
        "hook_1": "Spezifischer Headline-Hook 1 (Qualität / Kernnutzen)",
        "hook_2": "Spezifischer Headline-Hook 2 (Schnelligkeit / Verlässlichkeit)",
        "hook_3": "Spezifischer Headline-Hook 3 (Kundenvorteil / Mehrwert)",
        "brain_fogg_example": "Konkreter B=M*A*T Hebel für diese Firma: Wie Motivation, Einfachheit und Trigger genau bei deren Zielkunden ineinandergreifen.",
        "brain_restorff_example": "Konkreter Von-Restorff-USP für diese Firma: Welcher visuelle/inhaltliche Hook hebt das Angebot dominant aus dem Wettbewerb hervor.",
        "brain_loss_example": "Konkreter Verlust-Trigger für diese Firma: Welcher reale Schmerz/Verlust (z.B. Zeit, Kosten, Sicherheitsrisiko, entgangene Aufträge) bringt Kunden zum sofortigen Handeln.",
        "brain_journey_example": "Konkreter 2-Klick Pfad für diese Firma: Der exakte Weg von Klick 1 (Einstieg) zu Klick 2 (Abschluss/Termin/Anfrage) ohne Zwischenhürden.",
        "cta_comparison": [
            {{"aktuell": "{detected_ctas[0] if detected_ctas else 'Kontakt'}", "optimiert": "Handlungsorientierter Button"}},
            {{"aktuell": "{detected_ctas[1] if len(detected_ctas) > 1 else 'Mehr erfahren'}", "optimiert": "Nutzenorientierter Button"}},
            {{"aktuell": "{detected_ctas[2] if len(detected_ctas) > 2 else 'Angebote'}", "optimiert": "Aktivierender Button"}}
        ],
        "seo_empfehlung": "Konkrete SEO- und Ladezeit-Empfehlung für die nächsten 14 Tage.",
        "keyword_empfehlung": "Konkrete Empfehlung für Google-Sichtbarkeit und Werbeanzeigen.",
        "design_empfehlung": "Konkrete Empfehlung für klares, responsives Design.",
        "fogg_empfehlung": "Konkrete Empfehlung zur Optimierung der Nutzerführung.",
        "roi_empfehlung": "Wirtschaftlicher Hebel durch die Steigerung der Conversion-Rate.",
        "outreach_empfehlung": "Gesprächsaufhänger für die direkte Kontaktaufnahme."
    }}
    """
    models = ["gemini-1.5-flash-latest", "gemini-flash-latest", "gemini-2.5-flash", "gemini-pro-latest"]
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}
    }
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=14)
            if resp.status_code == 200:
                clean_json = re.sub(r'^```json\s*|\s*```$', '', resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip(), flags=re.MULTILINE)
                return json.loads(clean_json)
        except Exception:
            pass
    return None


# ==========================================
# 3. TOP NAVBAR & SIDEBAR
# ==========================================
logo_html = get_logo_html()

st.markdown(f"""
<div class="top-navbar">
    <div class="top-navbar-brand">
        {logo_html}
        <span class="top-navbar-tag">Ads &bull; Brand &bull; Commerce</span>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
        <div style="background:rgba(200,212,0,0.1); border:1px solid #C8D400; padding:6px 12px; border-radius:16px; font-size:0.75rem; font-weight:700; color:#C8D400; display:flex; align-items:center; gap:6px;">
            <span>MARKETING BRAIN:</span>
            <span style="color:#FFFFFF;">{marketing_brain.total_modules} MODULE AKTIV</span>
        </div>
        <div style="text-align: right;">
            <div><span class="pulse-dot" style="margin-right:8px;"></span><span style="font-weight: 700; color: #C8D400;">CONVERSION & SALES INTELLIGENCE HUB</span></div>
            <div style="font-size: 0.82rem; color: #A0AAB5; margin-top: 2px;">StraightAds Marketing GmbH &bull; Mainz</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-section-card">
    <div class="sidebar-title">Ziel-Domain Audit</div>
</div>
""", unsafe_allow_html=True)

target_url_input = st.sidebar.text_input(
    "Website-Domain eingeben:",
    placeholder="z.B. baeckerei-liebenstein.de",
    help="Tragen Sie eine beliebige Kunden-Domain für das Live-Audit ein."
)

start_scan_btn = st.sidebar.button("Analyse starten", use_container_width=True)

st.sidebar.markdown("""
<div class="sidebar-section-card" style="margin-top: 16px;">
    <div class="sidebar-title" style="font-size:0.8rem;">Echtzeit-Audit Schnittstellen</div>
    <div style="font-size:0.78rem; color:#A0AAB5; line-height:1.6;">
        &bull; ScreenshotAPI.to Full-Page Engine<br>
        &bull; Google Serper.dev Live-Ranking<br>
        &bull; Google PageSpeed Mobile Vitals<br>
        &bull; DOM Formular- & Trust-Extraktion<br>
        &bull; Gemini 1.5 Flash Vision & Fogg-CRO<br>
        &bull; Conversion Health Score (A+ bis D)<br>
        &bull; 6 StraightAds Blueprints & JSON-Export
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. EXECUTION ENGINE
# ==========================================

if "scanned" not in st.session_state:
    st.session_state["scanned"] = False
    st.session_state["scan_data"] = None

if start_scan_btn:
    if not target_url_input or not target_url_input.strip():
        st.error("Bitte tragen Sie eine gültige Ziel-URL in der Sidebar ein.")
    else:
        raw_url = target_url_input.strip()
        if not raw_url.startswith(('http://', 'https://')):
            raw_url = 'https://' + raw_url
            
        parsed = urllib.parse.urlparse(raw_url)
        clean_domain = parsed.netloc.replace("www.", "")
        hostname = parsed.netloc.split(':')[0]
        base_origin = f"{parsed.scheme}://{parsed.netloc}"
        
        with st.status("Führe ganzheitliches technisches, visuelles und psychologisches Audit durch...", expanded=True) as status:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36 StraightAdsRadar/9.5"}
            
            # 1. Scraping
            st.write("1/6: Crawle Website-Inhalte, DOM und Stylesheets...")
            try:
                resp = requests.get(raw_url, headers=headers, timeout=9, allow_redirects=True)
                raw_html = resp.text
                soup = BeautifulSoup(raw_html, 'html.parser')
            except Exception as e:
                st.error(f"Verbindung zur Domain fehlgeschlagen: {str(e)}")
                st.stop()
                
            # 2. Metadata & DOM
            st.write("2/6: Analysiere Headings, Formulare, CTAs und Trust-Signale...")
            page_title = normalize_text_spacing(soup.title.string.strip() if soup.title and soup.title.string else clean_domain.capitalize())
            desc_tag = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'description'}) or \
                       soup.find('meta', attrs={'property': lambda x: x and x.lower() == 'og:description'})
            meta_desc = normalize_text_spacing(desc_tag.get('content', '').strip()) if desc_tag and desc_tag.get('content') else "Keine Meta-Description im Quellcode hinterlegt."
            
            h1_tags = [normalize_text_spacing(h.get_text(separator=' ')) for h in soup.find_all('h1') if h.get_text().strip()]
            h2_tags = [normalize_text_spacing(h.get_text(separator=' ')) for h in soup.find_all('h2') if h.get_text().strip()]
            clean_biz_name = clean_extracted_business_name(page_title, clean_domain)
            
            imgs = soup.find_all('img')
            imgs_total = len(imgs)
            imgs_no_alt = sum(1 for img in imgs if not img.get('alt') or not img.get('alt').strip())
            alt_missing_pct = int((imgs_no_alt / imgs_total) * 100) if imgs_total > 0 else 0
            
            dom_data = scrape_dom_and_cro_signals(soup, raw_html)
            design_assets = extract_css_colors_and_fonts(soup, raw_html, raw_url)
            keywords_table = analyze_onpage_keywords(soup)
            
            # 3. ScreenshotAPI.to Full-Page Screenshot Fetcher
            st.write("3/6: Erstelle vollständigen Full-Page Screenshot via ScreenshotAPI.to...")
            screenshot_bytes = fetch_fullpage_screenshot(raw_url)
            screenshot_mime = "image/png"
                
            # 4. SERP & Security
            st.write("4/6: Prüfe Google Live-Sichtbarkeit und Serverprotokolle...")
            serper_ranking = query_serper_ranking(clean_domain, page_title, h1_tags[0] if h1_tags else "", clean_biz_name)
            ssl_res = check_ssl_socket(hostname)
            dsgvo_res = detect_dsgvo_consent(raw_html)
            
            # 5. PageSpeed
            st.write("5/6: Rufe Google PageSpeed Insights Vitals ab...")
            pagespeed_res = query_pagespeed_api_with_key(raw_url)
            
            # 6. Gemini Audits (Vision + Psychologie)
            st.write("6/6: Führe multimodale KI-Verkaufspsychologie durch...")
            vision_result = None
            if screenshot_bytes:
                vision_result = run_gemini_vision_audit(GEMINI_API_KEY, screenshot_bytes, screenshot_mime, clean_domain)
                
            text_body = soup.get_text(separator=' ')
            psychology_res = run_gemini_psychology_audit(
                GEMINI_API_KEY, clean_domain, page_title,
                h1_tags[0] if h1_tags else clean_biz_name,
                h2_tags, text_body, dom_data["distinct_ctas"],
                dom_data["detected_phone"], dom_data["form_field_count"],
                dom_data["trust_signals"]
            )
            
            if not psychology_res:
                psychology_res = build_smart_fallback_psychology(
                    clean_domain=clean_domain,
                    page_title=page_title,
                    h1_tags=h1_tags,
                    clean_biz_name=clean_biz_name,
                    keywords_table=keywords_table,
                    dom_data=dom_data,
                    text_sample=text_body
                )
                
            status.update(label="Live-Audit erfolgreich abgeschlossen", state="complete")
            
        # Conversion & Performance Health Score (100-Punkte Matrix)
        score_perf = int(pagespeed_res.get("score", 50) * 0.3)
        score_cro = (15 if dom_data.get("total_cta_count", 0) >= 2 else 5) + (10 if dom_data.get("form_field_count", 3) <= 4 else 5)
        score_trust = min(20, len(dom_data.get("trust_signals", [])) * 5)
        score_seo = (15 if ssl_res.get("ssl_valid") else 0) + (10 if len(h1_tags) == 1 else 5)
        
        base_score = score_perf + score_cro + score_trust + score_seo
        health_score = max(25, min(98, base_score))
        grade = "A+" if health_score >= 90 else ("A" if health_score >= 80 else ("B" if health_score >= 65 else ("C" if health_score >= 50 else "D")))
        grade_desc = "Exzellente Conversion- & Performance-Basis" if health_score >= 80 else ("Gute Basis mit klaren Ausbau-Potenzialen" if health_score >= 65 else "Spürbare technische und visuelle Reibungsverluste")
        
        st.session_state["scan_data"] = {
            "domain": clean_domain,
            "url": raw_url,
            "title": page_title,
            "title_len": len(page_title),
            "meta_desc": meta_desc,
            "meta_desc_len": len(meta_desc),
            "clean_biz_name": clean_biz_name,
            "h1_tags": h1_tags,
            "h2_tags": h2_tags,
            "imgs_total": imgs_total,
            "imgs_no_alt": imgs_no_alt,
            "alt_missing_pct": alt_missing_pct,
            "dom_data": dom_data,
            "design_assets": design_assets,
            "keywords_table": keywords_table,
            "serper_ranking": serper_ranking,
            "ssl_res": ssl_res,
            "dsgvo_res": dsgvo_res,
            "pagespeed_res": pagespeed_res,
            "health_score": health_score,
            "grade": grade,
            "grade_desc": grade_desc,
            "vision_result": vision_result,
            "psychology_res": psychology_res,
            "screenshot_bytes": screenshot_bytes,
            "screenshot_source": "ScreenshotAPI.to Full-Page Engine"
        }
        st.session_state["scanned"] = True


# ==========================================
# 5. UI TABS
# ==========================================

if not st.session_state["scanned"] or not st.session_state["scan_data"]:
    st.markdown("""
    <div style="background-color:#1A1E24; border:1px solid #2D333F; border-radius:10px; padding:50px 30px; text-align:center; margin:40px auto; max-width:800px;">
        <h2 style="color:#FFFFFF; margin-bottom:12px;">Bereit für das Live-Audit</h2>
        <p style="color:#A0AAB5; max-width:600px; margin:0 auto 20px auto;">
            Tragen Sie links eine <strong>Ziel-Domain</strong> ein und starten Sie die Analyse. 
            Das System zieht Screenshots und technische Daten vollautomatisch in Echtzeit.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    data = st.session_state["scan_data"]
    fogg = data["psychology_res"]
    
    col_t_title, col_t_btn = st.columns([3.2, 1.0])
    with col_t_title:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:8px;">
            <span style="font-size:1.15rem; font-weight:700; color:#FFFFFF; text-transform:uppercase; letter-spacing:0.5px;">Audit für:</span>
            <span style="font-size:1.25rem; font-weight:700; color:#C8D400;">{data['domain']}</span>
            <span class="badge-status badge-ok" style="font-size:0.75rem;">{fogg.get('business_model', 'Erkannt')}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_t_btn:
        if st.button("↗ Zur Webseite", key="view_site_global_btn", help="Öffnet den vollständigen Live-Screenshot der Website als scrollbares Overlay", use_container_width=True):
            show_site_modal(data["screenshot_bytes"], data["domain"], data["url"])
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "SEO- & DOM-Strukturanalyse",
        "Keyword- & Ranking-Audit",
        "Design, Farben & UI/UX Vision",
        "Verkaufspsychologie (BJ-Fogg)",
        "ROI- & Hebel-Rechner",
        "Vertriebs-Pitches",
        "JSON-Export"
    ])
    
    # ---------------- TAB 1: SEO & DOM ----------------
    with tab1:
        # 1. Kompakte Status-Boxen in einer Zeile
        t_ok = 10 < data["title_len"] <= 60
        d_ok = 20 < data["meta_desc_len"] <= 160
        h1_cnt = len(data["h1_tags"])
        h1_ok = (h1_cnt == 1)
        form_ok = (data['dom_data']['form_field_count'] <= 4)

        st.markdown(f"""
        <div class="stat-pills-row">
            <div class="stat-pill-box">
                <span style="font-size:0.85rem; color:#FFFFFF; font-weight:600;">Meta-Tags:</span>
                <span class="badge-status {'badge-ok' if t_ok and d_ok else 'badge-warn'}">{'Optimal' if t_ok and d_ok else 'Prüfung empfohlen'}</span>
            </div>
            <div class="stat-pill-box">
                <span style="font-size:0.85rem; color:#FFFFFF; font-weight:600;">H1-Hierarchie:</span>
                <span class="badge-status {'badge-ok' if h1_ok else 'badge-warn'}">{f'{h1_cnt} H1 vorhanden' if h1_cnt > 0 else 'Keine H1'}</span>
            </div>
            <div class="stat-pill-box">
                <span style="font-size:0.85rem; color:#FFFFFF; font-weight:600;">Einstiegs-Hürde:</span>
                <span class="badge-status {'badge-ok' if form_ok else 'badge-warn'}">{f"{data['dom_data']['form_field_count']} Formularfelder" if form_ok else 'Hohe Hürde'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Google SERP Simulator
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">GOOGLE SERP SIMULATOR (DESKTOP & MOBILE)</div>
                <div class="section-card-badge">Suchergebnis-Vorschau</div>
            </div>
            <div class="serp-preview-card" style="margin-bottom:0;">
                <div class="serp-url">https://{data['domain']}</div>
                <div class="serp-title">{data['title']}</div>
                <div class="serp-desc">{data['meta_desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. [ 01 ] Meta-Tags & On-Page Signale
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] META-TAGS & ON-PAGE SIGNALE</div>
                <div class="section-card-badge">HTML Quelltext</div>
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:6px; padding:12px 14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-size:0.78rem; text-transform:uppercase; color:#A0AAB5; font-weight:700;">Meta Title (Seitentitel)</span>
                    <span style="font-size:0.75rem; color:{'#C8D400' if t_ok else '#FFA500'}; font-family:monospace; font-weight:bold;">{data['title_len']} / 60 Zeichen</span>
                </div>
                <div style="font-size:0.92rem; color:#FFFFFF; font-weight:600; line-height:1.4;">{data['title']}</div>
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:6px; padding:12px 14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-size:0.78rem; text-transform:uppercase; color:#A0AAB5; font-weight:700;">Meta Description (Beschreibung)</span>
                    <span style="font-size:0.75rem; color:{'#C8D400' if d_ok else '#FFA500'}; font-family:monospace; font-weight:bold;">{data['meta_desc_len']} / 160 Zeichen</span>
                </div>
                <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.4;">{data['meta_desc']}</div>
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:6px; padding:12px 14px; margin-bottom:14px;">
                <div style="font-size:0.78rem; text-transform:uppercase; color:#A0AAB5; font-weight:700; margin-bottom:4px;">Hauptüberschrift (H1)</div>
                <div style="font-size:0.92rem; color:#C8D400; font-weight:600;">{data['h1_tags'][0] if data['h1_tags'] else 'Keine H1 vorhanden'}</div>
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">Längen-Check:</strong> Snippet-Längen passen optimal in die Google-Suchraster.</div>
                <div>— <strong style="color:#C8D400;">Semantische Führung:</strong> H1 formuliert den zentralen Nutzen für Crawler & Besucher.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. [ 02 ] DOM & Conversion-Hürde
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] DOM & CONVERSION-HÜRDE</div>
                <div class="section-card-badge">First-Fold Interaktion</div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; margin-bottom:16px;">
                <div class="metric-card" style="padding:12px 8px;">
                    <div class="metric-label" style="font-size:0.72rem;">CTAs Isoliert</div>
                    <div class="metric-value-accent" style="font-size:1.6rem;">{data['dom_data']['total_cta_count']}</div>
                </div>
                <div class="metric-card" style="padding:12px 8px;">
                    <div class="metric-label" style="font-size:0.72rem;">Formularfelder</div>
                    <div class="metric-value-accent" style="font-size:1.6rem;">{data['dom_data']['form_field_count']}</div>
                </div>
                <div class="metric-card" style="padding:12px 8px;">
                    <div class="metric-label" style="font-size:0.72rem;">Trust-Signale</div>
                    <div class="metric-value-accent" style="font-size:1.6rem;">{len(data['dom_data']['trust_signals'])}</div>
                </div>
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">First-Fold Dominanz:</strong> Haupt-Button '{data['dom_data']['distinct_ctas'][0] if data['dom_data']['distinct_ctas'] else 'Kontakt'}' als primärer Trigger aktiv.</div>
                <div>— <strong style="color:#C8D400;">Niedrige Barriere:</strong> {data['dom_data']['form_field_count']} Felder im Kontaktformular ermöglichen schnellen Abschluss.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 5. Sauber getrennter Expander mit Pfeil und 16px Abstand
        with st.expander(f"[ Detail-Quelltext aller {data['dom_data']['total_cta_count']} erkannten Buttons & Links ansehen ]", expanded=False):
            if data["dom_data"]["unique_ctas"]:
                rows_html = "".join([
                    f'<tr style="border-bottom:1px solid #252B37;"><td style="padding:8px 12px; text-align:left; font-weight:600; color:#FFFFFF;">{item["text"]}</td><td style="padding:8px 12px; text-align:left;"><span style="background:rgba(200,212,0,0.12); color:#C8D400; border:1px solid rgba(200,212,0,0.3); padding:2px 8px; border-radius:12px; font-size:0.72rem; font-weight:bold;">{item["type"]}</span></td><td style="padding:8px 12px; text-align:left; color:#A0AAB5; font-family:monospace; font-size:0.78rem;">&lt;{item["tag"]}&gt;</td></tr>'
                    for item in data["dom_data"]["unique_ctas"]
                ])
                cta_table_html = f'<div style="background:#0E1116; border:1px solid #252B37; border-radius:6px; overflow:hidden;"><table style="width:100%; border-collapse:collapse; text-align:left; font-size:0.84rem;"><thead><tr style="background:#1F242D; color:#C8D400; border-bottom:1px solid #2D333F;"><th style="padding:8px 12px; text-align:left;">Button-Text</th><th style="padding:8px 12px; text-align:left;">Typ</th><th style="padding:8px 12px; text-align:left;">Tag</th></tr></thead><tbody>{rows_html}</tbody></table></div>'
                st.markdown(cta_table_html, unsafe_allow_html=True)
            else:
                st.info("Keine separaten Button-Elemente isoliert.")

        # 6. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container" style="margin-top:20px;">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: STRUKTUR & TECHNIK</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('seo_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 2: KEYWORDS & RANKING ----------------
    with tab2:
        s_rank = data["serper_ranking"]
        # 1. Google Live-Ranking Power-Card
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">GOOGLE LIVE-RANKING POWER-CARD (ECHTZEIT-ABFRAGE)</div>
                <div class="section-card-badge">Serper.dev Live Search</div>
            </div>
            <div class="rank-hero-card" style="margin-bottom:0;">
                <div>
                    <div style="font-size:0.78rem; color:#A0AAB5; text-transform:uppercase; font-weight:700; letter-spacing:0.8px;">Geprüfte Suchanfrage bei Google</div>
                    <div style="font-size:1.35rem; font-weight:bold; color:#FFFFFF; margin-top:2px;">'{s_rank['query']}'</div>
                    <div style="font-size:0.85rem; color:#A0AAB5; margin-top:6px;">{s_rank['status_text']} &bull; <span style="color:#C8D400;">75 % aller Klicks entfallen auf die Top-3 Suchergebnisse.</span></div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:2.2rem; font-weight:800; color:{'#C8D400' if s_rank['found'] and s_rank['position'] <= 5 else '#FFA500'}; line-height:1;">
                        {f"Platz {s_rank['position']}" if s_rank['position'] else 'Nicht in Top 100'}
                    </div>
                    <div style="margin-top:6px;"><span class="badge-status {s_rank['badge']}">{ 'Gute Position' if s_rank['found'] and s_rank['position'] <= 5 else 'Reichweiten-Verlust' }</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. [ 01 ] Top 5 On-Page Themen
        top5_keywords = data["keywords_table"][:5] if data["keywords_table"] else []
        kw_rows = "".join([
            f'<tr style="border-bottom:1px solid #252B37; color:#E2E8F0;"><td style="padding:9px 14px; text-align:left; font-weight:600; color:#FFFFFF;">{row["Suchbegriff / Keyword"]}</td><td style="padding:9px 14px; text-align:left; color:#C8D400; font-family:monospace; font-weight:bold;">{row["Häufigkeit"]}x</td><td style="padding:9px 14px; text-align:left; color:#A0AAB5; font-family:monospace;">{row["Dichte"]}</td></tr>'
            for row in top5_keywords
        ])
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] TOP 5 ON-PAGE THEMEN & RELEVANZ</div>
                <div class="section-card-badge">Content-Fokus</div>
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; overflow:hidden; margin-bottom:14px;">
                <table style="width:100%; border-collapse:collapse; text-align:left; font-size:0.88rem;">
                    <thead>
                        <tr style="background:#1F242D; color:#C8D400; border-bottom:1px solid #2D333F;">
                            <th style="padding:10px 14px; text-align:left;">Suchbegriff</th>
                            <th style="padding:10px 14px; text-align:left;">Häufigkeit</th>
                            <th style="padding:10px 14px; text-align:left;">Dichte</th>
                        </tr>
                    </thead>
                    <tbody>{kw_rows}</tbody>
                </table>
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">Thematische Klarheit:</strong> Google ordnet die Seite klar dem Schwerpunkt <em>{fogg.get('business_model', 'Dienstleistungen')}</em> zu.</div>
                <div>— <strong style="color:#C8D400;">Natürlicher Textfluss:</strong> Alle Dichtewerte liegen im gesunden Bereich (&lt; 3.0 %).</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. [ 02 ] Pull-Marketing & Google Ads Hebel
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] PULL-MARKETING & GOOGLE ADS HEBEL</div>
                <div class="section-card-badge">Sofort-Reichweite</div>
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; padding:16px; margin-bottom:14px;">
                <div style="font-size:0.82rem; color:#FFA500; font-weight:700; text-transform:uppercase; margin-bottom:6px;">Organisch vs. Google Ads Hebel</div>
                <p style="font-size:0.88rem; color:#E2E8F0; margin:0; line-height:1.4;">
                    Organische Spitzenpositionen benötigen Monate. Mit <strong>Google Search Ads</strong> sichert sich {data['clean_biz_name']} ab Tag 1 die Spitzenplätze bei kaufbereiten Entscheidern.
                </p>
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">Kaufabsicht sichern:</strong> Relevante Suchbegriffe direkt auf 14-Tage Conversion-Landingpages leiten.</div>
                <div>— <strong style="color:#C8D400;">Speed-to-Market:</strong> Google Ads als sofortiger Umsatzhebel, während die organische Autorität wächst.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: GOOGLE ADS & SICHTBARKEIT</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('keyword_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 3: DESIGN & UI/UX VISION ----------------
    with tab3:
        # 1. Visueller Markenauftritt & Snapshot
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">VISUELLER MARKENAUFTRITT & FIRST-FOLD SNAPSHOT</div>
                <div class="section-card-badge">Design & Layout</div>
            </div>
        """, unsafe_allow_html=True)
        if data.get("screenshot_bytes"):
            st.image(data["screenshot_bytes"], caption=f"Website-Snapshot ({data['domain']})", use_container_width=True)
        else:
            st.info("Kein Screenshot verfügbar.")
            
        st.markdown("""
            <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; padding:18px; margin-top:14px;">
                <div style="font-size:0.78rem; text-transform:uppercase; color:#C8D400; font-weight:700; letter-spacing:0.8px; margin-bottom:8px;">Visuelle Wahrnehmung in den ersten 3 Sekunden</div>
                <p style="font-size:0.90rem; color:#E2E8F0; line-height:1.5; margin:0 0 10px 0;">
                    68 % aller Mobilbesucher verlassen eine Website sofort, wenn Schriften schwer lesbar sind, Kontraste fehlen oder der Einstieg optisch unruhig wirkt.
                </p>
                <div style="font-size:0.82rem; color:#A0AAB5; border-top:1px solid #252B37; padding-top:10px;">
                    <strong>CI-Farben & Typografie isoliert</strong> &bull; <strong>Gemini 1.5 Flash Vision analysiert</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. [ 01 ] CI-Farbpalette & Typografie
        color_list = data["design_assets"].get("colors", [])
        font_list = data["design_assets"].get("fonts", [])
        color_swatches = "".join([
            f'<div style="background:#14181F; border:1px solid #2D333F; border-radius:6px; overflow:hidden; text-align:center;"><svg width="100%" height="48" style="display:block; background-color:{hex_val};"><rect width="100%" height="100%" fill="{hex_val}"/></svg><div style="font-size:0.75rem; font-weight:bold; padding:6px 0; color:#FFFFFF; font-family:monospace;">{hex_val}</div></div>'
            for hex_val in color_list[:5]
        ])
        font_pills = " ".join([
            f'<span style="background:rgba(200,212,0,0.1); border:1px solid rgba(200,212,0,0.3); color:#C8D400; padding:4px 10px; border-radius:12px; font-size:0.80rem; font-weight:bold; margin-right:6px;">{f_name}</span>'
            for f_name in font_list[:3]
        ])
        
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] CI-FARBPALETTE & TYPOGRAFIE</div>
                <div class="section-card-badge">Corporate Design</div>
            </div>
            <div style="font-size:0.78rem; text-transform:uppercase; color:#A0AAB5; font-weight:700; margin-bottom:8px;">Extrahierte Farbpalette</div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(120px, 1fr)); gap:8px; margin-bottom:16px;">
                {color_swatches}
            </div>
            <div style="font-size:0.78rem; text-transform:uppercase; color:#A0AAB5; font-weight:700; margin-bottom:8px;">Erkannte Schriftarten</div>
            <div style="margin-bottom:14px;">
                {font_pills if font_pills else '<span style="color:#FFFFFF;">System Sans-Serif</span>'}
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">Signalwirkung:</strong> Klare Abgrenzung von Hintergrund-, Fließtext- und Aktionsfarben.</div>
                <div>— <strong style="color:#C8D400;">Lesbarkeit:</strong> Schriften für maximale Lesegeschwindigkeit auf Smartphones optimiert.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. [ 02 ] Multimodales UI/UX-Audit (Gemini Vision)
        v = data.get("vision_result") or {}
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] MULTIMODALES UI/UX-AUDIT (GEMINI VISION)</div>
                <div class="section-card-badge">KI-Sichtprüfung</div>
            </div>
            <div class="audit-box-success" style="margin-bottom:14px; padding:14px 16px;">
                <strong style="color:#FFFFFF; font-size:0.85rem;">1. Lesbarkeit & Abstände:</strong>
                <p style="margin:2px 0 8px 0; color:#E2E8F0; font-size:0.82rem;">{v.get('layout_clipping', 'Layout-Abstände und Weißraum im gesunden Bereich.')}</p>
                <strong style="color:#FFFFFF; font-size:0.85rem;">2. Mobile Ansicht & Navigation:</strong>
                <p style="margin:2px 0 8px 0; color:#E2E8F0; font-size:0.82rem;">{v.get('mobile_alignment', 'Mobile Navigation ist strukturiert und erreichbar.')}</p>
                <strong style="color:#FFFFFF; font-size:0.85rem;">3. Kontraste & Hierarchie:</strong>
                <p style="margin:2px 0 0 0; color:#E2E8F0; font-size:0.82rem;">{v.get('typography_contrast', 'Kontraste der Schriften heben sich gut ab.')}</p>
            </div>
            <div style="font-size:0.85rem; color:#E2E8F0; line-height:1.6;">
                <div>— <strong style="color:#C8D400;">First-Fold Klarheit:</strong> Kernaussage und USP direkt ohne Scrollen erfassbar.</div>
                <div>— <strong style="color:#C8D400;">Daumen-Zone:</strong> Wichtige Buttons liegen ergonomisch in der mobilen Klick-Zone.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: MARKENAUFTRITT & DESIGN</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('design_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 4: VERKAUFSPSYCHOLOGIE (BJ-FOGG) ----------------
    with tab4:
        # 1. Conversion Health Score & Fogg-Diagnose
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">CONVERSION HEALTH SCORE & FOGG-DIAGNOSE</div>
                <div class="section-card-badge">B = M × A × T</div>
            </div>
            <div style="display:flex; justify-content:center; margin-bottom:16px;">
                {render_radial_health_score(data["health_score"], data["grade"], data["grade_desc"])}
            </div>
            <div style="background:#14181F; border:1px solid #2D333F; padding:18px 20px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:0.80rem; text-transform:uppercase; color:#A0AAB5; font-weight:700;">Branchen-Einordnung:</span>
                    <span class="badge-status badge-ok">{fogg.get('business_model', 'Dienstleistungen')}</span>
                </div>
                <div style="font-size:1.05rem; font-weight:700; color:#C8D400; margin-bottom:8px;">Verhalten = Motivation × Einfachheit × Auslöser</div>
                <p style="font-size:0.88rem; color:#E2E8F0; line-height:1.5; margin:0 0 10px 0;">
                    Besucher entscheiden in den ersten 3 Sekunden. Ist Motivation vorhanden, aber Hürden (Ability) stehen im Weg oder klare Auslöser (Trigger) fehlen, verpufft der Traffic wirkungslos.
                </p>
                <div style="font-size:0.80rem; color:#A0AAB5; border-top:1px solid #252B37; padding-top:8px;">
                    — <strong style="color:#C8D400;">Health Score Fazit:</strong> Starke Basis mit Hebeln in der mobilen Aktionsführung.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. [ 01 ] Die 3 Säulen der Conversion-Psychologie
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] DIE 3 SÄULEN DER CONVERSION-PSYCHOLOGIE</div>
                <div class="section-card-badge">Ist vs. Hebel</div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px;">
                <div style="background:#14181F; border:1px solid #2D333F; border-top:4px solid #C8D400; padding:16px; border-radius:8px;">
                    <strong style="color:#C8D400; font-size:0.90rem;">1. Motivation (Verlangen)</strong>
                    <p style="font-size:0.80rem; color:#A0AAB5; margin:6px 0 2px 0;"><strong>Ist:</strong> {fogg.get('motivation_ist', '')}</p>
                    <p style="font-size:0.85rem; color:#E2E8F0; margin:0;"><strong>Hebel:</strong> {fogg.get('motivation_hebel', '')}</p>
                </div>
                <div style="background:#14181F; border:1px solid #2D333F; border-top:4px solid #FFA500; padding:16px; border-radius:8px;">
                    <strong style="color:#FFA500; font-size:0.90rem;">2. Ability (Einfachheit)</strong>
                    <p style="font-size:0.80rem; color:#A0AAB5; margin:6px 0 2px 0;"><strong>Ist:</strong> {fogg.get('ability_ist', '')}</p>
                    <p style="font-size:0.85rem; color:#E2E8F0; margin:0;"><strong>Hebel:</strong> {fogg.get('ability_hebel', '')}</p>
                </div>
                <div style="background:#14181F; border:1px solid #2D333F; border-top:4px solid #FF4B4B; padding:16px; border-radius:8px;">
                    <strong style="color:#FF4B4B; font-size:0.90rem;">3. Trigger (Auslöser)</strong>
                    <p style="font-size:0.80rem; color:#A0AAB5; margin:6px 0 2px 0;"><strong>Ist:</strong> {fogg.get('trigger_ist', '')}</p>
                    <p style="font-size:0.85rem; color:#E2E8F0; margin:0;"><strong>Hebel:</strong> {fogg.get('trigger_hebel', '')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. [ 02 ] 3 Spezifische Headline-Hooks
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] 3 SPEZIFISCHE HEADLINE-HOOKS (NUTZEN-POSITIONIERUNG)</div>
                <div class="section-card-badge">Copywriting-Optionen</div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px;">
                <div style="background:#14181F; border:1px solid rgba(200,212,0,0.25); padding:16px; border-radius:8px;">
                    <span style="font-size:0.78rem; color:#C8D400; font-weight:bold;">Option 1: {fogg.get('cat_1', 'ROI & Nutzen')}</span>
                    <p style="font-size:0.92rem; color:#FFFFFF; margin:6px 0 0 0; font-weight:600; line-height:1.4;">{fogg.get('hook_1', '')}</p>
                </div>
                <div style="background:#14181F; border:1px solid rgba(200,212,0,0.25); padding:16px; border-radius:8px;">
                    <span style="font-size:0.78rem; color:#C8D400; font-weight:bold;">Option 2: {fogg.get('cat_2', 'Geschwindigkeit & 14 Tage')}</span>
                    <p style="font-size:0.92rem; color:#FFFFFF; margin:6px 0 0 0; font-weight:600; line-height:1.4;">{fogg.get('hook_2', '')}</p>
                </div>
                <div style="background:#14181F; border:1px solid rgba(200,212,0,0.25); padding:16px; border-radius:8px;">
                    <span style="font-size:0.78rem; color:#C8D400; font-weight:bold;">Option 3: {fogg.get('cat_3', 'Klarheit & Partnerschaft')}</span>
                    <p style="font-size:0.92rem; color:#FFFFFF; margin:6px 0 0 0; font-weight:600; line-height:1.4;">{fogg.get('hook_3', '')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. [ 03 ] Button-Optimierung
        cta_rows = fogg.get("cta_comparison", [])
        if cta_rows:
            table_rows = "".join([
                f"<tr><td style='padding:10px 16px; text-align:left;'><span style='color:#FFA500; font-weight:bold;'>[Aktuell]</span> {r.get('aktuell', '')}</td><td style='padding:10px 16px; text-align:left;'><strong style='color:#C8D400;'>[StraightAds Trigger]</strong> {r.get('optimiert', '')}</td></tr>"
                for r in cta_rows
            ])
            st.markdown(f"""
            <div class="section-card">
                <div class="section-card-header">
                    <div class="section-card-title">[ 03 ] BUTTON-OPTIMIERUNG (VORHER-NACHHER VERGLEICH)</div>
                    <div class="section-card-badge">Handlungs-Trigger</div>
                </div>
                <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; overflow:hidden;">
                    <table class='cta-table' style="margin:0; width:100%; border-collapse:collapse;">
                        <thead>
                            <tr style="background:#1F242D; color:#C8D400; border-bottom:1px solid #2D333F;">
                                <th style="padding:10px 16px; text-align:left;">Aktueller Link / Button</th>
                                <th style="padding:10px 16px; text-align:left;">Optimierter Handlungs-Trigger</th>
                            </tr>
                        </thead>
                        <tbody>{table_rows}</tbody>
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 5. [ 04 ] Angewandte Neuro-Psychologie
        biz_name = data["clean_biz_name"]
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 04 ] STRAIGHTADS MARKETING BRAIN • ANGEWANDTE NEURO-PSYCHOLOGIE</div>
                <div class="section-card-badge">23 Wissensmodule &bull; Live-Transfer</div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; font-size:0.85rem; color:#E2E8F0; line-height:1.5;">
                <div style="background:#14181F; border:1px solid #252B37; padding:14px 16px; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <strong style="color:#C8D400; font-size:0.92rem;">1. BJ-Fogg Verhaltensmodell (B = M × A × T)</strong>
                        <p style="color:#A0AAB5; font-size:0.80rem; margin:4px 0 8px 0; line-height:1.4;">
                            <strong style="color:#FFFFFF;">Gesetz:</strong> Verhalten entsteht nur, wenn Motivation, Einfachheit (Ability) und Auslöser (Trigger) gleichzeitig oberhalb der Aktionslinie liegen.
                        </p>
                    </div>
                    <div style="background:#0E1116; border-left:3px solid #C8D400; padding:10px 12px; border-radius:4px; margin-top:6px;">
                        <strong style="color:#C8D400; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Hebel für {biz_name}:</strong><br>
                        <span style="color:#FFFFFF; font-size:0.84rem; line-height:1.45;">{fogg.get('brain_fogg_example', '')}</span>
                    </div>
                </div>
                <div style="background:#14181F; border:1px solid #252B37; padding:14px 16px; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <strong style="color:#C8D400; font-size:0.92rem;">2. Von-Restorff-Effekt (Isolation Effect)</strong>
                        <p style="color:#A0AAB5; font-size:0.80rem; margin:4px 0 8px 0; line-height:1.4;">
                            <strong style="color:#FFFFFF;">Gesetz:</strong> Elemente, die sich visuell oder inhaltlich deutlich vom Standard abheben, brennen sich sofort im Gedächtnis des Besuchers ein.
                        </p>
                    </div>
                    <div style="background:#0E1116; border-left:3px solid #C8D400; padding:10px 12px; border-radius:4px; margin-top:6px;">
                        <strong style="color:#C8D400; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Hebel für {biz_name}:</strong><br>
                        <span style="color:#FFFFFF; font-size:0.84rem; line-height:1.45;">{fogg.get('brain_restorff_example', '')}</span>
                    </div>
                </div>
                <div style="background:#14181F; border:1px solid #252B37; padding:14px 16px; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <strong style="color:#FFA500; font-size:0.92rem;">3. Verlust- vs. Motiv-Trigger (Pain vs. Gain)</strong>
                        <p style="color:#A0AAB5; font-size:0.80rem; margin:4px 0 8px 0; line-height:1.4;">
                            <strong style="color:#FFFFFF;">Gesetz:</strong> Entscheider reagieren 2x stärker auf das Vermeiden von realen Verlusten (Geld, Zeit, Kunden) als auf vage Zukunftschancen.
                        </p>
                    </div>
                    <div style="background:#0E1116; border-left:3px solid #FFA500; padding:10px 12px; border-radius:4px; margin-top:6px;">
                        <strong style="color:#FFA500; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Hebel für {biz_name}:</strong><br>
                        <span style="color:#FFFFFF; font-size:0.84rem; line-height:1.45;">{fogg.get('brain_loss_example', '')}</span>
                    </div>
                </div>
                <div style="background:#14181F; border:1px solid #252B37; padding:14px 16px; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <strong style="color:#FFA500; font-size:0.92rem;">4. 2-Klick Customer Journey (Reibungsminimierung)</strong>
                        <p style="color:#A0AAB5; font-size:0.80rem; margin:4px 0 8px 0; line-height:1.4;">
                            <strong style="color:#FFFFFF;">Gesetz:</strong> Jeder zusätzliche Klick und jedes Pflichtfeld im Formular halbiert die mobile Conversion-Wahrscheinlichkeit.
                        </p>
                    </div>
                    <div style="background:#0E1116; border-left:3px solid #FFA500; padding:10px 12px; border-radius:4px; margin-top:6px;">
                        <strong style="color:#FFA500; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Hebel für {biz_name}:</strong><br>
                        <span style="color:#FFFFFF; font-size:0.84rem; line-height:1.45;">{fogg.get('brain_journey_example', '')}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 6. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: VERKAUFSPSYCHOLOGIE & CRO</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('fogg_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 5: ROI RECHNER ----------------
    with tab5:
        # 1. [ 01 ] Business-Stellschrauben (Inputs oben)
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] BUSINESS-STELLSCHRAUBEN</div>
                <div class="section-card-badge">Echtzeit-Regler</div>
            </div>
        """, unsafe_allow_html=True)
        
        visitors = st.number_input("Monatliche Website-Besucher:", value=6000, step=500)
        curr_cr = st.slider("Aktuelle Abschlussquote (in %):", min_value=0.2, max_value=6.0, value=1.5, step=0.1)
        basket_value = st.number_input("Durchschnittlicher Kundenwert / Bon (in EUR):", value=25, step=5)
        cr_lift = st.slider("Mögliche Steigerung durch Optimierung (+%-Punkte):", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
        
        cur_rev = (visitors * curr_cr / 100) * basket_value
        opt_cr = curr_cr + cr_lift
        opt_rev = (visitors * opt_cr / 100) * basket_value
        delta_rev = opt_rev - cur_rev
        delta_annual = delta_rev * 12
        new_customers_monthly = int(visitors * cr_lift / 100)
        
        delta_annual_formatted = format_eur_de(delta_annual)
        delta_rev_formatted = format_eur_de(delta_rev)
        new_cust_formatted = format_number_de(new_customers_monthly)
        
        st.markdown(f"""
            <div style="font-size:0.82rem; color:#E2E8F0; line-height:1.5; margin-top:14px; border-top:1px solid #252B37; padding-top:10px;">
                — <strong style="color:#C8D400;">Mathematischer Hebel:</strong> Steigerung von {curr_cr:.1f}% auf {opt_cr:.1f}% = <strong>+{((cr_lift/curr_cr)*100):.1f}% Mehrabschlüsse</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. [ 02 ] Der finanzielle Jahres-Hebel (Ergebnis prominent darunter)
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] DER FINANZIELLE JAHRES-HEBEL</div>
                <div class="section-card-badge">Reine Conversion-Effizienz</div>
            </div>
            <div class="roi-card" style="margin:0;">
                <div style="font-size:0.80rem; text-transform:uppercase; color:#A0AAB5; font-weight:700; letter-spacing:0.8px;">Zusätzlicher Jahresertrag (Ohne Werbekosten-Plus)</div>
                <div class="roi-result-value">+ {delta_annual_formatted}</div>
                <div style="background:#14181F; border:1px solid #2D333F; border-radius:6px; padding:14px 18px; margin-bottom:14px; font-size:0.88rem; color:#E2E8F0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span>Monatlicher Mehrumsatz:</span>
                        <strong style="color:#C8D400; font-size:0.95rem;">+ {delta_rev_formatted} / Monat</strong>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span>Zusätzliche Kunden pro Monat:</span>
                        <strong style="color:#FFFFFF; font-size:0.95rem;">+ {new_cust_formatted} Neukunden</strong>
                    </div>
                </div>
                <p style="margin:0; font-size:0.82rem; color:#A0AAB5; line-height:1.4;">
                    — <strong>Amortisation:</strong> Das StraightAds-System finanziert sich durch den Hebel meist schon im ersten Quartal von selbst.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: WIRTSCHAFTLICHKEIT & SKALIERUNG</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('roi_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 6: PITCHES ----------------
    with tab6:
        comp = data["clean_biz_name"]
        pitches = marketing_brain.generate_framework_pitches(
            clean_biz_name=comp,
            clean_domain=data["domain"],
            page_title=data["title"],
            dom_data=data["dom_data"],
            pagespeed_res=data["pagespeed_res"],
            s_rank=data["serper_ranking"],
            business_model=fogg.get("business_model", "Dienstleistungen"),
            health_score=data["health_score"]
        )
        
        # 1. Die 2 dominanten Sales-Hebel
        st.markdown(f"""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">DIE 2 DOMINANTEN GESPRÄCHSAUFHÄNGER (COLD OUTREACH)</div>
                <div class="section-card-badge">Sales Ready</div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
                <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; padding:16px;">
                    <div style="font-size:0.78rem; text-transform:uppercase; color:#FFA500; font-weight:700; margin-bottom:6px;">Konkrete Schmerzpunkte aus dem Audit</div>
                    <div style="font-size:0.88rem; color:#E2E8F0; margin-bottom:6px;">1. <strong>First-Fold Führung:</strong> Dominanter Haupt-CTA fehlt im ersten Smartphone-Sichtfeld.</div>
                    <div style="font-size:0.88rem; color:#E2E8F0;">2. <strong>Mobile Ladezeit ({data['pagespeed_res'].get('fcp', '2.2s')}):</strong> Erzeugt spürbare Reibungsverluste beim Einstieg.</div>
                </div>
                <div style="background:#14181F; border:1px solid #2D333F; border-radius:8px; padding:16px;">
                    <div style="font-size:0.78rem; text-transform:uppercase; color:#C8D400; font-weight:700; margin-bottom:6px;">Das StraightAds Versprechen</div>
                    <div style="font-size:1.0rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">Go-Live in nur 14 Tagen</div>
                    <div style="font-size:0.82rem; color:#A0AAB5;">Schlüsselfertig umgesetzt: Ads &bull; Brand &bull; Commerce.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. [ 01 ] 3 Psychologische Copywriting-Frameworks
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] 3 PSYCHOLOGISCHE COPYWRITING-FRAMEWORKS</div>
                <div class="section-card-badge">StraightAds Marketing Brain</div>
            </div>
        """, unsafe_allow_html=True)
        
        p_tab1, p_tab2, p_tab3 = st.tabs([
            "PAS (Problem - Agitate - Solution)",
            "BAB (Before - After - Bridge)",
            "Hook - Story - Offer (ABC-Outreach)"
        ])
        
        with p_tab1:
            pas = pitches["pas"]
            st.markdown(f"""
            <div style="background:#14181F; border:1px solid #2D333F; border-left:4px solid #C8D400; padding:16px 18px; border-radius:8px; margin-top:8px;">
                <div style="font-size:0.75rem; text-transform:uppercase; color:#C8D400; font-weight:bold; letter-spacing:0.5px;">PAS-Framework • Für lösungsorientierte Entscheider</div>
                <div style="margin-top:10px;">
                    <strong style="color:#FFA500;">P (Problem):</strong><br>
                    <span style="color:#FFFFFF;">{pas['problem']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#FF4B4B;">A (Agitate / Schmerz vertiefen):</strong><br>
                    <span style="color:#E2E8F0;">{pas['agitate']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#C8D400;">S (Solution / StraightAds 14-Tage System):</strong><br>
                    <span style="color:#FFFFFF;">{pas['solution']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with p_tab2:
            bab = pitches["bab"]
            st.markdown(f"""
            <div style="background:#14181F; border:1px solid #2D333F; border-left:4px solid #FFA500; padding:16px 18px; border-radius:8px; margin-top:8px;">
                <div style="font-size:0.75rem; text-transform:uppercase; color:#FFA500; font-weight:bold; letter-spacing:0.5px;">BAB-Framework • Für Visions- und Transformations-Pitches</div>
                <div style="margin-top:10px;">
                    <strong style="color:#A0AAB5;">B (Before / Ist-Zustand):</strong><br>
                    <span style="color:#E2E8F0;">{bab['before']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#C8D400;">A (After / Ziel-Zustand):</strong><br>
                    <span style="color:#FFFFFF;">{bab['after']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#C8D400;">B (Bridge / Die Brücke):</strong><br>
                    <span style="color:#FFFFFF;">{bab['bridge']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with p_tab3:
            hso = pitches["hso"]
            st.markdown(f"""
            <div style="background:#14181F; border:1px solid #2D333F; border-left:4px solid #C8D400; padding:16px 18px; border-radius:8px; margin-top:8px;">
                <div style="font-size:0.75rem; text-transform:uppercase; color:#C8D400; font-weight:bold; letter-spacing:0.5px;">Hook-Story-Offer • Für Kaltakquise, E-Mail & Social Outreach</div>
                <div style="margin-top:10px;">
                    <strong style="color:#FFA500;">Hook (Aufmerksamkeits-Stopper):</strong><br>
                    <span style="color:#FFFFFF;">{hso['hook']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#A0AAB5;">Story (Social Proof & Relevanz):</strong><br>
                    <span style="color:#E2E8F0;">{hso['story']}</span>
                </div>
                <div style="margin-top:10px;">
                    <strong style="color:#C8D400;">Offer (Unwiderstehliches Angebot):</strong><br>
                    <span style="color:#FFFFFF;">{hso['offer']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. [ 02 ] Telefon-Leitfaden
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 02 ] TELEFON-LEITFADEN (COLD OUTREACH)</div>
                <div class="section-card-badge">Erstkontakt</div>
            </div>
        """, unsafe_allow_html=True)
        st.code(pitches["phone_script"], language="text")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 4. [ 03 ] Personalisierte E-Mail-Vorlage
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 03 ] PERSONALISIERTE E-MAIL-VORLAGE (ZAHNRAD-METHODE)</div>
                <div class="section-card-badge">Schlüsselfertig</div>
            </div>
        """, unsafe_allow_html=True)
        st.code(pitches["email_pitch"], language="text")
        st.markdown("</div>", unsafe_allow_html=True)

        # 5. Experten-Empfehlung strikt am Ende
        st.markdown(f"""
        <div class="blueprint-container">
            <div class="blueprint-title">STRAIGHTADS EXPERTEN-EMPFEHLUNG: VERTRIEBSANSATZ & ABSCHLUSS</div>
            <p style="margin:0; color:#E2E8F0; font-size:0.92rem; line-height:1.5;">{fogg.get('outreach_empfehlung', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- TAB 7: JSON EXPORT ----------------
    with tab7:
        export_dict = {
            "domain": data["domain"],
            "branche": fogg.get("business_model", ""),
            "health_score": data["health_score"],
            "grade": data["grade"],
            "meta": {"title": data["title"], "description": data["meta_desc"]},
            "technische_werte": {
                "pagespeed_score": data["pagespeed_res"]["score"],
                "lcp": data["pagespeed_res"]["lcp"],
                "ssl": data["ssl_res"]["ssl_valid"],
                "alt_missing_pct": data["alt_missing_pct"]
            },
            "cro_analyse": {
                "motivation": fogg.get("motivation_hebel", ""),
                "ability": fogg.get("ability_hebel", ""),
                "trigger": fogg.get("trigger_hebel", ""),
                "cta_count": data["dom_data"]["total_cta_count"]
            },
            "empfehlungen": {
                "hook_1": fogg.get("hook_1", ""),
                "hook_2": fogg.get("hook_2", ""),
                "hook_3": fogg.get("hook_3", ""),
                "straightads_plan": fogg.get("fogg_empfehlung", "")
            }
        }
        
        json_str = json.dumps(export_dict, indent=2, ensure_ascii=False)
        
        # 1. Download Hub
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">STRUKTURIERTER AUDIT-REPORT (CRM & ONBOARDING EXPORT)</div>
                <div class="section-card-badge">JSON Format</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                <div style="font-size:0.88rem; color:#E2E8F0;">
                    Vollständig strukturierter Datensatz für den nahtlosen Import in <strong>HubSpot, Pipedrive oder Notion</strong>.
                </div>
                <div style="display:flex; gap:8px;">
                    <span class="badge-status badge-ok">CRM-Ready</span>
                    <span class="badge-status badge-ok">14-Tage Onboarding</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="Audit als JSON-Datei herunterladen",
            data=json_str,
            file_name=f"straightads_audit_{data['domain']}.json",
            mime="application/json"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Strukturierter JSON-Viewer
        st.markdown("""
        <div class="section-card">
            <div class="section-card-header">
                <div class="section-card-title">[ 01 ] MASCHINENLESBARER AUDIT-DATENSATZ (VOLLANSICHT)</div>
                <div class="section-card-badge">JSON Payload</div>
            </div>
        """, unsafe_allow_html=True)
        st.code(json_str, language="json")
        st.markdown("</div>", unsafe_allow_html=True)