# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from prompts.granite_prompt_formatter import GranitePromptFormatter
from prompts.plain_prompt_formatter import PlainPromptFormatter
from prompts.prompt_formatter import PromptFormatter

DEFAULT_PROMPT_FORMATTER = "plain"


class PromptFormatterFactory:
    """
    Factory singleton class for creating or retrieving a PromptFormatter instance
    based on configuration.
    """

    _instance: PromptFormatter = None

    @staticmethod
    def get_prompt_formatter(config: dict) -> PromptFormatter:
        """
        Returns a singleton instance of the prompt formatter.

        Args:
            config (dict): Configuration dictionary containing 'prompt_formatter' key.

        Returns:
            PromptFormatter: The configured prompt formatter instance.
        """
        if PromptFormatterFactory._instance is None:
            prompt_formatter = config.get("prompt_formatter", DEFAULT_PROMPT_FORMATTER)
            providers = {
                "plain": PlainPromptFormatter,
                "granite": GranitePromptFormatter,
            }
            formatter_class = providers.get(prompt_formatter, PlainPromptFormatter)
            PromptFormatterFactory._instance = formatter_class()
        return PromptFormatterFactory._instance
