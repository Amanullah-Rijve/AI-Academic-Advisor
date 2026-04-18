import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

class VectorStore:
    def __init__(self):
        self.texts = []
        self.index = faiss.IndexFlatL2(384)  # embedding size

    def add_documents(self, chunks):
        embeddings = model.encode(chunks)

        self.texts = chunks
        self.index.add(np.array(embeddings).astype("float32"))

    def search(self, query, k=5):
        query_vec = model.encode([query])
        distances, indices = self.index.search(
            np.array(query_vec).astype("float32"), k
        )

        return [self.texts[i] for i in indices[0]]