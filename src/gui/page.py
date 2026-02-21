# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
# This class represents a generic application page. All the application pages must
# derive from this class and implement the render method.


class Page:
    # This is the method each subclass must implement to render the page.
    def render(self) -> None:
        raise NotImplementedError("Subclasses must implement the render method")
