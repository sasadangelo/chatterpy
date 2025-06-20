# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Any, Dict, List
from langchain_community.llms.ollama import Ollama
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG
from requests.exceptions import ConnectionError as RequestsConnectionError
from langchain_core.messages import BaseMessage

DEFAULT_OLLAMA_LLM_CONFIG: Dict[str, Any] = {
    "temperature": 0.8,
    "max_tokens": 128,
}


class OllamaProvider(LLMProvider):
    def create_model(self) -> None:
        model_name = self.config["model"]
        base_url = self.config["base_url"]

        parameters: Dict[str, Any] = DEFAULTS_LLM_CONFIG.copy()
        parameters.update(DEFAULT_OLLAMA_LLM_CONFIG)
        parameters.update(self.config.get("parameters", {}))

        self._debug_log("Model parameters::", *(f"- {k}: {v}" for k, v in parameters.items()))

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

    def generate(self, messages: List[BaseMessage]) -> str:
        """
        Generate a response from the Ollama model given a list of chat messages.

        Each message is a dict with keys: 'role' (system, user, assistant) and 'content'.

        This method converts the messages into a prompt text before invoking the model.
        """
        self._debug_log("Prompt:", messages)
        try:
            return self.model.invoke(messages)
        except RequestsConnectionError as e:
            self._debug_log("Ollama server connection error:", str(e))
            raise RuntimeError(
                "❌ The language model server (Ollama) is currently unavailable.\n"
                "➡️ Make sure it's running at http://localhost:11434 and try again."
            ) from e
