# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import uuid

from chatbot.conversation import Conversation
from core import LoggerManager


class Session:
    """
    Manages a chat session with a unique identifier.

    This class encapsulates a conversation with a unique session ID,
    preparing the architecture for future multi-conversation support.
    """

    def __init__(self, system_message: str, session_id: str | None = None) -> None:
        """
        Initialize a session with a unique ID and conversation.

        Args:
            system_message: The system prompt that defines the AI's behavior
            session_id: Optional session ID. If not provided, a new UUID will be generated
        """
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self._session_id: str = session_id if session_id else str(uuid.uuid4())
        self._conversation: Conversation = Conversation(system_message=system_message)

        self._logger.info(f"Session created with ID: {self._session_id}")

    @property
    def session_id(self) -> str:
        """
        Get the session ID.

        Returns:
            The unique session identifier
        """
        return self._session_id

    @property
    def conversation(self) -> Conversation:
        """
        Get the conversation associated with this session.

        Returns:
            The Conversation object
        """
        return self._conversation
