import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import streamlit as st

def create_analysis_pdf(filename, score, read_score, sentiment, grade, overall_score, 
                       strengths, weaknesses, tips, keywords, section_scores=None, 
                       recommendations=None):
    """
    Create a professionally formatted PDF report of the pitch deck analysis.
    
    Args:
        filename: Name of the analyzed file
        score: Section coverage score
        read_score: Readability score
        sentiment: Sentiment analysis result
        grade: Overall grade
        overall_score: Overall numerical score
        strengths: List of strengths
        weaknesses: List of weaknesses
        tips: List of tips/recommendations
        keywords: List of key terms
        section_scores: Dictionary of section scores (optional)
        recommendations: List of detailed recommendations (optional)
    
    Returns:
        PDF file as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Custom styles
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        textColor=colors.HexColor('#3182CE'),
        spaceAfter=12
    )
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        leftIndent=20,
        firstLineIndent=-15,
        spaceAfter=6
    )
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph(f"PitchPerfect AI Analysis Report", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # File info and date
    elements.append(Paragraph(f"Analysis of: <b>{filename}</b>", normal_style))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Summary scores
    data = [
        ["Section Coverage", "Readability", "Overall Score", "Grade"],
        [f"{score}/10", f"{read_score:.1f}", f"{overall_score}/100", grade]
    ]
    
    # Create table for summary scores
    summary_table = Table(data, colWidths=[1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#EBF4FF')),
        ('TEXTCOLOR', (0, 0), (3, 0), colors.HexColor('#2C5282')),
        ('ALIGN', (0, 0), (3, 1), 'CENTER'),
        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (3, 0), 10),
        ('BOTTOMPADDING', (0, 0), (3, 0), 8),
        ('BACKGROUND', (0, 1), (3, 1), colors.white),
        ('GRID', (0, 0), (3, 1), 1, colors.HexColor('#CBD5E0')),
        ('FONTNAME', (0, 1), (3, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (3, 1), 12),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Create radar chart for section scores if available
    if section_scores:
        # Generate radar chart
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, polar=True)
        
        # Prepare data
        categories = list(section_scores.keys())
        values = list(section_scores.values())
        
        # Number of variables
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Add values (and close the loop)
        values += values[:1]
        
        # Draw the plot
        ax.plot(angles, values, linewidth=2, linestyle='solid', color='#3182CE')
        ax.fill(angles, values, alpha=0.25, color='#3182CE')
        
        # Add labels
        plt.xticks(angles[:-1], categories, size=8)
        
        # Add y-axis labels (0-10)
        plt.yticks([2, 4, 6, 8, 10], ['2', '4', '6', '8', '10'], color='grey', size=7)
        plt.ylim(0, 10)
        
        # Save chart to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        
        # Add chart to PDF
        img = Image(img_buffer, width=4*inch, height=4*inch)
        elements.append(Paragraph("Section Coverage Analysis", section_title))
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
    
    # Strengths
    elements.append(Paragraph("Strengths", section_title))
    for strength in strengths:
        elements.append(Paragraph(f"• {strength}", bullet_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Areas to Improve
    elements.append(Paragraph("Areas to Improve", section_title))
    for weakness in weaknesses:
        elements.append(Paragraph(f"• {weakness}", bullet_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Recommendations
    elements.append(Paragraph("Recommendations", section_title))
    for tip in tips:
        elements.append(Paragraph(f"• {tip}", bullet_style))
    
    # Detailed recommendations if available
    if recommendations:
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Detailed Recommendations", section_title))
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(f"{i}. {rec}", bullet_style))
    
    # Key Terms
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Key Terms", section_title))
    
    # Create a table for keywords (3 columns)
    keyword_rows = []
    row = []
    for i, keyword in enumerate(keywords):
        row.append(keyword)
        if (i + 1) % 3 == 0 or i == len(keywords) - 1:
            # Pad the row if needed
            while len(row) < 3:
                row.append("")
            keyword_rows.append(row)
            row = []
    
    if keyword_rows:
        keyword_table = Table(keyword_rows, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
        keyword_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7FAFC')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(keyword_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        f"Generated by PitchPerfect AI on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey)
    ))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def get_pdf_download_link(pdf_bytes, filename="analysis_report.pdf"):
    """
    Generate a download link for the PDF report.
    
    Args:
        pdf_bytes: PDF file as bytes
        filename: Name for the downloaded file
    
    Returns:
        HTML string with download link
    """
    b64 = base64.b64encode(pdf_bytes.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="text-decoration: none;">📥 Download PDF Report</a>'
    return href

def display_download_button(analysis_data, filename):
    """
    Display a download button for the PDF report in Streamlit.
    
    Args:
        analysis_data: Dictionary containing analysis results
        filename: Name of the analyzed file
    """
    # Extract data from analysis_data
    score = analysis_data.get('score', 0)
    read_score = analysis_data.get('readability', 0)
    sentiment = analysis_data.get('sentiment', 'Neutral')
    strengths = analysis_data.get('strengths', [])
    weaknesses = analysis_data.get('weaknesses', [])
    tips = analysis_data.get('tips', [])
    keywords = analysis_data.get('keywords', [])
    section_scores = analysis_data.get('section_scores', {})
    advanced_results = analysis_data.get('advanced_results', {})
    grade = advanced_results.get('grade', 'B+')
    overall_score = advanced_results.get('overall_score', 75)
    recommendations = advanced_results.get('recommendations', [])
    
    # Create PDF
    pdf_buffer = create_analysis_pdf(
        filename, score, read_score, sentiment, grade, overall_score,
        strengths, weaknesses, tips, keywords, section_scores, recommendations
    )
    
    # Display download button
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_buffer,
        file_name=f"{filename.split('.')[0]}_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )