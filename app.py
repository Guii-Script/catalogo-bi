import streamlit as st
import pandas as pd
import re

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

# --- CSS Customizado ---
def load_custom_css():
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
        @keyframes gradientShift {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}

        /* === PARTÍCULAS === */
        [data-testid="stAppViewContainer"]::before {{
            content: ""; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, {COLORS['primary_light']}aa, transparent 50%),
                radial-gradient(2px 2px at 40px 70px, {COLORS['accent_purple']}aa, transparent 50%),
                radial-gradient(1px 1px at 90px 40px, {COLORS['accent_teal']}aa, transparent 50%),
                radial-gradient(1px 1px at 130px 80px, {COLORS['accent_orange']}aa, transparent 50%);
            background-repeat: repeat; background-size: 250px 250px;
            animation: float 20s linear infinite; z-index: 0; opacity: 0.3;
        }}
        @keyframes float {{ 100% {{ transform: translateY(-250px); }} }}

        /* === HEADER === */
        .main-header {{
            background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem 0; margin-bottom: 3rem;
            position: relative; z-index: 10;
        }}

        /* === TÍTULO PRINCIPAL === */
        h1 {{
            font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 4rem; text-align: center;
            background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['accent_purple']} 50%, {COLORS['accent_teal']} 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            margin-bottom: 1rem; position: relative; z-index: 5;
            text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}
        @keyframes titleGlow {{
            from {{ text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3); }}
            to {{ text-shadow: 0 4px 30px rgba(6, 214, 160, 0.4), 0 0 40px rgba(91, 146, 200, 0.2); }}
        }}

        /* === SUBTÍTULO === */
        .subtitle-container {{ text-align: center; position: relative; z-index: 5; }}
         .subtitle-container p {{
            color: {COLORS['text_secondary']} !important; font-size: 1.3rem;
            max-width: 700px; margin: 0 auto 3rem auto;
            line-height: 1.6; font-weight: 300;
        }}

        /* === BARRA DE BUSCA === */
        [data-testid="stTextInput"] {{ position: relative; z-index: 10; }}
        [data-testid="stTextInput"] input {{
            background: rgba(30, 41, 59, 0.8) !important; backdrop-filter: blur(10px);
            border: 2px solid rgba(91, 146, 200, 0.3) !important; border-radius: 15px !important;
            color: {COLORS['text_primary']} !important; padding: 1rem 1.5rem !important;
            font-size: 1.1rem !important; transition: all 0.3s ease !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        }}
        [data-testid="stTextInput"] input:focus {{
            border-color: {COLORS['accent_purple']} !important;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.4) !important;
            transform: translateY(-2px);
        }}
        [data-testid="stTextInput"] input::placeholder {{ color: {COLORS['text_secondary']} !important; }}

        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.95) !important; backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}
        [data-testid="stSidebar"] h2 {{
            color: {COLORS['text_primary']} !important; font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 1.8rem;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }}
        
        /* === BOTÃO DE RECOLHER/EXPANDIR SIDEBAR === */
        [data-testid="stSidebarNavCollapseButton"] {{
            background-color: rgba(91, 146, 200, 0.2);
            border: 1px solid rgba(91, 146, 200, 0.4); border-radius: 50%;
            transition: all 0.3s ease; transform: scale(1.1);
        }}
        [data-testid="stSidebarNavCollapseButton"]:hover {{
            background-color: rgba(139, 92, 246, 0.3); border-color: rgba(139, 92, 246, 0.5);
            transform: scale(1.2);
        }}
        [data-testid="stSidebarNavCollapseButton"] svg {{ fill: {COLORS['text_primary']}; }}

        /* === CARDS === */
        .portfolio-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px; padding: 1.6rem; 
            min-height: 380px;
            display: flex; flex-direction: column; position: relative; overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.03);
            animation: cardEntrance 0.8s ease-out forwards; opacity: 0; transform: translateY(50px);
            z-index: 2;
        }}
        @keyframes cardEntrance {{ to {{ opacity: 1; transform: translateY(0); }} }}

        .portfolio-card::before {{
            content: ''; position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.03), transparent);
            transition: left 0.6s;
        }}
        .portfolio-card:hover::before {{ left: 100%; }}

        .portfolio-card:hover {{
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 80px rgba(139, 92, 246, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.03);
            border-color: rgba(139, 92, 246, 0.18);
        }}
        
        /* === IMAGEM (MOLDURA NA PRÓPRIA FOTO) === */
        .portfolio-card img {{
            border-radius: 12px;
            margin-bottom: 1.25rem;
            max-height: 220px;
            object-fit: cover;
            width: 100%;
            border: 3px solid rgba(139, 92, 246, 0.28);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5),
                        0 0 25px rgba(139, 92, 246, 0.18);
            transition: all 0.35s ease;
            display: block;
        }}
        .portfolio-card img:hover {{
            transform: scale(1.03);
            box-shadow: 0 16px 40px rgba(139, 92, 246, 0.32),
                        0 0 50px rgba(91, 146, 200, 0.18);
        }}

        /* ESTILOS PARA TÍTULO E PARÁGRAFO DENTRO DO CARD */
        .portfolio-card h2 {{
            color: {COLORS['text_accent']}; font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 1.35rem; line-height: 1.2; margin-bottom: 0.45rem;
        }}
        
        .portfolio-card p {{
             color: {COLORS['text_secondary']}; font-size: 0.95rem; line-height: 1.45; margin-bottom: 1rem;
        }}

        /* === TÍTULOS DAS SEÇÕES === */
        h3 {{
            font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.5rem; text-align: center;
            margin-top: 3rem; margin-bottom: 1rem; padding-bottom: 25px;
            position: relative; color: {COLORS['text_primary']}; z-index: 5;
        }}
        h3::after {{
            content: ''; position: absolute; bottom: 0; left: 50%;
            transform: translateX(-50%); width: 100px; height: 4px;
            background: linear-gradient(90deg, {COLORS['accent_purple']}, {COLORS['accent_teal']});
            border-radius: 2px;
        }}

        /* === TAGS === */
        .tag-wrapper {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 1rem 0 0 0; margin-top: auto; }}
        .tag {{
            background: rgba(139, 92, 246, 0.14); color: {COLORS['text_primary']}; padding: 8px 14px;
            border-radius: 20px; font-weight: 600; font-size: 0.85rem;
            border: 1px solid rgba(139, 92, 246, 0.18); backdrop-filter: blur(6px);
            transition: all 0.25s ease;
        }}
        .tag:hover {{ transform: translateY(-2px); background: rgba(139, 92, 246, 0.22); box-shadow: 0 6px 18px rgba(139, 92, 246, 0.08); }}
        .tag.status-ativo {{ background: rgba(6, 214, 160, 0.12); border-color: rgba(6, 214, 160, 0.18); }}
        .tag.status-inativo {{ background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.12); }}

        /* === BOTÕES (Usado pelo st.link_button nativo, se funcionar) === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important; border: none !important; border-radius: 12px !important;
            font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.3s ease !important;
            position: relative; overflow: hidden;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2) !important; width: 100%;
            text-decoration: none; display: inline-block; text-align: center; line-height: normal; cursor: pointer;
        }}
        [data-testid="stButton"] button::before, [data-testid="stLinkButton"] a::before {{
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
            transition: left 0.5s;
        }}
        [data-testid="stButton"] button:hover::before, [data-testid="stLinkButton"] a:hover::before {{ left: 100%; }}
        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-3px) !important; box-shadow: 0 12px 35px rgba(139, 92, 246, 0.35) !important;
        }}
        [data-testid="stButton"] button:disabled {{
            background: rgba(55, 65, 81, 0.5) !important; color: {COLORS['text_secondary']} !important;
            box-shadow: none !important; transform: none !important; opacity: 0.7; cursor: not-allowed;
        }}

        /* === ESTILO PARA O BOTÃO DE FALLBACK (HTML PURO) === */
        .fallback-link-button {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important; border: none !important; border-radius: 12px !important;
            font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.3s ease !important;
            position: relative; overflow: hidden;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3) !important; width: 100%;
            text-decoration: none !important; display: inline-block; text-align: center;
            line-height: normal; cursor: pointer; box-sizing: border-box; /* Importante p/ padding */
        }}
         .fallback-link-button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 35px rgba(139, 92, 246, 0.5) !important;
            color: {COLORS['white']} !important;
        }}
        .fallback-link-button::before {{
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
            transition: left 0.5s;
        }}
        .fallback-link-button:hover::before {{ left: 100%; }}

        /* === POPOVER (Mantido para o futuro, caso o bug seja corrigido) === */
        [data-testid="stPopover"] {{
            background: rgba(30, 41, 59, 0.95) !important; backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}
        [data-testid="stPopover"] p, [data-testid="stPopover"] span, [data-testid="stPopover"] li {{ color: {COLORS['text_primary']} !important; }}
        [data-testid="stPopover"] strong {{ color: {COLORS['accent_teal']}; }}
        [data-testid="stPopover"] button {{ 
             background: rgba(55, 65, 81, 0.5) !important; color: {COLORS['text_primary']} !important;
             border: 1px solid rgba(255, 255, 255, 0.1) !important; width: 100%;
        }}
        [data-testid="stPopover"] button:hover {{ background: rgba(75, 85, 99, 0.7) !important; border-color: {COLORS['accent_purple']} !important; }}

        /* === ESTATÍSTICAS NO HEADER === */
        .stats-container {{ display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; }}
        .stat-item {{
            text-align: center; background: rgba(30, 41, 59, 0.6); padding: 1.5rem 2rem;
            border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px); transition: all 0.3s ease;
        }}
        .stat-item:hover {{ transform: translateY(-5px); border-color: {COLORS['accent_purple']}; box-shadow: 0 10px 25px rgba(139, 92, 246, 0.12); }}
        .stat-number {{
            font-size: 2.5rem; font-weight: 800; display: block;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_teal']});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .stat-label {{ color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; }}

        /* === RESPONSIVIDADE === */
        @media (max-width: 768px) {{ h1 {{ font-size: 2.5rem; }} .stats-container {{ gap: 1rem; }} .stat-item {{ padding: 1rem; }} }}

        /* === SCROLLBAR === */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: {COLORS['background_main']}; }}
        ::-webkit-scrollbar-thumb {{ background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']}); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['accent_teal']}); }}
        </style>
    """, unsafe_allow_html=True)

# Executa o CSS
load_custom_css()

# --- Carregamento de Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except Exception:
    # Mantemos a experiência: mostra mensagem e não trava por KeyError em dev
    URL_PLANILHA = None

@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        return pd.DataFrame()
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_esperadas = ['Nome_Dash','Descricao', 'Imagem_Path','Link','Status','Responsavel','Publico','Midia','Periodicidade','Horario','Divulgacao']
        for c in colunas_esperadas:
            if c not in df.columns: df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Header com Estatísticas ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("Portfólio de Business Intelligence")

st.markdown(
    "<div class='subtitle-container'><p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos</p></div>",
    unsafe_allow_html=True,
)

if df is not None and not df.empty:
    total_dashboards = len(df)
    ativos = len(df[df['Status'].str.lower() == 'ativo'])
    plataformas = df[df['Midia'].str.lower() != 'n/a']['Midia'].nunique()
    
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
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Fecha .main-header

# --- Barra Lateral com Logo e Filtros ---
# Tenta carregar logo/fundo local; se não existir, ignora.
try:
    # Verifique se o nome "fundo.png" está correto e se o arquivo
    # está NA MESMA PASTA que o seu script .py
    st.sidebar.image("fundo.png", use_container_width=True)
except Exception:
    pass # Ignora silenciosamente se 'fundo.png' não for encontrado

st.sidebar.markdown("---")
st.sidebar.header("Filtros Avançados")

if df is not None and not df.empty:
    def lista(col):
        return ["Todos"] + sorted(df[col].replace('N/A', pd.NA).dropna().unique().tolist())

    filtro_responsavel = st.sidebar.selectbox("👤 Responsável", lista("Responsavel"))
    filtro_publico = st.sidebar.selectbox("🎯 Público", lista("Publico"))
    filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista("Midia"))
    filtro_status = st.sidebar.selectbox("📈 Status", lista("Status"))
    
    st.sidebar.markdown("---") # Divisor

    # --- Lógica de Busca e Filtro ---
    search_term = st.text_input("🔍 **Buscar dashboards:**", placeholder="Digite o nome do dashboard, tecnologia ou palavra-chave...")
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

    # Aplicar filtros
    df_filtrado = df.copy()
    if search_term:
        df_filtrado = df_filtrado[
            df_filtrado["Nome_Dash"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descricao"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Midia"].str.contains(search_term, case=False, na=False)
        ]
    
    filter_mapping = {
        "Responsavel": (filtro_responsavel, "Todos"),
        "Publico": (filtro_publico, "Todos"), 
        "Midia": (filtro_midia, "Todos"),
        "Status": (filtro_status, "Todos")
    }
    
    for col, (filtro, padrao) in filter_mapping.items():
        if filtro != padrao:
            df_filtrado = df_filtrado[df_filtrado[col] == filtro]

    # --- [ESTE É O BLOCO CORRIGIDO] Exibição dos Cards em Grid ---
    if len(df_filtrado) == 0:
        st.error("🔍 Nenhum dashboard encontrado com os critérios selecionados.")
        st.info("💡 Tente ajustar os filtros ou termos de busca.")
    else:
        # Define os grupos de público para iterar
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Publico"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            # Adiciona o título da seção
            st.markdown(f"### {g}", unsafe_allow_html=True)
            # Filtra o dataframe para o grupo atual
            subset = df_filtrado[df_filtrado["Publico"] == g]
            
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3
                
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        # --- 1. Obter todos os dados do 'row' ---
                        nome_dash = row.get('Nome_Dash','N/A')
                        descricao = row.get('Descricao','')
                        image_path = row.get("Imagem_Path", "") # Pega o caminho da planilha
                        link_value_raw = row.get("Link", "")
                        link_value = link_value_raw.strip() if isinstance(link_value_raw, str) else ""
                        
                        midia = row.get('Midia','N/A')
                        status = row.get('Status','N/A')
                        periodicidade = row.get('Periodicidade','N/A')
                        
                        responsavel = row.get('Responsavel','N/A')
                        horario = row.get('Horario','N/A')
                        divulgacao = row.get('Divulgacao','N/A')
                        publico = row.get('Publico','N/A')

                        # --- 2. Construir o HTML da Imagem ---
                        image_html = ""
                        if image_path and image_path.lower() != 'n/a':
                            # A tag <img> vai funcionar para URLs ou caminhos locais
                            safe_src = image_path.replace('"', '%22')
                            image_html = f'<img src="{safe_src}" alt="Imagem do dashboard {nome_dash}">' 
                        else:
                            # Placeholder se não houver imagem
                            image_html = f"""
                            <div style="
                                height:220px; border-radius:12px; background:rgba(91,146,200,0.06);
                                border:2px dashed rgba(91,146,200,0.12); display:flex; align-items:center; 
                                justify-content:center; color:{COLORS['text_secondary']}; font-size:0.95rem; margin-bottom:1.25rem;">
                                🖼️ Imagem não disponível
                            </div>
                            """

                        # --- 3. Construir o HTML das Tags ---
                        platform_icons = {'Power BI': '📊','Tableau': '📈','Qlik': '🔍','Google Data Studio': '🌐','Excel': '📋','Metabase': '🛠️'}
                        icon = platform_icons.get(midia, '📊')
                        status_class = "status-ativo" if str(status).lower() == "ativo" else "status-inativo"
                        
                        tags_html = f"""
                        <div class="tag-wrapper">
                            <span class="tag">🖥️ {midia}</span>
                            <span class="tag {status_class}">● {status}</span>
                            <span class="tag">🕐 {periodicidade}</span>
                        </div>
                        """
                        
                        # --- 4. Construir o HTML dos Botões ---
                        
                        # Botão 1 (Detalhes): Convertido para um botão HTML desabilitado
                        # que mostra os detalhes ao passar o mouse (tooltip)
                        details_tooltip = f"Responsável: {responsavel} | Periodicidade: {periodicidade} | Horário: {horario} | Divulgação: {divulgacao} | Público: {publico}"
                        details_button_html = f"""
                        <button disabled title="{details_tooltip}" style="width:100%; padding:12px 24px; border-radius:12px; background:rgba(55,65,81,0.5); color: #94A3B8; border:none; cursor: help; font-weight: 600;">
                            📋 Detalhes
                        </button>
                        """
                        
                        # Botão 2 (Acessar / Em Breve): Convertido para HTML puro
                        access_button_html = ""
                        if link_value and link_value.lower() != "n/a":
                            # Usando a classe .fallback-link-button que você já estilizou
                            access_button_html = f"""<a href="{link_value}" target="_blank" class="fallback-link-button" title="Acessar dashboard {nome_dash}">🚀 Acessar</a>"""
                        else:
                            # Botão desabilitado
                            access_button_html = f"""<button disabled style="width:100%; padding:12px 24px; border-radius:12px; background:rgba(55,65,81,0.5); color: #94A3B8; border:none; font-weight: 600;">⏳ Em breve</button>"""

                        # --- 5. Montar o Card Completo ---
                        # Aqui usamos as tags H2 e P que o seu CSS .portfolio-card h2 já estiliza
                        card_html = f"""
                        <div class="portfolio-card" style="animation-delay: {j*0.06}s">
                            {image_html}
                            
                            <h2>{icon} {nome_dash}</h2>
                            <p>{descricao}</p>
                            
                            {tags_html}
                            
                            <div style="margin-top: auto; display: flex; gap: 10px; width: 100%; padding-top: 1rem;">
                                <div style="flex: 1;">
                                    {details_button_html}
                                </div>
                                <div style="flex: 1;">
                                    {access_button_html}
                                </div>
                            </div>
                        </div>
                        """
                        
                        # --- 6. Renderizar o card de UMA SÓ VEZ ---
                        st.markdown(card_html, unsafe_allow_html=True)
                
                # Espaço entre as linhas do grid
                st.markdown("<br>", unsafe_allow_html=True) 
            
            # Espaço extra entre as seções
            st.markdown("<br>", unsafe_allow_html=True)
    # --- [FIM DO BLOCO CORRIGIDO] ---

else:
    st.warning("📊 Aguardando dados... Verifique a conexão com a planilha ou a variável 'GOOGLE_SHEET_URL' em st.secrets.")

# ---- Footer ---
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
