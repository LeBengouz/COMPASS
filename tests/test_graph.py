from src.pdf_parser import pdf_to_markdown 
from src.chunking import split_per_paragraphs, create_chunks 
from src.embeddings import EmbeddingModel, VectorIndex 
from src.passage_matcher import find_target_chunk 
from src.retrieval import retrieve_context, transform_chunks_to_text 
from src.use_llm import generate_prerequisite_map 
from src.graph_builder import build_prerequisite_graph, graph_to_dot


# Parse pdf
pdf_path = "data/papers/attention_is_all_you_need.pdf" 
markdown = pdf_to_markdown(pdf_path)

# chunking
paragraphs = split_per_paragraphs(markdown)
chunks = create_chunks(paragraphs)

# Create embeddings
embedding_model = EmbeddingModel()
texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = embedding_model.encode(texts)


# Faiss index
vector_index = VectorIndex(embeddings.shape[1])
vector_index.add(embeddings)

target_passage = """
An attention function can be described as mapping a query 
and a set of key-value pairs to an output, where the query, 
keys, values, and output are all vectors.
"""

target_chunk, score = find_target_chunk(target_passage, chunks)
assert target_chunk is not None


# context retrieval
context = retrieve_context(
    target_passage, 
    target_chunk, 
    chunks, 
    embedding_model, 
    vector_index
)

local_context = transform_chunks_to_text(context["local"])
section_context = transform_chunks_to_text(context["section"])
semantic_context = transform_chunks_to_text(context["semantic"])

user_background = """ 
Linear algebra, probability and classical machine learning.
Little knowledge of deep learning.
"""


# generate json with LLM
result = generate_prerequisite_map(
    target_passage=target_passage,
    local_context=local_context,
    section_context=section_context,
    semantic_context=semantic_context,
    background=user_background
)

print("\nPrerequisite map:")
print( result.model_dump_json( indent=2 ) )



# TEST building graph
graph = build_prerequisite_graph(result)

assert len(graph.nodes) > 0
assert len(graph.edges) > 0

print("\nGraph nodes:")
print(list(graph.nodes))

print("\nGraph edges:")
print(list(graph.edges))


# TEST convert to dot
dot = graph_to_dot(graph, result.target) 

print("\nDOT representation:")
print(dot)