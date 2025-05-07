1. Importation des bibliothèques nécessaires
Dans l'exercice, plusieurs bibliothèques sont importées, chacune ayant un rôle spécifique :

python
Copier le code
import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
asyncio : Permet de travailler avec des fonctions asynchrones, ce qui rend l'exécution du code plus rapide en permettant à l'application de faire d'autres choses pendant que des tâches lentes (comme l'accès au réseau) sont effectuées en arrière-plan.

crawl4ai : C'est une bibliothèque utilisée pour effectuer des crawls Web (explorations de sites). Elle permet de naviguer, récupérer du contenu et le traiter.

requests : Permet de récupérer des pages Web en effectuant des requêtes HTTP.

ElementTree : Sert à analyser les fichiers XML (comme les fichiers sitemap utilisés pour référencer toutes les pages d'un site Web).

2. Récupération des URL à partir du fichier Sitemap
Le Sitemap est un fichier XML qui contient la liste de toutes les pages d'un site Web. C'est un moyen pour le propriétaire du site de fournir un plan du site aux moteurs de recherche et autres outils.

python
Copier le code
def get_pydantic_ai_docs_urls():
    """
    Récupère toutes les URL à partir du fichier Sitemap du site Pydantic.
    """
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse le fichier XML
        root = ElementTree.fromstring(response.content)

        # Extrait toutes les URLs du fichier Sitemap
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]

        return urls
    except Exception as e:
        print(f"Erreur lors de la récupération du sitemap: {e}")
        return []
Ce code charge un fichier XML (Sitemap) à partir d'une URL et en extrait toutes les URLs des pages qu'il contient.

requests.get : Envoie une requête HTTP pour obtenir le contenu du fichier Sitemap.

ElementTree : Parse le fichier XML pour extraire les liens (<loc>).

3. Exploration des pages et génération de Markdown
Ensuite, l'exercice utilise un crawler asynchrone pour parcourir les pages obtenues à partir du Sitemap. Chaque page est analysée et le contenu est généré en Markdown.

python
Copier le code
async def crawl_sequential(urls: List[str]):
    print("\n=== Crawling séquentiel avec réutilisation de la session ===")

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Création du crawler
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        session_id = "session1"  # Réutilisation de la même session pour toutes les URL
        for url in urls:
            result = await crawler.arun(
                url=url,
                config=crawl_config,
                session_id=session_id
            )
            if result.success:
                print(f"Exploration réussie de: {url}")
                print(f"Longueur du Markdown: {len(result.markdown.raw_markdown)}")
            else:
                print(f"Échec de l'exploration: {url} - Erreur: {result.error_message}")
    finally:
        # Ferme le crawler (et le navigateur) après l'exploration
        await crawler.close()
AsyncWebCrawler : C'est l'objet qui s'occupe de l'exploration. Il permet de naviguer sur les pages Web de manière asynchrone.

BrowserConfig : Configure les options du navigateur, par exemple, headless=True signifie que le navigateur fonctionne sans interface graphique, ce qui est utile pour les environnements automatisés comme les serveurs.

CrawlerRunConfig : Configure l'exécution du crawler, ici spécifiquement pour générer du contenu Markdown à partir des pages explorées.

arun() : Cette fonction permet de parcourir chaque URL et de récupérer son contenu.

Après chaque exploration, le contenu de la page est converti en Markdown et sa longueur est affichée.

4. Exécution du programme principal
python
Copier le code
async def main():
    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Trouvé {len(urls)} URLs à explorer")
        await crawl_sequential(urls)
    else:
        print("Aucune URL trouvée à explorer")

if __name__ == "__main__":
    asyncio.run(main())
main() : Cette fonction récupère les URLs à partir du Sitemap, puis lance l'exploration séquentielle de ces pages.

asyncio.run(main()) : Exécute la fonction main de manière asynchrone.

Résumé :
Récupération du Sitemap : Le programme commence par récupérer un fichier XML (le Sitemap) qui contient les URLs des pages à explorer.

Exploration des Pages : Pour chaque URL, un crawler explore la page, extrait son contenu et génère du Markdown.

Affichage des Résultats : Après chaque exploration, le programme affiche des informations sur la page (comme la longueur du Markdown généré).

Améliorations Possibles : Le programme peut être amélioré en ajoutant des fonctionnalités comme la gestion d'erreurs plus robuste, l'exportation des résultats en fichiers Markdown ou l'ajout de parallélisme pour accélérer l'exploration.
