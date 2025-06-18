# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
"""
chatterpy_gui.py

This module defines the ChatBotApp class and related functions for managing
the Streamlit chatbot application. It handles application initialization,
page navigation, and singleton management.

Classes:
    - ChatBotApp: Manages the Streamlit chatbot application, initializes the
      initial page, and handles page selection.

Functions:
    - singleton: A decorator that implements the Singleton design pattern,
      ensuring that a class has only one instance.
    - load_environment: Loads environment variables from a specified .env file.
    - load_config: Loads a YAML configuration file and returns its content.

Copyright (C) 2023 Salvatore D'Angelo
Maintainer: Salvatore D'Angelo sasadangelo@gmail.com

This file is part of the Running Data Analysis project.

SPDX-License-Identifier: MIT
"""

import yaml
from dotenv import load_dotenv
from typing import Optional, Dict
import functools
from gui.chatbot_page import ChatBotPage
from gui.page import Page
import streamlit as st


def singleton(cls):
    """
    Decorator to implement the Singleton design pattern.

    A Singleton ensures that a class has only one instance and provides a global
    access point to that instance.

    Args:
        cls (type): The class to be decorated. This class will be ensured to have
                    only one instance.

    Returns:
        function: A wrapper function that returns the single instance of the class.
    """
    instances = {}

    # Function to get the singleton instance.
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# This class is responsible for managing the Streamlit application
# and navigation between different pages. It initializes the initial page,
# handles page selection, and serves as the entry point for running the
# application.
@singleton
class ChatBotApp:
    """
    Manage the Streamlit chatbot application and navigation.

    This class is responsible for initializing the application, managing the
    navigation between different pages, and serving as the entry point for
    running the Streamlit chatbot. It sets up the initial page, handles page
    selection, and provides the main application logic.

    Attributes:
        current_page (Page): The current page being displayed.
        config (dict): Configuration settings for the application.
    """

    current_page: Optional["Page"]

    def __init__(self, config: Dict) -> None:
        """
        Initialize the ChatBotApp instance and load the activities.

        Args:
            config (dict): Configuration settings for the application. This
                           configuration is used to set up the application.

        Initializes the `current_page` to `None` and sets the `config` attribute
        based on the provided configuration. The constructor is responsible for
        preparing the initial state of the application.
        """
        self.current_page = None
        self.config = config

    def run(self) -> None:
        """
        Runs the ChatBotApp and initializes the first page as
        ChatBotPage using the provided configuration.

        This method sets the initial page to be an instance of `ChatBotPage`
        initialized with the application configuration and selects it as the
        current page.

        It is responsible for starting the application and displaying the
        initial page to the user.
        """
        try:
            self.select_page(ChatBotPage(self.config))
        except RuntimeError as e:
            st.error(str(e))

    def select_page(self, page: "Page") -> None:
        """
        Selects and renders the current page based on user navigation logic.
        Here you can add logic for navigating between different pages.
        For example, if you want to show the ActivityOverviewPage as the
        initial page.

        Args:
            page (Page): The page object to be displayed. It should have a
                         `render` method to display the content.
        """
        self.current_page = page
        self.current_page.render()


def load_environment(env_file: str) -> None:
    """
    Load environment variables from a specified .env file.

    Args:
        env_file (str): Path to the .env file containing environment variables.
    """
    try:
        load_dotenv(env_file)
    except Exception as e:
        print(f"Warning: Could not load environment file {env_file}: {e}")


def load_config(config_file: str) -> Dict:
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)
        return yaml_config
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
    return {}


if __name__ == "__main__":
    # Load environment variables
    load_environment(".env")
    # Load the configuration file
    chatbot_config = load_config("config.yml")

    app = ChatBotApp(chatbot_config)
    app.run()
