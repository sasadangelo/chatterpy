from prompts.granite_prompt_formatter import GranitePromptFormatter
from prompts.plain_prompt_formatter import PlainPromptFormatter
from prompts.prompt_formatter import PromptFormatter

DEFAULT_PROMPT_FORMATTER = "plain"


class PromptFormatterFactory:
    _instance = None

    @staticmethod
    def get_prompt_formatter(config) -> PromptFormatter:
        if PromptFormatterFactory._instance is None:
            prompt_formatter = config.get("prompt_formatter", DEFAULT_PROMPT_FORMATTER)

            if prompt_formatter == "plain":
                PromptFormatterFactory._instance = PlainPromptFormatter()
            elif prompt_formatter == "granite":
                PromptFormatterFactory._instance = GranitePromptFormatter()
            else:
                PromptFormatterFactory._instance = PlainPromptFormatter()
        return PromptFormatterFactory._instance
