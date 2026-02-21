# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Any

from core import LoggerManager, chatterpy_config
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from protocols.protocol import LLMProtocol


# To use ChatGPT 3.5 set protocol.name="gpt-3.5-turbo" and protocol.api_url="https://api.openai.com/v1" in the
# config.yml. To use ChatGPT 4 set protocol.name="gpt-4" and protocol.api_url="https://api.openai.com/v1" in the
# config.yml
class OpenAIProtocol(LLMProtocol):
    _logger = LoggerManager.get_logger(name=__name__)

    def create_protocol(self):
        model: str = chatterpy_config.protocol.model.name
        base_url: str = chatterpy_config.protocol.api_url
        params = dict(chatterpy_config.protocol.model.parameters)

        # Non standard parameters / OpenAI-incompatible
        model_kwargs = {}

        if "repeat_penalty" in params:
            # OpenAI API calls it frequency_penalty
            model_kwargs["frequency_penalty"] = params.pop("repeat_penalty")

        # Log modello, URL e parametri
        self._logger.info(f"OpenAI protocol: model={model} - url={base_url}")

        # Log parameters
        if params:
            self._logger.info(f"OpenAI parameters: {params}")
        else:
            self._logger.info("OpenAI parameters: (none)")

        # Log model_kwargs se presenti
        if model_kwargs:
            self._logger.info(f"OpenAI model_kwargs: {model_kwargs}")

        # Make sure all the parameters are compatible string/numbers/bool
        params_clean: dict[str, Any] = {k: v for k, v in params.items() if v is not None}
        params_clean.update(model_kwargs)

        params.update(model_kwargs)
        self._protocol = ChatOpenAI(
            model=model,
            base_url=base_url,
            **params_clean,  # Only OpenAI-valid parameters
        )

    def invoke(self, messages: LanguageModelInput) -> AIMessage:
        return self._protocol.invoke(input=messages)
