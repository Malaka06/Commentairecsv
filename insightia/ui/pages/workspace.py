import csv
import io
import pandas as pd
import streamlit as st

from ui.components import card, end_card
from core.demo_data import load_demo_ecommerce, load_demo_saas, load_demo_minimal


def detect_sep_from_bytes(file_bytes: bytes) -> str:
    try:
        sample = file_bytes[:4096].decode("utf-8", errors="ignore")
        return csv.Sniffer().sniff(sample).delimiter
    except Exception:
        return ";"


def read_csv_safely_from_bytes(file_bytes: bytes, sep: str) -> pd.DataFrame:
    bio = io.BytesIO(file_bytes)
    return pd.read_csv(bio, sep=sep, on_bad_lines="skip")


def validate_text_column(df: pd.DataFrame, text_col: str) -> tuple[bool, str]:
    if df.empty:
        return False, "Le fichier est vide."
    if text_col not in df.columns:
        return False, "La colonne sélectionnée n’existe pas."
    non_empty = df[text_col].astype(str).fillna("").str.strip().ne("").sum()
    if non_empty == 0:
        return False, "La colonne texte ne contient aucun contenu exploitable (tout est vide)."
    return True, f"OK — {non_empty} lignes non-vides détectées dans la colonne texte."


def _load_demo(which: str):
    try:
        if which == "ecom":
            df_demo = load_demo_ecommerce()
            name = "demo_insightia_ecommerce.csv"
        elif which == "saas":
            df_demo = load_demo_saas()
            name = "demo_insightia_saas.csv"
        else:
            df_demo = load_demo_minimal()
            name = "demo_minimal"
    except FileNotFoundError as e:
        st.error(str(e))
        st.info("Fallback : chargement d’un petit dataset minimal.")
        df_demo = load_demo_minimal()
        name = "demo_minimal"

    # Assure la présence d'une colonne texte standard
    if "commentaire" not in df_demo.columns:
        st.error("Le dataset démo doit contenir une colonne 'commentaire'.")
        return

    st.session_state["dataset"] = df_demo
    st.session_state["text_col"] = "commentaire"
    st.session_state["sep"] = None
    st.session_state["file_name"] = name
    st.session_state["analysis"] = None
    st.session_state["backlog"] = None
    st.success(f"Dataset démo chargé ✅ ({name})")
    st.rerun()


def page_workspace():
    card("Import", "Importer un CSV • Choisir la colonne texte • Valider")
    st.caption("Import rapide : choisissez le séparateur, sélectionnez la colonne texte, puis enregistrez.")

    st.session_state.setdefault("dataset", None)
    st.session_state.setdefault("text_col", None)
    st.session_state.setdefault("sep", None)
    st.session_state.setdefault("file_name", None)
    st.session_state.setdefault("analysis", None)
    st.session_state.setdefault("backlog", None)

    # ✅ MODE DÉMO (2 boutons)
    st.subheader("Mode démo")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Charger Démo E-commerce", use_container_width=True):
            _load_demo("ecom")
    with c2:
        if st.button("Charger Démo SaaS B2B", use_container_width=True):
            _load_demo("saas")
    with c3:
        if st.button("Démo minimale", use_container_width=True):
            _load_demo("minimal")

    st.markdown(
        "<div class='muted'>Ces jeux de données sont conçus pour faire ressortir des thèmes nets + des priorités P0/P1/P2.</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # CSV upload
    uploaded = st.file_uploader("Fichier CSV", type=["csv"])
    if uploaded is None:
        # si dataset déjà en session (démo ou précédent import), on montre
        if st.session_state["dataset"] is not None and st.session_state["text_col"] is not None:
            st.subheader("Aperçu (dataset en session)")
            st.dataframe(st.session_state["dataset"].head(25), use_container_width=True)
            st.info("Dataset déjà chargé. Tu peux passer à Analyse.")
        else:
            st.info("Charge un CSV pour démarrer, ou utilise le mode démo.")
        end_card()
        return

    file_bytes = uploaded.getvalue()
    st.session_state["file_name"] = uploaded.name

    auto_sep = detect_sep_from_bytes(file_bytes)
    sep = st.selectbox(
        "Séparateur",
        options=[",", ";", "\t"],
        index=[",", ";", "\t"].index(auto_sep) if auto_sep in [",", ";", "\t"] else 1,
    )

    try:
        df = read_csv_safely_from_bytes(file_bytes, sep=sep)
    except Exception as e:
        st.error("Lecture CSV impossible.")
        st.code(str(e))
        end_card()
        return

    if df.empty:
        st.warning("CSV chargé mais vide.")
        end_card()
        return

    st.subheader("Aperçu")
    st.dataframe(df.head(25), use_container_width=True)

    st.subheader("Configuration")
    text_col = st.selectbox("Colonne texte", options=df.columns.tolist())

    ok, msg = validate_text_column(df, text_col)
    if ok:
        st.success(msg)
    else:
        st.error(msg)

    col1, col2 = st.columns([1, 1])
    with col1:
        save = st.button(
            "Enregistrer le dataset",
            type="primary",
            disabled=not ok,
            use_container_width=True,
        )
    with col2:
        clear = st.button("Réinitialiser", use_container_width=True)

    if clear:
        st.session_state["dataset"] = None
        st.session_state["text_col"] = None
        st.session_state["sep"] = None
        st.session_state["analysis"] = None
        st.session_state["backlog"] = None
        st.session_state["file_name"] = None
        st.rerun()

    if save:
        st.session_state["dataset"] = df
        st.session_state["text_col"] = text_col
        st.session_state["sep"] = sep
        st.session_state["analysis"] = None
        st.session_state["backlog"] = None
        st.success("Dataset enregistré en session ✅")

    end_card()
