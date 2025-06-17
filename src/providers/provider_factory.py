# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from providers.llamacpp_provider import LLamaCppProvider
from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.watsonx_provider import WatsonXProvider


class LLMProviderFactory:
    providers = {
        "llamacpp": LLamaCppProvider,
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "watsonx": WatsonXProvider,
    }

    # The single provider instance
    _instance = None

    @classmethod
    def get_provider(cls, config):
        # If the instance already exists, return it
        if cls._instance is not None:
            return cls._instance

        # Otherwise, create it
        provider_name = config["provider"]
        provider_class = cls.providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider_name}")
        cls._instance = provider_class(config)
        return cls._instance
