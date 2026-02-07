print("Start Import Check")
try:
    print("Importing spacy...")
    import spacy
    print("Spacy imported.")
except Exception as e:
    print(f"Spacy failed: {e}")

try:
    print("Importing sentence_transformers...")
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformers imported.")
except Exception as e:
    print(f"SentenceTransformers failed: {e}")
print("End Import Check")
