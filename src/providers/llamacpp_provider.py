import os
import pprint
from typing import List, Union
from providers.provider import LLMProvider
from llama_cpp import Llama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

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
        self.system_message = self.config['system_message']

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
        self.model = Llama(model_path=transformers_path + "/" + model_path, chat_format=chat_format, n_ctx=self.parameters['context_size'])

    def generate(self, chat_history_messages, user_message):
        # Concatenate the user message to the chat history to create a context for the LLM
        chat_messages = chat_history_messages + [user_message]
        format_messages = self.__format_messages(chat_messages)
        if self.config['debug'] == True:
            pprint.pprint("****************************************************************")
            pprint.pprint("Prompt:")
            pprint.pprint(format_messages)
            pprint.pprint("****************************************************************")
        result = self.model.create_chat_completion(format_messages,
                                                   max_tokens=self.parameters['max_tokens'],
                                                   temperature=self.parameters['temperature'],
                                                   top_p=self.parameters['top_p'],
                                                   top_k=self.parameters['top_k'],
                                                   repeat_penalty=self.parameters['repeat_penalty'])
        return result['choices'][0]['message']['content']

    # Depending on message type in input it returns:
    # - system
    # - user
    # - assistant
    def __get_role(self, message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
        if isinstance(message, HumanMessage):
            return "user"
        elif isinstance(message, AIMessage):
            return "assistant"
        else:
            return "system"

    # Convert the prompt messages list format
    def __format_messages(self, messages: List[Union[SystemMessage, HumanMessage, AIMessage]]) -> List[dict]:
        formatted_messages = [{"role": "system", "content": self.system_message}]
        for message in messages:
            formatted_messages.append({"role": self.__get_role(message), "content": message.content})
        return formatted_messages
