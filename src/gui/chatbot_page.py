# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
import streamlit as st
from langchain.schema import AIMessage, HumanMessage
from chatbot.chatbot import ChatBOT

# from src.models.base_model import Model
from gui.page import Page


# This class is responsible for displaying the ChatBOT page using Streamlit.
class ChatBotPage(Page):
    def __init__(self, config: dict) -> None:
        """
        Initialize ChatBotPage with the given configuration.
        """
        self.config = config

    # Renders the ChatBOT page.
    def render(self) -> None:
        """
        Render the chat bot page using Streamlit.
        This includes initializing the page layout, processing user input,
        displaying chat history, and handling conversation clearing.
        """
        # Initialize the page with the title, header, and sidebar.
        self.__init_page()
        # Initialize the conversation.
        self.__init_messages()

        # Wait for user input from the chat input widget
        if user_input := st.chat_input("Input your question!"):
            with st.spinner("ChatterPy is typing ..."):
                # Generate the answer but do not display directly here,
                # messages will be rendered from chat history below.
                _ = st.session_state.chatbot.get_answer(user_input)

        # Retrieve and display the full chat history
        messages = st.session_state.chatbot.get_chat_history()
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            else:
                # Handle unexpected message types gracefully
                st.write(f"[Unsupported message type]: {message}")

    # Initialize the ChatBOT page
    def __init_page(self) -> None:
        """
        Initialize Streamlit page settings and
        create ChatBOT instance if not present in session state.
        """
        st.set_page_config(page_title="ChatterPy")
        st.header("ChatterPy")
        if "chatbot" not in st.session_state:
            st.session_state.chatbot = ChatBOT(self.config)

    # Clear the conversation
    def __init_messages(self) -> None:
        """
        Add a button in the sidebar to clear the chat conversation.
        Clears conversation on button press.
        """
        clear_button = st.sidebar.button("Clear Conversation", key="clear")
        if clear_button:
            st.session_state.chatbot.clear_conversation()  # Optionally rerun to refresh UI
