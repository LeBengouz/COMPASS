from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# Create embeddings of the paragraphs

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def encode(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True)


# faiss used to find closest chunks to a text
class VectorIndex:
    def __init__(self, dimension):
        """
        dimension : int representing vector size of embeddings that FAISS will stock

        Inner Product used to measure similarity ~cosin similarity
        """
        self.index = faiss.IndexFlatIP(dimension)

    def add(self, embeddings):
        embeddings = np.asarray(embeddings, dtype="float32")
        self.index.add(embeddings)

    def search(self, query_embedding, k=5):
        query_embedding = np.asarray(query_embedding, dtype="float32")
        scores, indices = self.index.search(query_embedding, k)

        return scores, indices