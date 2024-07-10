import os
import bs4
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o cliente OpenAI
llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  api_key=os.environ.get("OPENAI_API_KEY")
)

# Definir consulta do usuário
query = """
	Vou viajar para Holanda em agosto de 2024.
	Quero que faça para um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço de passagem de Natal para Holanda.
"""

def research_agent(query, llm):
  # Carregar ferramentas Langchain
	tools = load_tools(["ddg-search", "wikipedia"], llm=llm)
	# Carregar prompt do hub Langchain
	prompt = hub.pull("hwchase17/react")
	# Criar agente reativo
	agent = create_react_agent(llm, tools, prompt)
	# Inicializar executor de agente
	agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt, verbose=True)
	# Executar agente
	webContext = agent_executor.invoke({"input": query})
	return webContext['output']

def load_data():
	# Inicializa o carregador de dados da web com o URL especificado e configurações de BeautifulSoup
	loader = WebBaseLoader(
		web_paths=("https://www.dicasdeviagem.com/holanda/",),  # URL da página a ser carregada
		bs_kwargs=dict(
			parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "posttitle slidecaptionwrap"))  # Apenas analisa o conteúdo das classes especificadas
		),
	)
	# Carrega os documentos da web
	docs = loader.load()
	# Inicializa o divisor de texto para dividir os documentos em partes menores
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=1000,  # Tamanho máximo de cada fragmento de texto
		chunk_overlap=200  # Sobreposição entre fragmentos consecutivos
	)
	# Divide os documentos carregados em partes menores
	splits = text_splitter.split_documents(docs)
	# Cria um armazenamento vetorial (vector store) a partir dos documentos divididos
	vector_store = Chroma.from_documents(
		documents=splits,  # Documentos divididos
		embedding=OpenAIEmbeddings()  # Utiliza embeddings do OpenAI para representar os documentos
	)
	# Converte o armazenamento vetorial em um retriever para consulta de documentos relevantes
	retrivier = vector_store.as_retriever()
	# Retorna o retriever para uso posterior
	return retrivier

def get_relevant_docs(query):
	# Carrega os dados e obtém o retriever
	retrivier = load_data()
	# Utiliza o retriever para encontrar documentos relevantes com base na consulta
	relevant_docs = retrivier.invoke(query)
	# Imprime os documentos relevantes encontrados
	print(relevant_docs)
	# Retorna os documentos relevantes
	return relevant_docs

def supervisor_agent(query, llm, webContext, relevant_documents):
	# Define o template do prompt para o agente supervisor
	prompt_template = """
		Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagem completo e detalhado.
		Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos relevantes para elaborar o roteiro.
		Contexto: {webContext}
		Documento relevante: {relevant_documents}
		Usuário: {query}
		Assistente:
	"""
	# Cria um template de prompt com as variáveis de entrada
	prompt = PromptTemplate(
		input_variables=['webContext', 'relevant_documents', 'query'],
		template=prompt_template
)
	# Cria uma sequência executável combinando o prompt e o modelo de linguagem (llm)
	sequence = RunnableSequence(
		prompt | llm
	)
	# Invoca a sequência com os dados fornecidos e obtém a resposta
	response = sequence.invoke({"webContext": webContext, "relevant_documents": relevant_documents, "query": query})
	# Retorna a resposta gerada
	return response

def get_response(query, llm):
	# Obtém o contexto da web usando o agente de pesquisa
	webContext = research_agent(query, llm)
	# Obtém documentos relevantes para a consulta
	relevant_documents = get_relevant_docs(query)
	# Usa o agente supervisor para gerar uma resposta com base na consulta, contexto e documentos relevantes
	response = supervisor_agent(query, llm, webContext, relevant_documents)
	# Retorna a resposta gerada
	return response

print(get_response(query, llm).content)
