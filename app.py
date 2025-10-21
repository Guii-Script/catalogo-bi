import streamlit as st
import pandas as pd
import re # Biblioteca de Expressões Regulares, usada para a busca

# --- Configuração da Página ---
# Define as configurações iniciais da página, como título da aba e layout
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="✨", # Ícone atualizado
    layout="wide"
)

# --- Injeção de CSS Customizado ---
# Esta função injeta o bloco de CSS para reestilizar a aplicação.
def load_custom_css():
    st.markdown(f"""
        <style>
            /* --- 1. Configurações Globais --- */
            /* Define o fundo da aplicação para um tom off-white */
            [data-testid="stAppViewContainer"] {{
                background-color: #F8F9FA;
            }}

            /* --- 2. Tipografia --- */
            /* Título principal da página */
            h1 {{
                color: #0d2e5b; /* Cor primária (azul escuro) */
                font-weight: 700;
            }}
            /* Título de seção (ex: "Exibindo...") */
            h3 {{
                color: #333333; /* Cinza escuro para contraste suave */
            }}

            /* --- 3. Card de Portfólio --- */
            /* Seleciona o container que o Streamlit cria com 'border=True' */
            [data-testid="stVerticalBlockBorderWrapper"] > div {{
                background-color: #FFFFFF; /* Cor base (branco) */
                border: 1px solid #EAEAEA; /* Borda sutil */
                border-radius: 12px;       /* Cantos mais suaves */
                /* Sombra em camadas para profundidade */
                box-shadow: 0 4px 8px rgba(0,0,0,0.04), 0 8px 16px rgba(0,0,0,0.04);
                transition: all 0.3s ease-out; /* Transição suave para hover */
                min-height: 400px;         /* Altura mínima para alinhamento do grid */
                display: flex;
                flex-direction: column;
                padding: 24px;
            }}
            /* Efeito de hover "premium" */
            [data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
                transform: scale(1.015); /* Zoom sutil */
                border-color: #5b92c8;   /* Cor secundária (azul claro) */
                box-shadow: 0 8px 16px rgba(0,0,0,0.06), 0 12px 24px rgba(0,0,0,0.06);
            }}

            /* --- 4. Título e Descrição do Card --- */
            /* O Streamlit usa 'st.subheader' que renderiza como h2 */
            [data-testid="stVerticalBlockBorderWrapper"] h2 {{
                color: #0d2e5b;
                font-weight: 600;
                margin-bottom: 12px;
                line-height: 1.3;
            }}
            [data-testid="stVerticalBlockBorderWrapper"] p {{
                color: #333333; /* Cor do texto de descrição */
                font-size: 15px;
            }}

            /* --- 5. Tags (Etiquetas) Customizadas --- */
            .tag-wrapper {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin: 12px 0px;
            }}
            .tag {{
                background-color: #e7f0f9; /* Tonalidade muito clara de #5b92c8 */
                color: #0d2e5b; /* Texto na cor primária */
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 500;
                line-height: 1.4;
            }}
            /* Variação de tag para status "Ativo" */
            .tag.status-ativo {{
                background-color: #E6F6E8; /* Verde claro */
                color: #1E6426; /* Verde escuro */
            }}
             /* Variação de tag para status "Inativo" ou "Manutenção" */
            .tag.status-inativo {{
                background-color: #FDF3F3; /* Vermelho claro */
                color: #9C2B2B; /* Vermelho escuro */
            }}


            /* --- 6. Layout do Card --- */
            /* Garante que os botões fiquem alinhados no rodapé */
            .stButton, .stLinkButton {{
                margin-top: auto;
            }}
            
            /* --- 7. Estilização de Componentes Streamlit --- */
            /* Botão Primário (Acessar) */
            [data-testid="stButton"] button:not(:disabled), [data-testid="stLinkButton"] a {{
                background-color: #0d2e5b;
                color: #FFFFFF;
                border: 1px solid #0d2e5b;
                transition: all 0.2s ease;
            }}
            /* Hover do Botão Primário */
            [data-testid="stButton"] button:not(:disabled):hover, [data-testid="stLinkButton"] a:hover {{
                background-color: #5b92c8;
                border-color: #5b92c8;
                color: #FFFFFF;
            }}
            /* Botão Desabilitado (Link Indisponível) */
            [data-testid="stButton"] button:disabled {{
                background-color: #F0F2F6;
                border-color: #EAEAEA;
                color: #AAAAAA;
            }}
            
            /* Popover (Detalhes) */
            [data-testid="stPopover"] {{
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #FFFFFF;
                border-right: 1px solid #EAEAEA;
            }}
        </style>
    """, unsafe_allow_html=True)

# Executa a injeção do CSS
load_custom_css()


# --- Carregamento de Dados ---
# Busca a URL da planilha dos 'Secrets' do Streamlit
# Esta é a abordagem segura para evitar expor o link no GitHub.
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.stop()
except Exception as e:
    st.error(f"Um erro inesperado ocorreu ao tentar ler os segredos: {e}")
    st.stop()

# Função para carregar e cachear os dados da planilha.
# O cache (ttl=600) armazena os dados por 10 minutos, melhorando a
# performance ao evitar requisições repetidas ao Google Sheets.
@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(url, encoding='utf-8')
        
        # Define as colunas esperadas para evitar erros
        colunas_essenciais = ['Report', 'Descrição', 'Link', 'Status', 'Responsável', 'Público', 'Mídia', 'Periodicidade', 'Horário', 'Divulgação']
        for col in colunas_essenciais:
            if col not in df.columns:
                df[col] = pd.NA
        
        # Converte todas as colunas para string para consistência na busca
        df = df.astype(str)
        # Substitui valores nulos (nan, <NA>) por 'N/A' para exibição
        df.replace(['nan', '<NA>', 'NaN'], 'N/A', inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return pd.DataFrame()

# Executa o carregamento dos dados
df = carregar_dados(URL_PLANILHA)

# --- Título Principal ---
st.title("💼 Portfólio de Dashboards de BI")
st.write("Navegue pelo nosso catálogo de dashboards. Use a busca e os filtros para refinar.")
st.write("") # Adiciona um espaço vertical

# --- Lógica Principal (Busca, Filtros e Grid) ---
if not df.empty:
    
    # --- 1. BARRA DE BUSCA ---
    # Componente de entrada de texto para a busca em tempo real.
    search_term = st.text_input(
        "Buscar por nome ou descrição:", 
        placeholder="Digite um termo-chave..."
    )
    
    # --- 2. BARRA LATERAL DE FILTROS ---
    st.sidebar.header("Filtros do Catálogo")
    
    # Função auxiliar para gerar listas de opções para os filtros
    def criar_lista_filtro(coluna):
        # Remove valores nulos ('N/A') e duplicados, depois ordena
        opcoes = df[coluna].replace('N/A', pd.NA).dropna().unique()
        return ["Todos"] + sorted(list(opcoes))

    # Cria os seletores (selectbox) na barra lateral
    try:
        filtro_responsavel = st.sidebar.selectbox("Responsável:", criar_lista_filtro('Responsável'))
        filtro_publico = st.sidebar.selectbox("Público:", criar_lista_filtro('Público'))
        filtro_midia = st.sidebar.selectbox("Mídia:", criar_lista_filtro('Mídia'))
        filtro_status = st.sidebar.selectbox("Status:", criar_lista_filtro('Status'))
    except KeyError as e:
        st.sidebar.error(f"Erro: Coluna '{e.args[0]}' não encontrada.")
        # Define padrões para evitar que o app pare
        filtro_responsavel = filtro_publico = filtro_midia = filtro_status = "Todos"
    
    # --- 3. LÓGICA DE FILTRAGEM ---
    df_filtrado = df

    # Aplica a busca (case-insensitive)
    if search_term:
        search_regex = re.escape(search_term)
        df_filtrado = df_filtrado[
            df_filtrado['Report'].str.contains(search_regex, case=False, na=False) |
            df_filtrado['Descrição'].str.contains(search_regex, case=False, na=False)
        ]

    # Aplica os filtros da sidebar
    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Mídia'] == filtro_midia]
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    
    # --- 4. LÓGICA DE EXIBIÇÃO EM GRID ---
    st.write(f"### Exibindo {len(df_filtrado)} dashboards:")
    st.divider()

    NUM_COLUNAS = 3 # Define o número de colunas do grid
    reports_list = df_filtrado.to_dict('records') # Converte o dataframe para iterar

    if not reports_list:
        st.info("Nenhum dashboard encontrado com os filtros e busca selecionados.")

    # Itera pela lista de reports em "fatias" (chunks)
    for i in range(0, len(reports_list), NUM_COLUNAS):
        cols = st.columns(NUM_COLUNAS)
        chunk = reports_list[i : i + NUM_COLUNAS]

        # Preenche cada coluna com um card
        for j, report_data in enumerate(chunk):
            with cols[j]:
                # 'border=True' é o seletor usado pelo nosso CSS customizado
                with st.container(border=True):
                    
                    # Título (usando markdown para h2)
                    st.markdown(f"<h2>{report_data.get('Report', 'Sem Título')}</h2>", unsafe_allow_html=True)
                    
                    # Descrição (limitada em caracteres)
                    descricao = report_data.get('Descrição', 'N/A')
                    st.write(descricao[:120] + ("..." if len(descricao) > 120 else ""))
                    
                    # --- Tags de HTML Customizadas ---
                    # Define a classe do status
                    status_val = report_data.get('Status', 'N/A').lower()
                    if status_val == 'ativo':
                        status_class = 'status-ativo'
                    elif status_val == 'inativo' or status_val == 'manutenção':
                        status_class = 'status-inativo'
                    else:
                        status_class = ''

                    tags_html = f"""
                    <div class="tag-wrapper">
                        <span class="tag">👤 {report_data.get('Público', 'N/A')}</span>
                        <span class="tag">🔧 {report_data.get('Mídia', 'N/A')}</span>
                        <span class="tag {status_class}"> {report_data.get('Status', 'N/A')}</span>
                    </div>
                    """
                    st.markdown(tags_html, unsafe_allow_html=True)

                    # --- Popover (Detalhes) ---
                    with st.popover("Ver mais detalhes"):
                        st.markdown(f"**Responsável:** {report_data.get('Responsável', 'N/A')}")
                        st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                        st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                        st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")

                    # --- Botão de Ação ---
                    link = report_data.get('Link')
                    # 'key' é essencial para evitar erros de ID duplicado em loops
                    key_base = f"{i}_{j}" 
                    
                    if link and link.lower() != 'n/a':
                        st.link_button(
                            "Acessar Dashboard", 
                            link, 
                            use_container_width=True, 
                            type="primary",
                            key=f"link_{key_base}"
                        )
                    else:
                        st.button(
                            "Link Indisponível", 
                            use_container_width=True, 
                            disabled=True, 
                            key=f"disabled_{key_base}"
                        )

else:
    st.warning("Não foi possível carregar os dados do catálogo ou a planilha está vazia.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")