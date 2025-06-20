# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Any, Dict, List
from langchain_core.messages import BaseMessage

# Default configuration values for all LLM providers.
# These can be overridden by provider-specific or user-defined settings.
DEFAULTS_LLM_CONFIG: Dict[str, Any] = {
    "temperature": 0.7,
    "max_tokens": 200,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "context_size": 2048,
}


class LLMProvider:
    def __init__(self, config: dict) -> None:
        """
        Base class constructor for all LLM providers.
        It stores the configuration and initializes the model.
        """
        self.config = config
        self.create_model()

    def _debug_log(self, *args: Any) -> None:
        """
        Print debug information if 'debug' is enabled in the config.
        Supports printing plain values as well as lists of BaseMessage instances.
        """
        if self.config.get("debug", False):
            print("****************************************************************")
            for arg in args:
                if isinstance(arg, list) and all(isinstance(m, BaseMessage) for m in arg):
                    print("Chat messages:")
                    for i, msg in enumerate(arg, 1):
                        print(f"  {i}. [{msg.type}] {msg.content}")
                else:
                    print(arg)
            print("****************************************************************")

    def create_model(self) -> None:
        """
        Abstract method to be implemented by subclasses.
        Responsible for initializing the provider-specific model.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Abstract method to be implemented by subclasses.
        Accepts a prompt string and returns the model's generated output.
        """
        raise NotImplementedError("Subclasses should implement this method.")
