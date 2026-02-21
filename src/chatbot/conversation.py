# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core import LoggerManager
from langchain_core.messages import SystemMessage
from langchain_core.messages.base import BaseMessage
from memory import BaseChatMemoryStrategy, MemoryFactory


class Conversation:
    """
    Manages the conversation history and applies memory strategies.

    This class maintains the chat history and uses a memory strategy
    to process messages before sending them to the LLM.
    """

    def __init__(self, system_message: str) -> None:
        """
        Initialize the conversation with a system message.

        Args:
            system_message: The system prompt that defines the AI's behavior
        """
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self._system_message = SystemMessage(content=system_message)
        self._history: list[BaseMessage] = []
        self._memory_strategy: BaseChatMemoryStrategy = MemoryFactory.get_memory()

        # Log the memory strategy name in a readable format
        strategy_name = self._memory_strategy.__class__.__name__.replace("MemoryStrategy", "")
        self._logger.info(f"Memory Strategy: {strategy_name}")

        # Log additional info for Window strategy
        if hasattr(self._memory_strategy, "_window"):
            window_size = getattr(self._memory_strategy, "_window")
            self._logger.info(f"Window Size: {window_size} exchanges ({window_size * 2} messages)")

    def add_message(self, message: BaseMessage) -> None:
        """
        Add a message to the conversation history.

        Args:
            message: A LangChain message (HumanMessage, AIMessage, SystemMessage, etc.)
        """
        self._history.append(message)

    def get_messages_for_llm(self) -> list[BaseMessage]:
        """
        Get the processed messages to send to the LLM.

        This method applies the configured memory strategy to process
        the conversation history before sending it to the LLM.

        Returns:
            A list of messages processed according to the memory strategy
        """
        return self._memory_strategy.process_messages(
            system_message=self._system_message,
            history_messages=self._history,
        )

    def get_full_history(self) -> list[BaseMessage]:
        """
        Get the complete conversation history without processing.

        Returns:
            The full list of messages in the conversation
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear all conversation history (keeps system message)."""
        self._history.clear()

    def get_message_count(self) -> int:
        """
        Get the number of messages in the conversation history.

        Returns:
            The count of messages (excluding system message)
        """
        return len(self._history)
