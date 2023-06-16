import faiss
import pandas
import torch

from models.Embedders.miniLM import Embedder
from tools.text_extractor import *


class Document:
    def __init__(self, name, content=None, path=None, delimiter='\n'):
        self.embedder = Embedder()
        self.name = name
        self.content = content
        self.path = path
        self.delimiter = delimiter

        self.df = None
        self.index = None

        if self.path is not None:
            self.extract_content()
            self.make_df()
            self.make_index()
        elif self.content is not None:
            self.make_df()
            self.make_index()

    def extract_content(self):
        text = text_from_pdf(self.path)
        # Join pages
        text = '\n'.join(text)
        text = text.replace('-\n', '')
        text = text.split(self.delimiter)
        self.content = text

    def make_df(self):
        self.df = pandas.DataFrame(self.content, columns=['text'])
        embeddings_dataset = self.embedder.encode_batch(self.df['text'].tolist())
        self.df['embeddings'] = [embeddings_dataset[i].tolist() for i in range(len(embeddings_dataset))]

    def make_index(self):
        embeddings_tensor = torch.stack(
            [torch.Tensor(self.df["embeddings"][i]) for i in range(len(self.df["embeddings"]))])
        self.index = faiss.IndexFlatL2(embeddings_tensor.shape[1])
        self.index.add(embeddings_tensor.numpy())

    def edit_splitting(self, delimiter):
        self.delimiter = delimiter
        self.extract_content()
        self.make_df()
        self.make_index()

    def search(self, query, k=2):
        query_embedding = self.embedder.encode(query)
        query_embedding = torch.Tensor(query_embedding).unsqueeze(0)
        query_embedding = query_embedding.numpy()

        D, I = self.index.search(x=query_embedding, k=k)
        retrieved = ""
        for i in range(k):
            retrieved += self.df["text"][I[0][i]]
            if i != k - 1:
                retrieved += self.delimiter
        return retrieved
