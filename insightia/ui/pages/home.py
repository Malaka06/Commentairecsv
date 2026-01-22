import streamlit as st
from ui.components import card, end_card


def page_home():
    st.markdown(
        """
        <div style="max-width:840px; margin-bottom:10px;">
          <div style="font-size:28px; font-weight:950; letter-spacing:-0.03em; line-height:1.1;">
            Donner du sens à la voix du client.
          </div>
          <div style="color:#64748B; font-size:15px; margin-top:8px;">
            Une lecture claire des irritants, une priorisation exploitable, et des livrables prêts pour un comité.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        card("Thèmes", "Comprendre ce qui revient")
        st.markdown("Regroupement automatique des verbatims en **thèmes explicables**.")
        end_card()

    with c2:
        card("Backlog", "Décider quoi traiter")
        st.markdown("Catégorie, sévérité, urgence : une **priorisation lisible**.")
        end_card()

    with c3:
        card("Livrables", "Partager rapidement")
        st.markdown("Exports **CSV / PDF / PPTX** pour aligner les parties prenantes.")
        end_card()

    card("Ce que tu peux faire ici", "Parcours recommandé")
    st.markdown("""
1) **Import** : charger un CSV + choisir la colonne texte  
2) **Analyse** : obtenir thèmes + exemples  
3) **Backlog** : prioriser les actions  
4) **Livrables** : exporter la synthèse  
""")
    # CTA en vrai lien cliquable
    st.markdown("<a class='nav-item active' href='?page=import'>Commencer → Import</a>", unsafe_allow_html=True)
    end_card()
