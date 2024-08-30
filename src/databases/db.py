class Database:
    def store(self, chunks, embeddings):
        raise NotImplementedError("Subclasses must implement the store method")