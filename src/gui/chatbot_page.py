# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast

import streamlit as st
from chatbot.chatbot import ChatBOT
from gui.page import Page
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from streamlit.delta_generator import DeltaGenerator


# This class is responsible for displaying the ChatBOT page using Streamlit.
class ChatBotPage(Page):
    # Renders the ChatBOT page.
    def render(self) -> None:
        # Initialize the page with the title, header, and sidebar.
        self.__init_page()
        # Initialize the conversation.
        self.__init_messages()

        # Display chat history first
        chatbot: ChatBOT = cast(ChatBOT, st.session_state.chatbot)
        messages: list[BaseMessage] = chatbot.get_messages()
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message(name="assistant"):
                    st.markdown(body=message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message(name="user"):
                    st.markdown(body=message.content)

        # Supervise user input
        if user_input := st.chat_input("Input your question!"):
            # Display user message immediately
            with st.chat_message(name="user"):
                st.markdown(body=user_input)

            # Display assistant response with streaming
            with st.chat_message(name="assistant"):
                message_placeholder: DeltaGenerator = st.empty()
                full_response = ""

                # Stream the response (the spinner is not needed with streaming)
                for chunk in chatbot.get_answer(question=user_input):
                    if chunk.content:
                        # Handle content as string
                        content = chunk.content if isinstance(chunk.content, str) else str(chunk.content)
                        full_response += content
                        # Show cursor while streaming
                        message_placeholder.markdown(body=full_response + "▌")

                # Display final response without cursor
                message_placeholder.markdown(body=full_response)

    # Initialize the ChatBOT page
    def __init_page(self) -> None:
        st.set_page_config(page_title="ChatterPy")
        st.header(body="ChatterPy")
        if "chatbot" not in st.session_state:
            chatbot: ChatBOT = ChatBOT()
            st.session_state.chatbot = chatbot
        else:
            chatbot = cast(ChatBOT, st.session_state.chatbot)

        # Sidebar: Session Management
        st.sidebar.title(body="Sessions")

        # Display current session
        current_session_id: str | None = chatbot.get_session_id()
        if current_session_id:
            st.sidebar.markdown(body=f"**Current:** `{current_session_id[:8]}...`")

        # New session button
        if st.sidebar.button(label="➕ New Session", key="new_session"):
            chatbot.create_session()
            st.rerun()

        # List all sessions
        sessions: list[str] = chatbot.list_sessions()
        st.sidebar.markdown(body=f"**All Sessions ({len(sessions)}):**")

        for session_id in sessions:
            col1, col2 = st.sidebar.columns(spec=[3, 1])
            with col1:
                # Show shortened session ID
                short_id: str = session_id[:8] + "..."
                is_current: bool = session_id == current_session_id
                label = f"{'→ ' if is_current else '   '}{short_id}"
                if st.button(label, key=f"switch_{session_id}", use_container_width=True):
                    if not is_current:
                        chatbot.switch_session(session_id)
                        st.rerun()
            with col2:
                # Delete button (disabled for current session if it's the only one)
                can_delete: bool = len(sessions) > 1
                if st.button(label="🗑️", key=f"delete_{session_id}", disabled=not can_delete):
                    if chatbot.delete_session(session_id):
                        st.rerun()

    # Clear the conversation
    def __init_messages(self) -> None:
        clear_button: bool = st.sidebar.button(label="🗑️ Clear Conversation", key="clear")
        if clear_button:
            chatbot: ChatBOT = cast(ChatBOT, st.session_state.chatbot)
            chatbot.clear_conversation()
            st.rerun()
