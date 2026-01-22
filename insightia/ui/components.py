import streamlit as st

def card(title: str, subtitle: str = ""):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f"<div class='muted' style='margin-top:-2px; margin-bottom:10px;'>{subtitle}</div>",
            unsafe_allow_html=True,
        )

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)
