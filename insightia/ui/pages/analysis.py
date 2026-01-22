from __future__ import annotations

import hashlib
import pandas as pd
import streamlit as st

from core.text_cleaning import clean_text_fast
from core.clustering import ClusteringParams, run_kmeans_tfidf
from ui.components import card, end_card


def _hash_for_cache(df: pd.DataFrame, text_col: str, n_topics: int, max_rows: int) -> str:
    head_bytes = df.head(200).to_csv(index=False).encode("utf-8", errors="ignore")
    h = hashlib.sha256(head_bytes).hexdigest()[:16]
    return f"{h}|{text_col}|{n_topics}|{max_rows}"


def page_analysis():
    card("Analyse", "V1 — TF-IDF + KMeans • Explicable • Rapide")

    df = st.session_state.get("dataset", None)
    text_col = st.session_state.get("text_col", None)

    if df is None or text_col is None:
        st.warning("Va d’abord dans Import : charge un CSV et enregistre le dataset.")
        end_card()
        return

    st.caption("Astuce : commence avec 12 thèmes. Ajuste ensuite selon la granularité souhaitée.")

    col1, col2, col3 = st.columns(3)
    with col1:
        max_rows = st.slider("Max lignes analysées", 200, 20000, 2000, 200)
    with col2:
        n_topics = st.slider("Nombre de thèmes", 6, 30, 12, 1)
    with col3:
        sample_if_large = st.checkbox("Échantillonner si trop grand", value=True)

    run = st.button("Lancer l’analyse", type="primary")

    st.session_state.setdefault("analysis", None)
    st.session_state.setdefault("analysis_key", None)

    key = _hash_for_cache(df, text_col, int(n_topics), int(max_rows))

    if not run and st.session_state["analysis"] is None:
        st.info("Configure puis clique sur “Lancer l’analyse”.")
        end_card()
        return

    if st.session_state["analysis"] is not None and st.session_state["analysis_key"] == key and not run:
        result_df = st.session_state["analysis"]
    else:
        dfx = df.copy()

        if len(dfx) > int(max_rows):
            dfx = (
                dfx.sample(n=int(max_rows), random_state=42).reset_index(drop=True)
                if sample_if_large
                else dfx.head(int(max_rows)).reset_index(drop=True)
            )

        with st.spinner("Nettoyage + vectorisation + clustering..."):
            cleaned = clean_text_fast(dfx[text_col].fillna("").astype(str).tolist())
            dfx["commentaire_clean"] = cleaned
            dfx = dfx[dfx["commentaire_clean"].str.strip().ne("")].reset_index(drop=True)

            if len(dfx) < int(n_topics):
                st.error(f"Pas assez de lignes non-vides ({len(dfx)}) pour {int(n_topics)} thèmes.")
                end_card()
                return

            params = ClusteringParams(
                n_topics=int(n_topics),
                max_features=8000,
                ngram_range=(1, 2),
                min_df=2,
                random_state=42,
                n_init=10,
                top_n_words=3,
            )

            res = run_kmeans_tfidf(dfx["commentaire_clean"].tolist(), params)
            dfx["topic"] = res.topics
            dfx["topic_label"] = dfx["topic"].map(res.topic_labels)

        st.session_state["analysis"] = dfx
        st.session_state["analysis_key"] = key
        result_df = dfx

    # KPIs
    k1, k2 = st.columns(2)
    k1.metric("Commentaires analysés", len(result_df))
    k2.metric("Thèmes détectés", int(result_df["topic_label"].nunique()))

    # Top thèmes
    st.subheader("Top thèmes")
    counts = result_df["topic_label"].value_counts().reset_index()
    counts.columns = ["theme", "count"]
    st.dataframe(counts, use_container_width=True, height=360)

    # Exemples
    st.subheader("Exemples par thème")
    top_labels = result_df["topic_label"].value_counts().head(12).index.tolist()
    pick = st.selectbox("Choisir un thème", options=top_labels)
    examples = (
        result_df.loc[result_df["topic_label"] == pick, text_col]
        .dropna().astype(str).head(10).tolist()
    )
    for i, ex in enumerate(examples, 1):
        st.write(f"{i}. {ex}")

    # Export
    st.subheader("Export")
    st.download_button(
        "Télécharger CSV enrichi (thèmes)",
        data=result_df.to_csv(index=False).encode("utf-8"),
        file_name="insightia_themes.csv",
        mime="text/csv",
        use_container_width=True,
    )

    end_card()
