import streamlit as st


def inject_css():
    st.markdown(
        """
    <style>
      :root{
        --bg:#F6F8FC;
        --card:#FFFFFF;
        --stroke:#E6EAF2;
        --text:#0F172A;
        --muted:#64748B;

        --brand1:#1D4ED8;
        --brand2:#0F2E6B;

        --shadow:0 14px 35px rgba(15,23,42,0.10);
        --shadowSoft:0 10px 18px rgba(15,23,42,0.06);

        --rLG:22px;
        --rMD:14px;
      }

      /* Layout général */
      .stApp{ background: var(--bg); }
      div.block-container{
        max-width: 1180px;
        padding-top: 1.0rem;
        padding-bottom: 2.2rem;
      }
      header[data-testid="stHeader"]{ background: transparent; }

      /* Brand / Logo */
      .brand-link{
        display:inline-block;
        margin: 4px 0 10px 2px;
        text-decoration:none;
      }
      .brand-logo{
        height: 52px;
        width: auto;
        border-radius: 12px;
      }
      .brand-fallback{
        display:inline-block;
        margin: 10px 0 8px 2px;
        font-weight: 950;
        font-size: 20px;
        color: var(--text);
        text-decoration:none;
        letter-spacing: -0.02em;
      }

      /* Hero */
      .hero{
        background: linear-gradient(90deg, var(--brand1), var(--brand2));
        border-radius: 28px;
        padding: 22px 22px;
        color:#fff;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: var(--shadow);
        margin-bottom: 12px;
      }
      .hero-badge{
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.22);
        font-weight: 900;
        font-size: 12px;
      }
      .hero-title{
        margin-top: 10px;
        font-size: 44px;
        font-weight: 950;
        letter-spacing: -0.03em;
        line-height: 1.05;
      }
      .hero-sub{
        margin-top: 8px;
        font-size: 15px;
        opacity: 0.95;
        max-width: 900px;
      }

      /* Stepper */
      .stepper{
        display:flex; gap:10px; flex-wrap:wrap;
        margin-top: 10px;
      }
      .step{
        display:inline-flex;
        align-items:center;
        gap:10px;
        padding:10px 12px;
        border-radius: 16px;
        border:1px solid rgba(255,255,255,0.18);
        background: rgba(255,255,255,0.10);
        font-weight: 900;
        font-size: 13px;
        color:#fff;
        opacity: 0.92;
      }
      .step.active{
        background: rgba(255,255,255,0.22);
        border:1px solid rgba(255,255,255,0.30);
        opacity: 1;
      }
      .step small{
        font-weight:700;
        color: rgba(255,255,255,0.85);
      }

      /* Cards */
      .card{
        background: var(--card);
        border: 1px solid var(--stroke);
        border-radius: var(--rLG);
        padding: 16px 18px;
        box-shadow: var(--shadowSoft);
        margin-bottom: 14px;
      }
      .card-title{
        font-size: 18px;
        font-weight: 950;
        letter-spacing: -0.02em;
        color: var(--text);
        margin-bottom: 6px;
      }
      .muted{ color: var(--muted); }

      /* DataFrame */
      div[data-testid="stDataFrame"]{
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid var(--stroke);
      }

      /* =========================
         NAVIGATION (BOUTONS)
         IMPORTANT : ce CSS cible les boutons Streamlit
         utilisés pour la nav dans layout.py
         ========================= */

      /* On rend les boutons "nav" propres et full width dans chaque colonne */
      .stButton > button {
        width: 100% !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        padding: 10px 12px !important;
        background: #FFFFFF !important;
        border: 1px solid var(--stroke) !important;
        color: var(--text) !important;
        box-shadow: 0 6px 12px rgba(15,23,42,0.06) !important;
      }
      .stButton > button:hover{
        background:#EEF2FF !important;
        border-color:#C7D2FE !important;
        color:#1D4ED8 !important;
      }

      /* Bouton actif = disabled, mais on le garde "sélectionné" */
      .stButton > button:disabled{
        background:#EEF2FF !important;
        border-color:#C7D2FE !important;
        color:#1D4ED8 !important;
        opacity: 1 !important;
        cursor: default !important;
      }

      /* Bonus : arrondis / style global des boutons */
      button{
        border-radius: 12px;
      }
    </style>
    """,
        unsafe_allow_html=True,
    )
