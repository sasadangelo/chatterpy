# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Any, Dict
from langchain_community.llms import Ollama
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG
from requests.exceptions import ConnectionError as RequestsConnectionError

# Ollama-specific default parameters that override the global defaults
DEFAULT_OLLAMA_LLM_CONFIG: Dict[str, Any] = {
    "temperature": 0.8,
    "max_tokens": 128,
}


class OllamaProvider(LLMProvider):
    def create_model(self) -> None:
        """
        Initialize the Ollama model instance with the merged configuration parameters.

        The parameter precedence is: global defaults < Ollama-specific defaults < user config.
        """
        model_name = self.config["model"]
        base_url = self.config["base_url"]

        # Start with global default parameters
        parameters: Dict[str, Any] = DEFAULTS_LLM_CONFIG.copy()
        # Override with Ollama-specific default parameters
        parameters.update(DEFAULT_OLLAMA_LLM_CONFIG)
        # Override with user-provided parameters from the config file
        parameters.update(self.config.get("parameters", {}))

        # Log the final parameters if debug is enabled
        self._debug_log("Model parameters::", *(f"- {k}: {v}" for k, v in parameters.items()))

        # Instantiate the Ollama model with the specified parameters
        self.model = Ollama(
            model=model_name,
            base_url=base_url,
            temperature=parameters["temperature"],
            num_predict=parameters["max_tokens"],
            top_p=parameters["top_p"],
            top_k=parameters["top_k"],
            repeat_penalty=parameters["repeat_penalty"],
            num_ctx=parameters["context_size"],
        )

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the Ollama model given an input prompt.

        Logs the prompt if debugging is enabled and returns the generated text.
        """
        self._debug_log("Prompt:", prompt)
        try:
            result = self.model.invoke(prompt)
            return result
        except RequestsConnectionError as e:
            # Log the error (optional)
            self._debug_log("Ollama server connection error:", str(e))
            raise RuntimeError(
                "❌ The language model server (Ollama) is currently unavailable.\n"
                "➡️ Make sure it's running at http://localhost:11434 and try again."
            ) from e
