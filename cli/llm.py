import os
from dotenv import set_key
from constants import PROVIDER_SPECS

def llm_command(source_lang: str, target_lang: str, text: str) -> None:
    supported_providers = tuple(PROVIDER_SPECS.keys())

    llm_provider = os.environ.get('LLM_PROVIDER')

    if llm_provider not in supported_providers:
        raise ValueError(f"The LLM provider '{llm_provider}' is not supported. Please use the config flag to set environment variables.")
    
    llm_model_name = os.environ.get(PROVIDER_SPECS[llm_provider]['model_env'])
    llm_api_key = os.environ.get(PROVIDER_SPECS[llm_provider]['api_key_env'])

    if llm_model_name == None:
        raise ValueError(f"No {PROVIDER_SPECS[llm_provider]['model_env']} environment variable found.")
    if llm_api_key == None:
        raise ValueError(f"No {PROVIDER_SPECS[llm_provider]['api_key_env']} environment variable found.")

    result = translate_with_llm(llm_provider, llm_model_name, llm_api_key, source_lang, target_lang, text)
    print(result)


def translate_with_llm(llm_provider: str, llm_model_name: str, llm_api_key: str, source_lang: str, target_lang: str, text: str) -> str:
    if llm_provider == 'openai':
        return translate_with_openai(llm_model_name, llm_api_key, source_lang, target_lang, text)
    if llm_provider == 'anthropic':
        return translate_with_anthropic()
    if llm_provider == 'gemini':
        return translate_with_gemini()
    raise ValueError(f"The LLM provider {provider} is not supported inside this function!")

def translate_with_openai(llm_model_name: str, llm_api_key: str, source_lang: str, target_lang: str, text: str) -> str:
    print(f"Requesting translation from {source_lang} to {target_lang} from OpenAI for the following text:")
    print(text)
    from openai import OpenAI, APIConnectionError, PermissionDeniedError, AuthenticationError, RateLimitError
    
    client = OpenAI(api_key=llm_api_key)
    
    try:
        response = client.responses.create(
            model=llm_model_name,
            instructions=f"You are a {source_lang} to {target_lang} translator. Provide only the tranlation of the given text.",
            input=text,
        )
    except APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)
    except PermissionDeniedError as e:
        print(f'Status code {e.status_code} raised, permission denied.')
        print(' Cause: You don’t have access to the requested resource.')
        print(' Solution: Ensure you are using the correct API key, organization ID, and resource ID.')
        exit(1)
    except AuthenticationError as e:
        print(f"Status code {e.status_code} raised, authentication error")
        print(' Cause: Your API key or token was invalid, expired, or revoked.')
        print(' Solution: Check your API key or token and make sure it is correct and active. You may need to generate a new one from your account dashboard.')
        exit(1)
    except RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        exit(1)

    return response.output_text
