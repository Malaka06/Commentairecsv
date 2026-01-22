from pathlib import Path
from contextlib import contextmanager
import streamlit as st

from ui.theme import inject_css


# ======================
# CONFIG
# ======================

APP_NAME = "INSIGHTIA"
TAGLINE = "Transformer les verbatims clients en décisions actionnables"

BASE_DIR = Path(__file__).resolve().parent.parent  # insightia/
LOGO_PATH = BASE_DIR / "assets" / "logo_insightia.png"

ORDER = [
    ("home", "Accueil", 1),
    ("import", "Import", 1),
    ("analysis", "Analyse", 2),
    ("backlog", "Backlog", 3),
    ("livrables", "Livrables", 4),
    ("use-cases", "Cas d’usage", 3),
    ("method", "Méthode", 4),
]


# ======================
# ROUTING
# ======================

def get_page_key() -> str:
    key = st.query_params.get("page", "home")
    valid = {k for k, _, _ in ORDER}
    return key if key in valid else "home"


def set_page(key: str):
    st.query_params["page"] = key
    st.rerun()


# ======================
# UI ELEMENTS
# ======================

def _img_to_base64(path: Path) -> str:
    import base64
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def render_brand():
    # Logo (affichage)
    if LOGO_PATH.exists():
        st.markdown(
            f"""
            <a href="#" onclick="return false;">
              <img src="data:image/png;base64,{_img_to_base64(LOGO_PATH)}"
                   style="height:52px;border-radius:12px;margin-bottom:8px;" />
            </a>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='font-weight:900;font-size:20px'>{APP_NAME}</div>",
            unsafe_allow_html=True,
        )


def get_step_for_page(page_key: str) -> int:
    for k, _, step in ORDER:
        if k == page_key:
            return step
    return 1


def render_hero(active_step: int):
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-title">{APP_NAME}</div>
          <div class="hero-sub">{TAGLINE}</div>
          <div class="stepper">
            <div class="step {'active' if active_step==1 else ''}">1. Import</div>
            <div class="step {'active' if active_step==2 else ''}">2. Analyse</div>
            <div class="step {'active' if active_step==3 else ''}">3. Backlog</div>
            <div class="step {'active' if active_step==4 else ''}">4. Livrables</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_nav(current_key: str):
    dataset = st.session_state.get("dataset", None)
    analysis = st.session_state.get("analysis", None)
    backlog = st.session_state.get("backlog", None)

    dataset_ready = dataset is not None and not getattr(dataset, "empty", False)
    analysis_ready = analysis is not None and not getattr(analysis, "empty", False)
    backlog_ready = backlog is not None and not getattr(backlog, "empty", False)

    status = {
        "import": dataset_ready,
        "analysis": analysis_ready,
        "backlog": backlog_ready,
        "livrables": analysis_ready,
    }

    cols = st.columns(len(ORDER))
    for i, (key, label, _) in enumerate(ORDER):
        with cols[i]:
            is_active = (key == current_key)

            disabled = is_active
            if key == "analysis" and not dataset_ready:
                disabled = True
            if key in ("backlog", "livrables") and not analysis_ready:
                disabled = True

            if st.button(label, key=f"nav_{key}", disabled=disabled, use_container_width=True):
                set_page(key)

            if key in status:
                st.markdown(
                    f"<span class='pill {'ok' if status[key] else 'no'}'>"
                    f"{'Prêt' if status[key] else 'Manquant'}</span>",
                    unsafe_allow_html=True,
                )

    # Guidance discret si bloqué
    if current_key == "analysis" and not dataset_ready:
        st.info("Charge un CSV ou une démo pour accéder à l’analyse.")
    if current_key in ("backlog", "livrables") and not analysis_ready:
        st.info("Lance l’analyse pour générer les thèmes avant cette étape.")


def render_footer():
    st.markdown(
        """
        <div class="footer">
          <div>
            <b>INSIGHTIA</b> — Voice of Customer<br/>
            <span class="muted">Projet personnel • Ouverte aux opportunités</span>
          </div>
          <div>
            <span class="muted">Pour en savoir davantage :</span><br/>
            <b><a href="mailto:Aimeemalaka84@gmail.com">Aimeemalaka84@gmail.com</a></b>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================
# APP SHELL
# ======================

@contextmanager
def app_shell():
    inject_css()

    current = get_page_key()
    step = get_step_for_page(current)

    render_brand()
    render_hero(active_step=step)
    render_nav(current)

    yield

    render_footer()
