from providers.provider import LLMProvider
from langchain_openai import ChatOpenAI

DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=200
DEFAULT_TOP_P=0.9
DEFAULT_TOP_K=40
DEFAULT_REPEAT_PENALTY=1.1
DEFAULT_CONTEXT_SIZE=2048

# Make sure you have a Python 3 virtual environment active:
# $ source venv/bin/activate
#
# Make sure you installed the following dependencies:
# $ (venv) pip3 install llama_cpp_python
# $ (venv) pip3 install sse_starlette
# $ (venv) pip3 install starlette_context
# $ (venv) pip3 install pydantic_settings
# $ (venv) pip3 install fastapi
#
# Then run the llama.cpp server with the input mode:
# $ (venv) python3 -m llama_cpp.server --model <GGUF model path>

# To use ChatGPT 3.5 set model_name="gpt-3.5-turbo" and omit the parameter openai_api_base
# To use ChatGPT 4 set model_name="gpt-4" and omit the parameter openai_api_base
class OpenAIProvider(LLMProvider):
    def create_model(self):
        model_name = self.config['model']
        base_url = self.config['base_url']

        # Set the default parameters
        parameters = {
            'temperature': DEFAULT_TEMPERATURE,
            'max_tokens': DEFAULT_MAX_TOKENS,
            'top_p': DEFAULT_TOP_P,
            'repeat_penalty': DEFAULT_REPEAT_PENALTY
        }

        # Overwrite default values with the one in the YAML file
        if 'parameters' in self.config:
            parameters.update(self.config['parameters'])

        if self.config['debug'] == True:
            print("****************************************************************")
            print("Model parameters::                                              ")
            print("- temperature:", parameters['temperature'])
            print("- max_tokens:", parameters['max_tokens'])
            print("- top_p:", parameters['top_p'])
            print("- repeat_penalty:", parameters['repeat_penalty'])
            print("****************************************************************")

        self.model = ChatOpenAI(temperature=parameters['temperature'],
                                max_tokens=parameters['max_tokens'],
                                model_name=model_name,
                                openai_api_base=base_url,
                                model_kwargs={"top_p": parameters['top_p'],
                                              "frequency_penalty": parameters['repeat_penalty']})

    def generate(self, prompt):
        if self.config['debug'] == True:
            print("****************************************************************")
            print("Prompt:")
            print(prompt)
            print("****************************************************************")
        result = self.model.invoke(prompt)
        return result.content
