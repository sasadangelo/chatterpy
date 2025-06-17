class PromptFormatter:
    def get_prompt(self, context, system_message, chat_history_messages, user_message):
        raise NotImplementedError("Subclasses must implement the generate method")
