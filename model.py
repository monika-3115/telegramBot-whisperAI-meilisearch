from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
OLLAMA_API_KEY = "ollama"
OLLAMA_BASE_URL = 'https://ollama.dealwallet.com/v1/'

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key=OLLAMA_API_KEY, 
)

def get_chat_response(prompt):
    try:
        llama_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            model='llama3',
        )
        return llama_completion.choices[0].message.content
    except Exception as e:
        return f"Exception: {e}"
