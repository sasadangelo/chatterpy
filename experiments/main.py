from langchain.agents import initialize_agent, AgentOutputParser
#from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from github_facade import GitHub
from langchain.agents.agent_types import AgentType
from langchain.tools import tool
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
model_name = "llama3"
base_url = "http://localhost:11434"

load_dotenv(".env")

# Inizializza il modello OpenAI
# llm = Ollama(model=model_name, base_url=base_url)
llm = ChatOllama(model=model_name, base_url=base_url)

# Crea un'istanza della tua classe GitHub
github_client = GitHub()

# Definisci un wrapper per creare issue su GitHub usando l'API Python
#def create_github_issue(repo_name: str, title: str, body: str, assignee: str) -> str:
#    issue = github_client.create_issue(repo_name=repo_name, title=title, body=body, assignee=assignee)
#    return f"Issue creata: {issue.html_url}"

#@tool(name="create_github_issue")
def create_github_issue(p: str) -> str:
    """
    Create an issue in the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository);
    title (the title of the issu);
    body (the content of the issue);
    assignee (the GitHub username to assign the issue to)
    """
    print("######## I'm in create_github_issue:\n\n", p,"\n\n")
    return f"Issue creata: http://ciccioformaggio/1"

# Crea un tool strutturato
github_issue_tool = Tool.from_function(
    name="create_github_issue",
    func=create_github_issue,
    description="Create an issue in the specified GitHub repository. The function expects the following parameters:"
        "repo_name (the name of the repository), title (the title of the issu), body (the content of the issue), "
        "assignee (the GitHub username to assign the issue to)."
)

# Definisci gli strumenti che l'agent può usare
tools = [github_issue_tool]  # Wrap the tool in a list

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# Definisci il prompt da passare all'agent
prompt = (
    "Create a single issue in the repository 'sasadangelo/chess' calling create_github_issue once with the following details: "
    "Title: 'Bug in End Game Gym';"
    "Body: 'The bug is related to the Start Game button that doesn't work.', "
    "and assign it to 'sasadangelo'."
)
#messages = [HumanMessage(prompt)]
result =agent.invoke({"input": prompt})
print(result)

#llm_with_tools = llm.bind_tools(tools)
#ai_msg = llm_with_tools.invoke(messages)
#print(ai_msg)
#agentAction = ToolsAgentOutputParser().invoke(ai_msg)
#print(agentAction)
#print(initial_prompt_template)
# Initialize the agent using the new method with a structured prompt
#agent = create_react_agent(llm=llm, tools=tools,
#                           prompt=initial_prompt_template)
#agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



# Prepara l'input per l'agent
#input_data = {
#    "task": prompt,
#    "tool_names": [tool.name for tool in tools],
#    "tools": tools,
#    "agent_scratchpad": "",  # Inizialmente vuoto
#    "intermediate_steps": [],  # Inizialmente vuoto
#}

# Set up the output parser
#output_parser = CustomOutputParser()

# Invoke the agent
#try:
#    print("11111")
    #result = agent_executor.invoke(input_data)
    #result = agent_executor.invoke({"input": "hi!"})
#    result = agent.invoke(input_data)
#    print("22222")
#    print("result: ", result)
#    parsed_result = output_parser.parse(result)
#    print("33333")
#    print(parsed_result)
#    print("44444")
#except Exception as e:
#    print(f"An error occurred: {str(e)}")



