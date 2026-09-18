from src.pdf_parser import pdf_to_markdown
from src.chunking import split_per_paragraphs, create_chunks
from src.embeddings import EmbeddingModel, VectorIndex
from src.passage_matcher import find_target_chunk




markdown = pdf_to_markdown(
    "data/papers/attention_is_all_you_need.pdf"
)

# test split paragraphs
paragraphs = split_per_paragraphs(markdown)

print("Nombre de paragraphes :", len(paragraphs))

#for paragraph in paragraphs[:10]:
#    print("----")
#    print(paragraph[:500])


# test fonction chunking
chunks = create_chunks(paragraphs)

#print("\nNombre de chunks :", len(chunks))

#for chunk in chunks[:5]:
#    print("----")
#    print("ID :", chunk["id"])
#    print("Text :", chunk["text"][:300])

# Test embedding
model = EmbeddingModel()

texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts)

print("\nShape des embeddings :", embeddings.shape)
assert embeddings.shape == (len(chunks), 384)


# Test FAISS index
dimension = embeddings.shape[1]

vector_index = VectorIndex(dimension)
vector_index.add(embeddings)

print("Nombre de vecteurs dans l'index :", vector_index.index.ntotal)
assert vector_index.index.ntotal == len(chunks)


# Test d'une recherche
query = ["An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors."]

query_embedding = model.encode(query)

scores, indices = vector_index.search(query_embedding, k=5)

print("\nIndices trouvés :", indices)
print("Scores :", scores)
for rank, index in enumerate(indices[0]):
    print("\n----")
    print("Rank :", rank + 1)
    print("Chunk ID :", index)
    print("Score :", scores[0][rank])
    print("Text :", chunks[index]["text"][:500])
# Problème : le 1er trouvé c'est exactement le même passage du coup

print("==============================")

# Test passage matcher
target_passage = """
An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.
"""

chunk, score = find_target_chunk(target_passage, chunks
)

print("\nBest matching chunk")
print("Score :", score)
print("Chunk :", chunk)

assert chunk is not None
assert score > 0