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
    def __init__(self, config):
        self.config = config

    # Renders the ChatBOT page.
    def render(self):
        # Initialize the page with the title, header, and sidebar.
        self.__init_page()
        # Initialize the conversation.
        self.__init_messages()

        # Supervise user input
        if user_input := st.chat_input("Input your question!"):
            with st.spinner("ChatterPy is typing ..."):
                _ = st.session_state.chatbot.get_answer(user_input)

        # Display chat history
        messages = st.session_state.chatbot.get_chat_history()
        for message in messages:
            if isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)

    # Initialize the ChatBOT page
    def __init_page(self) -> None:
        st.set_page_config(page_title="ChatterPy")
        st.header("ChatterPy")
        chatbot = None
        if "chatbot" not in st.session_state:
            chatbot = ChatBOT(self.config)
            st.session_state.chatbot = chatbot
        else:
            chatbot = st.session_state.chatbot

    # Clear the conversation
    def __init_messages(self) -> None:
        clear_button = st.sidebar.button("Clear Conversation", key="clear")
        if clear_button:
            st.session_state.chatbot.clear_conversation()
