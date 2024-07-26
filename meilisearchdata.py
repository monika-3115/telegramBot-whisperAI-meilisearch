import meilisearch
from dotenv import load_dotenv
import os
load_dotenv()
MASTER_KEY = os.getenv("MASTER_KEY")
MEILISEARCH_URL = os.getenv("MEILISEARCH_URL")

def meili_search_text(text):
    client = meilisearch.Client(MEILISEARCH_URL, MASTER_KEY)
    index = client.index('movies')
    response = index.search(
        text, 
        {
            'hybrid': {
                'semanticRatio': 0.8,
                'embedder': 'default'
            }
        }
    )
    print(response)
    results = response['hits']
    messages = []
    if results:
        for result in results:
            title = result.get('title')
            overview = result.get('overview')
            message_text = f"<b>{title}</b>\n\n{overview}"
            messages.append(message_text)
    else:
        messages.append("No results found.")
    
    return messages

