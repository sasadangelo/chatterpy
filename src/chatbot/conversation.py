# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Any
from memory.memory_factory import MemoryFactory
from langchain_core.messages import HumanMessage, AIMessage


# This class represents a generic chatbot conversion.
# It contains the chat history of the messages and the cost of each one.
class Conversation:
    def __init__(self, config: dict) -> None:
        """
        Initialize the conversation with a memory backend based on the config.
        """
        self.config = config
        self._initialize_conversation(config)

    def _initialize_conversation(self, config: dict) -> None:
        """
        Create or reset the conversation memory.
        """
        self.config = config
        self.conversation = MemoryFactory.get_memory(config)

    def save_interaction(self, user_message: HumanMessage, ai_message: AIMessage) -> None:
        """
        Save user and AI messages into the memory.
        """
        self.conversation.save_context({"input": user_message.content}, {"output": ai_message.content})

    def get_chat_history_messages(self) -> Any:
        """
        Retrieve chat history messages from memory.
        Returns either a string or a list depending on memory implementation.
        """
        return self.conversation.load_memory_variables({}).get("history", "")

    def clear(self) -> None:
        """
        Clear the conversation history.
        """
        self._initialize_conversation(self.config)
