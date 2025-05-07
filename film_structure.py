import os
os.environ["GROQ_API_KEY"] = "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"

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Film(BaseModel):
    title: str = Field(description="Titre du film.")
    genre: list[str] = Field(description="Genre du film.")
    year: int = Field(description="Année de sortie.")

llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)
parser = PydanticOutputParser(pydantic_object=Film)

prompt_text = """
Donne un film correspondant à la requête ci-dessous au format suivant :\n
{format_instructions}\n
{query}
"""

prompt_template = PromptTemplate(
    template=prompt_text,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt = prompt_template.format(query="Un film d'action avec Tom Cruise des années 90")
result = llm.invoke(prompt)
print("\nTexte brut :")
print(result.content)

parsed = parser.parse(result.content)
print("\nRésultat structuré :")
print(parsed)
