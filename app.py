import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Paleta de Cores ---
COLORS = {
    "primary_dark": "#0d2e5b",
    "primary_medium": "#1e4a7f",
    "primary_light": "#5b92c8",
    "accent_purple": "#8B5CF6",
    "accent_teal": "#06D6A0",
    "accent_orange": "#FF9E64",
    "background_main": "#0F172A",
    "background_card": "#1E293B",
    "background_sidebar": "#0F172A",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_accent": "#E2E8F0",
    "white": "#FFFFFF"
}


# --- CSS Customizado ---
def load_custom_css():
    """Carrega o estilo visual completo do portfólio."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

        /* === FUNDO === */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(-45deg, {COLORS['background_main']}, {COLORS['primary_dark']}, {COLORS['background_sidebar']}, {COLORS['primary_medium']});
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: {COLORS['text_primary']};
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }}
        @keyframes gradientShift {{ 
            0% {{background-position:0% 50%}} 
            50% {{background-position:100% 50%}} 
            100% {{background-position:0% 50%}} 
        }}

        /* === PARTÍCULAS === */
        [data-testid="stAppViewContainer"]::before {{
            content: ""; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, {COLORS['primary_light']}aa, transparent 50%),
                radial-gradient(2px 2px at 40px 70px, {COLORS['accent_purple']}aa, transparent 50%),
                radial-gradient(1px 1px at 90px 40px, {COLORS['accent_teal']}aa, transparent 50%),
                radial-gradient(1px 1px at 130px 80px, {COLORS['accent_orange']}aa, transparent 50%);
            background-repeat: repeat; 
            background-size: 250px 250px;
            animation: float 20s linear infinite; 
            z-index: 0; opacity: 0.3;
        }}
        @keyframes float {{ 100% {{ transform: translateY(-250px); }} }}

        /* === HEADER === */
        .main-header {{
            background: rgba(30, 41, 59, 0.8); 
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem 0; 
            margin-bottom: 3rem;
            position: relative; 
            z-index: 10;
        }}

        /* === TÍTULO PRINCIPAL === */
        h1 {{
            font-family: 'Space Grotesk', sans-serif; 
            font-weight: 800; 
            font-size: 4rem; 
            text-align: center;
            background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['accent_purple']} 50%, {COLORS['accent_teal']} 100%);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            background-clip: text;
            margin-bottom: 1rem; 
            position: relative; 
            z-index: 5;
            text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}
        @keyframes titleGlow {{
            from {{ text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3); }}
            to {{ text-shadow: 0 4px 30px rgba(6, 214, 160, 0.4), 0 0 40px rgba(91, 146, 200, 0.2); }}
        }}

        /* === SUBTÍTULO === */
        .subtitle-container {{
            text-align: center; 
            position: relative; 
            z-index: 5; 
        }}
        .subtitle-container p {{
            color: {COLORS['text_secondary']} !important; 
            font-size: 1.3rem;
            max-width: 700px; 
            margin: 0 auto 3rem auto;
            line-height: 1.6; 
            font-weight: 300;
        }}

        /* === CARDS === */
        .portfolio-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; 
            padding: 2rem; 
            min-height: 450px; 
            display: flex; 
            flex-direction: column; 
            position: relative; 
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            animation: cardEntrance 0.8s ease-out forwards; 
            opacity: 0; 
            transform: translateY(50px);
            z-index: 2;
        }}
        @keyframes cardEntrance {{ to {{ opacity: 1; transform: translateY(0); }} }}

        .portfolio-card:hover {{
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 80px rgba(139, 92, 246, 0.2);
            border-color: rgba(139, 92, 246, 0.3);
        }}
        .portfolio-card img {{
            border-radius: 10px; 
            margin-bottom: 1.5rem; 
            max-height: 200px; 
            object-fit: cover; 
            width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)


# --- Carregar CSS ---
load_custom_css()


# --- Carregar Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado.")
    st.stop()


@st.cache_data(ttl=600)
def carregar_dados(url):
    """Lê a planilha de dashboards e garante colunas padronizadas."""
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_esperadas = [
            'Nome_Dash', 'Descricao', 'Imagem_Path', 'Link',
            'Status', 'Responsavel', 'Publico', 'Midia',
            'Periodicidade', 'Horario', 'Divulgacao'
        ]
        for c in colunas_esperadas:
            if c not in df.columns:
                df[c] = "N/A"
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


df = carregar_dados(URL_PLANILHA)


# --- HEADER ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("Portfólio de Business Intelligence")
st.markdown(
    "<div class='subtitle-container'><p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos.</p></div>",
    unsafe_allow_html=True,
)

# --- Estatísticas ---
if not df.empty:
    total_dashboards = len(df)
    ativos = len(df[df['Status'].str.lower() == 'ativo'])
    plataformas = df[df['Midia'].str.lower() != 'n/a']['Midia'].nunique()

    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item"><span class="stat-number">{total_dashboards}</span><span class="stat-label">Dashboards</span></div>
            <div class="stat-item"><span class="stat-number">{ativos}</span><span class="stat-label">Ativos</span></div>
            <div class="stat-item"><span class="stat-number">{plataformas}</span><span class="stat-label">Plataformas</span></div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# --- SIDEBAR ---
st.sidebar.image("fundo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.header("Filtros Avançados")

if not df.empty:

    def lista(col):
        """Retorna lista de filtros únicos + opção 'Todos'."""
        return ["Todos"] + sorted(df[col].replace('N/A', pd.NA).dropna().unique().tolist())

    filtro_responsavel = st.sidebar.selectbox("👤 Responsável", lista("Responsavel"))
    filtro_publico = st.sidebar.selectbox("🎯 Público", lista("Publico"))
    filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista("Midia"))
    filtro_status = st.sidebar.selectbox("📈 Status", lista("Status"))

    st.sidebar.markdown("---")

    # --- Busca ---
    search_term = st.text_input(
        "🔍 **Buscar dashboards:**",
        placeholder="Digite o nome, tecnologia ou palavra-chave..."
    )

    df_filtrado = df.copy()

    # --- Aplicar filtros ---
    if search_term:
        mask = (
            df_filtrado["Nome_Dash"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descricao"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Midia"].str.contains(search_term, case=False, na=False)
        )
        df_filtrado = df_filtrado[mask]

    filtros = {
        "Responsavel": filtro_responsavel,
        "Publico": filtro_publico,
        "Midia": filtro_midia,
        "Status": filtro_status
    }

    for col, val in filtros.items():
        if val != "Todos":
            df_filtrado = df_filtrado[df_filtrado[col] == val]

    # --- Exibir Cards ---
    if df_filtrado.empty:
        st.error("🔍 Nenhum dashboard encontrado.")
        st.info("💡 Ajuste os filtros ou termos de busca.")
    else:
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Publico"].replace('N/A', pd.NA).dropna().unique())

        for grupo in grupos:
            st.markdown(f"### {grupo}")
            subset = df_filtrado[df_filtrado["Publico"] == grupo]
            registros = subset.to_dict('records')
            NUM_COLS = 3

            for i in range(0, len(registros), NUM_COLS):
                cols = st.columns(NUM_COLS)
                chunk = registros[i:i + NUM_COLS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        st.markdown(f'<div class="portfolio-card" style="animation-delay:{j * 0.1}s">', unsafe_allow_html=True)

                        # Imagem
                        if row["Imagem_Path"].lower() != "n/a":
                            st.image(row["Imagem_Path"], use_container_width=True)

                        # Ícones
                        icones = {
                            'Power BI': '📊', 'Tableau': '📈',
                            'Qlik': '🔍', 'Google Data Studio': '🌐',
                            'Excel': '📋', 'Metabase': '🛠️'
                        }
                        icon = icones.get(row["Midia"], "📊")

                        st.subheader(f"{icon} {row['Nome_Dash']}")
                        st.write(row["Descricao"])

                        status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"

                        st.markdown(f"""
                            <div class="tag-wrapper">
                                <span class="tag">🖥️ {row['Midia']}</span>
                                <span class="tag {status_class}">● {row['Status']}</span>
                                <span class="tag">🕐 {row['Periodicidade']}</span>
                            </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)

                        with col1:
                            with st.popover("📋 Detalhes"):
                                st.write(f"**👤 Responsável:** {row['Responsavel']}")
                                st.write(f"**🕐 Periodicidade:** {row['Periodicidade']}")
                                st.write(f"**⏰ Horário:** {row['Horario']}")
                                st.write(f"**📢 Divulgação:** {row['Divulgacao']}")
                                st.write(f"**🎯 Público:** {row['Publico']}")

                        with col2:
                            link = row["Link"].strip()
                            if link and link.lower() != "n/a":
                                st.link_button("🚀 Acessar", link, use_container_width=True)
                            else:
                                st.button("⏳ Em breve", use_container_width=True, disabled=True)

                        st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

else:
    st.warning("📊 Aguardando dados... Verifique a planilha.")


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style='color:{COLORS['text_secondary']}; font-size:0.8rem; text-align:center;'>
        <p>✨ Portfólio BI v2.0</p>
        <p>Dados atualizados a cada 10 minutos</p>
    </div>
""", unsafe_allow_html=True)
