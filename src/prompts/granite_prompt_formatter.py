# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Union, List
from langchain.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from prompts.prompt_formatter import PromptFormatter


class GranitePromptFormatter(PromptFormatter):
    """
    Granite prompt formatter that generates a prompt in the Granite v2 format.
    """

    PROMPT_TEMPLATE = (
        "{system_message}\n\n"
        "Use the following pieces of context enclosed by triple backquote to answer the question at the end.\n"
        "Don't mention the word 'context' in the answer.\n\n"
        "Context:\n"
        "```\n"
        "{context}\n"
        "```\n\n"
        "Chat history:\n"
        "{chat_history}\n\n"
        "Question: {user_message}\n"
        "Answer:"
    )

    def get_prompt(
        self,
        context: str,
        system_message: SystemMessage,
        chat_history_messages: List[BaseMessage],
        user_message: HumanMessage,
    ) -> str:
        """
        Format the prompt by combining the system message, context, chat history and user message.
        """
        # Generate chat history in Granite format excluding system message
        chat_history = self.__granite_v2_prompt(chat_history_messages)
        return PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["system_message", "context", "chat_history", "user_message"],
        ).format(
            system_message=system_message.content,
            context=context or "",
            chat_history=chat_history or "",
            user_message=user_message.content,
        )

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
        """
        Converts chat messages into the Granite v2 prompt format by prepending
        special tokens for roles.

        Args:
            chat_messages (List[BaseMessage]): List of chat messages.

        Returns:
            str: Granite v2 formatted prompt string.
        """
        # Construct the prompt by iterating through the messages
        prompt = []
        for message in chat_messages:
            prompt.append(self.__get_role(message))
            prompt.append(message.content)
        return "\n".join(prompt)

    # Depending on message type in input it returns:
    # - system
    # - user
    # - assistant
    def __get_role(self, message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
        """
        Returns the Granite role token for a given message.

        Args:
            message (BaseMessage): The message object.

        Returns:
            str: Role token string like '<|user|>', '<|assistant|>', or '<|system|>'.
        """
        if isinstance(message, HumanMessage):
            return "<|user|>"
        elif isinstance(message, AIMessage):
            return "<|assistant|>"
        else:
            return "<|system|>"
