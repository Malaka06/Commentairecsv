import streamlit as st
import pandas as pd
from ui.components import card, end_card


def _top_themes(df: pd.DataFrame, n: int = 5):
    if df is None or df.empty or "topic_label" not in df.columns:
        return pd.DataFrame(columns=["theme", "count"])
    out = df["topic_label"].value_counts().head(n).reset_index()
    out.columns = ["theme", "count"]
    return out


def _executive_html(df_analysis: pd.DataFrame, df_backlog: pd.DataFrame, text_col: str) -> str:
    topA = _top_themes(df_analysis, 5)
    topB = _top_themes(df_backlog, 5)

    # Exemples P0
    p0_examples = []
    if df_backlog is not None and not df_backlog.empty and "severity" in df_backlog.columns:
        subset = df_backlog[df_backlog["severity"] == "P0"].head(5)
        for _, r in subset.iterrows():
            p0_examples.append(f"<li><b>{r.get('topic_label','')}</b> — {str(r.get(text_col,''))}</li>")

    p0_html = "<ul>" + "".join(p0_examples) + "</ul>" if p0_examples else "<p>Aucun P0 détecté.</p>"

    def table_html(df, title):
        if df is None or df.empty:
            return f"<p><i>{title} : aucune donnée.</i></p>"
        return (
            f"<h3>{title}</h3>"
            + df.to_html(index=False, escape=False)
        )

    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>INSIGHTIA — Executive Summary</title>
  <style>
    body {{ font-family: Arial, sans-serif; background:#F6F8FC; color:#0F172A; margin:0; padding:24px; }}
    .wrap {{ max-width: 980px; margin:0 auto; }}
    .hero {{
      background: linear-gradient(90deg,#1D4ED8,#0F2E6B);
      color:white; border-radius:18px; padding:18px 18px; margin-bottom:16px;
    }}
    .hero h1 {{ margin:0; font-size:22px; }}
    .hero p {{ margin:6px 0 0; opacity:0.92; }}
    .card {{
      background:white; border:1px solid #E6EAF2; border-radius:16px;
      padding:14px 16px; margin-bottom:14px;
      box-shadow: 0 10px 18px rgba(15,23,42,0.06);
    }}
    h2 {{ margin:0 0 8px; font-size:16px; }}
    h3 {{ margin:14px 0 8px; font-size:14px; }}
    table {{ width:100%; border-collapse: collapse; font-size:13px; }}
    th, td {{ border:1px solid #E6EAF2; padding:8px; text-align:left; }}
    th {{ background:#EEF2FF; }}
    .muted {{ color:#64748B; font-size:13px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>INSIGHTIA — Executive Summary</h1>
      <p>Thèmes dominants, signaux d’urgence, et priorités actionnables.</p>
    </div>

    <div class="card">
      <h2>Résumé</h2>
      <p class="muted">
        Ce rapport synthétise les verbatims clients en thèmes et priorités. Il est conçu pour accélérer la décision.
      </p>
    </div>

    <div class="card">
      {table_html(topA, "Top thèmes (Analyse)")}
      {table_html(topB, "Top thèmes (Backlog priorisé)")}
    </div>

    <div class="card">
      <h2>Exemples P0 (à traiter en priorité)</h2>
      {p0_html}
    </div>

    <div class="card">
      <h2>Note méthode</h2>
      <p class="muted">V1 : TF-IDF (1–2 grams) + KMeans, labels via mots dominants, priorisation via règles explicites.</p>
    </div>
  </div>
</body>
</html>
"""
    return html


def page_livrables():
    card("Livrables", "Exports prêts à partager (CSV + synthèse)")

    df_analysis = st.session_state.get("analysis")
    df_backlog = st.session_state.get("backlog")
    text_col = st.session_state.get("text_col")

    if df_analysis is None:
        st.warning("Lance d’abord l’analyse pour générer les thèmes.")
        end_card()
        return

    # CSV exports
    st.subheader("Exports CSV")

    st.download_button(
        "Télécharger Analyse (CSV enrichi)",
        data=df_analysis.to_csv(index=False).encode("utf-8"),
        file_name="insightia_analyse.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if df_backlog is not None:
        st.download_button(
            "Télécharger Backlog (CSV priorisé)",
            data=df_backlog.to_csv(index=False).encode("utf-8"),
            file_name="insightia_backlog.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("Backlog non généré (optionnel).")

    st.divider()

    # Executive summary (HTML)
    st.subheader("Synthèse (Executive Summary)")

    html = _executive_html(df_analysis, df_backlog, text_col=text_col or "commentaire")
    st.download_button(
        "Télécharger la synthèse (HTML imprimable)",
        data=html.encode("utf-8"),
        file_name="insightia_executive_summary.html",
        mime="text/html",
        use_container_width=True,
    )

    with st.expander("Aperçu"):
        st.components.v1.html(html, height=650, scrolling=True)

    end_card()
