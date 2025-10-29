import streamlit as st
import pandas as pd
from utils import create_portfolio_cards

# Configuração da página
st.set_page_config(page_title="Portfólio de BI", page_icon="📊", layout="wide")

# Carregar CSS externo
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Carregar dados ---
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# --- Layout principal ---
def main():
    st.markdown("<h1 class='main-title'>📊 Portfólio do Setor de Business Intelligence</h1>", unsafe_allow_html=True)
    st.write("")
    df = load_data()
    create_portfolio_cards(df)

if __name__ == "__main__":
    main()
