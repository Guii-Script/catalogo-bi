import streamlit as st
from pathlib import Path 
import pandas as pd      

# --- Paleta de Cores Profissional ---
COLORS = {
    "primary_dark": "#0d2e5b",
    "primary_medium": "#1e4a7f",
    "primary_light": "#5b92c8",
    "accent_purple": "#5b92c8",
    "accent_teal": "#06D6A0",
    "accent_orange": "#5b92c8",
    "background_main": "#0F172A",
    "background_card": "#1E293B",
    "background_sidebar": "#0F172A",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_accent": "#E2E8F0",
    "white": "#FFFFFF",
    "gradient_start": "#1e4a7f",
    "gradient_end": "#0d2e5b"
}

def load_css():
    """Lê o arquivo style.css, injeta as cores da paleta e aplica ao Streamlit."""
    
    try:
        current_dir = Path(__file__).resolve().parent
        css_file_path = current_dir / "style.css"

        with open(css_file_path) as f:
            css = f.read()
        
        css_com_cores = css.format(**COLORS)
        st.markdown(f"<style>{css_com_cores}</style>", unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"ERRO: 'style.css' não encontrado.")
        st.info("Certifique-se que 'style.css' está na mesma pasta que 'ui_components.py'.")
    except Exception as e:
        st.error(f"Um erro inesperado ocorreu ao ler o CSS: {e}")


def render_team_selector(df_active, lista_func):
    """Renderiza a tela inicial de seleção de time (roteador)."""
    
    st.title("Bem-vindo(a) ao Portfólio BI")
    st.markdown(
        "<div class='subtitle-container'><p>Para começar, selecione o seu time para ver os dashboards relevantes.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if not df_active.empty:
        teams = lista_func(df_active, "Publico") 
        teams = [t for t in teams if t.lower() not in ["todos", "n/a"]] 

        if not teams:
            st.warning("Nenhum time (Público) encontrado nos dados. Carregando todos os dashboards.")
            if st.button("Continuar"):
                st.session_state.team_selected = True
                st.session_state.selected_team = "Todos"
                st.rerun()
        else:
            st.markdown("### 🎯 Selecione seu Time:")
            st.markdown("<br>", unsafe_allow_html=True)
            
            num_cols = 3 
            cols = st.columns(num_cols)
            col_index = 0
            
            for team in teams:
                with cols[col_index % num_cols]:
                    if st.button(team, key=f"team_{team}", use_container_width=True):
                        st.session_state.team_selected = True
                        st.session_state.selected_team = team
                        st.rerun()
                col_index += 1
            
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("Ou veja todos os dashboards disponíveis:")
            if st.button("Ver Todos os Dashboards 🚀", key="view_all", use_container_width=False):
                st.session_state.team_selected = True
                st.session_state.selected_team = "Todos"
                st.rerun()
    else:
        st.info("Carregando dados dos times...")

def render_header_stats(df_full):
    """Renderiza o título e os KPIs no topo da galeria principal."""
    
    st.title("Portfólio de Business Intelligence")
    st.markdown(
        "<div class='subtitle-container'><p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos</p></div>",
        unsafe_allow_html=True,
    )

    if not df_full.empty:
        total_dashboards = len(df_full)
        ativos = len(df_full[df_full['Status'].str.lower() == 'ativo'])
        plataformas = df_full[df_full['Midia'].str.lower() != 'n/a']['Midia'].nunique()
        
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

def render_sidebar(df_active, lista_func):
    """Renderiza a barra lateral com filtros e retorna os valores selecionados."""
    
    try:
        st.sidebar.image("fundo.png", use_container_width=True)
    except Exception:
        st.sidebar.warning("Logo 'fundo.png' não encontrada.")
        
    st.sidebar.markdown("---")
    
    if st.sidebar.button("⬅ Voltar (Trocar Time)", use_container_width=True):
        st.session_state.team_selected = False
        st.session_state.selected_team = "Todos"
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.header("Filtros Avançados")

    publico_list = lista_func(df_active, "Publico")
    try:
        default_index = publico_list.index(st.session_state.selected_team)
    except ValueError:
        default_index = 0 
        
    filtro_publico = st.sidebar.selectbox(
        "🎯 Público", 
        publico_list, 
        index=default_index 
    )
    
    filtro_responsavel = st.sidebar.selectbox("👤 Responsável", lista_func(df_active, "Responsavel"))
    filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista_func(df_active, "Midia"))
    
    st.sidebar.markdown("---") 

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
    
    return filtro_publico, filtro_responsavel, filtro_midia

def render_dashboard_card(row, key_base):
    """Renderiza um único card de dashboard."""
    
    # A div do card é aplicada via CSS
    st.markdown('<div class="portfolio-card">', unsafe_allow_html=True)
    
    # --- Imagem ---
    image_path = row.get("Imagem_Path", "")
    if image_path and image_path.lower() != 'n/a':
        try:
            st.image(image_path, use_container_width=True)
        except Exception as img_err:
            st.warning(f"⚠️ Imagem não encontrada: {image_path}", icon="🖼️")
    
    # --- Conteúdo HTML ---
    platform_icons = {'Power BI': '📊','Tableau': '📈','Qlik': '🔍','Google Data Studio': '🌐','Excel': '📋','Metabase': '🛠️'}
    icon = platform_icons.get(row['Midia'], '📊')
    status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"
    
    html_content = f"""
        <h2>{icon} {row['Nome_Dash']}</h2>
        <p>{row['Descricao']}</p>
        <div class="tag-wrapper">
            <span class="tag">🖥️ {row['Midia']}</span>
            <span class="tag {status_class}">● {row['Status']}</span>
            <span class="tag">🕐 {row['Periodicidade']}</span>
        </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

    # --- Botões Nativos ---
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        with st.popover("📋 Detalhes"):
            st.write(f"**👤 Responsável:** {row['Responsavel']}")
            st.write(f"**🕐 Periodicidade:** {row['Periodicidade']}")
            st.write(f"**⏰ Horário:** {row['Horario']}")
            st.write(f"**📢 Divulgação:** {row['Divulgacao']}")
            st.write(f"**🎯 Público:** {row['Publico']}")
    
    with col_btn2:
        link_value_raw = row.get("Link", "") 
        link_value = link_value_raw.strip() if isinstance(link_value_raw, str) else "" 

        if link_value and link_value.lower() != "n/a":
            try: 
                st.link_button(
                    "🚀 Acessar",
                    link_value,
                    use_container_width=True,
                    key=f"link_{key_base}" 
                )
            except (TypeError, Exception) as e: 
                fallback_button_html = f"""<a href="{link_value}" target="_blank" class="fallback-link-button" style="text-decoration: none;" title="Abrir link para {row.get('Nome_Dash', 'N/A')}">🚀 Acessar</a>"""
                st.markdown(fallback_button_html, unsafe_allow_html=True)
        else:
            st.button("⏳ Em breve", use_container_width=True, disabled=True, key=f"btn_{key_base}")
    
    # Fecha o card
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard_grid(df_filtrado, filtro_publico):
    """Renderiza o grid de cards, agrupados por público."""
    
    if len(df_filtrado) == 0:
        st.error("🔍 Nenhum dashboard encontrado com os critérios selecionados.")
        st.info("💡 Tente ajustar os filtros ou termos de busca.")
    else:
        # Esta é a linha que estava dando erro
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Publico"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            st.markdown(f"### {g}") 
            subset = df_filtrado[df_filtrado["Publico"] == g]
            
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3
                        
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        key_base = f"{g}_{i}_{j}"
                        render_dashboard_card(row, key_base)
                
                # Espaço entre as linhas do grid
                st.markdown("<br>", unsafe_allow_html=True) 
            
            # Espaço extra entre as seções
            st.markdown("<br>", unsafe_allow_html=True)