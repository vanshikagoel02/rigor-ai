import sys
import os

# Add the current directory to sys.path so we can import src modules
sys.path.append(os.getcwd())

from src.auditor import IntegrityAuditor

def verify():
    print("Initializing IntegrityAuditor...")
    auditor = IntegrityAuditor()
    
    query = "What are the pricing tiers for the API and what are the rate limits?"
    chunks = [
        "The API offers three pricing tiers: Free, Pro, and Enterprise. The Free tier includes 1000 calls per month.",
        "Pro tier costs $49/month and allows 50,000 calls. Enterprise offers custom limits.",
        "Rate limits are enforced based on the API key used. 429 errors indicate rate limiting.",
        "The API offers three pricing tiers: Free, Pro, and Enterprise.", # Redundant
        "Apples are nutritious fruits that come in various colors." # Irrelevant
    ]
    
    print("\nRunning Audit...")
    result = auditor.audit(query, chunks)
    
    print("\n=== Audit Result ===")
    print(f"Status: {result.status}")
    print(f"Score: {result.score}")
    print(f"Relevance Scores: {result.relevance_scores}")
    print(f"Coverage Score: {result.coverage_score}")
    print(f"Missing Concepts: {result.missing_concepts}")
    print(f"Redundancy Score: {result.redundancy_score}")
    print("\n--- Explanation ---")
    print(f"Summary: {result.explanation['summary']}")
    print(f"Missing: {result.explanation['missing_concepts']}")
    print(f"Redundancy: {result.explanation['redundancy_note']}")
    print(f"Tips: {result.explanation['improvement_tip']}")
    
    # Simple assertions
    if result.score > 0 and result.status in ["Safe", "Risky", "Insufficient"]:
        print("\n✅ Verification PASSED: Score and status generated.")
    else:
        print("\n❌ Verification FAILED: Invalid score or status.")

if __name__ == "__main__":
    verify()
