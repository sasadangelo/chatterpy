# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from chatbot.chatbot import ChatBOT
from core import LoggerManager, chatterpy_config, setup_logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging first
setup_logging(
    level=chatterpy_config.log.level,
    console=chatterpy_config.log.console,
    file=chatterpy_config.log.file,
    rotation=chatterpy_config.log.rotation,
    retention=chatterpy_config.log.retention,
    compression=chatterpy_config.log.compression,
)

# Create a main logger
logger = LoggerManager.get_logger(name="main")

# Create a ChatBOT object
chatbot: ChatBOT = ChatBOT()

# Print a welcome message for the ChatterPy command-line interface.
print("Welcome to the ChatterPy command-line interface!")
print("Start the conversation (Type 'quit' or press 'CTRL-D' to exit)")


# This is the main entry point of the ChatterPy command-line interface.
# It handles command-line arguments, initializes the ChatBOT, and
# facilitates a conversation with the ChatterPy until the user chooses to exit.
def main() -> None:
    try:
        while True:
            # Ask input from the user
            user_message: str = input("you> ")
            if user_message.lower() == "quit":
                print("\nBye.")
                break

            # Log user message
            logger.info(f"user> {user_message}")

            # Generate the chatbot's response
            response: str = chatbot.get_answer(question=user_message)

            # Log AI response
            logger.info(f"assistant> {response}")

            # Print the chatbot's response
            print("")
            print("assistant>", response)

    except EOFError:
        # Terminate the conversation
        print("\nBye.")
    finally:
        # Clean up resources before exit
        if hasattr(chatbot, "rag") and chatbot.rag and hasattr(chatbot.rag, "db") and chatbot.rag.db:
            chatbot.rag.db.close()


if __name__ == "__main__":
    # Call the main function when the script is executed.
    main()
