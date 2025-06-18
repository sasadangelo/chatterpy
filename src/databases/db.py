# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Union, List
from langchain.schema import Document


class Database:
    def store(self, chunksList: List[Union[str, Document]]):
        """
        Abstract method to store data chunks with embeddings.

        Args:
            chunks (List[Union[str, Document]]): List of text chunks or Document objects to store.
            embeddings (Any): Embedding model or function to convert chunks into vectors.
        """
        raise NotImplementedError("Subclasses must implement the store method")
