from typing import List, Tuple, Dict

def generate_grounded_answer(query: str, chunks: List[str], relevance_scores: List[float], integrity_score: float) -> Dict[str, str]:
    """
    Generates a grounded answer based on top-ranked retrieved chunks.
    
    Args:
        query: User query
        chunks: List of retrieved text chunks
        relevance_scores: List of scores corresponding to chunks
        integrity_score: Overall integrity score (0-100)
        
    Returns:
        Dict containing:
        - 'answer': The generated text
        - 'is_grounded': Boolean indicating if answer is reliable
        - 'sources': Indices of chunks used
    """
    
    # Gating Logic
    # User Requirement: integrity_score >= threshold (e.g. 70 or 0.7)
    # Our integrity score is 0-100. Let's use 70 as the cutoff for "Safe/Good"
    # Actually, the app defines "Safe" as >= 80, "Risky" as >= 50.
    # Let's be strict: only answer if "Safe" or high "Risky" (e.g. > 65 or 70).
    # "The system should not confidently answer if retrieval quality is poor."
    
    THRESHOLD = 60.0 # Slightly lenient to allow for decent but imperfect retrieval in demos
    
    if integrity_score < THRESHOLD:
        return {
            "answer": "Retrieval integrity is too low to generate a reliable grounded answer. Please improve your retrieval context.",
            "is_grounded": False,
            "sources": []
        }
        
    # Extractive Logic
    # 1. Pair chunks with scores
    scored_chunks = list(zip(range(len(chunks)), chunks, relevance_scores))
    
    # 2. Filter for relevant chunks only (e.g. > 0.4 score) to avoid noise
    relevant_chunks = [item for item in scored_chunks if item[2] > 0.4]
    
    # 3. Sort by score descending
    relevant_chunks.sort(key=lambda x: x[2], reverse=True)
    
    # 4. Select top 2-3 chunks
    top_chunks = relevant_chunks[:2]
    
    if not top_chunks:
        return {
            "answer": "No specific chunks were found to be highly relevant to the query.",
            "is_grounded": False,
            "sources": []
        }
        
    # 5. Formulate Answer
    # Since we can't use LLM to summarize, we just concatenate the best segments.
    # To be nicer, we could just take the full text of the best chunk, or the first sentence of the top 2.
    # Let's take the full text of the top chunk, and maybe the second if it's short.
    
    answer_text = ""
    sources = []
    
    for idx, text, score in top_chunks:
        answer_text += f"{text}\n\n"
        sources.append(idx + 1) # 1-based index for display
        
    return {
        "answer": answer_text.strip(),
        "is_grounded": True,
        "sources": sources
    }
