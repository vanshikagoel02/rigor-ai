from dataclasses import dataclass, field
from typing import List, Dict
import numpy as np

from src import metrics, text_utils, explainer

@dataclass
class AuditResult:
    score: float
    status: str
    relevance_scores: List[float]
    coverage_score: float
    missing_concepts: List[str]
    redundancy_score: float
    explanation: Dict[str, str] = field(default_factory=dict)

class IntegrityAuditor:
    def __init__(self):
        # Weighted Scoring Configuration
        self.w_relevance = 0.4
        self.w_coverage = 0.4
        self.w_redundancy = 0.1
        self.w_penalty = 0.1 # Penalty for gaps
        
    def audit(self, query: str, chunks: List[str]) -> AuditResult:
        if not query or not chunks:
            return AuditResult(0, "Insufficient", [], 0, [], 0)
            
        # 1. Compute Metrics
        relevance_scores = metrics.compute_relevance(query, chunks)
        avg_relevance = np.mean(relevance_scores) if relevance_scores else 0.0
        
        concepts = text_utils.extract_key_concepts(query)
        coverage_data = metrics.compute_coverage(concepts, chunks)
        coverage_score = coverage_data["score"]
        
        redundancy_score = metrics.compute_redundancy(chunks)
        
        # 2. Compute Integrity Score
        # Formula: (Rel * 0.4 + Cov * 0.4) - (Red * 0.1)
        raw_score = (avg_relevance * self.w_relevance) + (coverage_score * self.w_coverage)
        
        # Penalties
        # If coverage is very low, apply extra penalty
        gap_penalty = 0.0
        if coverage_score < 0.5:
             gap_penalty += 0.1
             
        final_score = raw_score - (redundancy_score * self.w_redundancy) - gap_penalty
        
        # Normalize to 0-100
        # raw_score max is 0.8. We map 0.0-0.8 roughly to 0-100, but let's be simpler.
        # Let's just scale final_score (which is roughly -0.2 to 0.8) to 0-100
        # A perfect score is 0.8. Let's multiply by 125 to get 100? 
        # 0.4 + 0.4 = 0.8. 0.8 * 125 = 100.
        score_100 = max(0.0, min(100.0, final_score * 125))
        
        # 3. determine Status
        if score_100 >= 80:
            status = "Safe"
        elif score_100 >= 50:
            status = "Risky"
        else:
            status = "Insufficient"
            
        # 4. Generate Explanation
        explanation = explainer.generate_audit_explanation(
            score_100, status, relevance_scores, coverage_data, redundancy_score
        )
        
        return AuditResult(
            score=score_100,
            status=status,
            relevance_scores=relevance_scores,
            coverage_score=coverage_score,
            missing_concepts=coverage_data["missing"],
            redundancy_score=redundancy_score,
            explanation=explanation
        )
