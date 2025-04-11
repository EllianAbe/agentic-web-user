import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers.json import parse_json_markdown
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",  # ou gpt-3.5-turbo
)

template = """
Você é um agente de automação web. Dado um comando em linguagem natural, gere uma lista de passos JSON que um navegador automatizado pode seguir com Playwright.

Formato dos passos (JSON):
[
    {{ "action": "goto", "args": {{"url": "..."}} }},
    {{ "action": "fill", "args": {{"selector": "...", "value": "..."}} }},
    {{ "action": "press", "args":{{"key": "..."}} }},
    {{ "action": "click", "args": {{"selector": "...", ...}} }},
    ...
]

Comando: {prompt}
"""

prompt_template = PromptTemplate.from_template(template)


def interpret_prompt(prompt: str):
    prompt_filled = prompt_template.format(prompt=prompt)
    messages = [
        SystemMessage(content="Você transforma comandos em ações Playwright."),
        HumanMessage(content=prompt_filled),
    ]

    response = llm(messages)
    try:
        # Extrai JSON bruto da resposta (pode ajustar com regex, se necessário)
        # Cuidado: use json.loads em produção
        steps = parse_json_markdown(response.content.strip())
        return steps
    except Exception as e:
        print("Erro ao interpretar resposta:", e)
        return []
