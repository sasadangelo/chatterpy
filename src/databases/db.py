# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from collections.abc import Iterable


class Database:
    def store(self, chunks: Iterable[str]) -> None:
        raise NotImplementedError("Subclasses must implement the store method")
