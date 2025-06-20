# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from langchain_openai import ChatOpenAI
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG
from langchain_core.messages import BaseMessage


# Make sure you have a Python 3 virtual environment active:
# $ source venv/bin/activate
#
# Make sure you installed the following dependencies:
# $ (venv) pip3 install llama_cpp_python
# $ (venv) pip3 install sse_starlette
# $ (venv) pip3 install starlette_context
# $ (venv) pip3 install pydantic_settings
# $ (venv) pip3 install fastapi
#
# Then run the llama.cpp server with the input mode:
# $ (venv) python3 -m llama_cpp.server --model <GGUF model path>


# To use ChatGPT 3.5 set model_name="gpt-3.5-turbo" and omit the parameter openai_api_base
# To use ChatGPT 4 set model_name="gpt-4" and omit the parameter openai_api_base
from typing import Any, Dict, List


class OpenAIProvider(LLMProvider):
    def create_model(self) -> None:
        """
        Initialize the OpenAI Chat model with configuration parameters.

        The parameters are merged from global defaults and any user overrides in the config.
        """
        model_name = self.config["model"]
        base_url = self.config["base_url"]

        # Start with global default parameters (these are typical OpenAI defaults)
        parameters: Dict[str, Any] = DEFAULTS_LLM_CONFIG.copy()
        # Override with user-provided parameters from the config file
        parameters.update(self.config.get("parameters", {}))

        # Log the final parameters if debug is enabled
        self._debug_log("Model parameters::", *(f"- {k}: {v}" for k, v in parameters.items()))

        # Instantiate the ChatOpenAI model with the specified parameters
        self.model: ChatOpenAI = ChatOpenAI(
            temperature=parameters["temperature"],
            max_tokens=parameters["max_tokens"],
            model_name=model_name,
            openai_api_base=base_url,
            model_kwargs={
                "top_p": parameters["top_p"],
                "frequency_penalty": parameters["repeat_penalty"],
            },
        )

    def generate(self, messages: List[BaseMessage]) -> str:
        """
        Generate a response from OpenAI model given a list of chat messages.

        messages: list of dicts with keys: 'role' ('system','user','assistant'), 'content' (str).
        """
        self._debug_log("Messages:", messages)

        # Pass directly the messages to the model native chat
        response = self.model.chat(messages)  # oppure .invoke(messages) a seconda della libreria
        return response.content
