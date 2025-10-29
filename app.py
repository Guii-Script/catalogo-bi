import streamlit as st
import pandas as pd
from utils import create_portfolio_cards

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboards e Relatórios",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Carregar CSS ---
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Carregar Dados ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=",", quotechar='"', on_bad_lines="skip", engine="python")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame(columns=["Título", "Categoria", "Descrição", "Link", "Imagem_Path"])

# --- Layout Principal ---
def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="title">💎 Portfólio de Business Intelligence</h1>
        <p class="subtitle">Visualize nossos dashboards e relatórios interativos</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df.empty:
        st.warning("Nenhum projeto encontrado no arquivo CSV.")
        return

    # --- Filtros Laterais ---
    st.sidebar.markdown("### 🔍 Filtros")
    categorias = ["Todas"] + sorted(df["Categoria"].dropna().unique().tolist())
    filtro_categoria = st.sidebar.selectbox("Categoria:", categorias)

    # Filtro de busca
    termo_busca = st.sidebar.text_input("Buscar por nome ou descrição:")

    # Filtrar DataFrame
    if filtro_categoria != "Todas":
        df = df[df["Categoria"] == filtro_categoria]

    if termo_busca:
        termo = termo_busca.lower()
        df = df[df.apply(lambda row: termo in row["Título"].lower() or termo in row["Descrição"].lower(), axis=1)]

    # --- Exibir Cards ---
    create_portfolio_cards(df)

if __name__ == "__main__":
    main()
