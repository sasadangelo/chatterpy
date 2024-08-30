# ChatterPy

## What is ChatterPy?

ChatterPy is a multi-model and multi-provider chatbot with RAG (Retrieval-Augmented Generation) written in Python and LangChain. It is an evolution of my [ChatPDF](https://github.com/sasadangelo/chatpdf) project and consists of two main components:

* **ChatterPy**: The actual chatbot.
* **DataWaeve CLI**: A command-line interface for scraping data from various sources (e.g., PDFs, Wikipedia) and storing it in a vector store.

ChatterPy can be run in text or GUI mode, while DataWaeve CLI is available only in text mode. ChatterPy uses a configuration file to set up the provider (e.g., OpenAI, Ollama, LLamaCPP), the model (e.g., LLama3, GPT, LLama2), and more.

## Prerequisites

ChatterPy is a multi-provider and multi-model chatbot, so the prerequisites depend on the provider or model you choose to activate. By default, ChatterPy uses the Ollama provider with the LLama3 model. To get started, install the Ollama CLI on your machine by downloading it from [here](https://github.com/ollama/ollama). After installation, you can download the LLama3 model with the following command:
```
ollama pull llama3
```

Once downloaded, you need to serve the model with this command:
```
ollama serve
```

ChatterPy also supports the following providers:

* **WatsonX**
* **LLama.CPP**
* **OpenAI** (ChatGPT or any server supporting the OpenAI standard, like Red Hat Instruct Lab or Python LLama.CPP)

Additionally, you need Python 3 installed on your machine.

## How to install ChatterPY and DataWaeve CLI

Follow these instructions to install ChatterPy:

1. Clone the repository:
```
git clone https://github.com/sasadangelo/chatterpy
cd chatterpy
```

2. Create a Python 3 virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies for ChatterPy and DataWaeve CLI:
```
pip3 install -r chatterpy_requirements.txt
pip3 install -r datawaeve_requirements.txt
```

## Configure ChatterPy

ChatterPy and Datawaeve CLI use the following [configuration file](https://github.com/sasadangelo/chatterpy/blob/main/src/config.yml). Below is a description of the fields:

### Provider and Model Configuration

These parameters configure the LLM provider (e.g., Ollama, LLamaCPP, WatsonX, OpenAI) and the model to use. The model name depends on the provider.
```
provider="ollama"
model="llama3"
```

### Decoding Parameters

Configure the decoding parameters of the model:
```
parameters:
  temperature: 0.8
  max_tokens: 200
  top_k: 40
  top_p: 0.9
  repeat_penalty: 1.1
  context_size: 8192
```

### Prompt Formatter

Choose the chat history format (currently, only Grafite on WatsonX requires a specific prompt format called "granite"; all others work with plain text):
```
prompt_formatter: plain
```

### System Message

Configure the system message:
```
system_message: |
  You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
  Please ensure that your responses are socially unbiased and positive in nature.
  If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
  If you don't know the answer to a question, please don't share false information and say you don't know the answer.
```

### Memory Strategy

Choose the memory strategy: buffer, window, or summary. The `buffer` option allows the prompt to grow indefinitely, which can be problematic in the long term. The `window` strategy keeps only the last N messages in chat history, while the `summary` strategy creates a summary of the chat history.
```
chat_history_memory: buffer

# chat_history_memory: window
# chat_history_memory_window: 3

# chat_history_memory: summary
```

### RAG Parameters

These parameters activate and configure the Retrieval-Augmented Generation (RAG) component. ChatterPy currently supports LLama3 with the Ollama provider for embedding and Qdrant in local mode as the vector store:
```
rag_enabled: false
rag_top_k_chunks: 10

qdrant_path: ~/.qdrant
qdrant_collection: mycollection

embedding_provider: "ollama"
embedding_model: "llama3"
embedding_vector_size: 4096
# embedding_distance_function allowed values: Cosine, Euclid, Dot
embedding_distance_function: Cosine
```

### DataWaeve CLI Parameters

DataWaeve CLI parameters overlap with RAG parameters since both use the same vector store for data storage and retrieval:
```
document_chunk_size: 100
document_chunk_overlap: 0

qdrant_path: ~/.qdrant
qdrant_collection: mycollection

embedding_provider: "ollama"
embedding_model: "llama3"
embedding_vector_size: 4096
# embedding_distance_function allowed values: Cosine, Euclid, Dot
embedding_distance_function: Cosine
```

### Provider-Specific Parameters

WatsonX requires the following additional parameters:
```
api_url: "https://<region>.ml.cloud.ibm.com"
parameters:
  decoding_method: sample
```

Ollama requires these additional parameters:
```
base_url: http://localhost:11434
```

Open AI requires these additional parameters:
```
base_url: "http://localhost:8000/v1"
```

LLamaCPP requires these additional parameters:
```
transformers_path: "~/.cache/huggingface/transformers"
model_path: "llama-2-7b-chat-gguf/llama-2-7b-chat.Q2_K.gguf"
chat_format: "llama-2"
```

## Set UP the Environment Variables

WatsonX and ChatGPT providers requires the setting of the following environment variables. In both the cases copy the `env-sample` file in the `.env` file.

### WatsonX Environment Variables

You need to set the following environment variables:
```
WATSONX_APIKEY="<your WatsonX API Key>"
WATSONX_PROJECT_ID="<your WatsonX Project ID Here>"
```

### ChatGPT Environment Variables

You need to set the following environment variable:
```
OPENAI_API_KEY="<your OpenAI API Key>"
```

## How to run the ChatterPy and DataWaeve CLI

### How to run the ChatterPy in GUI mode

To ChatterPy in GUI mode run the following command:
```
cd src
streamlit run chatterpy_gui.py
```

### How to run the ChatterPy in Text mode

To ChatterPy in Text mode run the following command:
```
cd src
python3 chatterpy_app.py -c config.yml
```

### How to run the DataWaeve CLI

To run the datawaeve cli type the following command:
```
cd src
python3 datawaeve_app.py -c config.yml [--pdf <pdf file name>] [--wikipedia <wikipedia url>]
```

You can provide one or more PDF file or Wikipedia page. You can also provide a folder with one or more PDF file.
