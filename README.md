# ChatterPy

## What is ChatterPy?

ChatterPy is a multi-providers, multi-protocols, and multi-model chatbot with Retrieval-Augmented Generation (RAG) written in Python and LangChain. It is an evolution of my [ChatPDF](https://github.com/sasadangelo/chatpdf) project and consists of two main components:

* **ChatterPy**: The actual chatbot.
* **DataWaeve CLI**: A command-line interface for scraping data from various sources (e.g., PDFs, Wikipedia) and storing it in a vector store.

ChatterPy can be run in text or GUI mode, while DataWaeve CLI is available only in text mode. ChatterPy uses a configuration file to set up the provider (e.g., OpenAI, Ollama, WatsonX), the model (e.g., LLama3, GPT, LLama2), and more.

## Prerequisites

ChatterPy is a multi-providers, multi-protocols, and multi-model chatbot, so the prerequisites depend on the provider or model you choose to activate. By default, ChatterPy uses the Ollama provider and protocol with the LLama3.1 model. To get started, install the Ollama CLI on your machine by downloading it from [here](https://github.com/ollama/ollama). After installation, you can start the ollama server with the command:
```
ollama serve
```

In another terminal:
- you should download the LLM **llama3.1** model in the `~/.ollama` folder:
```
ollama pull llama3.1
```

- you can list the downloaded model using the commands:
```
ollama list
```

ChatterPy also supports the following providers:

* **Ollama**
* **WatsonX**
* **OpenAI** (ChatGPT or any server supporting the OpenAI standard, like Red Hat Instruct Lab or Python LLama.CPP)

Additionally, you need Python 3 installed on your machine.

## How to install ChatterPY and DataWaeve CLI

Follow these instructions to install ChatterPy:

1. Clone the repository:
```
git clone https://github.com/sasadangelo/chatterpy
cd chatterpy
```

2. Create a Python 3 virtual environment and install dependencies with uv:
```
uv sync --dev
```

## Configure ChatterPy

See this document to understand [how to configure ChatterPy and Datawaeve CLI](docs/Configure.md).

## How to run the ChatterPy and DataWaeve CLI

### How to run the ChatterPy in GUI mode

To ChatterPy in GUI mode run the following command:
```
cd src && uv run streamlit run chatterpy_gui.py
```

### How to run the ChatterPy in Text mode

To ChatterPy in Text mode run the following command:
```
cd src && uv run python3 chatterpy_app.py
```

### How to run the DataWaeve CLI

To run the datawaeve cli type the following command:
```
cd src && uv run python3 datawaeve_app.py [--pdf <pdf file name>] [--wikipedia <wikipedia url>]
```

You can provide one or more PDF file or Wikipedia page. You can also provide a folder with one or more PDF file.

## Video Demo

This is the ChatterPy video demo.
<video width="600" controls>
  <source src="docs/media/chatterpy.mp4" type="video/mp4">
  Il tuo browser non supporta il tag video.
</video>
