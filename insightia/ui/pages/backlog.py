import streamlit as st
from ui.components import card, end_card
from core.prioritization import build_backlog


def _badge(sev: str) -> str:
    color = {"P0": "#DC2626", "P1": "#F59E0B", "P2": "#10B981"}.get(sev, "#64748B")
    return (
        f"<span style='background:{color};color:white;padding:4px 10px;"
        f"border-radius:999px;font-weight:900;font-size:12px;'>{sev}</span>"
    )


def page_backlog():
    card("Backlog priorisé", "Transformer les thèmes en priorités actionnables")

    df_analysis = st.session_state.get("analysis")
    text_col = st.session_state.get("text_col")

    if df_analysis is None:
        st.warning("Lance d’abord l’analyse pour générer les thèmes.")
        end_card()
        return

    if st.button("Générer / Rafraîchir le backlog", type="primary"):
        with st.spinner("Construction du backlog…"):
            st.session_state["backlog"] = build_backlog(df_analysis, text_col=text_col)
        st.success("Backlog généré ✅")

    backlog = st.session_state.get("backlog")
    if backlog is None:
        st.info("Clique sur “Générer / Rafraîchir le backlog”.")
        end_card()
        return

    # --- KPIs rapides ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Items", len(backlog))
    c2.metric("P0", int((backlog["severity"] == "P0").sum()))
    c3.metric("P1", int((backlog["severity"] == "P1").sum()))

    st.divider()

    # --- Top thèmes ---
    st.subheader("Top thèmes à traiter")
    top_themes = (
        backlog.groupby("topic_label")
        .agg(items=("priority_score", "count"), score_moyen=("priority_score", "mean"))
        .sort_values("score_moyen", ascending=False)
        .head(6)
        .reset_index()
    )
    st.dataframe(top_themes, use_container_width=True, height=240)

    st.divider()

    # --- Filtres ---
    st.subheader("Filtrer")
    colA, colB, colC = st.columns(3)
    with colA:
        sev = st.multiselect("Sévérité", ["P0", "P1", "P2"], default=["P0", "P1", "P2"])
    with colB:
        cats = sorted(backlog["category"].unique().tolist())
        cat = st.multiselect("Catégorie", cats, default=cats)
    with colC:
        per_theme = st.slider("Items par thème", 3, 30, 10, 1)

    filtered = backlog[backlog["severity"].isin(sev) & backlog["category"].isin(cat)]

    st.divider()

    # --- Backlog par thème (lisible comité) ---
    st.subheader("Backlog par thème")
    for theme in top_themes["topic_label"].tolist():
        subset = filtered[filtered["topic_label"] == theme].head(int(per_theme))
        if subset.empty:
            continue

        st.markdown(f"### {theme}")

        for _, row in subset.iterrows():
            st.markdown(
                f"""
                <div class="card">
                  <div style="display:flex; gap:10px; align-items:center;">
                    {_badge(row["severity"])}
                    <div style="font-weight:950;">{row["category"]}</div>
                    <div class="muted" style="margin-left:auto;">Score: <b>{int(row["priority_score"])}</b></div>
                  </div>

                  <div style="margin-top:8px;">{row[text_col]}</div>

                  <div class="muted" style="margin-top:8px;">
                    Action suggérée : <b>{row["action_suggeree"]}</b>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.download_button(
        "Télécharger Backlog (CSV)",
        data=backlog.to_csv(index=False).encode("utf-8"),
        file_name="insightia_backlog.csv",
        mime="text/csv",
    )

    end_card()
