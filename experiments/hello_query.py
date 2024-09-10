from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model_name = "llama-2-7b-chat"
base_url = "http://localhost:8000/v1"

llm = ChatOpenAI(model=model_name, openai_api_base=base_url)

query = "Who is Katy Perry?"

messages = [
  SystemMessage(content="you're an helpful assistant"),
  HumanMessage(content=query)
]

result = llm.invoke(messages)
print(result.content)