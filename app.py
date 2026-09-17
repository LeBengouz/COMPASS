import streamlit as st
import tempfile

from src.pdf_parser import pdf_to_markdown


st.set_page_config(
    page_title="COMPASS",
    layout="wide",
)

st.title("COMPASS")

research_paper = st.file_uploader(
    "Charger le papier de recherche à étudier",
    type=["pdf"],
)

if research_paper is not None:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(research_paper.getvalue())
        pdf_path = tmp.name

    research_paper_markdown = pdf_to_markdown(pdf_path)

    st.success("PDF correctement chargé")

    with st.expander("Consulter le texte extrait"):
        st.text(research_paper_markdown[:10000])