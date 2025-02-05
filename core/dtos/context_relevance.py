from enum import Enum


class RelevanceEnum(str, Enum):
    """
    Measure for the relevance level of context with a given question.
    """
    no_relevance = 'no_relevance'
    partial_relevance = 'partial_relevance'
    full_relevance = 'full_relevance'