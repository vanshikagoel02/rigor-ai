import streamlit as st
import plotly.graph_objects as go

def apply_custom_css():
    """Applies the Dark ML-style theme."""
    st.markdown("""
        <style>
        /* General Body and Background */
        .stApp {
            background-color: #0e1117; /* Dark bluish-black */
            color: #fafafa;
        }
        
        /* Titles and Headers */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #ffffff;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #a0a0a0;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* Input Card Styling */
        .input-card {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            border: 1px solid #363945;
        }
        
        /* Chunk Cards */
        .chunk-card {
            background-color: #1e212b;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #4B4B4B; /* Default gray border */
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .chunk-card:hover {
            transform: translateY(-2px);
        }
        
        /* Status Badges */
        .badge-safe {
            background-color: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            padding: 5px 10px;
            border-radius: 12px;
            font-weight: bold;
            border: 1px solid #4caf50;
            display: inline-block;
        }
        .badge-risky {
            background-color: rgba(255, 152, 0, 0.2);
            color: #ff9800;
            padding: 5px 10px;
            border-radius: 12px;
            font-weight: bold;
            border: 1px solid #ff9800;
            display: inline-block;
        }
        .badge-insufficient {
            background-color: rgba(244, 67, 54, 0.2);
            color: #f44336;
            padding: 5px 10px;
            border-radius: 12px;
            font-weight: bold;
            border: 1px solid #f44336;
            display: inline-block;
        }
        
        /* Buttons */
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

def render_status_badge(status):
    """Renders a status badge."""
    if status == "Safe":
        badge_class = "badge-safe"
        icon = "✅"
    elif status == "Risky":
        badge_class = "badge-risky"
        icon = "⚠️"
    else:
        badge_class = "badge-insufficient"
        icon = "🛑"
        
    st.markdown(f'<div class="{badge_class}">{icon} {status.upper()}</div>', unsafe_allow_html=True)

def plot_integrity_score(score, status):
    """Plots a gauge chart for the integrity score."""
    if status == "Safe":
        color = "#4caf50"
    elif status == "Risky":
        color = "#ff9800"
    else:
        color = "#f44336"
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Retrieval Integrity Score"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(244, 67, 54, 0.1)'},
                {'range': [50, 80], 'color': 'rgba(255, 152, 0, 0.1)'},
                {'range': [80, 100], 'color': 'rgba(76, 175, 80, 0.1)'}],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Inter"},
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_chunk_card(index, text, score, is_redundant):
    """Renders a card for a retrieved chunk."""
    border_color = "#4B4B4B"
    if score > 0.7:
        border_color = "#4caf50"
    elif score < 0.3:
        border_color = "#f44336"
        
    redundant_tag = ""
    if is_redundant:
        redundant_tag = '<span style="color:#ff9800; font-size:0.8rem; float:right;">⚠️ Redundant</span>'
        
    html = f"""
    <div class="chunk-card" style="border-left: 5px solid {border_color};">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-weight:bold; color:#888;">Chunk {index+1}</span>
            <span style="background:#333; padding:2px 6px; border-radius:4px; font-size:0.8rem;">Relevance: {score:.2f}</span>
        </div>
        {redundant_tag}
        <div style="font-size:0.95rem; line-height:1.5; color:#ddd;">
            {text[:300] + "..." if len(text) > 300 else text}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)