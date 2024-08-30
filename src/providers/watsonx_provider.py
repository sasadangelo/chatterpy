from typing import Union
from providers.provider import LLMProvider
from langchain_ibm import WatsonxLLM

class WatsonXProvider(LLMProvider):
    def create_model(self):
        self.url = self.config["api_url"]
        self.project_id = self.config["project_id"]
        self.parameters = self.config.get("parameters", {})

        self.model = WatsonxLLM(
            model_id=self.config["model"],
            url=self.url,
            project_id=self.project_id,
            params=self.parameters
        )

    def generate(self, prompt):
        if self.config['debug'] == True:
            print("****************************************************************")
            print("Prompt:")
            print(prompt)
            print("****************************************************************")
        return self.model.invoke(prompt)
