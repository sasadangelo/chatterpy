# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage


class PromptFormatter:
    """
    Base class/interface for all prompt formatter implementations.
    """

    def get_prompt(
        self,
        context: str,
        system_message: SystemMessage,
        chat_history_messages: List[BaseMessage],
        user_message: HumanMessage,
    ) -> str:
        """
        Generate the final prompt string given the context, system message,
        chat history, and current user message.

        Args:
            context (str): Contextual information (e.g., retrieved documents).
            system_message (SystemMessage): The initial system message.
            chat_history_messages (List[BaseMessage]): List of prior conversation messages.
            user_message (HumanMessage): The latest user message.

        Returns:
            str: Formatted prompt string ready for model input.
        """
        raise NotImplementedError("Subclasses must implement the get_prompt method.")
