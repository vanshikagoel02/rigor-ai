import streamlit as st
import time
from src.auditor import IntegrityAuditor
from src.report_generator import generate_pdf_report
from src.answer_generator import generate_grounded_answer
from src.text_utils import normalize_inputs
from utils import visualizers
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Retrieval Integrity Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Initialize ---
@st.cache_resource
def get_auditor():
    return IntegrityAuditor()

auditor = get_auditor()
visualizers.apply_custom_css()

# --- Branding ---
st.markdown("""
    <div style='text-align: center; margin-bottom: -20px;'>
        <h3 style='color: #a0a0a0; font-size: 1.2rem; margin-bottom: 0;'>RIGOR-AI</h3>
        <p style='color: #666; font-size: 0.9rem; margin-top: 0;'>Retrieval Integrity & Grounding Observation for RAG Systems</p>
    </div>
""", unsafe_allow_html=True)
st.title("🛡️ Retrieval Integrity Auditor")
st.markdown('<p class="subtitle">Audit the quality of your RAG context <i>before</i> generation.</p>', unsafe_allow_html=True)

# --- Demo Data ---
DEMO_SCENARIO = {
    "query": "What are the pricing tiers for the API and what are the rate limits?",
    "chunks": [
        "The API offers three pricing tiers: Free, Pro, and Enterprise. The Free tier includes 1000 calls per month.",
        "Pro tier costs $49/month and allows 50,000 calls. Enterprise offers custom limits.",
        "Rate limits are enforced based on the API key used. 429 errors indicate rate limiting.",
        "The API offers three pricing tiers: Free, Pro, and Enterprise.",
        "Apples are nutritious fruits that come in various colors."
    ]
}

# --- Input Section ---
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    # State Management for Input Source
    if 'active_source' not in st.session_state:
        st.session_state.active_source = 'manual' # Default
        
    col_demo, col_audit = st.columns([1, 1])
    
    with col_demo:
        if st.button("Load Demo Scenario", use_container_width=True):
            st.session_state.active_source = 'demo'
            # Pre-fill manual inputs for visibility (optional but helpful)
            st.session_state.input_query = DEMO_SCENARIO["query"]
            st.session_state.input_chunks = "\n\n".join(DEMO_SCENARIO["chunks"])
            st.rerun()

        if st.session_state.active_source == 'demo':
            if st.button("Clear Demo / Reset", type="secondary", use_container_width=True):
                st.session_state.active_source = 'manual'
                st.session_state.input_query = ""
                st.session_state.input_chunks = ""
                st.rerun()

    # File Upload
    uploaded_file = st.file_uploader("📎 Upload Context File (Optional)", type=['txt', 'md', 'pdf'], help="Upload a document to audit retrieved context automatically")
    
    # Logic: Determine Active Data
    # Priority: Demo (> File -> Manual)
    # The prompt says: IF demo loaded: use demo. ELSE IF file uploaded: use file. ELSE: manual.
    
    final_query = ""
    final_chunks = []
    
    # If file was just uploaded, switch source to file unless demo is explicitly active?
    # Actually, simpler: check state.
    
    if st.session_state.active_source == 'demo':
        st.info("🔹 Demo Scenario Active. (Clear Demo to use File Upload or Manual Input)")
        final_query = DEMO_SCENARIO["query"]
        final_chunks = DEMO_SCENARIO["chunks"]
        
        # Display as disabled text areas
        st.text_area("User Query (Demo)", value=final_query, disabled=True, height=70)
        st.text_area("Retrieved Chunks (Demo)", value="\n\n".join(final_chunks), disabled=True, height=150)
        
    elif uploaded_file:
        st.session_state.active_source = 'file'
        # File Processing
        try:
            file_text = ""
            if uploaded_file.type == "application/pdf":
                import pypdf
                pdf_reader = pypdf.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    extract = page.extract_text()
                    if extract: file_text += extract + "\n"
            else:
                file_text = uploaded_file.read().decode("utf-8")
                
            # Auto-chunking (paragraphs)
            raw_file_chunks = [c.strip() for c in file_text.split('\n\n') if c.strip()]
            
            if not raw_file_chunks:
                st.warning("⚠️ File uploaded but no text paragraphs found.")
            else:
                st.success(f"✅ File Loaded: {uploaded_file.name} ({len(raw_file_chunks)} chunks). Manual chunks ignored.")
                final_chunks = raw_file_chunks
                
            # Query is still manual
            final_query = st.text_area("User Query", value=st.session_state.get('input_query', ""), height=70, placeholder="Enter query regarding the file...", key="file_query_input")
            st.text_area("Retrieved Chunks", value="[Using File Content]", disabled=True, height=100)
            
        except Exception as e:
            st.error(f"Error reading file: {e}")
            
    else:
        st.session_state.active_source = 'manual'
        # Manual Input
        final_query = st.text_area("User Query", value=st.session_state.get('input_query', ""), height=70, placeholder="Enter the user prompt here...", key="manual_query_input")
        chunks_text = st.text_area("Retrieved Chunks (separated by empty lines)", value=st.session_state.get('input_chunks', ""), height=150, placeholder="Chunk 1...\n\nChunk 2...", key="manual_chunks_input")
        if chunks_text:
            final_chunks = chunks_text.split('\n\n')

    # Audit Button
    with col_audit:
        if st.button("🔍 Run Audit", type="primary", use_container_width=True):
            # 1. Normalize
            clean_query, clean_chunks = normalize_inputs(final_query, final_chunks)
            
            # 2. Guardrails
            if not clean_query:
                st.error("⚠️ User Query cannot be empty.")
            elif not clean_chunks:
                st.error("⚠️ No valid chunks found. Please provide context.")
            else:
                # 3. Execution
                with st.spinner("Auditing retrieval integrity..."):
                    time.sleep(0.5) # UX delay
                    result = auditor.audit(clean_query, clean_chunks)
                
                # --- Audit Results Display ---
                st.divider()
                st.subheader("Audit Results")
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    visualizers.render_status_badge(result.status)
                    st.write("")
                    visualizers.plot_integrity_score(result.score, result.status)
                    
                with c2:
                    st.markdown(f"**Summary:** {result.explanation['summary']}")
                    
                    # Explainability Tabs
                    tab1, tab2, tab3 = st.tabs(["Missing", "Redundancy", "Suggestions"])
                    with tab1:
                        if result.missing_concepts:
                            st.error(f"Missing: {', '.join(result.missing_concepts)}")
                        else:
                            st.success("No missing concepts detected.")
                    with tab2:
                        if result.redundancy_score > 0.1:
                            st.warning(result.explanation['redundancy_note'])
                        else:
                            st.success("Redundancy is low.")
                    with tab3:
                        st.info(result.explanation['improvement_tip'])
                        
                    # PDF Report
                    pdf_bytes = generate_pdf_report(result, clean_query)
                    file_name = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    st.download_button("📄 Download Audit Report (PDF)", data=pdf_bytes, file_name=file_name, mime="application/pdf")

                # --- Answer Generation (Optional & Gated) ---
                # Threshold check: defined in src.answer_generator but checked here for UI flow?
                # Actually, the requirement says "Answer generation... Gated by integrity score".
                # We should call it, and if it returns check, display.
                # Or check score first. The logic is inside generate_grounded_answer too.
                
                st.divider()
                st.subheader("Grounded Answer Generation")
                
                # Check threshold locally or let generator handle?
                # Let's let generator handle and check logical flag.
                
                gen_result = generate_grounded_answer(clean_query, clean_chunks, result.relevance_scores, result.score)
                
                if gen_result['is_grounded']:
                    st.success("✅ Integrity sufficient for answer generation.")
                    st.markdown(f"**Answer:**\n\n{gen_result['answer']}")
                    st.caption(f"Sources used: {gen_result['sources']}")
                else:
                    st.warning("⚠️ Retrieval Integrity too low for confident answer generation.")
                    st.markdown(f"_{gen_result['answer']}_")

                # --- Chunk Analysis ---
                st.divider()
                st.subheader(f"Chunk Analysis ({len(clean_chunks)} chunks)")
                
                chunk_cols = st.columns(2)
                # Compute redundancy flags for UI
                # (Simple pairwise check matches app logic)
                from src import metrics
                processed = []
                red_flags = []
                for c in clean_chunks:
                    is_red = False
                    for p in processed:
                        if metrics.compute_jaccard_similarity(c, p) > 0.6:
                            is_red = True
                            break
                    processed.append(c)
                    red_flags.append(is_red)
                
                for i, (chunk, score, is_r) in enumerate(zip(clean_chunks, result.relevance_scores, red_flags)):
                    with chunk_cols[i % 2]:
                        visualizers.render_chunk_card(i, chunk, score, is_r)

    st.markdown('</div>', unsafe_allow_html=True)