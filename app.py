import streamlit as st
import pandas as pd
import re # Usado para a busca

# --- Configuração da Página ---
# Define o layout inicial da página
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="✨", # Ícone de "excelência"
    layout="wide"
)

# --- CSS Avançado ---
# para reestilizar os componentes padrão do Streamlit.
def load_custom_css():
    st.markdown("""
        <style>
            /* --- Fundo e Layout --- */
            [data-testid="stAppViewContainer"] {
                /* Um gradiente sutil é mais profissional que uma cor sólida */
                background: linear-gradient(170deg, #F0F2F6 0%, #E9EEF5 100%);
            }

            /* --- Títulos --- */
            h1 {
                color: #0D1F3C; /* Um azul escuro, forte */
                font-weight: 700;
            }
            h3 {
                color: #0D1F3C; /* Título de "Exibindo..." */
            }

            /* --- O Card--- */
            [data-testid="stVerticalBlockBorderWrapper"] > div {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0; /* Borda sutil */
                box-shadow: 0 4px 6px rgba(0,0,0,0.04); /* Sombra inicial leve */
                transition: all 0.3s ease-in-out; /* Animação suave para TUDO */
                min-height: 380px; /* Altura mínima para alinhar os botões */
                display: flex;
                flex-direction: column;
                padding: 24px 24px 20px 24px;
            }

            /* --- Animação de Hover (A "Excelência") --- */
            [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
                transform: translateY(-5px); /* Levita o card */
                box-shadow: 0 10px 20px rgba(0,0,0,0.08); /* Sombra mais forte */
                border-color: #0068C9; /* Borda na cor primária */
            }

            /* --- Título dentro do Card --- */
            [data-testid="stVerticalBlockBorderWrapper"] h2 {
                color: #004a8d; /* Cor primária escura */
                font-weight: 600;
                margin-bottom: 10px;
            }

            /* --- Tags (Etiquetas) Customizadas --- */
            .tag-wrapper {
                display: flex;
                flex-wrap: wrap; /* Permite que as tags quebrem a linha */
                gap: 8px;
                margin: 10px 0px;
            }
            .tag {
                background-color: #E6F0F8; /* Fundo azul claro */
                color: #004a8d; /* Texto azul escuro */
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 13px;
                font-weight: 600;
                line-height: 1.4;
            }
            
            /* --- Botões e Popover --- */
            .stButton, .stLinkButton {
                margin-top: auto; /* O truque para alinhar no rodapé */
            }
            [data-testid="stPopover"] {
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            [data-testid="stSidebar"] {
                background-color: #FFFFFF;
            }
        </style>
    """, unsafe_allow_html=True)

# Executa a função para carregar o CSS
load_custom_css()


# --- Carregamento de Dados ---
# (Mesma lógica segura de antes)
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.stop()
except Exception as e:
    st.error(f"Um erro inesperado ocorreu ao tentar ler os segredos: {e}")
    st.stop()

@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(url, encoding='utf-8')
        # Garante que as colunas existam
        colunas_essenciais = ['Report', 'Descrição', 'Link', 'Status', 'Responsável', 'Público', 'Mídia', 'Periodicidade', 'Horário', 'Divulgação']
        for col in colunas_essenciais:
            if col not in df.columns:
                df[col] = pd.NA
        
        # Converte tudo para string para evitar erros de busca
        df = df.astype(str)
        # Substitui 'nan' ou '<NA>' por 'N/A' para uma exibição mais limpa
        df.replace(['nan', '<NA>', 'NaN'], 'N/A', inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Título Principal ---
st.title("💼 Portfólio de Dashboards de BI")
st.write("Navegue pelo nosso catálogo de dashboards. Use a busca e os filtros para refinar.")
st.write("") # Espaço

# --- Lógica Principal (Busca, Filtros e Grid) ---
if not df.empty:
    
    # --- 1. BARRA DE BUSCA (A Nova Interação) ---
    search_term = st.text_input(
        "Buscar por nome ou descrição:", 
        placeholder="Digite um termo-chave..."
    )
    
    # --- 2. BARRA LATERAL DE FILTROS ---
    st.sidebar.header("Filtros do Catálogo")
    
    def criar_lista_filtro(coluna):
        return ["Todos"] + sorted(list(df[coluna].dropna().unique()))

    try:
        filtro_responsavel = st.sidebar.selectbox("Responsável:", criar_lista_filtro('Responsável'))
        filtro_publico = st.sidebar.selectbox("Público:", criar_lista_filtro('Público'))
        filtro_midia = st.sidebar.selectbox("Mídia:", criar_lista_filtro('Mídia'))
        filtro_status = st.sidebar.selectbox("Status:", criar_lista_filtro('Status'))
    except KeyError as e:
        st.sidebar.error(f"Erro: Coluna '{e.args[0]}' não encontrada.")
        filtro_responsavel = filtro_publico = filtro_midia = filtro_status = "Todos"
    
    # --- 3. LÓGICA DE FILTRAGEM (Busca + Filtros) ---
    df_filtrado = df

    # Aplica a BUSCA primeiro
    if search_term:
        # Busca case-insensitive (ignorando maiúsculas/minúsculas)
        # 're.escape' protege contra caracteres especiais na busca
        search_regex = re.escape(search_term)
        df_filtrado = df_filtrado[
            df_filtrado['Report'].str.contains(search_regex, case=False, na=False) |
            df_filtrado['Descrição'].str.contains(search_regex, case=False, na=False)
        ]

    # Aplica os FILTROS da sidebar no resultado da busca
    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Mídia'] == filtro_midia]
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    
    # --- 4. LÓGICA DE EXIBIÇÃO EM GRID (Portfólio) ---
    st.write(f"### Exibindo {len(df_filtrado)} dashboards:")
    st.divider()

    NUM_COLUNAS = 3 
    reports_list = df_filtrado.to_dict('records')

    if not reports_list:
        st.info("Nenhum dashboard encontrado com os filtros e busca selecionados.")

    # Itera e cria o grid
    for i in range(0, len(reports_list), NUM_COLUNAS):
        cols = st.columns(NUM_COLUNAS)
        chunk = reports_list[i : i + NUM_COLUNAS]

        for j, report_data in enumerate(chunk):
            with cols[j]:
                # 'border=True' é o "gatilho" para o nosso CSS customizado
                with st.container(border=True):
                    
                    # Título (st.subheader vira <h2>)
                    st.subheader(report_data.get('Report', 'Sem Título'))
                    
                    # Descrição (limitada para não quebrar o layout)
                    descricao = report_data.get('Descrição', 'Sem descrição.')
                    st.write(descricao[:120] + ("..." if len(descricao) > 120 else ""))
                    
                    # --- Tags de HTML Customizadas ---
                    # Esta é a parte visual mais importante
                    tags_html = f"""
                    <div class="tag-wrapper">
                        <span class="tag">👤 {report_data.get('Público', 'N/A')}</span>
                        <span class="tag">🔧 {report_data.get('Mídia', 'N/A')}</span>
                        <span class="tag">🟢 {report_data.get('Status', 'N/A')}</span>
                    </div>
                    """
                    st.markdown(tags_html, unsafe_allow_html=True)

                    # --- Popover (Detalhes) ---
                    # (Mesma lógica de antes, sem o 'key' problemático)
                    with st.popover("Ver mais detalhes"):
                        st.markdown(f"**Responsável:** {report_data.get('Responsável', 'N/A')}")
                        st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                        st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                        st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")

                    # --- Botão de Ação ---
                    link = report_data.get('Link')
                    if link and link.lower() != 'n/a':
                        st.link_button(
                            "Acessar Dashboard", 
                            link, 
                            use_container_width=True, 
                            type="primary",
                            key=f"link_{i}_{j}" # Chave única
                        )
                    else:
                        st.button(
                            "Link Indisponível", 
                            use_container_width=True, 
                            disabled=True, 
                            key=f"disabled_{i}_{j}" # Chave única
                        )

else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")