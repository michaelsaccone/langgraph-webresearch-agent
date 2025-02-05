from dotenv import load_dotenv
load_dotenv()

"""
Group of functions to split a text in multiple chunk based on different techniques.
"""
from collections.abc import Callable
from typing import List

from bs4 import Tag
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLSemanticPreservingSplitter

"""
Splits text using an embedder between sentences for a semantic comparation.
Based on distances between sentences decides to merge or split.
"""
semantic_text_splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="gradient" # or percentile
)

"""
Recursively split text using characters [ "\n\n", "\n", " ", "" ]
to get small and smaller chunks based on the provided size.
This split method seems to be the most efficient for the small cost.
Tries to separate into paragraph, then sentences, then words, then characters.
"""
recursive_char_splitter = RecursiveCharacterTextSplitter(
    # number of characters for each chunk
    chunk_size=1000,
    # overlapping characters between chunks
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False
)

"""
HTML splitters are many, all trying to manage html code and preserve semantic
Html Semantic Splitter Combines a tag splitter and 
"""
headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
]

def code_handler(element: Tag) -> str:
    data_lang = element.get("data-lang")
    code_format = f"<code:{data_lang}>{element.get_text()}</code>"

    return code_format


html_splitter = HTMLSemanticPreservingSplitter(
    headers_to_split_on=headers_to_split_on,
    separators=["\n\n", "\n", ". ", "! ", "? "],
    max_chunk_size=300,
    preserve_images=True,
    preserve_videos=True,
    elements_to_preserve=["table", "ul", "ol", "code"],
    denylist_tags=["script", "style", "head"],
    custom_handlers={"code": code_handler},
)
"""
 
 = = = = = = = FUNCTIONS = = = = = = = = =
  
    The following functions are a level of abstraction 
    for the different techniques. In the future the same techniques might
    use different libraries. 
    So the library layer is covered.    
"""

def split_merging_metadata(text: str | Document, splitter: Callable[[list[str] | str], List[Document]]) -> List[Document]:
    final_docs = []
    if type(text) == Document:
        content = text.page_content
        metadata = text.metadata
        docs = splitter([content])
        # Preserve metadata
        final_docs = [Document(page_content=doc.page_content, metadata=metadata | doc.metadata) for doc in docs]
    else:
        final_docs = splitter([text])
    return final_docs

def semantic_split(text: str | Document) -> List[Document]:
    docs = split_merging_metadata(text, semantic_text_splitter.create_documents)
    return docs

def text_split(text: str | Document) -> List[Document]:
    docs = split_merging_metadata(text, recursive_char_splitter.create_documents)
    return docs

def html_split(text: str | Document) -> List[Document]:
    # Since html split doesn't want an array of string but exceptionally only a string,
    # we pass a function that given an array, calls the splitter with the first and only entry.
    docs = split_merging_metadata(text, lambda x: html_splitter.split_text(x[0]))
    return docs
