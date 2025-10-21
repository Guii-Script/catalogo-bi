import streamlit as st
import pandas as pd
import re # Usado para a funcionalidade de busca

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="🚀", # Ícone de "foguete" para representar avanço e design
    layout="wide"
)

# --- Cores da Paleta ---
# Definimos as cores para fácil gerenciamento e consistência
COLOR_PRIMARY = "#0d2e5b"  # Azul escuro principal
COLOR_SECONDARY = "#5b92c8" # Azul claro de destaque
COLOR_BACKGROUND_START = "#0d2e5b" # Fundo do app, início do degradê (seu azul escuro)
COLOR_BACKGROUND_END = "#1d4a7c"   # Fundo do app, fim do degradê (um azul um pouco mais claro que o primário para o degradê)
COLOR_CARD_BACKGROUND = "rgba(13, 46, 91, 0.85)" # Fundo do card (azul escuro com transparência)
COLOR_TEXT_LIGHT = "#FFFFFF" # Texto claro (branco)
COLOR_TEXT_MUTED = "#CCCCCC" # Texto suave (cinza claro)

# --- Injeção de CSS Customizado ---
# Este bloco de CSS transforma completamente a estética da aplicação.
def load_custom_css():
    st.markdown(f"""
        <style>
            /* --- 1. Configurações Globais --- */
            /* Fundo da aplicação com um degradê vertical vibrante */
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(180deg, {COLOR_BACKGROUND_START} 0%, {COLOR_BACKGROUND_END} 100%);
                color: {COLOR_TEXT_LIGHT}; /* Cor de texto padrão para o fundo */
            }}

            /* Ajustes para o sidebar */
            [data-testid="stSidebar"] {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_TEXT_LIGHT};
                border-right: 1px solid {COLOR_SECONDARY};
            }}
            /* Cor do texto do filtro na sidebar */
            [data-testid="stSidebar"] .st-bd {{ /* st-bd é o label do selectbox */
                color: {COLOR_TEXT_LIGHT};
            }}

            /* --- 2. Tipografia --- */
            h1, h2, h3, h4, h5, h6 {{
                color: {COLOR_TEXT_LIGHT}; /* Todos os títulos em branco */
            }}
            /* Título principal da página */
            h1 {{
                font-weight: 800;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3); /* Sombra para o título principal */
            }}
            /* Título do card (st.subheader) */
            [data-testid="stVerticalBlockBorderWrapper"] h2 {{
                color: {COLOR_TEXT_LIGHT};
                font-weight: 700;
                margin-bottom: 15px;
                line-height: 1.3;
            }}
            /* Descrição do card */
            [data-testid="stVerticalBlockBorderWrapper"] p {{
                color: {COLOR_TEXT_MUTED}; /* Texto suave para descrições */
                font-size: 15px;
            }}
            /* Texto de caption (Público, Responsável no card) */
            [data-testid="stVerticalBlockBorderWrapper"] .st-b5 {{
                color: {COLOR_TEXT_MUTED};
                font-size: 13px;
            }}


            /* --- 3. Card de Portfólio (Design Impactante) --- */
            /* O container 'border=True' é o alvo do nosso CSS */
            [data-testid="stVerticalBlockBorderWrapper"] > div {{
                background-color: {COLOR_CARD_BACKGROUND}; /* Fundo azul escuro translúcido */
                border: 1px solid {COLOR_SECONDARY};       /* Borda de destaque */
                border-radius: 12px;
                /* Sombra em camadas para um efeito de profundidade flutuante */
                box-shadow: 0 6px 15px rgba(0,0,0,0.2), 0 12px 30px rgba(0,0,0,0.15);
                transition: all 0.3s ease-out; /* Transição suave para interatividade */
                min-height: 400px;
                display: flex;
                flex-direction: column;
                padding: 28px;
            }}
            /* Efeito de hover "premium" nos cards */
            [data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
                transform: translateY(-8px) scale(1.02); /* Levanta e aumenta ligeiramente */
                box-shadow: 0 12px 25px rgba(0,0,0,0.3), 0 20px 45px rgba(0,0,0,0.2);
                border-color: {COLOR_TEXT_LIGHT}; /* Borda branca no hover para contraste máximo */
            }}

            /* --- 4. Tags (Etiquetas "Pill" Aprimoradas) --- */
            .tag-wrapper {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 15px 0px;
            }}
            .tag {{
                background-color: {COLOR_PRIMARY}; /* Fundo mais escuro para a tag */
                color: {COLOR_TEXT_LIGHT};        /* Texto branco na tag */
                padding: 7px 16px;
                border-radius: 25px; /* Formato de pílula */
                font-size: 13px;
                font-weight: 600;
                border: 1px solid {COLOR_SECONDARY}; /* Borda sutil */
            }}
            /* Variação de tag para status "Ativo" */
            .tag.status-ativo {{
                background-color: #4CAF50; /* Verde vibrante */
                border-color: #66BB6A;
                color: {COLOR_TEXT_LIGHT};
            }}
            /* Variação de tag para status "Inativo" ou "Manutenção" */
            .tag.status-inativo {{
                background-color: #F44336; /* Vermelho vibrante */
                border-color: #EF5350;
                color: {COLOR_TEXT_LIGHT};
            }}

            /* --- 5. Botões e Popover --- */
            .stButton, .stLinkButton {{
                margin-top: auto; /* Alinha no rodapé do card */
            }}
            /* Botão Primário (Acessar) */
            [data-testid="stButton"] button:not(:disabled), [data-testid="stLinkButton"] a {{
                background-color: {COLOR_SECONDARY}; /* Cor secundária de destaque */
                color: {COLOR_PRIMARY};             /* Texto azul escuro */
                border: none; /* Sem borda para um look mais clean */
                font-weight: 700;
                letter-spacing: 0.5px;
                padding: 12px 20px;
                border-radius: 8px; /* Cantos levemente arredondados */
                transition: all 0.2s ease;
            }}
            /* Hover do Botão Primário */
            [data-testid="stButton"] button:not(:disabled):hover, [data-testid="stLinkButton"] a:hover {{
                background-color: {COLOR_TEXT_LIGHT}; /* Fundo branco no hover */
                color: {COLOR_PRIMARY};             /* Texto azul escuro */
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }}
            /* Botão Desabilitado (Link Indisponível) */
            [data-testid="stButton"] button:disabled {{
                background-color: {COLOR_PRIMARY};
                border-color: {COLOR_PRIMARY};
                color: {COLOR_TEXT_MUTED};
                opacity: 0.6; /* Transparência para desabilitado */
            }}
            
            /* Popover (Detalhes) - volta a ser branco para contraste */
            [data-testid="stPopover"] {{
                background-color: {COLOR_TEXT_LIGHT};
                color: {COLOR_PRIMARY};
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}
            /* Texto dentro do Popover */
            [data-testid="stPopover"] .stMarkdown {{
                color: {COLOR_PRIMARY};
            }}
            
            /* --- 6. Elementos Decorativos (Inspirado no Menu) --- */
            /* Linha decorativa horizontal */
            hr {{
                border-top: 1px dashed {COLOR_SECONDARY};
                opacity: 0.4;
                margin: 2rem 0;
            }}
            /* Título do filtro na sidebar */
            [data-testid="stSidebar"] h2 {{
                color: {COLOR_TEXT_LIGHT};
                margin-bottom: 25px;
            }}
            
            /* Ajusta a cor do placeholder de busca */
            [data-testid="stTextInput"] input::placeholder {{
                color: {COLOR_TEXT_MUTED};
            }}
            /* Cor do texto digitado na busca */
            [data-testid="stTextInput"] input {{
                color: {COLOR_PRIMARY};
            }}
            /* Cor de fundo da busca */
            [data-testid="stTextInput"] > div > div > input {{
                background-color: {COLOR_TEXT_LIGHT};
            }}
        </style>
    """, unsafe_allow_html=True)

# Executa a injeção do CSS
load_custom_css()


# --- Carregamento de Dados ---
# Busca a URL da planilha dos 'Secrets' do Streamlit.
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
st.write("Explore nossa coleção de dashboards estratégicos. Utilize a busca e os filtros laterais para encontrar insights relevantes.")
st.write("") # Espaço vertical

# --- Lógica Principal (Busca, Filtros e Grid) ---
if not df.empty:
    
    # --- 1. BARRA DE BUSCA ---
    # Componente de entrada de texto para a busca em tempo real.
    search_term = st.text_input(
        "Buscar por nome ou descrição:", 
        placeholder="Digite termos-chave (ex: Vendas, Marketing, Logística)..."
    )
    
    # --- 2. BARRA LATERAL DE FILTROS ---
    st.sidebar.header("Filtros de Portfólio")
    
    # Função auxiliar para gerar listas de opções para os filtros
    def criar_lista_filtro(coluna):
        # Remove valores nulos ('N/A') e duplicados, depois ordena
        opcoes = df[coluna].replace('N/A', pd.NA).dropna().unique()
        return ["Todos"] + sorted(list(opcoes))

    # Cria os seletores (selectbox) na barra lateral
    try:
        filtro_responsavel = st.sidebar.selectbox("Responsável:", criar_lista_filtro('Responsável'))
        filtro_publico = st.sidebar.selectbox("Público-alvo:", criar_lista_filtro('Público'))
        filtro_midia = st.sidebar.selectbox("Plataforma BI:", criar_lista_filtro('Mídia'))
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
    st.write(f"### {len(df_filtrado)} Dashboards Encontrados:")
    st.divider() # Linha decorativa

    NUM_COLUNAS = 3 # Define o número de colunas para o layout em grade
    reports_list = df_filtrado.to_dict('records') # Converte o dataframe para uma lista de dicionários

    if not reports_list:
        st.info("Nenhum dashboard corresponde aos critérios de busca ou filtros aplicados.")

    # Itera sobre a lista de reports, agrupando-os em "fatias" (chunks)
    for i in range(0, len(reports_list), NUM_COLUNAS):
        cols = st.columns(NUM_COLUNAS) # Cria as colunas para a linha atual do grid
        chunk = reports_list[i : i + NUM_COLUNAS]

        # Preenche cada coluna com um card de dashboard
        for j, report_data in enumerate(chunk):
            with cols[j]:
                # O container com 'border=True' é o seletor principal do nosso CSS para o card
                with st.container(border=True):
                    
                    # Título do Card
                    st.markdown(f"<h2>{report_data.get('Report', 'Sem Título')}</h2>", unsafe_allow_html=True)
                    
                    # Descrição do Dashboard (truncada para manter o layout limpo)
                    descricao = report_data.get('Descrição', 'N/A')
                    st.write(descricao[:120] + ("..." if len(descricao) > 120 else ""))
                    
                    # --- Tags de HTML Customizadas ---
                    # Aplica classes CSS dinamicamente com base no status
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
                        <span class="tag {status_class}">📊 {report_data.get('Status', 'N/A')}</span>
                    </div>
                    """
                    st.markdown(tags_html, unsafe_allow_html=True)

                    # --- Popover (Detalhes Adicionais) ---
                    # Exibe informações detalhadas ao clicar, mantendo o card principal conciso.
                    with st.popover("Ver mais detalhes"):
                        st.markdown(f"**Responsável:** {report_data.get('Responsável', 'N/A')}")
                        st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                        st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                        st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")

                    # --- Botão de Ação ---
                    # 'key' é crucial para garantir IDs únicos para cada botão no loop
                    key_base = f"{i}_{j}" 
                    link = report_data.get('Link')
                    
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
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")