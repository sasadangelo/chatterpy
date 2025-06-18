# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
import os
from typing import Any, Dict
from langchain_ibm import WatsonxLLM
from providers.provider import LLMProvider, DEFAULTS_LLM_CONFIG

# WatsonX-specific default parameters overriding the global defaults,
# including some extra parameters like min_new_tokens and decoding_method.
DEFAULTS_WATSONX_LLM_CONFIG: Dict[str, Any] = {
    "temperature": 0.2,
    "max_tokens": 900,
    "repeat_penalty": 1.05,
    "context_size": 8192,
    "min_new_tokens": 1,
    "decoding_method": "sample",
}


class WatsonXProvider(LLMProvider):
    def _map_config_keys_for_watsonx(self, params: dict) -> dict:
        """
        Map generic parameter names to WatsonX-specific parameter names.

        For example, 'max_tokens' is mapped to 'max_new_tokens' as required by WatsonX.
        """
        mapping = {
            "max_tokens": "max_new_tokens",
        }
        return {mapping.get(k, k): v for k, v in params.items()}

    def create_model(self) -> None:
        """
        Create and initialize the WatsonX LLM model instance.

        The parameters are merged in the order: global defaults -> WatsonX-specific defaults -> user config (mapped).
        """
        # Step 1: Read the user parameters from config
        config_params = self.config.get("parameters", {})

        # Step 2: Convert generic parameters to WatsonX-specific names
        mapped_config_params = self._map_config_keys_for_watsonx(config_params)

        # Step 3: Merge parameters with proper precedence
        parameters: Dict[str, Any] = DEFAULTS_LLM_CONFIG.copy()
        parameters.update(DEFAULTS_WATSONX_LLM_CONFIG)
        parameters.update(mapped_config_params)

        self.parameters = parameters

        # Instantiate the WatsonX LLM with required settings
        self.model = WatsonxLLM(
            model_id=self.config["model"],
            url=self.config["api_url"],
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            params=self.parameters,
        )

    def generate(self, prompt: str) -> str:
        """
        Generate text from the WatsonX model for the given prompt.

        Logs the prompt if debug is enabled and returns the generated text.
        """
        self._debug_log("Prompt:", prompt)
        return self.model.invoke(prompt)
