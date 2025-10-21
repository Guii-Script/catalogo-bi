import streamlit as st
import pandas as pd
import re

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="🎨", # Mudando o ícone para refletir o foco no design
    layout="wide",
    initial_sidebar_state="collapsed" # Menu retrátil
)

# --- Paleta de Cores (Ajustada para a nova referência) ---
COLOR_ACCENT_BLUE_DARK = "#0d2e5b"      # Azul escuro principal (texto, botões)
COLOR_ACCENT_BLUE_LIGHT = "#5b92c8"     # Azul claro de destaque (tags, detalhes)
COLOR_BACKGROUND_MAIN = "#F8F8F8"       # Fundo principal (branco/muito claro)
COLOR_BACKGROUND_ALT = "#EFEFEF"        # Fundo secundário (para seções, etc.)
COLOR_TEXT_MAIN_DARK = "#2C3E50"        # Texto principal escuro (leitura)
COLOR_TEXT_LIGHT = "#FFFFFF"            # Texto branco (sobre fundos escuros)

# SVG de pincelada azul (inspirado na sua referência) para o topo/rodapé e títulos
# Usamos o COLOR_ACCENT_BLUE_DARK para a pincelada
brush_stroke_svg_dark = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 100'%3E"
    f"%3Cpath fill='{COLOR_ACCENT_BLUE_DARK}' d='M0,0C0,0,166.667,100,333.333,100C500,100,666.667,0,1000,0L1000,100L0,100L0,0Z'%3E%3C/path%3E%3C/svg%3E"
)
brush_stroke_svg_light = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 100'%3E"
    f"%3Cpath fill='{COLOR_ACCENT_BLUE_LIGHT}' d='M0,0C0,0,166.667,100,333.333,100C500,100,666.667,0,1000,0L1000,100L0,100L0,0Z'%3E%3C/path%3E%3C/svg%3E"
)

def load_custom_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

        /* === FUNDO GERAL (AGORA CLARO COM DETALHES AZUIS) === */
        [data-testid="stAppViewContainer"] {{
            background-color: {COLOR_BACKGROUND_MAIN}; /* Fundo principal claro */
            color: {COLOR_TEXT_MAIN_DARK};
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            position: relative;
        }}

        /* Detalhe de pincelada no topo do main content */
        [data-testid="stMain"]::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 120px; /* Altura da "pincelada" */
            background: url("{brush_stroke_svg_dark}") no-repeat center top;
            background-size: cover;
            z-index: 1; /* Abaixo do conteúdo principal */
        }}
        /* Detalhe de pincelada no rodapé */
        [data-testid="stMain"]::after {{
            content: "";
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 100px; /* Altura da "pincelada" */
            background: url("{brush_stroke_svg_light}") no-repeat center bottom;
            background-size: cover;
            transform: rotate(180deg); /* Inverte para parecer do outro lado */
            z-index: 1;
        }}

        /* === TÍTULOS GERAIS === */
        h1 {{
            text-align: center;
            font-family: 'Playfair Display', serif; /* Fonte mais elegante para o título */
            font-weight: 700;
            font-size: 3.5rem; /* Título maior */
            color: {COLOR_ACCENT_BLUE_DARK};
            margin-bottom: 0.5rem;
            letter-spacing: 2px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            animation: fadeDown 1.2s ease-out;
            position: relative;
            z-index: 5;
            padding-top: 50px; /* Espaço para a pincelada de fundo */
        }}
        @keyframes fadeDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Descrição abaixo do título principal */
        [data-testid="stMarkdown"] > p:first-of-type {{
            color: {COLOR_TEXT_MAIN_DARK} !important;
            text-align: center;
            font-size: 1.1rem;
            max-width: 800px;
            margin: -10px auto 40px auto; /* Ajusta espaçamento */
            position: relative;
            z-index: 5;
        }}
        
        /* === TÍTULOS DE SEÇÃO (INSPIRADO EM "PIZZA"/"BURGER") === */
        h3 {{
            color: {COLOR_ACCENT_BLUE_DARK};
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-size: 2.2rem;
            margin-top: 50px;
            margin-bottom: 25px;
            position: relative;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            text-align: center; /* Centraliza o título */
            z-index: 5;
        }}
        /* Pseudo-elemento para a "pincelada" azul por trás do título da seção */
        h3::before {{
            content: "";
            position: absolute;
            bottom: -5px; left: 50%; /* Centraliza */
            transform: translateX(-50%);
            width: 150px; /* Largura da pincelada */
            height: 10px; /* Altura da pincelada */
            background-color: {COLOR_ACCENT_BLUE_LIGHT};
            border-radius: 5px;
            opacity: 0.7;
            z-index: -1;
        }}


        /* === BARRA LATERAL (AZUL ESCURO) === */
        [data-testid="stSidebar"] {{
            background: {COLOR_ACCENT_BLUE_DARK}; /* Fundo azul escuro */
            backdrop-filter: blur(12px);
            border-right: none; /* Remove a borda direita */
            box-shadow: 2px 0 15px rgba(0,0,0,0.2);
            z-index: 10;
        }}
        [data-testid="stSidebar"] h2 {{
            color: {COLOR_TEXT_LIGHT};
            font-weight: 700;
            margin-bottom: 25px;
        }}
        [data-testid="stSidebar"] .stSelectbox label, 
        [data-testid="stSidebar"] .stTextInput label {{
            font-weight: 600;
            color: {COLOR_TEXT_LIGHT};
            margin-bottom: 8px;
        }}
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background-color: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: {COLOR_TEXT_LIGHT};
        }}
        [data-testid="stSidebar"] .stSelectbox .st-bh, /* Ícone da seta */
        [data-testid="stSidebar"] .stSelectbox .st-bl, /* Texto selecionado */
        [data-testid="stSidebar"] .stSelectbox .st-bq {{ /* Placeholder */
            color: {COLOR_TEXT_LIGHT} !important;
        }}
        [data-testid="stSidebar"] .stTextInput input {{
             background-color: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: {COLOR_TEXT_LIGHT};
        }}
        [data-testid="stSidebar"] .stTextInput input::placeholder {{
             color: rgba(255,255,255,0.7);
        }}
        /* Info box na sidebar */
        [data-testid="stSidebar"] .stAlert {{
            background-color: rgba(91,146,200,0.2);
            border-left: 5px solid {COLOR_ACCENT_BLUE_LIGHT};
            color: {COLOR_TEXT_LIGHT};
        }}


        /* === BARRA DE BUSCA PRINCIPAL === */
        /* Buscador principal fora da sidebar */
        [data-testid="stTextInput"] label {{
            color: {COLOR_TEXT_MAIN_DARK} !important;
            font-weight: 600;
            font-size: 1.1rem;
            margin-left: 5px;
        }}
        [data-testid="stTextInput"] input {{
            background-color: {COLOR_WHITE};
            border: 1px solid #DDDDDD;
            color: {COLOR_TEXT_MAIN_DARK};
            border-radius: 10px;
            padding: 0.7rem 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            z-index: 5;
        }}
        [data-testid="stTextInput"] input:focus {{
            outline: none;
            border-color: {COLOR_ACCENT_BLUE_LIGHT};
            box-shadow: 0 0 15px rgba(91,146,200,0.3);
        }}
        [data-testid="stTextInput"] input::placeholder {{
            color: #888;
        }}

        /* === GRID DOS CARDS === */
        /* Espaçamento das colunas (para o st.columns) */
        .st-emotion-l9bjgi {{ /* Este seletor pode mudar entre versões do Streamlit */
            gap: 30px; /* Espaço maior entre os cards */
        }}
        
        /* === CARDS (BRANCOS, LIMPOS, CONTRASTE) === */
        [data-testid="stVerticalBlockBorderWrapper"] > div {{
            background: {COLOR_WHITE};
            border-radius: 16px;
            padding: 24px;
            min-height: 380px; /* Mantém um bom tamanho */
            display: flex;
            flex-direction: column;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); /* Sombra mais suave */
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            z-index: 5; /* Acima do fundo e detalhes */
            animation: fadeUp 0.8s ease forwards;
            border: 1px solid #EAEAEA; /* Borda sutil */
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            border-color: {COLOR_ACCENT_BLUE_LIGHT};
        }}

        /* === CONTEÚDO DO CARD === */
        [data-testid="stVerticalBlockBorderWrapper"] h2 {{
            color: {COLOR_ACCENT_BLUE_DARK} !important; /* Título do card azul escuro */
            font-weight: 700;
            font-size: 1.6rem;
            margin-bottom: 10px;
            line-height: 1.2;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] p {{
            color: {COLOR_TEXT_MAIN_DARK} !important; /* Descrição do card escuro */
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 15px;
        }}

        /* === TAGS === */
        .tag-wrapper {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }}
        .tag {{
            background: {COLOR_ACCENT_BLUE_LIGHT}; /* Fundo da tag azul claro */
            color: {COLOR_TEXT_LIGHT};
            padding: 6px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .tag.status-ativo {{
            background-color: #28a745;
        }}
        .tag.status-inativo {{
            background-color: #dc3545;
        }}

        /* === RODAPÉ DO CARD === */
        .card-bottom {{
            margin-top: auto;
            padding-top: 20px;
        }}

        /* === BOTÕES === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: {COLOR_ACCENT_BLUE_DARK}; /* Botão azul escuro */
            color: {COLOR_TEXT_LIGHT};
            border: none;
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 12px 20px;
            text-decoration: none; /* Remove sublinhado do link_button */
        }}
        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            background: {COLOR_ACCENT_BLUE_LIGHT}; /* Hover azul claro */
            color: {COLOR_ACCENT_BLUE_DARK};
            box-shadow: 0 6px 16px rgba(91,146,200,0.4);
            transform: translateY(-3px);
        }}
        [data-testid="stButton"] button:disabled {{
            background-color: #E0E0E0;
            color: #A0A0A0;
            box-shadow: none;
            transform: none;
        }}

        /* === POPOVER === */
        [data-testid="stPopover"] {{
            border-radius: 12px;
            background: {COLOR_WHITE};
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            padding: 15px;
        }}
        [data-testid="stPopover"] p, [data-testid="stPopover"] span, [data-testid="stPopover"] li {{
            color: {COLOR_TEXT_MAIN_DARK} !important;
            font-size: 0.95rem;
            line-height: 1.4;
        }}
        [data-testid="stPopover"] strong {{
            color: {COLOR_ACCENT_BLUE_DARK};
        }}


        /* === ANIMAÇÕES === */
        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div {{
            animation: fadeUp 0.8s ease forwards;
        }}

        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# --- Carregamento de Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado.")
    st.stop()

@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas = ['Report','Descrição','Link','Status','Responsável','Público','Mídia','Periodicidade','Horário','Divulgação']
        for c in colunas:
            if c not in df.columns: df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Cabeçalho com efeito ---
# O padding-top no H1 dentro do CSS já cria o espaço
st.title("✨ Portfólio de Dashboards de BI")
st.markdown(
    "<p>Explore os principais dashboards e análises desenvolvidos pelo nosso time de BI. Utilize a busca e filtros para navegar pelos projetos.</p>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

# --- Busca e Filtros ---
if not df.empty:
    search_term = st.text_input("🔍 Buscar dashboards:", placeholder="Digite palavras-chave...")

    st.sidebar.header("Filtros")
    def lista(col):
        return ["Todos"] + sorted(df[col].replace('N/A', pd.NA).dropna().unique().tolist())

    filtro_responsavel = st.sidebar.selectbox("Responsável:", lista("Responsável"))
    filtro_publico = st.sidebar.selectbox("Público-alvo:", lista("Público"))
    filtro_midia = st.sidebar.selectbox("Plataforma BI:", lista("Mídia"))
    filtro_status = st.sidebar.selectbox("Status:", lista("Status"))

    df_filtrado = df.copy()
    if search_term:
        df_filtrado = df_filtrado[
            df_filtrado["Report"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descrição"].str.contains(search_term, case=False, na=False)
        ]
    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Responsável"] == filtro_responsavel]
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Público"] == filtro_publico]
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Mídia"] == filtro_midia]
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Status"] == filtro_status]

    if len(df_filtrado) == 0:
        st.info("Nenhum dashboard encontrado com os critérios selecionados.")
    else:
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Público"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            st.markdown(f"### {g}") # Título da Seção (ex: "Diretoria")
            subset = df_filtrado[df_filtrado["Público"] == g]
            
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3 
            
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        with st.container(border=True): 
                            key = f"{g}_{i}_{j}"
                            
                            st.subheader(row["Report"])
                            st.write(row["Descrição"][:120] + ("..." if len(row["Descrição"]) > 120 else ""))

                            status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"
                            st.markdown(
                                f"""
                                <div class="tag-wrapper">
                                    <span class="tag">📊 {row['Mídia']}</span>
                                    <span class="tag {status_class}"> {row['Status']}</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            
                            st.markdown('<div class="card-bottom">', unsafe_allow_html=True)
                            with st.popover("📋 Ver detalhes"):
                                st.write(f"**Responsável:** {row['Responsável']}")
                                st.write(f"**Periodicidade:** {row['Periodicidade']}")
                                st.write(f"**Horário:** {row['Horário']}")
                                st.write(f"**Divulgação:** {row['Divulgação']}")

                            if row["Link"] and row["Link"].lower() != "n/a":
                                st.link_button("🚀 Acessar Dashboard", row["Link"], use_container_width=True, key=f"link_{key}")
                            else:
                                st.button("Indisponível", use_container_width=True, disabled=True, key=f"btn_{key}")
                            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)

else:
    st.warning("Erro ao carregar dados. Verifique a planilha ou os Secrets.")

st.sidebar.info("Os dados são atualizados automaticamente a cada 10 minutos.")