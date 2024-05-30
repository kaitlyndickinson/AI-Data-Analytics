from openai import OpenAI
import constants

client = OpenAI(
    api_key=constants.OPENAI_API_KEY,
)


def get_completion(messages, stream=True):
    """
    Generates a completion using OpenAI's GPT-3.5 model.

    Parameters:
    messages (str or List[str]): The prompt or list of prompts to generate completions for.
    stream (bool, optional): Whether to use streaming for the completion. Defaults to True.

    Returns: 
    ChatCompletion | Stream[ChatCompletionChunk]
    """
    completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        stream=stream
    )

    return completion


