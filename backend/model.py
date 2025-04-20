from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Recommender:
    def __init__(self, assessments):
        self.assessments = assessments
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # 384 is the embedding size for MiniLM
        self.embeddings = self.model.encode([a["description"] for a in assessments])
        self.index.add(np.array(self.embeddings))

    def recommend(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(np.array(query_embedding), top_k)
        return [self.assessments[i] for i in indices[0]]
