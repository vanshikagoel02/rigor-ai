import pydantic
import spacy
import sentence_transformers
import sys

print(f"Python: {sys.version}")
print(f"Pydantic: {pydantic.VERSION}")
print(f"Spacy: {spacy.__version__}")
print(f"Sentence Transformers: {sentence_transformers.__version__}")
