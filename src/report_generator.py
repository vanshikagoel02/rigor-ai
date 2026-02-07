from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

def generate_pdf_report(audit_result, query: str):
    """
    Generates a PDF report for the audit result.
    Returns: BytesIO object containing the PDF data.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0e1117'),
        alignment=1, # Center
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        alignment=1, # Center
        spaceAfter=24
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#262730'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    story = []
    
    # --- Header ---
    story.append(Paragraph("RIGOR-AI", title_style))
    story.append(Paragraph("Retrieval Integrity & Grounding Observation for RAG Systems", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    story.append(Spacer(1, 12))
    
    # --- Metadata ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Audit Report Generated:</b> {timestamp}", body_style))
    story.append(Spacer(1, 12))
    
    # --- User Query ---
    story.append(Paragraph("User Query", heading_style))
    story.append(Paragraph(query, body_style))
    story.append(Spacer(1, 12))
    
    # --- Executive Summary (Score & Status) ---
    story.append(Paragraph("Executive Summary", heading_style))
    
    # Status Color Logic
    status = audit_result.status
    if status == "Safe":
        status_color = colors.green
    elif status == "Risky":
        status_color = colors.orange
    else:
        status_color = colors.red
        
    summary_data = [
        ["Integrity Score", f"{audit_result.score:.1f} / 100"],
        ["Assessment", status]
    ]
    
    t = Table(summary_data, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (1, 1), (1, 1), status_color), # Status Color
        ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    
    # --- Findings ---
    story.append(Paragraph("Audit Findings", heading_style))
    
    # Missing Concepts
    if audit_result.missing_concepts:
        missing_text = ", ".join(audit_result.missing_concepts)
        story.append(Paragraph(f"<b>Missing Concepts:</b> <font color='red'>{missing_text}</font>", body_style))
    else:
        story.append(Paragraph("<b>Missing Concepts:</b> <font color='green'>None detected.</font>", body_style))
        
    # Redundancy
    redundancy_val = audit_result.redundancy_score
    if redundancy_val > 0.1:
         story.append(Paragraph(f"<b>Redundancy Level:</b> <font color='orange'>Detected (Score: {redundancy_val:.2f})</font>", body_style))
    else:
         story.append(Paragraph("<b>Redundancy Level:</b> <font color='green'>Minimal</font>", body_style))
         
    story.append(Spacer(1, 12))
    
    # --- Recommendations ---
    story.append(Paragraph("Recommendations", heading_style))
    tips = audit_result.explanation.get('improvement_tip', "No specific recommendations.")
    story.append(Paragraph(tips, body_style))
    
    # --- AI Summary ---
    story.append(Spacer(1, 12))
    story.append(Paragraph("Audit Summary", heading_style))
    story.append(Paragraph(audit_result.explanation.get('summary', ""), body_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
