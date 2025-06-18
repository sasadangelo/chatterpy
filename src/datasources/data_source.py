# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
class Source:
    """
    Abstract base class for data sources.
    """

    def load_data(self):
        """
        Abstract method to load data from the source.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("the 'load_data' method must be implemented by a subclass.")
