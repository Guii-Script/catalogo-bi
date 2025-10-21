import streamlit as st
import pandas as pd
import re

# --- Configuração da Página ---
# Menu retrátil (collapsed) e layout "wide"
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed" # Menu começa fechado
)

# --- Paleta de Cores ---
COLOR_PRIMARY = "#0d2e5b"
COLOR_SECONDARY = "#5b92c8"
COLOR_WHITE = "#FFFFFF"
COLOR_TEXT_DARK = "#0d2e5b"
COLOR_TEXT_LIGHT = "#FFFFFF"

# --- CSS Moderno e Animado ---
def load_custom_css():
    st.markdown(f"""
        <style>

        /* === FUNDO GERAL === */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(160deg, {COLOR_PRIMARY} 0%, {COLOR_SECONDARY} 100%);
            color: {COLOR_TEXT_LIGHT};
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            position: relative;
        }}

        /* === ANIMAÇÃO DE BRILHO SUAVE NO FUNDO === */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle at 25% 25%, rgba(255,255,255,0.07) 0%, transparent 40%),
                        radial-gradient(circle at 75% 75%, rgba(255,255,255,0.07) 0%, transparent 40%);
            animation: floatGlow 12s ease-in-out infinite alternate;
            z-index: 0;
        }}
        @keyframes floatGlow {{
            from {{ transform: scale(1) translate(0,0); }}
            to {{ transform: scale(1.1) translate(3%,3%); }}
        }}

        /* === TÍTULOS (Fora dos cards) === */
        h1 {{
            text-align: center;
            font-weight: 800;
            font-size: 2.8rem;
            color: {COLOR_WHITE};
            margin-bottom: 0.5rem;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(255,255,255,0.2);
            animation: fadeDown 1.2s ease-out;
            z-index: 2; /* Garante que fique acima da animação de fundo */
        }}
        @keyframes fadeDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Título da Seção (ex: "Diretoria") */
        h3 {{
            color: {COLOR_WHITE};
            border-bottom: 2px solid {COLOR_SECONDARY};
            padding-bottom: 6px;
            margin-top: 40px;
            font-weight: 600;
            letter-spacing: 0.5px;
            z-index: 2;
        }}

        /* === TEXTO DESCRITIVO (Fora dos cards) === */
        /* Seletor mais específico para não afetar o texto dos cards */
        [data-testid="stAppViewContainer"] > .main .block-container > div:first-child > div > div > p {{
             color: {COLOR_WHITE} !important;
             text-align: center;
             font-size: 18px;
             max-width: 700px;
             margin: auto;
        }}
        [data-testid="stAppViewContainer"] > .main .block-container > div:first-child > div > div > label {{
             color: {COLOR_WHITE} !important;
        }}


        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background: rgba(13, 46, 91, 0.9);
            backdrop-filter: blur(12px);
            border-right: 2px solid rgba(255,255,255,0.1);
        }}
        [data-testid="stSidebar"] h2 {{
            color: {COLOR_WHITE};
        }}
        [data-testid="stSidebar"] .stSelectbox label {{
            font-weight: 600;
            color: {COLOR_WHITE};
        }}

        /* === BARRA DE BUSCA === */
        input[type="text"] {{
            background-color: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            color: {COLOR_WHITE};
            border-radius: 10px;
            padding: 0.6rem;
            transition: all 0.3s ease;
            z-index: 2;
        }}
        input[type="text"]:focus {{
            outline: none;
            border-color: {COLOR_SECONDARY};
            box-shadow: 0 0 10px {COLOR_SECONDARY};
        }}

        /* === CARDS (O CONSERTO) === */
        /* Alvo: O container do card (st.container(border=True)) */
        [data-testid="stVerticalBlockBorderWrapper"] > div {{
            background: {COLOR_WHITE};
            border-radius: 16px;
            padding: 24px;
            min-height: 380px;  /* Altura menor para cards mais compactos */
            display: flex;
            flex-direction: column;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            z-index: 1; /* Garante que o card fique acima da animação de fundo */
            animation: fadeUp 0.8s ease forwards;
        }}

        /* Contêiner para o rodapé do card (alinha os botões) */
        .card-bottom {{
            margin-top: auto;   /* Empurra para o rodapé */
            padding-top: 15px;
        }}

        /* === EFEITO DE ILUMINAÇÃO AO PASSAR O MOUSE === */
        [data-testid="stVerticalBlockBorderWrapper"] > div::before {{
            content: "";
            position: absolute;
            top: -100%; left: -100%;
            width: 300%; height: 300%;
            background: radial-gradient(circle, rgba(91,146,200,0.15) 0%, transparent 60%);
            opacity: 0;
            transition: opacity 0.6s ease;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div:hover::before {{
            opacity: 1;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] > div:hover {{
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }}

        /* === TÍTULO DO CARD (CORRIGIDO) === */
        [data-testid="stVerticalBlockBorderWrapper"] h2 {{
            color: {COLOR_PRIMARY} !important; /* Cor escura para contraste */
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 8px;
        }}

        /* === DESCRIÇÃO DO CARD (CORRIGIDO) === */
        [data-testid="stVerticalBlockBorderWrapper"] p {{
            color: #333 !important; /* Cor escura para contraste */
            font-size: 15px;
            margin-bottom: 12px;
        }}

        /* === TAGS === */
        .tag-wrapper {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 12px 0;
        }}
        .tag {{
            background: {COLOR_SECONDARY};
            color: {COLOR_WHITE};
            padding: 5px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
            box-shadow: 0 0 8px rgba(91,146,200,0.4);
        }}
        .tag.status-ativo {{
            background-color: #28a745;
        }}
        .tag.status-inativo {{
            background-color: #dc3545;
        }}

        /* === BOTÕES === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: {COLOR_PRIMARY};
            color: {COLOR_WHITE};
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 3px 8px rgba(0,0,0,0.2);
        }}
        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            background: {COLOR_SECONDARY};
            color: {COLOR_PRIMARY};
            box-shadow: 0 5px 14px rgba(91,146,200,0.5);
            transform: translateY(-2px);
        }}
        /* Botão desabilitado */
        [data-testid="stButton"] button:disabled {{
            background-color: #EAEAEA;
            color: #AAAAAA;
            border: none;
        }}

        /* === POPOVER === */
        [data-testid="stPopover"] {{
            border-radius: 10px;
            background: #f8f9fa;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }}
        /* Texto dentro do popover (CORRIGIDO) */
        [data-testid="stPopover"] p, [data-testid="stPopover"] span, [data-testid="stPopover"] li {{
            color: #333 !important;
        }}

        /* === ANIMAÇÃO DE ENTRADA DOS CARDS === */
        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        /* (Removido o seletor de .horizontal-scroll-container) */
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
        df.fillna("N/A", inplace=True) # Preenche NAs
        return df.astype(str) # Converte tudo para string
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Cabeçalho com efeito ---
st.markdown("<br>", unsafe_allow_html=True)
st.title("✨ Portfólio de Dashboards de BI")
st.markdown(
    "<p>Explore os principais dashboards e análises desenvolvidos pelo nosso time de BI. Utilize a busca e filtros para navegar pelos projetos.</p>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# --- Busca e Filtros ---
if not df.empty:
    search_term = st.text_input("🔍 Buscar dashboards:", placeholder="Digite palavras-chave...")

    st.sidebar.header("Filtros")
    def lista(col):
        # .replace() é mais seguro em dados já como string
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
        # Lógica de agrupamento mantida
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Público"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            st.markdown(f"### {g}") # Título da Seção (ex: "Diretoria")
            subset = df_filtrado[df_filtrado["Público"] == g]
            
            # --- MUDANÇA AQUI: Implementação do Grid Vertical ---
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3 # 3 colunas por linha
            
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                # Pega a "fatia" de relatórios para esta linha
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        # 'border=True' é o seletor para o nosso card branco
                        with st.container(border=True): 
                            
                            # ID único para este card, baseado no grupo e índice
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
                            
                            # --- Bloco do rodapé do card ---
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
            
            # Adiciona um espaço extra entre as seções
            st.markdown("<br><br>", unsafe_allow_html=True)

else:
    st.warning("Erro ao carregar dados. Verifique a planilha ou os Secrets.")

st.sidebar.info("Os dados são atualizados automaticamente a cada 10 minutos.")