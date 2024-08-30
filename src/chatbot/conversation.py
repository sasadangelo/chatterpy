# Conversation - a Generic ChatBot conversation
#
# This class represents a generic chatbot conversation.
#
# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo sasadangelo@gmail.com
#
# SPDX-License-Identifier: MIT
from memory.memory_factory import MemoryFactory

# This class represents a generic chatbot conversion.
# It contains the chat history of the messages and the cost of each one.
class Conversation:
    def __init__(self, config):
        self.config = config
        self.__init(config)

    def __init(self, config):
        # Inizialize the conversation
        self.conversation = MemoryFactory.get_memory(config)

    def save_interaction(self, user_message, ai_message):
       self.conversation.save_context({"input": user_message.content}, {"output": ai_message.content})

    def get_chat_history_messages(self):
       return self.conversation.load_memory_variables({}).get('history', '')

    def clear(self):
        self.__init(self.config)