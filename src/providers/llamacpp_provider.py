# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
import os
from typing import Any, Dict, List
from langchain_community.llms.llamacpp import LlamaCpp
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

# Provider-specific default configuration for LlamaCpp
DEFAULTS_LLAMACPP_LLM_CONFIG: Dict[str, Any] = {
    "temperature": 0.2,
    "max_tokens": 16,
    "top_p": 0.95,
    "context_size": 512,
}


class LLamaCppProvider(LLMProvider):
    def create_model(self) -> None:
        """
        Initializes the LlamaCpp model with merged configuration parameters.

        Merges global defaults, provider-specific defaults, and user-provided config.
        Expands the transformers path and creates the LlamaCpp model instance.
        """
        model_path = self.config["model_path"]
        chat_format = self.config["chat_format"]

        # Start with global default parameters
        parameters: Dict[str, Any] = DEFAULTS_LLM_CONFIG.copy()
        # Override with LlamaCpp specific defaults
        parameters.update(DEFAULTS_LLAMACPP_LLM_CONFIG)
        # Finally override with any user-provided parameters from config file
        parameters.update(self.config.get("parameters", {}))

        # Log final parameters if debugging is enabled
        self._debug_log("Model parameters::", *(f"- {k}: {v}" for k, v in parameters.items()))

        # Expand user path to absolute path for transformers/models
        transformers_path = os.path.expanduser(self.config["transformers_path"])
        # Initialize the LlamaCpp model with the full model path and chat format
        self.model = LlamaCpp(
            model_path=transformers_path + "/" + model_path,
            chat_format=chat_format,
            n_ctx=parameters["context_size"],
        )

    def generate(self, messages: List[BaseMessage]) -> str:
        """
        Generate a response using the LlamaCpp model, from a list of BaseMessage instances.

        The messages are converted into a plain prompt string with role prefixes,
        which is suitable for LlamaCpp's plain text interface.
        """
        prompt_parts = []

        # Extract system message if present
        system_message = next((m for m in messages if isinstance(m, SystemMessage)), None)
        if system_message:
            prompt_parts.append(system_message.content.strip())

        # Identify latest user message (usually the last one)
        user_message = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)
        chat_history = [m for m in messages if m not in (system_message, user_message)]

        # Add all previous assistant/user exchanges before the latest question
        for msg in chat_history:
            if isinstance(msg, HumanMessage):
                prompt_parts.append(f"User: {msg.content.strip()}")
            elif isinstance(msg, AIMessage):
                prompt_parts.append(f"Assistant: {msg.content.strip()}")

        # Add final user message
        if user_message:
            prompt_parts.append(f"User: {user_message.content.strip()}")

        # Add assistant prefix as signal for generation
        prompt_parts.append("Assistant:")

        # Compose final prompt
        prompt = "\n".join(prompt_parts)

        self._debug_log("Prompt:", prompt)

        result = self.model.invoke(prompt)
        return result
