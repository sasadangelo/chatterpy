"""
chatterpy_app.py

This module provides a command-line interface for interacting with the ChatBOT.
It handles environment and configuration file loading, initializes the ChatBOT,
and facilitates a conversation with the ChatBOT.

Functions:
    - load_environment: Loads environment variables from a specified file.
    - load_config: Loads a configuration file and returns its content.
    - main: The main entry point of the application, handling user input and
      generating responses from the ChatBOT.

Copyright (C) 2023 Salvatore D'Angelo
Maintainer: Salvatore D'Angelo sasadangelo@gmail.com

This file is part of the Running Data Analysis project.

SPDX-License-Identifier: MIT
"""
import argparse
from dotenv import load_dotenv
import yaml
from chatbot.chatbot import ChatBOT


def load_environment(env_file):
    """
    Load environment variables from a specified file.

    Args:
        env_file (str): Path to the .env file containing environment variables.
    """
    load_dotenv(env_file)


def load_config(config_file):
    """
    Load a configuration file and return its content.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration data loaded from the file.
    """
    with open(config_file, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return config_data


# Parse command-line arguments
parser = argparse.ArgumentParser(description="LLM Provider Factory")
parser.add_argument(
    "--config", "-c", type=str, required=True, help="Path to the config file"
)
parser.add_argument(
    "--env",
    "-e",
    type=str,
    required=False,
    default=".env",
    help="Path to the environment file",
)
args = parser.parse_args()

# Load environment variables
load_environment(args.env)
# Load the configuration file
config = load_config(args.config)

# Create a ChatBOT object
chatbot = ChatBOT(config)

# Print a welcome message for the ChatterPy command-line interface.
print("Welcome to the ChatterPy command-line interface!")
print("Start the conversation (Type 'quit' or press 'CTRL-D' to exit)")


def main():
    """
    Main entry point of the ChatBOT command-line interface.

    Handles command-line arguments, initializes the ChatBOT, and facilitates
    a conversation with the ChatBOT until the user chooses to exit.
    """
    try:
        while True:
            # Ask input from the user
            user_message = input("you> ")
            if user_message.lower() == "quit":
                print("\nBye.")
                break

            # Generate the chatbot's response
            response = chatbot.get_answer(user_message)

            # Print the chatbot's response
            print("")
            print("assistant>", response)

    except EOFError:
        # Terminate the conversation
        print("\nBye.")


if __name__ == "__main__":
    # Call the main function when the script is executed.
    main()
