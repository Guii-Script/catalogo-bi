import streamlit as st
import pandas as pd
import re
import random

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Paleta de Cores Expandida ---
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
    "white": "#FFFFFF",
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2"
}

# SVG para efeitos wave
def create_wave_svg(color, height=120):
    return f"""
    data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E
        %3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='{color}'%3E%3C/path%3E
        %3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='{color}'%3E%3C/path%3E
        %3Cpath d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='{color}'%3E%3C/path%3E
    %3C/svg%3E
    """

def load_custom_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        /* === FUNDO COM GRADIENTE ANIMADO === */
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
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* === EFEITO DE PARTÍCULAS NO FUNDO === */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, {COLORS['primary_light']}aa, transparent 50%),
                radial-gradient(2px 2px at 40px 70px, {COLORS['accent_purple']}aa, transparent 50%),
                radial-gradient(1px 1px at 90px 40px, {COLORS['accent_teal']}aa, transparent 50%),
                radial-gradient(1px 1px at 130px 80px, {COLORS['accent_orange']}aa, transparent 50%);
            background-repeat: repeat;
            background-size: 250px 250px;
            animation: float 20s linear infinite;
            z-index: 0;
            opacity: 0.3;
        }}

        @keyframes float {{
            100% {{ transform: translateY(-250px); }}
        }}

        /* === HEADER COM EFEITO GLASS MORPHISM === */
        .main-header {{
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem 0;
            margin-bottom: 3rem;
            position: relative;
            z-index: 10;
        }}

        /* === TÍTULO PRINCIPAL COM EFEITO === */
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
        [data-testid="stMarkdown"] > p:first-of-type {{
            color: {COLORS['text_secondary']} !important;
            text-align: center;
            font-size: 1.3rem;
            max-width: 700px;
            margin: 0 auto 3rem auto;
            line-height: 1.6;
            position: relative;
            z-index: 5;
            font-weight: 300;
        }}

        /* === BARRA DE BUSCA ESTILIZADA === */
        [data-testid="stTextInput"] {{
            position: relative;
            z-index: 10;
        }}

        [data-testid="stTextInput"] input {{
            background: rgba(30, 41, 59, 0.8) !important;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(91, 146, 200, 0.3) !important;
            border-radius: 15px !important;
            color: {COLORS['text_primary']} !important;
            padding: 1rem 1.5rem !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        }}

        [data-testid="stTextInput"] input:focus {{
            border-color: {COLORS['accent_purple']} !important;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.4) !important;
            transform: translateY(-2px);
        }}

        [data-testid="stTextInput"] input::placeholder {{
            color: {COLORS['text_secondary']} !important;
        }}

        /* === SIDEBAR MODERNA === */
        [data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.95) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        [data-testid="stSidebar"] h2 {{
            color: {COLORS['text_primary']} !important;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }}

        /* === CARDS COM EFEITO 3D E GLASS MORPHISM === */
        .portfolio-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            min-height: 380px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: cardEntrance 0.8s ease-out forwards;
            opacity: 0;
            transform: translateY(50px);
        }}

        @keyframes cardEntrance {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .portfolio-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.6s;
        }}

        .portfolio-card:hover::before {{
            left: 100%;
        }}

        .portfolio-card:hover {{
            transform: translateY(-15px) scale(1.02);
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.4),
                0 0 80px rgba(139, 92, 246, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border-color: rgba(139, 92, 246, 0.3);
        }}

        /* === TÍTULOS DAS SEÇÕES === */
        h3 {{
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            text-align: center;
            margin: 4rem 0 2rem 0;
            position: relative;
            color: {COLORS['text_primary']};
        }}

        h3::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: linear-gradient(90deg, {COLORS['accent_purple']}, {COLORS['accent_teal']});
            border-radius: 2px;
        }}

        /* === TAGS MODERNAS === */
        .tag-wrapper {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 1.5rem 0;
        }}

        .tag {{
            background: rgba(139, 92, 246, 0.2);
            color: {COLORS['text_primary']};
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.85rem;
            border: 1px solid rgba(139, 92, 246, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        .tag:hover {{
            transform: translateY(-2px);
            background: rgba(139, 92, 246, 0.3);
            box-shadow: 0 5px 15px rgba(139, 92, 246, 0.2);
        }}

        .tag.status-ativo {{
            background: rgba(6, 214, 160, 0.2);
            border-color: rgba(6, 214, 160, 0.3);
        }}

        .tag.status-inativo {{
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.3);
        }}

        /* === BOTÕES COM EFEITO NEON === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3) !important;
        }}

        [data-testid="stButton"] button::before, [data-testid="stLinkButton"] a::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }}

        [data-testid="stButton"] button:hover::before, [data-testid="stLinkButton"] a:hover::before {{
            left: 100%;
        }}

        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px rgba(139, 92, 246, 0.5) !important;
        }}

        /* === POPOVER ESTILIZADO === */
        [data-testid="stPopover"] {{
            background: rgba(30, 41, 59, 0.95) !important;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        /* === ESTATÍSTICAS NO HEADER === */
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }}

        .stat-item {{
            text-align: center;
            background: rgba(30, 41, 59, 0.6);
            padding: 1.5rem 2rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        .stat-item:hover {{
            transform: translateY(-5px);
            border-color: {COLORS['accent_purple']};
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_teal']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
        }}

        .stat-label {{
            color: {COLORS['text_secondary']};
            font-size: 0.9rem;
            margin-top: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* === RESPONSIVIDADE === */
        @media (max-width: 768px) {{
            h1 {{ font-size: 2.5rem; }}
            .stats-container {{ gap: 1rem; }}
            .stat-item {{ padding: 1rem; }}
        }}

        /* === SCROLLBAR PERSONALIZADA === */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: {COLORS['background_main']};
        }}

        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']});
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['accent_teal']});
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

# --- Header com Estatísticas ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🚀 Portfólio de Business Intelligence")
st.markdown(
    "<p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos</p>",
    unsafe_allow_html=True,
)

if not df.empty:
    total_dashboards = len(df)
    ativos = len(df[df['Status'].str.lower() == 'ativo'])
    plataformas = df['Mídia'].nunique()
    
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <span class="stat-number">{total_dashboards}</span>
                <span class="stat-label">Dashboards</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{ativos}</span>
                <span class="stat-label">Ativos</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{plataformas}</span>
                <span class="stat-label">Plataformas</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{df['Público'].nunique()}</span>
                <span class="stat-label">Públicos</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Busca e Filtros ---
if not df.empty:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 **Buscar dashboards:**", placeholder="Digite o nome do dashboard, tecnologia ou palavra-chave...")

    st.sidebar.markdown("---")
    st.sidebar.header("🎛️ Filtros Avançados")
    
    def lista(col):
        return ["Todos"] + sorted(df[col].replace('N/A', pd.NA).dropna().unique().tolist())

    col1, col2, col3 = st.sidebar.columns(3)
    
    with col1:
        filtro_responsavel = st.selectbox("👤 Responsável", lista("Responsável"))
    with col2:
        filtro_publico = st.selectbox("🎯 Público", lista("Público"))
    with col3:
        filtro_status = st.selectbox("📈 Status", lista("Status"))
    
    filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista("Mídia"))

    # Aplicar filtros
    df_filtrado = df.copy()
    if search_term:
        df_filtrado = df_filtrado[
            df_filtrado["Report"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descrição"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Mídia"].str.contains(search_term, case=False, na=False)
        ]
    
    filter_mapping = {
        "Responsável": (filtro_responsavel, "Todos"),
        "Público": (filtro_publico, "Todos"), 
        "Mídia": (filtro_midia, "Todos"),
        "Status": (filtro_status, "Todos")
    }
    
    for col, (filtro, padrao) in filter_mapping.items():
        if filtro != padrao:
            df_filtrado = df_filtrado[df_filtrado[col] == filtro]

    # Exibir resultados
    if len(df_filtrado) == 0:
        st.error("🔍 Nenhum dashboard encontrado com os critérios selecionados.")
        st.info("💡 Tente ajustar os filtros ou termos de busca.")
    else:
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Público"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            st.markdown(f"### 🎯 {g}")
            subset = df_filtrado[df_filtrado["Público"] == g]
            
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3
            
            # Animação de entrada escalonada
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        # Card container customizado
                        st.markdown('<div class="portfolio-card">', unsafe_allow_html=True)
                        
                        # Ícone dinâmico baseado na plataforma
                        platform_icons = {
                            'Power BI': '📊', 'Tableau': '📈', 'Qlik': '🔍', 
                            'Google Data Studio': '🌐', 'Excel': '📋', 'Metabase': '🛠️'
                        }
                        icon = platform_icons.get(row['Mídia'], '📊')
                        
                        st.markdown(f"<h4>{icon} {row['Report']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: {COLORS['text_secondary']}; font-size: 0.95rem; line-height: 1.5;'>{row['Descrição']}</p>", unsafe_allow_html=True)

                        # Tags
                        status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"
                        st.markdown(
                            f"""
                            <div class="tag-wrapper">
                                <span class="tag">🖥️ {row['Mídia']}</span>
                                <span class="tag {status_class}">● {row['Status']}</span>
                                <span class="tag">🕐 {row['Periodicidade']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Detalhes e ações
                        col_btn1, col_btn2 = st.columns([1, 1])
                        
                        with col_btn1:
                            with st.popover("📋 Detalhes"):
                                st.write(f"**👤 Responsável:** {row['Responsável']}")
                                st.write(f"**🕐 Periodicidade:** {row['Periodicidade']}")
                                st.write(f"**⏰ Horário:** {row['Horário']}")
                                st.write(f"**📢 Divulgação:** {row['Divulgação']}")
                                st.write(f"**🎯 Público:** {row['Público']}")
                        
                        with col_btn2:
                            if row["Link"] and row["Link"].lower() != "n/a":
                                st.link_button("🚀 Acessar", row["Link"], use_container_width=True)
                            else:
                                st.button("⏳ Em breve", use_container_width=True, disabled=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

else:
    st.warning("📊 Aguardando dados... Verifique a conexão com a planilha.")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style='color: {COLORS['text_secondary']}; font-size: 0.8rem; text-align: center;'>
        <p>✨ Portfólio BI v2.0</p>
        <p>Dados atualizados a cada 10 minutos</p>
    </div>
    """, 
    unsafe_allow_html=True
)