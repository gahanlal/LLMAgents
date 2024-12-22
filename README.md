# LLMAgents
LLM agents to improve efficiency in various tasks:

Promptmakerwebsearch Agent: The file contains a Python-based tool that refines user-provided prompts using structured frameworks and web search results, enhancing prompt quality for OpenAI's GPT-3.5-turbo model. Complete explanation in txt file.

Database Agent: The `DBAgent` class interacts with a database by reflecting its schema, generating prompts using Jinja2 templates, sending queries to a large language model (LLM) for SQL generation, executing the SQL, and returning structured responses based on the query results. Complete explanation the txt file.

CriticAgent: The code verifies the correctness of an answer by checking it against a PDF document, web search results, and AI knowledge, then provides a final verdict using OpenAI's API. Complete explanation the txt file.
