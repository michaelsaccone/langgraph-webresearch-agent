

"""
Lo stato del Grafo e' che si puo' definire in modo custom oppure usare degli standard (come MessageGraph).
Questo oggetto contiene lo stato dell'agente e viene passato di nodo in nodo man mano che il cammino prosegue.
In base ai dati che si vogliono conservare, si puo' costruire uno stato piu' o meno complesso, e aggiornarlo
man mano tra i nodi. Ogni nodo prende in input questo stato, puo' leggerlo e aggiornarlo.
"""
from typing import TypedDict, List

from langchain_core.documents import Document

from core.dtos.context_relevance import RelevanceEnum


class GraphState(TypedDict):
    """
        The state of the main graph.

        Attributes:
            question: the question made by the user
            documents: List relevant documents found by semantic search in the vector database
            document_evaluation: comes from RelevanceEnum for document evaluation
            web_search: whether  to add web research for the question. If evaluation is false, web search is true.
            web_results_evaluation: comes from RelevanceEnum for web results evaluation
            generated_response: LLM final generation given the question and all the relevant context
    """
    question: str
    documents: List[Document]
    document_evaluation: RelevanceEnum
    web_search: bool
    web_results_evaluation: RelevanceEnum
    generated_response: str