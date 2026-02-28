# Configure ChatterPy

ChatterPy and Datawaeve CLI use the following [configuration file](https://github.com/sasadangelo/chatterpy/blob/main/src/config.yaml). Below is a description of the fields:

## Configure ChatterPy

### Provider and Model Configuration

These parameters configure the LLM provider (e.g., Ollama, LLamaCPP, WatsonX, OpenAI) and the model to use. The model name depends on the provider.
```
protocol:
  name: "ollama"
  api_url: http://localhost:11434
  model:
    name: "llama3.1:latest"
    parameters:
      ...
```

### Decoding Parameters

Configure the decoding parameters of the model:
```
protocol:
  ...
    parameters:
      temperature: 0.9
      max_tokens: 500
      top_k: 40
      top_p: 0.9
      repeat_penalty: 1.1
      context_size: 8192
```

### Logging

Configure the logging:
```
log:
  level: "INFO"
  console: false
  file: "logs/chat.log"
  rotation: "10 MB"
  retention: "7 days"
  compression: "zip"
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
memory:
  # possible values: buffer, window or summary
  chat_history: buffer
  # chat_history: buffer
  # chat_history: window
  # chat_history_window: 3 # only window
```
### Datawaeve Logging

Configure the Datawaeve logging:
```
datawave_log:
  level: "DEBUG"
  console: false
  file: "logs/datawave.log"
  rotation: "10 MB"
  retention: "7 days"
  compression: "zip"
```

## RAG Parameters

These parameters activate and configure the Retrieval-Augmented Generation (RAG) component. ChatterPy currently supports LLama3 with the Ollama provider for embedding and Qdrant in local mode as the vector store:
```
rag:
  enabled: false
  top_k_chunks: 10
  document_chunk_size: 100
  document_chunk_overlap: 0
  qdrant_path: ~/.qdrant
  qdrant_collection: mycollection
  embedding_protocol: "ollama"
  embedding_model: "llama3.1:latest"
  embedding_vector_size: 4096
  # embedding_distance_function allowed values: Cosine, Euclid, Dot
  embedding_distance_function: Cosine```
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
