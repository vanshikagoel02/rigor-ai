import re
from typing import List, Dict

# Pure Python implementation for Python 3.14 compatibility
# (Avoiding sentence-transformers/numpy dependencies which may be broken)

def tokenize(text: str) -> set:
    """Simple tokenizer that splits by non-alphanumeric and lowercases."""
    return set(re.findall(r'\b\w+\b', text.lower()))

def compute_jaccard_similarity(text1: str, text2: str) -> float:
    """Computes Jaccard similarity between two texts."""
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    return intersection / union if union > 0 else 0.0

def compute_relevance(query: str, chunks: List[str]) -> List[float]:
    """
    Computes relevance based on token overlap (Jaccard).
    Returns a list of scores between 0.0 and 1.0.
    """
    scores = []
    for chunk in chunks:
        # Boost intersection for query terms to simulate "relevance"
        # Jaccard is strict, so we might want a slightly looser metric:
        # Overlap coefficient: intersection / min(len(query), len(chunk))
        q_tokens = tokenize(query)
        c_tokens = tokenize(chunk)
        
        if not q_tokens:
            scores.append(0.0)
            continue
            
        intersection = len(q_tokens.intersection(c_tokens))
        # Use a modified score: percentage of query tokens found in chunk
        # This is strictly better for "Retrieval" relevance than Jaccard
        score = intersection / len(q_tokens) if q_tokens else 0.0
        scores.append(score)
        
    return scores

def compute_redundancy(chunks: List[str]) -> float:
    """
    Computes a redundancy penalty based on pairwise Jaccard similarity.
    Returns a score from 0.0 (unique) to 1.0 (highly redundant).
    """
    if len(chunks) < 2:
        return 0.0
        
    pairwise_scores = []
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            sim = compute_jaccard_similarity(chunks[i], chunks[j])
            pairwise_scores.append(sim)
    
    if not pairwise_scores:
        return 0.0
        
    # Average redundancy
    avg_redundancy = sum(pairwise_scores) / len(pairwise_scores)
    return max(0.0, min(1.0, avg_redundancy))

def compute_coverage(query_concepts: List[str], chunks: List[str]) -> Dict:
    """
    Checks presence of query concepts in the retrieved chunks.
    Returns a dict with 'score' and 'missing' concepts.
    """
    if not query_concepts:
        return {"score": 1.0, "missing": []}
        
    combined_text = " ".join(chunks).lower()
    missing = []
    found_count = 0
    
    for concept in query_concepts:
        # Simple string matching
        if concept.lower() in combined_text:
            found_count += 1
        else:
            missing.append(concept)
            
    score = found_count / len(query_concepts)
    return {"score": score, "missing": missing}

