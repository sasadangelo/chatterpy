import os
import pprint
from typing import List, Union
from providers.provider import LLMProvider
from langchain_community.llms import LlamaCpp

DEFAULT_MAX_TOKENS=16
DEFAULT_TEMPERATURE=0.2
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40
DEFAULT_REPEAT_PENALTY=1.1
DEFAULT_CONTEXT_SIZE=512

class LLamaCppProvider(LLMProvider):
    def create_model(self):
        model_path = self.config['model_path']
        chat_format = self.config['chat_format']

        # Set the default parameters
        self.parameters = {
            'max_tokens': DEFAULT_MAX_TOKENS,
            'temperature': DEFAULT_TEMPERATURE,
            'top_p': DEFAULT_TOP_P,
            'top_k': DEFAULT_TOP_K,
            'repeat_penalty': DEFAULT_REPEAT_PENALTY,
            'context_size': DEFAULT_CONTEXT_SIZE,
        }

        # Overwrite default values with the one in the YAML file
        if 'parameters' in self.config:
            self.parameters.update(self.config['parameters'])

        if self.config['debug'] == True:
            print("****************************************************************")
            print("Model parameters::                                              ")
            print("- max_tokens:", self.parameters['max_tokens'])
            print("- temperature:", self.parameters['temperature'])
            print("- top_p:", self.parameters['top_p'])
            print("- top_k:", self.parameters['top_k'])
            print("- repeat_penalty:", self.parameters['repeat_penalty'])
            print("- context_size:", self.parameters['context_size'])
            print("****************************************************************")

        transformers_path = os.path.expanduser(self.config['transformers_path'])
        self.model = LlamaCpp(model_path=transformers_path + "/" + model_path, chat_format=chat_format, n_ctx=self.parameters['context_size'])

    def generate(self, prompt):
        print("****************************************************************")
        print("Prompt:")
        print(prompt)
        print("****************************************************************")
        result = self.model.invoke(prompt)
        return result
