import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Cardápio de Dashboards de BI",
    page_icon="🍽️", # Mudei o ícone para "cardápio"
    layout="wide"
)

# --- O LINK MÁGICO (SEGURO) ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.info("Por favor, vá em 'Settings' > 'Secrets' no painel do Streamlit e adicione o link da sua planilha.")
    st.stop()
except Exception as e:
    st.error(f"Um erro inesperado ocorreu ao tentar ler os segredos: {e}")
    st.stop()


# --- Título ---
st.title("🍽️ Cardápio de Dashboards de BI")
st.write("Use os filtros na barra lateral para encontrar o dashboard que você precisa.")

# --- Cache ---
@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(url, encoding='utf-8')
        # Garante que colunas essenciais existam, mesmo que vazias
        for col in ['Link', 'Status', 'Responsável', 'Público']:
            if col not in df.columns:
                df[col] = pd.NA
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        st.info(f"Verifique se o link da planilha está correto e se ela está publicada como CSV. URL usado: {url[:50]}...")
        return pd.DataFrame()

# --- Carregar Dados ---
df = carregar_dados(URL_PLANILHA)

# !!!!! LINHA DE DEPURAÇÃO !!!!!
# Deixei esta linha para você confirmar se os nomes estão corretos
st.write("DEBUG: Colunas encontradas na planilha:", df.columns)


if not df.empty:
    # --- Barra Lateral de Filtros (ATUALIZADA) ---
    st.sidebar.header("Filtros do Cardápio")
    
    # Filtro por Responsável
    try:
        responsaveis = ["Todos"] + sorted(list(df['Responsável'].dropna().unique()))
        filtro_responsavel = st.sidebar.selectbox("Filtrar por Responsável:", responsaveis)
    except KeyError:
        st.sidebar.error("Coluna 'Responsável' não encontrada.")
        filtro_responsavel = "Todos"
        
    # Filtro por Público (NOVO)
    try:
        publico_opcoes = ["Todos"] + sorted(list(df['Público'].dropna().unique()))
        filtro_publico = st.sidebar.selectbox("Filtrar por Público:", publico_opcoes)
    except KeyError:
        st.sidebar.error("Coluna 'Público' não encontrada.")
        filtro_publico = "Todos"
        
    # Filtro por Status
    try:
        status_opcoes = ["Todos"] + sorted(list(df['Status'].dropna().unique()))
        filtro_status = st.sidebar.selectbox("Filtrar por Status:", status_opcoes)
    except KeyError:
        st.sidebar.error("Coluna 'Status' não encontrada.")
        filtro_status = "Todos"
    
    # --- Lógica de Filtragem ---
    df_filtrado = df

    if filtro_responsavel != "Todos" and 'Responsável' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    
    if filtro_publico != "Todos" and 'Público' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    
    if filtro_status != "Todos" and 'Status' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    # --- Exibir os Cards ---
    st.write(f"Exibindo {len(df_filtrado)} dashboards:")
    st.divider() # Uma linha horizontal para separar

    if df_filtrado.empty:
        st.info("Nenhum dashboard encontrado com os filtros selecionados.")

    # Loop para criar os cards
    for index, row in df_filtrado.iterrows():
        # Cria um container com borda para cada "card"
        with st.container(border=True):
            
            # --- Título e Status ---
            col1_header, col2_header = st.columns([0.8, 0.2]) # 80% para o título, 20% para o status
            with col1_header:
                st.subheader(row['Report']) # Nome do Dashboard
            
            with col2_header:
                # Usa 'st.badge' (requer Streamlit 1.28+) para um status visual
                if pd.notna(row['Status']):
                    if row['Status'].lower() == 'ativo':
                        st.badge("Ativo", icon="✅")
                    else:
                        st.badge(row['Status'], icon="⚠️")
            
            # --- Descrição ---
            if pd.notna(row['Descrição']):
                st.write(row['Descrição'])
            
            # --- Detalhes (em colunas) ---
            st.markdown("---") # Linha divisória interna
            col1_details, col2_details, col3_details = st.columns(3)
            
            with col1_details:
                st.caption("RESPONSÁVEL")
                st.write(row['Responsável'])
                
                st.caption("MÍDIA")
                st.write(row['Mídia'])
            
            with col2_details:
                st.caption("PERIODICIDADE")
                st.write(row['Periodicidade'])
                
                st.caption("HORÁRIO")
                st.write(row['Horário'])

            with col3_details:
                st.caption("PÚBLICO")
                st.write(row['Público'])
                
                st.caption("DIVULGAÇÃO")
                st.write(row['Divulgação'])
            
            st.markdown("---") # Linha divisória interna
            
            # --- Botão de Ação ---
            if 'Link' in df.columns and pd.notna(row['Link']):
                # 'use_container_width=True' faz o botão ficar largo e bonito
                st.link_button("Acessar Dashboard", row['Link'], use_container_width=True, type="primary")
            else:
                st.error("Link de acesso não cadastrado para este report.", icon="⚠️")
        
        # Um espaço entre os cards
        st.write("") 

else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos a partir da planilha principal.")