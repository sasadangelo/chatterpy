# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, get_buffer_string, trim_messages
from langchain_core.messages.base import BaseMessage
from protocols import LLMProtocol


class BaseChatMemoryStrategy(ABC):
    """Abstract base class for defining message processing strategies."""

    @abstractmethod
    def process_messages(
        self,
        system_message: SystemMessage,
        history_messages: list[BaseMessage],
    ) -> list[BaseMessage]:
        """
        Process and format the conversation history.

        Args:
            system_message: The core instructions for the AI.
            history_messages: The list of previous chat messages.

        Returns:
            A formatted list of messages to be sent to the LLM.
        """
        pass


class BufferMemoryStrategy(BaseChatMemoryStrategy):
    """Strategy that keeps the entire conversation history (Full Buffer)."""

    def process_messages(self, system_message: SystemMessage, history_messages: list[BaseMessage]) -> list[BaseMessage]:
        # Simply prepend the system message to the full history
        return [system_message] + history_messages


class WindowMemoryStrategy(BaseChatMemoryStrategy):
    """
    Strategy that keeps only the last 'k' conversation exchanges (Human+AI pairs).

    For example, window=3 means keep the last 3 exchanges (6 messages total).
    """

    def __init__(self, window: int) -> None:
        self._window = window  # Number of exchanges (Human+AI pairs) to retain

    def process_messages(self, system_message: SystemMessage, history_messages: list[BaseMessage]) -> list[BaseMessage]:
        # Calculate max_tokens as window * 2 (each exchange = Human + AI message)
        max_messages: int = self._window * 2

        # Trim messages based on count (token_counter=len)
        # We ensure the window starts with a HumanMessage for better LLM performance
        trimmed_history: list[BaseMessage] = trim_messages(
            history_messages,
            strategy="last",
            token_counter=len,
            max_tokens=max_messages,
            start_on="human",
            include_system=False,
        )
        # System message must stay at the top (index 0) to maintain context priority
        return [system_message] + trimmed_history


class SummaryMemoryStrategy(BaseChatMemoryStrategy):
    """Strategy that summarizes older messages to save context space."""

    def __init__(self, protocol: LLMProtocol):
        self._protocol: LLMProtocol = protocol

    def process_messages(self, system_message: SystemMessage, history_messages: list[BaseMessage]) -> list[BaseMessage]:
        # If the history is short (e.g., <= 4 messages), return as is to avoid unnecessary API calls
        if len(history_messages) <= 4:
            return [system_message] + history_messages

        # Split history: everything except the last 2 messages will be summarized
        to_summarize: list[BaseMessage] = history_messages[:-2]
        last_exchange: list[BaseMessage] = history_messages[-2:]

        # Explicitly request a summary in English
        summary_prompt: str = (
            "Summarize the following conversation history concisely in English. "
            f"Focus on key facts and context: {get_buffer_string(messages=to_summarize)}"
        )

        # Generate the summary using the provided LLM protocol
        summary_response: AIMessage = self._protocol.invoke(messages=[HumanMessage(content=summary_prompt)])

        # Extract content as string (handle both str and list types)
        summary_content: str = (
            summary_response.content if isinstance(summary_response.content, str) else str(summary_response.content)
        )

        # Create a SystemMessage to hold the condensed historical context
        summary_msg: SystemMessage = SystemMessage(content=f"Summary of previous interactions: {summary_content}")

        # Final structure: [Core Instructions] + [Historical Summary] + [Latest Messages]
        return [system_message, summary_msg] + last_exchange
