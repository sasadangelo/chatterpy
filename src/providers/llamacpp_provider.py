# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
import os
from typing import Any, Dict
from langchain_community.llms import LlamaCpp
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG

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

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LlamaCpp model given an input prompt.

        Logs the prompt if debugging is enabled and returns the model's output string.
        """
        self._debug_log("Prompt:", prompt)
        result = self.model.invoke(prompt)
        return result
