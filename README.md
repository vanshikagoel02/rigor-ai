
# 🛡️ RIGOR-AI: Retrieval Integrity & Grounding Observation for RAG Systems

> **"Stop measuring RAG by the answer. Start measuring the context."**

![Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![License](https://img.shields.io/badge/License-MIT-purple)

## 💡 The Problem
In Retrieval-Augmented Generation (RAG), **garbage in = garbage out**. 
Most RAG systems blindly trust the retrieved context, leading to hallucinations when the retrieval is irrelevant, incomplete, or redundant. Debugging "why the LLM hallucinated" is often a black box.

## 🚀 The Solution
**RIGOR-AI** is an auditing layer that sits *between* your Retriever and your Generator. It evaluates the quality of retrieved chunks **before** they reach the LLM. 

It assigns a **Retrieval Integrity Score** and generates a human-readable audit report, ensuring that your RAG pipeline is **explainable, reliable, and safe**.

## ✨ Key Features

### 🛡️ Pre-Generation Integrity Audit
Don't waste tokens on bad context. RIGOR-AI analyzes chunks for:
- **Relevance**: semantic similarity to the query.
- **Coverage**: Are key concepts from the query missing in the chunks?
- **Redundancy**: Are multiple chunks saying the same thing?

### 📊 Quantifiable "Integrity Score"
Get a single confidence score (0-100%) for your retrieval step.
- **Safe (80-100)**: Proceed to generation.
- **Risky (50-79)**: Proceed with caution / add warning.
- **Insufficient (<50)**: Halt generation or fallback to web search.

### 📄 Automated PDF Audit Reports
Generate professional PDF reports of the audit for compliance and debugging. Perfect for enterprise trails.

### 🧠 Grounded Answer Generation
Includes a built-in Answer Generator that only produces responses if the Integrity Score meets a safety threshold, citing specific chunks as sources.

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/) (Custom CSS for "Dark Mode" aesthetic)
- **NLP Engine**: 
  - `spacy` (Key phrase extraction, concept mapping)
  - `sentence-transformers` (Semantic similarity embeddings)
- **Visualization**: `plotly` (Interactive charts), `reportlab` (PDF generation)

## ✨ System Architecture 
{
RIGOR-AI/
│
├── app.py                     # Main Streamlit entry point
├── visualizers.py             # UI helpers (if used)
├── audit/
│   ├── relevance.py
│   ├── coverage.py
│   ├── redundancy.py
│   ├── integrity.py
│
├── utils/
│   ├── normalization.py
│   ├── file_parser.py
│   ├── pdf_export.py
│
├── assets/
│   ├── pipeline_ps1.png
│   ├── pipeline_ps2.png
│
├── requirements.txt
├── README.md                  # Main README (single, root-level)
├── ASSUMPTIONS.md
├── FINAL_SUMMARY.pdf
└── .gitignore
}

## 📸 Screenshots
*(Add your screenshots here!)*
| Dashboard View | Audit Report |
|:---:|:---:|
| ![Dashboard](<img width="980" height="727" alt="Screenshot 2026-02-07 142057" src="https://github.com/user-attachments/assets/a64892c9-ee9b-4131-be80-d6fc0b9f47c9" />) | ![Report](<img width="789" height="720" alt="Screenshot 2026-02-07 141820" src="https://github.com/user-attachments/assets/de0ac78d-8e11-4f2b-bee5-7f748a5da52e" />) |

## 🏁 Getting Started

### Prerequisites
- Python 3.9+
- A working internet connection (for downloading models)

### Installation

1. **Clone the Repo**
   ```bash
   git clone https://github.com/vanshikagoel02/rigor-ai.git
   cd rigor-ai
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLP Models**
   The system will automatically download `en_core_web_sm` and `all-MiniLM-L6-v2` on the first run.

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

## 🎯 How to Demo (for Hackathon Judges)
1. **Load Demo Scenario**: Click the "Load Demo Scenario" button in the sidebar.
2. **Run Audit**: Watch the Integrity Score calculate in real-time.
3. **Analyze**: Show the "Missing Concepts" tab to demonstrate explainability.
4. **Report**: Click "Download Audit Report" to show the PDF generation capability.
5. **Upload**: Upload a custom PDF to show it works on real data!

## 🔮 Future Roadmap
- [ ] **API Endpoint**: Serve RIGOR-AI as a microservice middleware.
- [ ] ** hallucinations detection**: Post-generation consistency check.
- [ ] **Custom thresholds**: Allow users to set their own "Safe/Risky" boundaries.

## 🤝 Contributing
Built with ❤️ by **[Team Name - shreyagoel1801]**. 
Pull requests are welcome!

---
*Built for [DataForge - IIT Roorkee] 2026.*
