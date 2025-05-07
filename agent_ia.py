import os
os.environ["GROQ_API_KEY"] = "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"

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, Tool
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)

math_prompt = PromptTemplate.from_template(
    "Calcule cette expression et réponds comme suit : 'Réponse : <nombre>' : {question}"
)
llm_math_chain = LLMMathChain.from_llm(llm=llm, prompt=math_prompt, verbose=True)

calculator = Tool(
    name="calculatrice",
    description="Effectue des calculs mathématiques",
    func=lambda x: llm_math_chain.run({"question": x}),
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="recherche",
    description="Recherche des infos sur internet",
    func=search.run
)

tools = [search_tool, calculator]
agent = StructuredChatAgent.from_llm_and_tools(llm=llm, tools=tools)

executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)

# Exemple d'utilisation
result = executor.invoke({"input": "Quelle est la différence de population entre la France et l’Italie ?"})
print(result["output"])
