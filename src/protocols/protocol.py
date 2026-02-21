# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod

from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import AIMessage


class LLMProtocol(ABC):
    def __init__(self) -> None:
        self.create_protocol()

    @abstractmethod
    def create_protocol(self) -> None:
        """Initialize the protocol client or model."""
        pass

    @abstractmethod
    def invoke(self, messages: LanguageModelInput) -> AIMessage:
        """Send a message to the LLM and return the AI response."""
        pass
