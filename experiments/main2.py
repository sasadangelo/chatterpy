from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from github_react_agent import GithubReActAgent
from github_facade import GitHub
from github import GithubException
from langchain.tools import tool

model_name = "llama3"
base_url = "http://localhost:11434"

load_dotenv(".env")
# Inizializza il modello OpenAI
llm = ChatOllama(model=model_name, base_url=base_url)

system_message = """
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
    Please ensure that your responses are socially unbiased and positive in nature.
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
    If you don't know the answer to a question, please don't share false information.
    """

# Initialize the messages list
messages = [{"role": "system", "content": system_message}]

agent = GithubReActAgent(llm=llm, verbose=True, handle_parsing_errors=True)

try:
    while True:
        # Input from the user
        query = input("You: ")

        # Add the user message to the conversation
        user_message = {"role": "user", "content": query}
        messages.append(user_message)

        ai_response = agent.invoke({"input": query})

        # Add the AI reply to the conversation
        ai_message = {"role": "assistant", "content": ai_response['output']}
        messages.append(ai_message)

        # Print the AI reply
        print(f"Assistant: {ai_response['output']}")
except EOFError:
    # Terminate the conversation when the user press CTRL-D
    print("\nBye.")
