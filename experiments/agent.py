from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel

class Agent(ABC):

    def __init__(self, llm: BaseChatModel, tools: list[Callable[..., str]], verbose: bool = True, handle_parsing_errors=True):
        self._llm = llm
        self._tools = tools
        self._verbose = verbose
        self.handle_parsing_errors = handle_parsing_errors

    @abstractmethod
    def invoke(self, user_input: str) -> dict[str, Any]:
        pass