# auto-research-agent/utils/pdf_generator.py

import os
import jinja2
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def generate_pdf_from_template(
    data: dict,
    template_name: str,
    template_dir: str,
    output_path: str
) -> bool:
    """
    Generates a PDF file from a Jinja2 HTML template and a data dictionary using ReportLab.

    Args:
        data: The dictionary containing data to be rendered in the template.
        template_name: The filename of the Jinja2 template (e.g., "report_template.html").
        template_dir: The directory where the template is located.
        output_path: The full path where the output PDF will be saved.

    Returns:
        True if the PDF was generated successfully, False otherwise.
    """
    if not data:
        print("PDF Generator: No data provided. Aborting.")
        return False

    print(f"PDF Generator: Starting PDF generation...")
    print(f"PDF Generator: Template directory: {template_dir}")
    print(f"PDF Generator: Template name: {template_name}")
    print(f"PDF Generator: Output path: {output_path}")
    print(f"PDF Generator: Data keys: {list(data.keys())}")

    try:
        # Check if template directory exists
        if not os.path.exists(template_dir):
            print(f"PDF Generator Error: Template directory does not exist: {template_dir}")
            return False

        # Check if template file exists
        template_path = os.path.join(template_dir, template_name)
        if not os.path.exists(template_path):
            print(f"PDF Generator Error: Template file does not exist: {template_path}")
            return False

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            print(f"PDF Generator: Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)

        # --- 1. Set up Jinja2 Environment ---
        template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)

        # --- 2. Render HTML from Template ---
        html_content = template.render(data=data)
        print(f"PDF Generator: Successfully rendered HTML template")

        # --- 3. Generate PDF using ReportLab ---
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )

        # Build PDF content
        story = []
        
        # Add title
        if 'title' in data:
            story.append(Paragraph(data['title'], title_style))
            story.append(Spacer(1, 20))
        
        # Add executive summary
        if 'executive_summary' in data:
            story.append(Paragraph("Executive Summary", heading_style))
            story.append(Paragraph(data['executive_summary'], body_style))
            story.append(Spacer(1, 20))
        
        # Add key insights
        if 'key_insights' in data and isinstance(data['key_insights'], list):
            story.append(Paragraph("Key Insights", heading_style))
            for insight in data['key_insights']:
                if isinstance(insight, dict):
                    insight_text = insight.get('insight', '')
                    explanation = insight.get('explanation', '')
                    relevance_score = insight.get('relevance_score', 'N/A')
                    
                    if insight_text:
                        story.append(Paragraph(f"<b>{insight_text}</b>", body_style))
                    if explanation:
                        story.append(Paragraph(explanation, body_style))
                    story.append(Paragraph(f"Relevance Score: {relevance_score}/10", body_style))
                    story.append(Spacer(1, 12))
        
        # Add source analysis
        if 'source_analysis' in data and isinstance(data['source_analysis'], dict):
            story.append(Paragraph("Source Analysis", heading_style))
            sentiment = data['source_analysis'].get('sentiment', 'N/A')
            confidence = data['source_analysis'].get('confidence', 'N/A')
            story.append(Paragraph(f"Overall Sentiment: {sentiment}", body_style))
            story.append(Paragraph(f"Confidence in Source: {confidence}", body_style))
            story.append(Spacer(1, 20))
        
        # Add conclusion
        if 'conclusion' in data:
            story.append(Paragraph("Conclusion", heading_style))
            story.append(Paragraph(data['conclusion'], body_style))
            story.append(Spacer(1, 20))
        
        # Add metadata if available
        if 'metadata' in data:
            story.append(Paragraph("Report Information", heading_style))
            metadata = data['metadata']
            for key, value in metadata.items():
                story.append(Paragraph(f"<b>{key}:</b> {value}", body_style))
                story.append(Spacer(1, 6))

        # Build PDF
        doc.build(story)
        print(f"PDF Generator: Successfully created PDF at {output_path}")
        return True

    except jinja2.TemplateNotFound as e:
        print(f"PDF Generator Error: Template '{template_name}' not found in '{template_dir}'. Error: {e}")
        return False
    except Exception as e:
        print(f"PDF Generator Error: An unexpected error occurred. Error type: {type(e).__name__}")
        print(f"PDF Generator Error: Error details: {e}")
        import traceback
        print(f"PDF Generator Error: Traceback: {traceback.format_exc()}")
        return False