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

# Log the session ID
logger.info(f"Session ID: {chatbot.get_session_id()}")

# Print a welcome message for the ChatterPy command-line interface.
print("Welcome to the ChatterPy command-line interface!")
print(f"Session ID: {chatbot.get_session_id()}")
print("\nCommands:")
print("  /new       - Create a new session")
print("  /delete    - Delete a session")
print("  /list      - List all sessions")
print("  /switch    - Switch to a different session")
print("  /clear     - Clear current conversation")
print("  quit       - Exit the application")
print("\nStart the conversation (Type 'quit' or press 'CTRL-D' to exit)")


def handle_command(command: str) -> None:
    """
    Handle CLI commands for session management.

    Args:
        command: The command string starting with '/'
    """
    cmd: str = command.lower().strip()

    if cmd == "/new":
        session_id: str = chatbot.create_session()
        print(f"✓ Created and switched to new session: {session_id}")
        logger.info(f"Created new session: {session_id}")

    elif cmd == "/list":
        sessions = chatbot.list_sessions()
        current_id = chatbot.get_session_id()
        print(f"\nSessions ({len(sessions)}):")
        for sid in sessions:
            marker = "→" if sid == current_id else " "
            print(f"  {marker} {sid}")
        print()

    elif cmd == "/switch":
        sessions = chatbot.list_sessions()
        current_id = chatbot.get_session_id()
        print("\nAvailable sessions:")
        for i, sid in enumerate(sessions, 1):
            marker = "→" if sid == current_id else " "
            print(f"  {i}. {marker} {sid}")
        try:
            choice = input("\nEnter session number to switch to (or press Enter to cancel): ").strip()
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(sessions):
                    session_id = sessions[idx]
                    if chatbot.switch_session(session_id):
                        print(f"✓ Switched to session: {session_id}")
                        logger.info(f"Switched to session: {session_id}")
                    else:
                        print("✗ Failed to switch session")
                else:
                    print("✗ Invalid session number")
        except (ValueError, IndexError):
            print("✗ Invalid input")

    elif cmd == "/delete":
        sessions = chatbot.list_sessions()
        current_id = chatbot.get_session_id()
        if len(sessions) == 1:
            print("✗ Cannot delete the last session")
            return
        print("\nAvailable sessions:")
        for i, sid in enumerate(sessions, 1):
            marker = "→" if sid == current_id else " "
            print(f"  {i}. {marker} {sid}")
        try:
            choice = input("\nEnter session number to delete (or press Enter to cancel): ").strip()
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(sessions):
                    session_id = sessions[idx]
                    confirm = input(f"Delete session {session_id}? (y/N): ").strip().lower()
                    if confirm == "y":
                        if chatbot.delete_session(session_id):
                            print(f"✓ Deleted session: {session_id}")
                            if session_id == current_id:
                                print(f"✓ Switched to session: {chatbot.get_session_id()}")
                            logger.info(f"Deleted session: {session_id}")
                        else:
                            print("✗ Failed to delete session")
                else:
                    print("✗ Invalid session number")
        except (ValueError, IndexError):
            print("✗ Invalid input")

    elif cmd == "/clear":
        chatbot.clear_conversation()
        print("✓ Conversation cleared")
        logger.info("Conversation cleared")

    else:
        print(f"✗ Unknown command: {command}")
        print("Available commands: /new, /delete, /list, /switch, /clear")


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

            # Handle commands
            if user_message.startswith("/"):
                handle_command(user_message)
                continue

            # Log user message
            logger.info(f"user> {user_message}")

            # Generate and print the chatbot's response in streaming mode
            print("")
            print("assistant> ", end="", flush=True)

            response_parts: list[str] = []
            for chunk in chatbot.get_answer(question=user_message):
                chunk_text: str = chunk.text
                print(chunk_text, end="", flush=True)
                response_parts.append(chunk_text)

            response: str = "".join(response_parts)
            print("")

            # Log AI response
            logger.info(f"assistant> {response}")

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
