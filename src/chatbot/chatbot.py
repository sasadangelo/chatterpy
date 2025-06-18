# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from chatbot.conversation import Conversation
from prompts.prompt_formatter_factory import PromptFormatterFactory
from providers.provider_factory import LLMProviderFactory
from rag.rag import RAG


class ChatBOT:
    def __init__(self, config: dict) -> None:
        """
        Initialize the ChatBOT with the given configuration.
        Sets up conversation history, LLM provider, RAG subsystem,
        system message, and prompt formatter.
        """
        self.config = config
        self.show_reasoning = config.get("show_reasoning", False)
        self.conversation = Conversation(config)
        # Initialize the model provider according to the configuration file
        # config.yml.
        self.provider = LLMProviderFactory.get_provider(config)
        self.rag = RAG(config)
        self.system_message = SystemMessage(content=self.config["system_message"])
        self.prompt_formatter = PromptFormatterFactory.get_prompt_formatter(self.config)

    # Once the user insert the question, this method is called to generate the answer.
    def get_answer(self, question):
        """
        Generate an answer for the given user question.

        Steps:
        - Wrap the user question as a HumanMessage.
        - Get the relevant context using RAG if enabled.
        - Format the prompt with context, system message, chat history, and user message.
        - Invoke the language model provider with the prompt.
        - Wrap the model output as an AIMessage.
        - Save the interaction in the conversation history.
        - Return the generated text.
        """
        # Add the user message to the list of users
        user_message = HumanMessage(content=question)
        # If RAG is enabled get the context from the RAG subsytem
        context = self.rag.get_context(question) if self.rag.is_enabled() else None
        # Create the prompt to pass to the model
        prompt = self.prompt_formatter.get_prompt(
            context,
            self.system_message,
            self.conversation.get_chat_history_messages(),
            user_message,
        )
        # Get the answer from the model
        ai_message_text = self.provider.generate(prompt)
        ai_message_text = self._process_output(ai_message_text)
        ai_message = AIMessage(content=ai_message_text)
        # Save the interaction in the chat history
        self.conversation.save_interaction(user_message, ai_message)
        return ai_message_text

    def _process_output(self, text: str) -> str:
        if self.show_reasoning:
            return self._format_thinking(text)
        else:
            return self._remove_thinking(text)

    def _remove_thinking(self, text: str) -> str:
        import re

        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    def _format_thinking(self, text: str) -> str:
        import re

        def replacer(match):
            thinking_text = match.group(0)[7:-8].strip()  # strip <think>...</think>
            return f"\n\n🧠 **Internal reasoning**\n```\n{thinking_text}\n```\n"

        return re.sub(r"<think>.*?</think>", replacer, text, flags=re.DOTALL).strip()

    # Return the chat history
    def get_chat_history(self):
        """
        Retrieve the current conversation's chat history messages.
        The return type may vary depending on the memory implementation.
        """
        return self.conversation.get_chat_history_messages()

    # Clear the conversation
    def clear_conversation(self):
        """
        Clear the current conversation history, resetting the conversation memory.
        """
        self.conversation.clear()
