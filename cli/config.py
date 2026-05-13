import os

from dotenv import set_key
from huggingface_hub import list_models
from constants import PROVIDER_SPECS

def config_command(model_name: str, list_model_names: bool, llm_provider: str, llm_model_name: str, llm_api_key: str):
    model_list = list_models(author="Helsinki-NLP")

    if list_model_names:
        for model in model_list:
            if "opus-mt_tiny" in model.id:
                print(model.id)

    if model_name:
        if "opus-mt_tiny" not in model_name:
            raise ValueError(f"The model name given is {model_name} but only the 'opus-mt-tiny' models are supported. Use the --list_model_names flag to find all supported models.")

        model_found = False
        for model in model_list:
            if model_name == model.id:
                model_found = True

        if not model_found:
            raise ValueError(f"The model {model_name} could not be found. ")

        set_key('.env', 'MODEL_NAME', model_name)
        print(f"Default model set to {model_name}")

    if llm_provider:
        supported_providers = tuple(PROVIDER_SPECS.keys())
        if llm_provider not in supported_providers:
            print(f"The LLM provider '{llm_provider}' is not supported. Please choose one from the list of supported providers:")
            for provider in supported_providers:
                print(provider)

            while llm_provider not in supported_providers:
                llm_provider = input('Choose provider: ')

                if llm_provider not in supported_providers:
                    print(f"The provider '{llm_provider}' is not supported. Please choose among the supported providers.")

        set_key('.env', 'LLM_PROVIDER', llm_provider)
        print('LLM_PROVIDER set to', llm_provider)

    if llm_model_name:
        if not llm_provider:
            llm_provider = os.environ.get('LLM_PROVIDER')
        set_key('.env', PROVIDER_SPECS[llm_provider]['model_env'], llm_model_name)
        print(f"{PROVIDER_SPECS[llm_provider]['model_env']} has been set to {llm_model_name}")

    if llm_api_key:
        if not llm_provider:
            llm_provider = os.environ.get('LLM_PROVIDER')
        llm_api_key = os.environ.get(PROVIDER_SPECS[llm_provider]['api_key_env'])
        set_key('.env', PROVIDER_SPECS[llm_provider]['api_key_env'], llm_api_key)
        print(f"{PROVIDER_SPECS[llm_provider]['api_key_env']} has been set to {llm_api_key}")
