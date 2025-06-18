# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Any, Dict
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.memory.chat_memory import BaseChatMemory
from providers.provider_factory import LLMProviderFactory

DEFAULT_CHAT_HISTORY_MEMORY = "buffer"


class MemoryFactory:
    """
    Factory to create chat memory instances based on configuration.
    Supports types: buffer, window, summary.
    """

    @staticmethod
    def get_memory(config: Dict[str, Any]) -> BaseChatMemory:
        """
        Returns an instance of BaseChatMemory based on the 'chat_history_memory' config.

        Args:
            config (dict): Configuration dictionary that may include:
                - chat_history_memory: type of memory ('buffer', 'window', 'summary')
                - chat_history_memory_window: window size for 'window' memory

        Raises:
            ValueError: if the memory type is unknown

        Returns:
            BaseChatMemory: instantiated memory object
        """
        memory_type = config.get("chat_history_memory", DEFAULT_CHAT_HISTORY_MEMORY)

        if memory_type == "buffer":
            return ConversationBufferMemory(return_messages=True)
        elif memory_type == "window":
            window_size = config.get("chat_history_memory_window", 5)
            return ConversationBufferWindowMemory(k=window_size, return_messages=True)
        elif memory_type == "summary":
            provider = LLMProviderFactory.get_provider(config)
            if not provider or not hasattr(provider, "model") or provider.model is None:
                raise RuntimeError("LLM provider or model not initialized for summary memory.")
            return ConversationSummaryMemory(llm=provider.model, return_messages=True)
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")
