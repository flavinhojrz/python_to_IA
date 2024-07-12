# Projeto de Gerenciamento de Viagens com OpenAI

## Descrição

Este projeto é um sistema de gerenciamento de viagens que utiliza a API do OpenAI para gerar roteiros de viagem detalhados e personalizados. O sistema carrega dados da web, divide-os em fragmentos menores, utiliza embeddings para representar os documentos e cria um armazenamento vetorial para recuperar informações relevantes. A integração com um modelo de linguagem grande (LLM) permite gerar respostas contextualizadas e informativas para os usuários.

## Funcionalidades

1. **Carregamento de Dados da Web**:
   - O sistema carrega dados de uma URL específica e analisa somente o conteúdo relevante usando BeautifulSoup.

2. **Divisão de Documentos**:
   - Os documentos carregados são divididos em partes menores para facilitar o processamento e a recuperação de informações.

3. **Armazenamento Vetorial**:
   - Cria um armazenamento vetorial usando embeddings do OpenAI para representar os documentos de forma eficiente.

4. **Recuperação de Documentos Relevantes**:
   - Utiliza um retriever para encontrar documentos relevantes com base na consulta do usuário.

5. **Geração de Roteiros de Viagem**:
   - Um agente supervisor gera roteiros de viagem detalhados utilizando o contexto da web, documentos relevantes e a consulta do usuário.

## Como Funciona

1. **Carregamento de Dados**:
   - A função `load_data` carrega e processa dados da web, dividindo os documentos e criando um armazenamento vetorial.

2. **Consulta de Documentos Relevantes**:
   - A função `get_relevant_docs` utiliza o retriever para encontrar documentos relevantes para a consulta do usuário.

3. **Geração de Resposta**:
   - A função `supervisor_agent` utiliza um modelo de linguagem grande (LLM) e um prompt template para gerar um roteiro de viagem detalhado com base na consulta do usuário, contexto da web e documentos relevantes.

4. **Integração Final**:
   - A função `get_response` coordena todo o processo, obtendo o contexto da web, documentos relevantes e gerando a resposta final.

## Exemplo de Uso

```python
# Exemplo de consulta para gerar um roteiro de viagem
query = "Planeje uma viagem de 7 dias para Amsterdã em outubro"
llm = OpenAI(api_key="sua_chave_de_api_aqui")

# Obtém e imprime o roteiro de viagem gerado
print(get_response(query, llm).content)
```

## Requisitos

- Python 3.7+
- Bibliotecas:
  - `openai`
  - `beautifulsoup4`
  - `dotenv`
  - `chroma`

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/projeto-gerenciamento-viagens.git
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure a chave da API do OpenAI no arquivo `.env`:
   ```
   API_KEY=sua_chave_de_api_aqui
   ```

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests. Sugestões e melhorias são bem-vindas!


