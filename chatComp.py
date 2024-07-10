import os
from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# OpenAI com a chave da API
client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a text that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message.content)
