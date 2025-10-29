import streamlit as st

def create_portfolio_cards(df):
    html = "<div class='portfolio-container'>"
    for _, row in df.iterrows():
        title = row.get("Título", "Sem título")
        subtitle = row.get("Categoria", "")
        desc = row.get("Descrição", "")
        link = row.get("Link", "#")
        image_path = row.get("Imagem_Path", "")

        html += "<div class='portfolio-card'>"

        # Imagem ou placeholder
        if image_path and image_path.lower() != "n/a":
            html += f'<img src="{image_path}" alt="{title}">'
        else:
            html += "<div class='image-placeholder'>🖼️ Imagem não disponível</div>"

        html += f"""
            <div class="portfolio-title">{title}</div>
            <div class="portfolio-subtitle">{subtitle}</div>
            <div class="portfolio-description">{desc}</div>
            <a href="{link}" target="_blank" class="portfolio-link">🔗 Ver Projeto</a>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
