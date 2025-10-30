import streamlit as st
import pandas as pd

@st.cache_data(ttl=600)
def carregar_dados(url):
    """Carrega dados da URL do Google Sheets e preenche colunas ausentes."""
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_esperadas = [
            'Nome_Dash','Descricao', 'Imagem_Path','Link','Status','Responsavel',
            'Publico','Midia','Periodicidade','Horario','Divulgacao'
        ]
        for c in colunas_esperadas:
            if c not in df.columns: 
                df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def lista(df_active, col):
    """Cria uma lista de valores únicos para um seletor, baseada nos dashboards ativos."""
    if df_active.empty:
        return ["Todos"]
    # Usa df_active para que os filtros só mostrem opções de dashboards ativos
    return ["Todos"] + sorted(df_active[col].replace('N/A', pd.NA).dropna().unique().tolist())