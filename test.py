import os
from langsmith import Client

os.environ["LANGCHAIN_API_KEY"] = "****"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

client = Client()
project = client.create_project(name="chatterpy")
print("Creato progetto:", project.name)
# try:
#     project = client.read_project(project_name="chatterpy")
#     print("✅ Connessione riuscita:", project)
# except Exception as e:
#     print("❌ Errore nella connessione:", e)
