# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from chatbot.conversation import Conversation
from core import LoggerManager, chatterpy_config
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from protocols import LLMProtocol, LLMProtocolFactory
from rag import RAG


class ChatBOT:
    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        # Initialize the model provider according to the configuration file config.yml.
        self._protocol: LLMProtocol = LLMProtocolFactory.get_protocol()
        self.rag = RAG()
        # Generate text using the model
        system_message: str = chatterpy_config.system_message
        self._logger.info(f"System Message: {system_message}")
        self._conversation = Conversation(system_message=system_message)

    def get_answer(self, question: str) -> str:
        """
        Get an answer from the chatbot for the given question.

        This method:
        1. Retrieves relevant context from RAG if enabled
        2. Adds RAG context as a SystemMessage to the conversation
        3. Adds the user's question as a HumanMessage to the conversation
        4. Gets the processed messages according to the memory strategy
        5. Sends them to the LLM to get a response
        6. Adds the AI's response to the conversation history
        7. Returns the response

        Args:
            question: The user's question

        Returns:
            The AI's response as a string
        """
        # Retrieve context from RAG if enabled
        context: list[str] | None = self.rag.get_context(user_message=question) if self.rag.is_enabled() else None

        # Add RAG context as SystemMessage if available
        if context:
            context_text: str = "\n".join(context)
            context_message: str = (
                f"RELEVANT CONTEXT:\n"
                f"Use the following information to answer the user's question:\n\n"
                f"{context_text}"
            )
            self._conversation.add_message(message=SystemMessage(content=context_message))

        # Add the user's question as HumanMessage (clean, without context)
        self._conversation.add_message(message=HumanMessage(content=question))
        # Get the messages to send to the LLM (processed by memory strategy)
        messages_for_llm: list[BaseMessage] = self._conversation.get_messages_for_llm()
        # Logging the messages to send to the LLM
        self._logger.debug("=" * 80)
        self._logger.debug(f"Chat History ({len(messages_for_llm)} messages sent to LLM):")
        self._logger.debug("-" * 80)
        for i, msg in enumerate(messages_for_llm, 1):
            role: str = msg.__class__.__name__.replace("Message", "")
            msg_content = msg.content if isinstance(msg.content, str) else str(msg.content)
            # Truncate long messages for readability
            # if len(msg_content) > 200:
            #    msg_content = msg_content[:200] + "..."
            self._logger.debug(f"[{i}] {role}: {msg_content}")
        self._logger.debug("=" * 80)
        # Get the answer from the model
        ai_message: AIMessage = self._protocol.invoke(messages=messages_for_llm)
        # Extract content as string (handle both str and list types)
        content: str = ai_message.content if isinstance(ai_message.content, str) else str(ai_message.content)
        # Add the AI response to the conversation history
        self._conversation.add_message(message=ai_message)
        return content

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self._conversation.clear_history()

    def get_message_count(self) -> int:
        """
        Get the number of messages in the conversation.

        Returns:
            The count of messages in the conversation history
        """
        return self._conversation.get_message_count()

    def get_messages(self) -> list[BaseMessage]:
        """
        Get the number of messages in the conversation.

        Returns:
            The count of messages in the conversation history
        """
        return self._conversation.get_full_history()
