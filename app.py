import streamlit as st
import pandas as pd

# Define o layout da página, o título no navegador e o ícone
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="💼", # Ícone de "pasta/portfólio"
    layout="wide"
)

# Carrega a URL da planilha a partir dos 'Secrets' do Streamlit
# Isso mantém seu link de dados seguro e fora do repositório público.
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.info("Por favor, vá em 'Settings' > 'Secrets' no painel do Streamlit e adicione o link da sua planilha.")
    st.stop()
except Exception as e:
    st.error(f"Um erro inesperado ocorreu ao tentar ler os segredos: {e}")
    st.stop()


# Função principal para carregar e cachear os dados da planilha
# O cache (ttl=600) impede que o app recarregue os dados do Google
# a cada interação, melhorando a performance. Ele atualiza a cada 10 minutos.
@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
        
    try:
        # Tenta ler o CSV. O encoding 'utf-8' é importante para acentuação.
        df = pd.read_csv(url, encoding='utf-8')
        
        # Garante que colunas essenciais para o app existam, mesmo que vazias
        # Isso evita que o app quebre se uma coluna for renomeada ou excluída
        colunas_essenciais = ['Report', 'Descrição', 'Link', 'Status', 'Responsável', 'Público', 'Mídia']
        for col in colunas_essenciais:
            if col not in df.columns:
                df[col] = pd.NA
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        st.info(f"Verifique se o link da planilha está correto e se ela está publicada como CSV.")
        return pd.DataFrame()

# --- Carregamento dos Dados ---
df = carregar_dados(URL_PLANILHA)

# --- Título Principal ---
st.title("💼 Portfólio de Dashboards de BI")
st.write("Navegue pelo nosso catálogo de dashboards. Use os filtros para refinar sua busca.")


if not df.empty:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header("Filtros do Catálogo")
    
    # Função auxiliar para criar listas de filtro, tratando valores nulos (NA)
    def criar_lista_filtro(coluna):
        return ["Todos"] + sorted(list(df[coluna].dropna().unique()))

    # Filtro por Responsável
    try:
        filtro_responsavel = st.sidebar.selectbox(
            "Filtrar por Responsável:", 
            criar_lista_filtro('Responsável')
        )
    except KeyError:
        st.sidebar.error("Coluna 'Responsável' não encontrada.")
        filtro_responsavel = "Todos"
        
    # Filtro por Público
    try:
        filtro_publico = st.sidebar.selectbox(
            "Filtrar por Público:", 
            criar_lista_filtro('Público')
        )
    except KeyError:
        st.sidebar.error("Coluna 'Público' não encontrada.")
        filtro_publico = "Todos"

    # Filtro por Mídia (Ex: Looker, Email)
    try:
        filtro_midia = st.sidebar.selectbox(
            "Filtrar por Mídia:", 
            criar_lista_filtro('Mídia')
        )
    except KeyError:
        st.sidebar.error("Coluna 'Mídia' não encontrada.")
        filtro_midia = "Todos"

    # Filtro por Status
    try:
        filtro_status = st.sidebar.selectbox(
            "Filtrar por Status:", 
            criar_lista_filtro('Status')
        )
    except KeyError:
        st.sidebar.error("Coluna 'Status' não encontrada.")
        filtro_status = "Todos"
    
    # --- Lógica de Filtragem ---
    # Começa com o dataframe completo e vai aplicando os filtros
    df_filtrado = df

    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Mídia'] == filtro_midia]

    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    
    # --- Lógica de Exibição em Grid (Portfólio) ---
    
    st.write(f"Exibindo {len(df_filtrado)} dashboards:")
    st.divider() # Linha horizontal

    # Define o número de colunas para o grid
    NUM_COLUNAS = 3 
    
    # Converte o dataframe filtrado em uma lista de dicionários para iterar
    reports_list = df_filtrado.to_dict('records')

    if not reports_list:
        st.info("Nenhum dashboard encontrado com os filtros selecionados.")

    # Itera pela lista de reports em "chunks" do tamanho do NUM_COLUNAS
    for i in range(0, len(reports_list), NUM_COLUNAS):
        
        # Cria as colunas para esta linha do grid
        cols = st.columns(NUM_COLUNAS)
        
        # Pega o "pedaço" de reports para esta linha (ex: 3 reports)
        chunk = reports_list[i : i + NUM_COLUNAS]

        # Itera sobre o chunk e preenche cada coluna
        for j, report_data in enumerate(chunk):
            
            # 'cols[j]' é a coluna atual (coluna 0, 1 ou 2)
            with cols[j]:
                
                # 'height' fixo é o segredo para um grid uniforme.
                # Ajuste este valor (ex: 350, 400) se o conteúdo não couber.
                with st.container(border=True, height=350):
                    
                    # Título do Card
                    st.subheader(report_data.get('Report', 'Sem Título'))
                    
                    # Descrição (limitada a 150 caracteres para não quebrar o layout)
                    descricao = report_data.get('Descrição', 'Sem descrição.')
                    if pd.isna(descricao): descricao = "Sem descrição."
                    st.write(descricao[:150] + ("..." if len(descricao) > 150 else ""))

                    # Informações secundárias (Público, Responsável)
                    st.caption(f"Público: {report_data.get('Público', 'N/A')} | Status: {report_data.get('Status', 'N/A')}")
                    
                    # Popover: um "botão" que abre uma janela com detalhes
                    # Isso mantém o card principal limpo.
                    with st.popover("Ver mais detalhes"):
                        st.markdown(f"**Responsável:** {report_data.get('Responsável', 'N/A')}")
                        st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                        st.markdown(f"**Mídia:** {report_data.get('Mídia', 'N/A')}")
                        st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                        st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")
                    
                    st.write("") # Espaçamento
                    
                    # Botão de Ação (só aparece se o link existir)
                    link = report_data.get('Link')
                    if link and pd.notna(link):
                        st.link_button("Acessar Dashboard", link, use_container_width=True, type="primary")
                    else:
                        st.button("Link Indisponível", use_container_width=True, disabled=True)

else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")