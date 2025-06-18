# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT


# This class represents a generic application page. All the application pages must
# derive from this class and implement the render method.
from abc import ABC, abstractmethod


# Abstract base class representing a generic Page.
class Page(ABC):
    # This is the method each subclass must implement to render the page.
    @abstractmethod
    def render(self) -> None:
        """
        Render the page.
        Subclasses must provide their own implementation.
        """
        pass
