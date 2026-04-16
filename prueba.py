import config
from groq import Groq

client = Groq(api_key=config.LLM_GROQ_API_KEY)

models = client.models.list()

for m in models.data:
    print(m.id)