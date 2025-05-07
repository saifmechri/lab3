import os
os.environ["GROQ_API_KEY"] = "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"
from langchain_groq import ChatGroq

# Créer le modèle
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)

# Demander une réponse à l'IA
response = llm.invoke("Donne-moi 3 pays d’Afrique.")

# Afficher la réponse
print("Réponse :", response.content)
