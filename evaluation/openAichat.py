from typing import Optional
import openai
def query_gpt(
prompt: str, temperature: float = 0.7
) -> Optional[str]:
    model = "gpt-4o-2024-08-06"
    api_key = "sk-QVjQZ6YsSIr49UYSstfIwVMhYaz5f7iED4fmBsSE1gjJvoXy"
    base_url = "https://sg.uiuiapi.com/v1/"
    openai.api_key = api_key
    openai.base_url = base_url

    try:
        chat_completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(e)
        return None

print(query_gpt("who are you"))