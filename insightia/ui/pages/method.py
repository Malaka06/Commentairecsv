import streamlit as st
from ui.components import card, end_card


def page_method():
    st.markdown(
        """
        <div style="max-width:900px; margin-bottom:8px;">
          <div style="font-size:22px; font-weight:950; letter-spacing:-0.02em;">
            Méthode
          </div>
          <div style="color:#64748B; font-size:14.5px; margin-top:6px;">
            Choix techniques orientés produit : stabilité, vitesse, explicabilité.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    card("Pipeline", "Du CSV aux thèmes")
    st.markdown("""
- **Nettoyage léger** : normalisation, suppression bruit, conservation des caractères FR  
- **Vectorisation** : TF-IDF (unigrams + bigrams)  
- **Regroupement** : KMeans (thèmes)  
- **Libellés** : mots dominants par thème (explicable)  
    """)
    end_card()

    card("Pourquoi cette V1", "Robuste dès le départ")
    st.markdown("""
- **Rapide** sur CPU (compatible Streamlit Cloud)  
- **Reproductible** (`random_state`, `n_init`)  
- **Auditables** : un thème = des mots dominants + des exemples  
- **Maintenable** : peu de dépendances, comportements stables  
    """)
    end_card()

    card("Garde-fous", "Qualité & fiabilité")
    st.markdown("""
- Limitation du volume analysé (échantillonnage contrôlé)  
- Contrôle colonnes vides / données manquantes  
- Messages d’erreurs explicites côté UI  
- Cache session (évite recalculs inutiles)  
    """)
    end_card()

    card("Évolutions prévues", "Quand ça vaut le coût")
    st.markdown("""
- Modèle “Advanced” (embeddings/BERTopic) **en option**, sans casser le moteur V1  
- Déduplication, recherche, comparaison Avant/Après plus robuste  
- Exports enrichis + templates de restitution  
    """)
    end_card()
