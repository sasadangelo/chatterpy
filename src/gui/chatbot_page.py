# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast

import streamlit as st
from chatbot.chatbot import ChatBOT
from gui.page import Page
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


# This class is responsible for displaying the ChatBOT page using Streamlit.
class ChatBotPage(Page):
    # Renders the ChatBOT page.
    def render(self) -> None:
        # Initialize the page with the title, header, and sidebar.
        self.__init_page()
        # Initialize the conversation.
        self.__init_messages()

        # Supervise user input
        if user_input := st.chat_input("Input your question!"):
            with st.spinner(text="ChatterPy is typing ..."):
                chatbot: ChatBOT = cast(ChatBOT, st.session_state.chatbot)
                _ = chatbot.get_answer(question=user_input)

        # Display chat history
        chatbot = cast(ChatBOT, st.session_state.chatbot)
        messages: list[BaseMessage] = chatbot.get_messages()
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message(name="assistant"):
                    st.markdown(body=message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message(name="user"):
                    st.markdown(body=message.content)

    # Initialize the ChatBOT page
    def __init_page(self) -> None:
        st.set_page_config(page_title="ChatterPy")
        st.header(body="ChatterPy")
        chatbot: ChatBOT | None = None
        if "chatbot" not in st.session_state:
            chatbot = ChatBOT()
            st.session_state.chatbot = chatbot
        else:
            chatbot = st.session_state.chatbot

    # Clear the conversation
    def __init_messages(self) -> None:
        clear_button: bool = st.sidebar.button("Clear Conversation", key="clear")
        if clear_button:
            chatbot: ChatBOT = cast(ChatBOT, st.session_state.chatbot)
            chatbot.clear_conversation()
