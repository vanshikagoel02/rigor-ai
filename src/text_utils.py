import re
from typing import List

# Pure Python implementation for Python 3.14 compatibility
# (Avoiding spacy dependencies)

def extract_key_concepts(text: str) -> List[str]:
    """
    Extracts key concepts (Capitalized phrases and significant nouns) from text.
    Returns a list of unique concept strings.
    """
    concepts = set()
    
    # 1. Extract Capitalized Phrases (Approximation of Named Entities)
    # Regex for sequences of Capitalized Words (e.g. "Retrieval Integrity" or "API")
    cap_phrases = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', text)
    for phrase in cap_phrases:
        if len(phrase) > 1: # Ignore single letters
            concepts.add(phrase.lower())
            
    # 2. Extract potential "noun chunks" using stopwords filter logic
    # This is a naive approximation but works for a hackathon demo
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "has", 
        "have", "had", "it", "this", "that", "these", "those", "what", "which",
        "who", "when", "where", "why", "how", "can", "could", "should", "would"
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Heuristic: Important words are long (>4 chars) and not stopwords
    # Or just add them as "concepts" if they aren't already covered by phrases
    for word in words:
        if len(word) > 4 and word not in stopwords:
            # Only add if not part of an existing phrase? 
            # Nah, let's just add it. Simpler.
            concepts.add(word)
            
    # Remove extremely common false positives if any? 
    
    return list(concepts)

def normalize_inputs(query_text: str, raw_chunks: List[str]) -> tuple:
    """
    Centralized input normalization.
    Strips whitespace, removes empty chunks, and ensures list format.
    
    Args:
        query_text: The user query string.
        raw_chunks: A list of text chunks (strings).
        
    Returns:
        (clean_query, clean_chunks) tuple.
    """
    clean_query = query_text.strip() if query_text else ""
    
    clean_chunks = []
    if raw_chunks:
        # Ensure it's a list even if passed as single string (defensive)
        if isinstance(raw_chunks, str):
            raw_chunks = [raw_chunks]
            
        for c in raw_chunks:
            if c:
                # Ensure c is a string
                text = str(c).strip()
                if text:
                    clean_chunks.append(text)
                    
    return clean_query, clean_chunks

