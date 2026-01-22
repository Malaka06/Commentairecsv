import streamlit as st
from ui.layout import app_shell, get_page_key
from ui.pages.livrables import page_livrables


from ui.pages.home import page_home
from ui.pages.workspace import page_workspace
from ui.pages.analysis import page_analysis
from ui.pages.backlog import page_backlog
from ui.pages.use_cases import page_use_cases
from ui.pages.method import page_method

st.set_page_config(page_title="INSIGHTIA", page_icon="📊", layout="wide")

ROUTES = {
    "home": page_home,
    "import": page_workspace,
    "analysis": page_analysis,
    "backlog": page_backlog,
    "use-cases": page_use_cases,
    "method": page_method,
    "livrables": page_livrables,
}

def main():
    page = get_page_key()
    with app_shell():
        ROUTES[page]()

if __name__ == "__main__":
    main()
