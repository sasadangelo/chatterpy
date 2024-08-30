from typing import Union
from langchain.prompts import PromptTemplate
from prompts.prompt_formatter import PromptFormatter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class GranitePromptFormatter(PromptFormatter):
    PROMPT_TEMPLATE = (
    "Use the following pieces of context enclosed by triple backquote to answer the question at the end.\n"
    "Don't mention the word 'context' in the answer.\n\n"
    "Context:\n"
    "```\n"
    "{context}\n"
    "```\n\n"
    "Question: {user_message}\n"
    "Answer:")

    def get_prompt(self, context, system_message, chat_history_messages, user_message):
        chat_messages = [system_message] + chat_history_messages
        chat_history = self.__granite_v2_prompt(chat_messages)
        combined_context = f"{context or ''}\n{chat_history or ''}"
        return PromptTemplate(template=self.PROMPT_TEMPLATE, input_variables=["context", "chat_history", "user_message"]).format(context=combined_context, user_message=user_message.content)

    # This method creates the Granite v2 prompt for the model starting from a message list like this:
    #
    # [
    #   SystemMessage,
    #   HumanMessage,
    #   AIMessage,
    #   HumanMessage,
    #   AIMessage,
    #   HumanMessage,
    #   ...
    # ]
    #
    # It returns a string like this:
    #
    # <|system|>
    # {system_message}
    # <|user|>
    # {user_message_1}
    # <|assistant|>
    # {assistant_message_1}
    # <|user|>
    # {user_message_2}
    # <|assistant|>
    # {assistant_message_1}
    # <|user|>
    # {user_message_3}
    def __granite_v2_prompt(self, chat_messages) -> str:
        # Construct the prompt by iterating through the messages
        prompt = []
        for message in chat_messages:
            prompt.append(self.__get_role(message))
            prompt.append(message.content)
        return '\n'.join(prompt)

    # Depending on message type in input it returns:
    # - system
    # - user
    # - assistant
    def __get_role(self, message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
        if isinstance(message, HumanMessage):
            return "<|user|>"
        elif isinstance(message, AIMessage):
            return "<|assistant|>"
        else:
            return "<|system|>"
