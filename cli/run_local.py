from cli.config import get_setting


def run_local_command(query, verbose):
    from transformers import MarianMTModel, MarianTokenizer

    try:
        hf_token = get_setting("HF_TOKEN")
    except RuntimeError:
        hf_token = None
    model_name = get_setting("MODEL_NAME")

    if not model_name:
        raise ValueError(
            "No model has been chosen. Use `run_local config --set_model_name` to set a model."
        )

    if verbose:
        from transformers.utils import logging

        logging.disable_progress_bar()
    else:
        print(f"Using model: {model_name}")

    tokenizer = MarianTokenizer.from_pretrained(model_name, token=hf_token)
    model = MarianMTModel.from_pretrained(model_name, token=hf_token)

    inputs = tokenizer(query, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)

    result = tokenizer.decode(translated[0], skip_special_tokens=True)

    print(result)
