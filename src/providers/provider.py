class LLMProvider:
    def __init__(self, config):
        self.config = config
        self.create_model()

    def create_model(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def generate(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")
