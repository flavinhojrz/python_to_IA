import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  api_key=os.environ.get("OPENAI_API_KEY")
)
tools = load_tools(["ddg-search", "wikipedia"], llm=llm)

agent = initialize_agent(
	tools,
	llm,
	agent='zero-shot-react-description',
	verbose=True,
)
print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")
# print(agent.agent.llm_chain.prompt.template)

query = """
	Compose a text that explains the concept of recursion in programming.
"""
agent.run(query)
