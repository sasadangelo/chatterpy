# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts.prompt_formatter import PromptFormatter
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage


class PlainPromptFormatter(PromptFormatter):
    """
    Plain prompt formatter that combines context and chat history with
    user message into a simple text prompt.
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

    def __init__(self) -> None:
        self.__chat_prompt_template = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    def get_prompt(
        self,
        context: str,
        system_message: SystemMessage,
        chat_history_messages: List[BaseMessage],
        user_message: HumanMessage,
    ) -> str:
        # Format chat history separately
        chat_history = self.__chat_prompt_template.format(messages=chat_history_messages)

        return PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["system_message", "context", "chat_history", "user_message"],
        ).format(
            system_message=system_message.content,
            context=context or "",
            chat_history=chat_history or "",
            user_message=user_message.content,
        )
