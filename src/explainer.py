from typing import List, Dict

def generate_audit_explanation(score: float, status: str, 
                             relevance_scores: List[float], 
                             coverage_data: Dict, 
                             redundancy_score: float) -> Dict[str, str]:
    """
    Generates human-readable explanations for the audit verification.
    Returns a dict with keys: 'summary', 'missing_concepts', 'redundancy_note', 'improvement_tip'
    """
    
    # 1. Summary Explanation
    if status == "Safe":
        summary = f"The retrieval is **Safe** ({score:.1f}/100). The chunks are highly relevant and cover required concepts."
    elif status == "Risky":
        summary = f"The retrieval is **Risky** ({score:.1f}/100). It may lack key details or contain irrelevant info."
    else:
        summary = f"The retrieval is **Insufficient** ({score:.1f}/100). The chunks fundamentally fail to address the query."
        
    # 2. Missing Concepts
    missing = coverage_data.get("missing", [])
    if missing:
        missing_text = f"The following key concepts are missing: **{', '.join(missing)}**."
    else:
        missing_text = "All key concepts from the query appear to be covered."
        
    # 3. Redundancy Note
    if redundancy_score > 0.3:
        redundancy_text = "⚠️ High redundancy detected. Multiple chunks contain near-identical information."
    elif redundancy_score > 0.1:
        redundancy_text = "ℹ️ Some redundancy detected, but it's acceptable."
    else:
        redundancy_text = "✅ Information is diverse with minimal repetition."
        
    # 4. Improvement Tip
    tips = []
    avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
    if avg_relevance < 0.6:
        tips.append("Try refining the query to be more specific.")
    if missing:
        tips.append(f"Ensure the database contains documents about '{missing[0]}'.")
    if redundancy_score > 0.3:
        tips.append("Reduce 'top_k' or apply Maximal Marginal Relevance (MMR) reranking.")
        
    if not tips:
        tips.append("The retrieval looks good! no immediate actions needed.")
        
    return {
        "summary": summary,
        "missing_concepts": missing_text,
        "redundancy_note": redundancy_text,
        "improvement_tip": " ".join(tips)
    }
