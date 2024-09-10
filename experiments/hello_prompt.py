from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

model_name = "llama-2-7b-chat"
base_url = "http://localhost:8000/v1"

llm = ChatOpenAI(model=model_name, openai_api_base=base_url)

query = "Katy Perry?"

prompt_template = PromptTemplate.from_template("Who is {input}?")
output_parser = StrOutputParser()
chain = prompt_template | llm
result = chain.invoke({"input": query})
print(result.content)