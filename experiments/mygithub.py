import os
from langchain.agents import create_react_agent, Tool
from langchain_openai import OpenAI
from github import Github
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.base import BaseOutputParser


# Define a custom output parser
class CustomOutputParser(BaseOutputParser):
    def parse(self, text):
        # Simple parser for demonstration; adapt to your needs
        if "Issue created:" in text:
            return text
        else:
            raise ValueError(f"Unexpected output: {text}")


model_name = "llama-2-7b-chat"
base_url = "http://localhost:8000/v1"

load_dotenv(".env")

# Inizializza il modello OpenAI
llm = OpenAI(temperature=0.5, model_name=model_name, openai_api_base=base_url)


# Definisci un wrapper per interagire con l'API di GitHub
def create_github_issue(repo_name, title, body, assignee):
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(title=title, body=body, assignee=assignee)
    return f"Issue creata: {issue.html_url}"


# Definisci gli strumenti che l'agent può usare
tools = [
    Tool(
        name="CreateGitHubIssue",
        func=create_github_issue,
        description="Crea un'issue in un repository GitHub specificato.",
    )
]

# Define the prompt template
initial_prompt_template = PromptTemplate(
    input_variables=["tool_names", "tools", "agent_scratchpad", "task"],
    template=(
        "You are a helpful assistant that interacts with GitHub.\n\n"
        "Available tools: {tool_names}\n\n"
        "tools: {tools}\n\n"
        "Task: {task}\n\n"
        "{agent_scratchpad}"
    ),
)
# Initialize the agent using the new method with a structured prompt
agent = create_react_agent(llm=llm, tools=tools,
                           prompt=initial_prompt_template)

# Esegui l'agent con un prompt
prompt = (
    "Crea un'issue nel repository 'sasadangelo/chess' intitolata "
    "'Bug in End Game Gym' e assegnala a 'sasadangelo'."
)
# Prepare the input dictionary with the required keys
input_data = {
    "task": prompt,
    "tool_names": [tool.name for tool in tools],
    "tools": tools,
    "agent_scratchpad": "",  # Initial scratchpad is empty
    "intermediate_steps": [],  # Initialize intermediate steps as an empty list
}

# Set up the output parser
output_parser = CustomOutputParser()

# Invoke the agent
try:
    result = agent.invoke(input_data)
    parsed_result = output_parser.parse(result)
    print(parsed_result)
except Exception as e:
    print(f"An error occurred: {str(e)}")
