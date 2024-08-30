from embeddings.embedding_provider import EmbeddingProvider
from langchain_community.embeddings import OllamaEmbeddings

class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config):
        model_name = config['embedding_model']
        self.embeddings = OllamaEmbeddings(model=model_name)
