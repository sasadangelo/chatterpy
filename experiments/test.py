from pydantic import BaseModel, Field
from langchain.agents import create_react_agent, Tool
from langchain.llms import Ollama
from typing import Any

# Step 1: Crea il modello Pydantic per gestire i parametri
class MultiplyParams(BaseModel):
    number1: int = Field(..., description="Il primo numero intero")
    number2: int = Field(..., description="Il secondo numero intero")

# Step 2: Funzione per moltiplicare due numeri
def multiply_numbers(number1: int, number2: int) -> int:
    return number1 * number2

# Step 3: Crea il tool per Langchain
def multiply_tool(input_data: Any) -> int:
    try:
        # Valida i dati di input con Pydantic
        params = MultiplyParams(**input_data)
        return multiply_numbers(params.number1, params.number2)
    except Exception as e:
        return str(e)

multiply_tool_description = "Calcola il prodotto tra due numeri interi."

tool = Tool(
    name="MultiplyNumbersTool",
    func=multiply_tool,
    description=multiply_tool_description
)

# Step 4: Configura il modello Ollama e crea l'agente
llm = Ollama(model="llama3.1")

tools = [tool]

# Step 5: Inizializza l'agente usando create_react_agent
agent = create_react_agent(
    llm=llm,
    tools=tools
)

# Funzione principale per interagire con l'agente
def main():
    user_input = "Calcola il prodotto di 6 e 7"
    response = agent.run(user_input)
    print(f"Risultato: {response}")

if __name__ == "__main__":
    main()
