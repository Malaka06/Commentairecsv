import streamlit as st
from ui.components import card, end_card


def page_use_cases():
    st.markdown(
        """
        <div style="max-width:900px; margin-bottom:10px;">
          <div style="font-size:22px; font-weight:950; letter-spacing:-0.02em;">
            Cas d’usage
          </div>
          <div style="color:#64748B; font-size:14.5px; margin-top:6px;">
            Là où INSIGHTIA aide à réduire l’ambiguïté et accélérer la décision.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        card("Produit / UX", "Roadmap & irritants")
        st.markdown("""
- Repérer les **irritants dominants** et leurs exemples  
- Prioriser correctifs (P0/P1/P2) avec signaux d’urgence  
- Mesurer l’effet d’une release via Avant/Après (option)  
        """)
        end_card()

    with c2:
        card("Support / Ops", "Réduction des contacts")
        st.markdown("""
- Identifier les sujets récurrents par canal  
- Alimenter FAQ / base de connaissance  
- Accélérer le tri par catégorie/sévérité  
        """)
        end_card()

    card("Direction / Pilotage", "Synthèse actionnable")
    st.markdown("""
- Visualiser volume, thèmes, priorités  
- Exporter une synthèse pour comité (CSV/PDF/PPTX)  
- Suivre l’évolution des irritants dans le temps  
    """)
    end_card()
