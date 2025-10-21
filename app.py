import streamlit as st
import pandas as pd
import re

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="✨",
    layout="wide"
)

# --- Cores da Paleta ---
COLOR_PRIMARY = "#0d2e5b"      # Azul Escuro (Títulos, Botões)
COLOR_SECONDARY = "#5b92c8"     # Azul Claro (Hover, Tags)
COLOR_BACKGROUND_DARK = "#0d2e5b" # Fundo (Início do Degradê)
COLOR_BACKGROUND_LIGHT = "#1d4a7c" # Fundo (Fim do Degradê)
COLOR_CARD = "#FFFFFF"         # Card (Branco)
COLOR_TEXT_DARK = "#0d2e5b"     # Texto no Card (Azul Escuro)
COLOR_TEXT_NORMAL = "#333333"   # Texto de Descrição
COLOR_TEXT_LIGHT = "#FFFFFF"    # Texto no Fundo Escuro (Títulos)

# --- CSS Customizado (A transformação do design) ---
def load_custom_css():
    # SVG do padrão Zig-Zag da sua referência, codificado para CSS
    zigzag_svg = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "width='100' height='20' viewBox='0 0 100 20'%3E%3Cpath "
        f"d='M0 10 L10 0 L20 10 L30 0 L40 10 L50 0 L60 10 L70 0 L80 10 L90 0 L100 10' "
        f"fill='none' stroke='{COLOR_SECONDARY}' stroke-width='2' opacity='0.2'/%3E%3C/svg%3E"
    )

    st.markdown(f"""
        <style>
            /* --- 1. Fundo e Layout Principal --- */
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(170deg, {COLOR_BACKGROUND_DARK} 0%, {COLOR_BACKGROUND_LIGHT} 100%);
            }}
            
            /* --- 2. Tipografia Principal --- */
            h1, h2 {{
                color: {COLOR_TEXT_LIGHT};
                font-weight: 700;
            }}
            /* Título da Seção (ex: "Diretoria") */
            h3 {{
                color: {COLOR_TEXT_LIGHT};
                font-weight: 600;
                border-bottom: 2px solid {COLOR_SECONDARY};
                padding-bottom: 10px;
                margin-top: 40px;
            }}

            /* --- 3. Barra Lateral (Com Padrão Zig-Zag) --- */
            [data-testid="stSidebar"] {{
                background-color: {COLOR_PRIMARY};
                background-image: url("{zigzag_svg}");
                background-repeat: repeat-x;
                background-position: top;
                padding-top: 50px; /* Espaço para o padrão aparecer */
            }}
            /* Texto e labels na sidebar */
            [data-testid="stSidebar"] h2, [data-testid="stSidebar"] .st-bd {{
                color: {COLOR_TEXT_LIGHT};
            }}

            /* --- 4. O Layout de Scroll Horizontal --- */
            .horizontal-scroll-container {{
                display: flex;
                overflow-x: auto; /* A mágica do scroll */
                padding: 20px 5px;
                gap: 25px; /* Espaço entre os cards */
                /* Remove a barra de scroll feia */
                scrollbar-width: thin;
                scrollbar-color: {COLOR_SECONDARY} {COLOR_PRIMARY};
            }}
            .horizontal-scroll-container::-webkit-scrollbar {{
                height: 8px;
            }}
            .horizontal-scroll-container::-webkit-scrollbar-track {{
                background: {COLOR_PRIMARY};
                border-radius: 4px;
            }}
            .horizontal-scroll-container::-webkit-scrollbar-thumb {{
                background-color: {COLOR_SECONDARY};
                border-radius: 4px;
            }}

            /* --- 5. O Card (Design "Premium" Branco) --- */
            /* O seletor [data-testid="stVerticalBlockBorderWrapper"] é o container do card */
            .horizontal-scroll-container [data-testid="stVerticalBlockBorderWrapper"] > div {{
                background-color: {COLOR_CARD};
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                transition: all 0.3s ease-out;
                
                /* Define o tamanho do card no scroll */
                flex: 0 0 360px; /* Não cresce, não encolhe, base de 360px */
                min-height: 380px; 
                
                display: flex;
                flex-direction: column;
                padding: 24px;
            }}
            .horizontal-scroll-container [data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                border-color: {COLOR_SECONDARY};
            }}

            /* --- 6. Conteúdo do Card (Títulos, Tags, Botões) --- */
            /* Título do Card */
            .horizontal-scroll-container h2 {{
                color: {COLOR_TEXT_DARK};
                font-weight: 700;
                font-size: 1.75rem;
                margin-bottom: 10px;
            }}
            /* Descrição do Card */
            .horizontal-scroll-container p {{
                color: {COLOR_TEXT_NORMAL};
                font-size: 15px;
            }}
            
            /* Tags (Etiquetas) */
            .tag-wrapper {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin: 12px 0px;
            }}
            .tag {{
                background-color: {COLOR_SECONDARY};
                color: {COLOR_TEXT_LIGHT};
                padding: 5px 14px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
            }}
            .tag.status-ativo {{
                background-color: #28a745; /* Verde para "Ativo" */
                color: {COLOR_TEXT_LIGHT};
            }}
            .tag.status-inativo {{
                background-color: #dc3545; /* Vermelho para "Inativo" */
                color: {COLOR_TEXT_LIGHT};
            }}
            
            /* Botões */
            .stButton, .stLinkButton {{
                margin-top: auto; /* Alinha no rodapé */
            }}
            /* Botão Primário (Acessar) */
            [data-testid="stButton"] button:not(:disabled), [data-testid="stLinkButton"] a {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_TEXT_LIGHT};
                font-weight: 600;
                border: none;
                transition: all 0.2s ease;
            }}
            [data-testid="stButton"] button:not(:disabled):hover, [data-testid="stLinkButton"] a:hover {{
                background-color: {COLOR_SECONDARY};
                color: {COLOR_PRIMARY};
            }}
            /* Botão Desabilitado */
            [data-testid="stButton"] button:disabled {{
                background-color: #EAEAEA;
                color: #AAAAAA;
                border: none;
            }}
            
            /* Popover (Detalhes) */
            [data-testid="stPopover"] {{
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            /* Texto dentro do Popover */
            [data-testid="stPopover"] .stMarkdown, [data-testid="stPopover"] p {{
                color: {COLOR_PRIMARY};
            }}

        </style>
    """, unsafe_allow_html=True)

# Executa a injeção do CSS
load_custom_css()

# --- Carregamento de Dados ---
# (Mesma lógica segura de antes)
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.stop()

@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_essenciais = ['Report', 'Descrição', 'Link', 'Status', 'Responsável', 'Público', 'Mídia', 'Periodicidade', 'Horário', 'Divulgação']
        for col in colunas_essenciais:
            if col not in df.columns:
                df[col] = pd.NA
        df = df.astype(str)
        df.replace(['nan', '<NA>', 'NaN'], 'N/A', inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Título Principal ---
st.title("✨ Portfólio de Dashboards de BI")
st.write("Explore nossa coleção de dashboards estratégicos. Utilize a busca e os filtros laterais para encontrar insights relevantes.")
st.write("")

# --- Lógica Principal (Busca, Filtros e Grid) ---
if not df.empty:
    
    # --- 1. BARRA DE BUSCA ---
    search_term = st.text_input(
        "Buscar por nome ou descrição:", 
        placeholder="Digite termos-chave (ex: Vendas, Marketing, Logística)..."
    )
    
    # --- 2. BARRA LATERAL DE FILTROS ---
    st.sidebar.header("Filtros de Portfólio")
    
    def criar_lista_filtro(coluna):
        opcoes = df[coluna].replace('N/A', pd.NA).dropna().unique()
        return ["Todos"] + sorted(list(opcoes))

    try:
        filtro_responsavel = st.sidebar.selectbox("Responsável:", criar_lista_filtro('Responsável'))
        filtro_publico = st.sidebar.selectbox("Público-alvo:", criar_lista_filtro('Público'))
        filtro_midia = st.sidebar.selectbox("Plataforma BI:", criar_lista_filtro('Mídia'))
        filtro_status = st.sidebar.selectbox("Status:", criar_lista_filtro('Status'))
    except KeyError as e:
        st.sidebar.error(f"Erro: Coluna '{e.args[0]}' não encontrada.")
        filtro_responsavel = filtro_publico = filtro_midia = filtro_status = "Todos"
    
    # --- 3. LÓGICA DE FILTRAGEM ---
    df_filtrado = df

    if search_term:
        search_regex = re.escape(search_term)
        df_filtrado = df_filtrado[
            df_filtrado['Report'].str.contains(search_regex, case=False, na=False) |
            df_filtrado['Descrição'].str.contains(search_regex, case=False, na=False)
        ]

    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Mídia'] == filtro_midia]
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    
    # --- 4. LÓGICA DE EXIBIÇÃO SECCIONADA ---
    # Pega os grupos únicos do filtro (ou da busca)
    # Se 'Público' foi filtrado, usa só ele. Senão, usa todos.
    if filtro_publico != "Todos":
        grupos_publico = [filtro_publico]
    else:
        grupos_publico = df_filtrado['Público'].replace('N/A', pd.NA).dropna().unique()
        grupos_publico = sorted(list(grupos_publico))

    if len(df_filtrado) == 0:
        st.info("Nenhum dashboard corresponde aos critérios de busca ou filtros aplicados.")

    # Itera sobre cada grupo de "Público"
    for publico in grupos_publico:
        st.markdown(f"### {publico}") # Título da Seção
        reports_do_grupo = df_filtrado[df_filtrado['Público'] == publico]
        
        # Abre o container de scroll horizontal
        st.markdown('<div class="horizontal-scroll-container">', unsafe_allow_html=True)
        
        # Itera sobre os dashboards DESSE GRUPO
        for index, report_data in reports_do_grupo.iterrows():
            # 'border=True' é o seletor para o nosso CSS
            with st.container(border=True):
                
                # Título do Card (st.subheader -> h2)
                st.subheader(report_data.get('Report', 'Sem Título'))
                
                # Descrição
                descricao = report_data.get('Descrição', 'N/A')
                st.write(descricao[:110] + ("..." if len(descricao) > 110 else ""))
                
                # --- Tags de HTML Customizadas ---
                status_val = report_data.get('Status', 'N/A').lower()
                status_class = ''
                if status_val == 'ativo':
                    status_class = 'status-ativo'
                elif status_val == 'inativo' or status_val == 'manutenção':
                    status_class = 'status-inativo'
                
                # Usamos Mídia e Status como tags principais
                tags_html = f"""
                <div class="tag-wrapper">
                    <span class="tag">🔧 {report_data.get('Mídia', 'N/A')}</span>
                    <span class="tag {status_class}"> {report_data.get('Status', 'N/A')}</span>
                </div>
                """
                st.markdown(tags_html, unsafe_allow_html=True)

                # --- Popover (Detalhes Adicionais) ---
                with st.popover("Ver mais detalhes"):
                    st.markdown(f"**Responsável:** {report_data.get('Responsável', 'N/A')}")
                    st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                    st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                    st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")

                # --- Botão de Ação ---
                key_base = f"{publico}_{index}" # Chave única para este card
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
        
        # Fecha o container de scroll horizontal
        st.markdown('</div>', unsafe_allow_html=True)
        # st.divider() # Opcional: linha entre as seções

else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")