from typing import List
import uvloop
from langchain_community.document_loaders import WebBaseLoader

from core.vector_store.text_splitters import text_split

base_urls = [
    "https://it.wikipedia.org/wiki/Mario_Rigoni_Stern",
    "https://ricette.giallozafferano.it/Risotto-alla-zucca.html",
    "https://it.wikipedia.org/wiki/Seconda_guerra_mondiale",
    "https://it.wikipedia.org/wiki/Giacomo_Leopardi"
]

"""
Asynchronously downloads the given web pages and parses them, yielding them one by one.
Any yielded page can then be split 
"""
async def download_web_pages(urls: List[str]):
    loader =  WebBaseLoader(base_urls)
    async for doc in loader.alazy_load():
        print(doc)


uvloop.run(download_web_pages([base_urls[0]]))
