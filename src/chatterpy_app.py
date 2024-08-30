import argparse
from dotenv import load_dotenv
import yaml
from chatbot.chatbot import ChatBOT

def load_environment(env_file):
    load_dotenv(env_file)

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

# Parse command-line arguments
parser = argparse.ArgumentParser(description='LLM Provider Factory')
parser.add_argument('--config', '-c', type=str, required=True, help='Path to the config file')
parser.add_argument('--env', '-e', type=str, required=False, default=".env", help='Path to the environment file')
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

# This is the main entry point of the ChatBOT command-line interface.
# It handles command-line arguments, initializes the ChatBOT, and
# facilitates a conversation with the ChatBOT until the user chooses to exit.
def main():
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