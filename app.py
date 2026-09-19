import streamlit as st
import tempfile

from src.pdf_parser import pdf_to_markdown
from src.chunking import split_per_paragraphs, create_chunks
from src.embeddings import EmbeddingModel, VectorIndex
from src.passage_matcher import find_target_chunk
from src.retrieval import retrieve_context, transform_chunks_to_text
from src.use_llm import generate_prerequisite_map
from src.graph_builder import build_prerequisite_graph, graph_to_dot, dot_to_png_bytes


@st.cache_resource
def load_embedding_model():
    return EmbeddingModel()


embedding_model = load_embedding_model()

if "prerequisite_map" not in st.session_state:
    st.session_state.prerequisite_map = None


st.set_page_config(
    page_title="COMPASS",
    layout="wide",
)

st.image("assets/logo_COMPASS.png",width=440)

st.title("COMPASS")

research_paper = st.file_uploader(
    "1. Load the research paper to be studied",
    type=["pdf"],
)

user_background = st.text_area(
    "2. What knowledge do you already have in this field?",
    placeholder=(
        "Ex : linear algebra, probability, "
        "Classical ML; little deep learning"
    )
)

target_passage = st.text_area(
    "3. Please, paste the passage you don't understand."
)

if st.button("Build my learning map"):
    if not research_paper:
        st.error("Please, upload a PDF first..")
        st.stop()

    if not target_passage.strip():
        st.error("Please, paste a passage to analyze..")
        st.stop()

    with st.spinner("Analyzing the paper...", show_time=True):
        # 0. Save the uploaded PDF temporarily 
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", ) as temp_file:
            temp_file.write(research_paper.getvalue())
            pdf_path = temp_file.name

        # 1. parser le PDF
        markdown = pdf_to_markdown(pdf_path)

        # 2. créer des chunks
        paragraphs = split_per_paragraphs(markdown)
        chunks = create_chunks(paragraphs)

        # 3. calculer les embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_model.encode(texts)
        vector_index = VectorIndex(embeddings.shape[1])
        vector_index.add(embeddings)

        # 4. retrouver le passage cible précis
        target_chunk, score = find_target_chunk(target_passage, chunks)


        # 5. récupérer le contexte (sémantique + spaciale)
        context = retrieve_context(
            target_text=target_passage,
            target_chunk=target_chunk,
            chunks=chunks,
            embedding_model=embedding_model,
            vector_index=vector_index,
        )
        local_text = transform_chunks_to_text(context["local"])
        section_text = transform_chunks_to_text(context["section"])
        semantic_text = transform_chunks_to_text(context["semantic"])


        # 6. appeler un LLM
        result = generate_prerequisite_map(
            target_passage=target_passage,
            local_context=local_text,
            section_context=section_text,
            semantic_context=semantic_text,
            background=user_background,
        )

        st.session_state.prerequisite_map = result

        st.success("Learning map successfully generated !")

if st.session_state.prerequisite_map is not None:
    # Showing concept data
    result = st.session_state.prerequisite_map

    st.divider()

    st.subheader("Your personalized prerequisite map")

    graph = build_prerequisite_graph(result)
    dot = graph_to_dot(graph, result.target)

    st.graphviz_chart(dot, use_container_width=True)
    st.caption(
    "Solid node: explicitly mentioned in the paper. "
    "Dashed node: inferred prerequisite. "
    "Arrows indicate learning dependencies."
    )

    # Exploration Concept
    st.divider()
    st.subheader("Explore the map")


    # Asking user to select a concept -> give exploration tips
    concept_names = [prerequisite.concept for prerequisite in result.prerequisites]

    selected_concept = st.selectbox("Explore a prerequisite", concept_names)
    selected_prerequisite = next(
        prerequisite
        for prerequisite in result.prerequisites 
        if prerequisite.concept == selected_concept
    )

    # Display the selected prerequisite
    st.markdown(f"### {selected_prerequisite.concept}")

    st.markdown("**Why is this concept usefull ?**")
    st.write(selected_prerequisite.reason)

    st.markdown("**Source**")
    if selected_prerequisite.source_type == "explicit":
        st.write("Explicitly mentioned in the paper.")
    else:
        st.write("Inferred prerequisite.")

    st.markdown("**What should I search ?**")
    for query in selected_prerequisite.search_queries:
        st.write(f"- {query}")

    st.markdown("**Checkpoint : Can you answer this question ?**")
    st.info(selected_prerequisite.checkpoint)

    st.divider()
    st.subheader("Download your map")

    png_bytes = dot_to_png_bytes(dot)

    st.download_button(label="Download graph as PNG", data=png_bytes, file_name="compass_learning_map.png", mime="image/png")