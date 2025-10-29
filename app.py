import streamlit as st
import pandas as pd
import os
from utils import create_portfolio_cards

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Carregar CSS ---
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("❌ Arquivo 'styles.css' não encontrado.")

# --- Carregar Dados ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=",", quotechar='"', on_bad_lines="skip", engine="python")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame(columns=["Título", "Categoria", "Descrição", "Link", "Imagem_Path"])

# --- Layout ---
def main():
    st.markdown("<h1 class='main-title'>📊 Portfólio do Setor de Business Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Explore nossos dashboards interativos e relatórios automatizados</p>", unsafe_allow_html=True)

    df = load_data()
    if df.empty:
        st.warning("Nenhum projeto encontrado.")
    else:
        create_portfolio_cards(df)

if __name__ == "__main__":
    main()
