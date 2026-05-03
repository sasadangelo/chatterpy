# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from chatbot.session import Session
from core import LoggerManager


class SessionManager:
    """
    Manages multiple chat sessions.

    This class provides functionality to create, retrieve, delete, and switch
    between multiple chat sessions. Each session maintains its own conversation
    history and unique identifier.
    """

    def __init__(self, system_message: str) -> None:
        """
        Initialize the SessionManager.

        Args:
            system_message: The system prompt that defines the AI's behavior
                          for all sessions
        """
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self._system_message: str = system_message
        self._sessions: dict[str, Session] = {}
        self._current_session_id: str | None = None

        # Create the first default session
        self.create_session()
        self._logger.info("SessionManager initialized")

    def create_session(self, session_id: str | None = None) -> Session:
        """
        Create a new session.

        Args:
            session_id: Optional session ID. If not provided, a new UUID will be generated

        Returns:
            The newly created Session object
        """
        session = Session(system_message=self._system_message, session_id=session_id)
        self._sessions[session.session_id] = session

        # Set as current session if it's the first one or no current session exists
        if self._current_session_id is None:
            self._current_session_id = session.session_id

        self._logger.info(f"Session created: {session.session_id}")
        return session

    def get_session(self, session_id: str) -> Session | None:
        """
        Retrieve a session by its ID.

        Args:
            session_id: The unique session identifier

        Returns:
            The Session object if found, None otherwise
        """
        return self._sessions.get(session_id)

    def get_current_session(self) -> Session | None:
        """
        Get the current active session.

        Returns:
            The current Session object if exists, None otherwise
        """
        if self._current_session_id is None:
            return None
        return self._sessions.get(self._current_session_id)

    def get_current_session_id(self) -> str | None:
        """
        Get the current session ID.

        Returns:
            The current session ID if exists, None otherwise
        """
        return self._current_session_id

    def switch_session(self, session_id: str) -> bool:
        """
        Switch to a different session.

        Args:
            session_id: The ID of the session to switch to

        Returns:
            True if the switch was successful, False if the session doesn't exist
        """
        if session_id in self._sessions:
            self._current_session_id = session_id
            self._logger.info(f"Switched to session: {session_id}")
            return True
        else:
            self._logger.warning(f"Session not found: {session_id}")
            return False

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session by its ID.

        Args:
            session_id: The unique session identifier

        Returns:
            True if the session was deleted, False if it doesn't exist
        """
        if session_id not in self._sessions:
            self._logger.warning(f"Cannot delete session: {session_id} not found")
            return False

        # Don't allow deleting the last session
        if len(self._sessions) == 1:
            self._logger.warning("Cannot delete the last session")
            return False

        # If deleting the current session, switch to another one
        if session_id == self._current_session_id:
            # Get the first session that is not the one being deleted
            for sid in self._sessions:
                if sid != session_id:
                    self._current_session_id = sid
                    break

        del self._sessions[session_id]
        self._logger.info(f"Session deleted: {session_id}")
        return True

    def list_sessions(self) -> list[str]:
        """
        Get a list of all session IDs.

        Returns:
            A list of session IDs
        """
        return list(self._sessions.keys())

    def get_session_count(self) -> int:
        """
        Get the number of sessions.

        Returns:
            The count of sessions
        """
        return len(self._sessions)
