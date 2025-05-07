import os
os.environ["GROQ_API_KEY"] = "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"  # Remplace par ta vraie clé

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)

# Modèle de prompt
prompt_template = PromptTemplate.from_template(
    "Liste {n} idées de plats pour la cuisine {cuisine}."
)

# On remplit avec des valeurs
prompt = prompt_template.format(n=3, cuisine="italienne")

# On envoie au LLM
response = llm.invoke(prompt)

# On affiche la réponse
print("\nRéponse :")
print(response.content)
