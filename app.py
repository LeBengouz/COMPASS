import streamlit as st
import tempfile

from src.pdf_parser import pdf_to_markdown

st.set_page_config(
    page_title="COMPASS",
    layout="wide",
)

st.title("COMPASS")

research_paper = st.file_uploader(
    "1] Load the research paper to be studied",
    type=["pdf"],
)

user_background = st.text_area(
    "2] What knowledge do you already have in this field?",
    placeholder=(
        "Ex : linear algebra, probability, "
        "Classical ML; little deep learning"
    )
)

target_passage = st.text_area(
    "3] Please, paste the passage you don't understand."
)

if st.button("Build my learning map"):
    # 1. parser le PDF
    # 2. créer des chunks
    # 3. calculer les embeddings
    # 4. retrouver le passage précis
    # 5. récupérer le contexte (sémantique + spaciale)
    # 6. appeler un LLM
    # 7. afficher résultats selon la structure donnée

    pass