import sentence_transformers
import torch


class Embedder:
    def __init__(self):
        # self.model = sentence_transformers.SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1").to("cuda")
        self.model = sentence_transformers.SentenceTransformer("sentence-transformers/msmarco-MiniLM-L6-cos-v5").to("cuda")
        self.model.eval()

    def encode(self, sentence):
        embeddings = self.model.encode(sentence)
        embeddings = torch.as_tensor(embeddings)
        return embeddings

    def encode_batch(self, sentences):
        embeddings = []
        for sentence in sentences:
            embeddings.append(self.encode(sentence))

        embeddings = torch.stack(embeddings)
        return embeddings

    def get_dim(self):
        return self.model.get_sentence_embedding_dimension()
