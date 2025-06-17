# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
class LLMProvider:
    def __init__(self, config):
        self.config = config
        self.create_model()

    def create_model(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def generate(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")
