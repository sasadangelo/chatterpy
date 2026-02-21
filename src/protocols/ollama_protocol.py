# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Any

from core import LoggerManager, chatterpy_config
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from protocols.protocol import LLMProtocol

OLLAMA_PARAM_MAP: dict[str, str] = {
    "max_tokens": "num_predict",
    "context_size": "num_ctx",
}


def translate_parameters(
    parameters: dict[str, Any],
    mapping: dict[str, str],
) -> dict[str, Any]:
    """
    Translate semantic config parameters into Ollama-specific parameters.
    Unknown parameters are passed through unchanged.
    """
    return {mapping.get(key, key): value for key, value in parameters.items() if value is not None}


class OllamaProtocol(LLMProtocol):
    _logger = LoggerManager.get_logger(name=__name__)

    def create_protocol(self) -> None:
        model: str = chatterpy_config.protocol.model.name
        base_url: str = chatterpy_config.protocol.api_url
        self._logger.info(f"Ollama protocol: model={model} - url={base_url}")
        # Translate semantic parameters into Ollama-specific
        params: dict[str, Any] = translate_parameters(
            parameters=chatterpy_config.protocol.model.parameters,
            mapping=OLLAMA_PARAM_MAP,
        )
        # Log LLM parameters
        if params:
            self._logger.info(f"Ollama parameters: {params}")
        else:
            self._logger.info("Ollama parameters: (none)")

        # Create the protocol with the parameters
        self._protocol = ChatOllama(
            model=model,
            base_url=base_url,
            **params,
        )

    def invoke(self, messages: LanguageModelInput) -> AIMessage:
        return self._protocol.invoke(input=messages)
