from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os

def create_sample_pdf():
    """Create a sample PDF newsletter for demonstration"""
    
    # Create the newsletters directory if it doesn't exist
    os.makedirs('newsletters', exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate("newsletters/sample-newsletter.pdf", pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#6366f1'),
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        textColor=HexColor('#8b5cf6'),
        alignment=1
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=18
    )
    
    # Add content
    story.append(Paragraph("Byte-Sized Brilliance", title_style))
    story.append(Paragraph("Your Monthly Tech Navigator", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("July 2025 – Getting Started – Your Digital Foundation", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("""
    Welcome to the inaugural edition of Byte-Sized Brilliance! In this month's newsletter, 
    we'll explore the foundational concepts that every tech enthusiast should know to build 
    a solid digital foundation.
    """, body_style))
    
    story.append(Paragraph("What's Inside:", styles['Heading3']))
    story.append(Paragraph("• Understanding the Basics of Web Development", body_style))
    story.append(Paragraph("• Introduction to Programming Concepts", body_style))
    story.append(Paragraph("• Essential Tools for Developers", body_style))
    story.append(Paragraph("• Career Paths in Technology", body_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Web Development Fundamentals", styles['Heading3']))
    story.append(Paragraph("""
    Web development is the art and science of creating websites and web applications. 
    It encompasses everything from simple static pages to complex web applications 
    that power modern businesses.
    """, body_style))
    
    story.append(Paragraph("""
    The three core technologies of web development are HTML (structure), CSS (styling), 
    and JavaScript (interactivity). Mastering these fundamentals opens the door to 
    endless possibilities in the digital world.
    """, body_style))
    
    story.append(PageBreak())
    
    story.append(Paragraph("Programming Concepts", styles['Heading2']))
    story.append(Paragraph("""
    Programming is the process of creating instructions for computers to follow. 
    Whether you're building a simple calculator or a complex artificial intelligence 
    system, the fundamental concepts remain the same.
    """, body_style))
    
    story.append(Paragraph("Key Concepts:", styles['Heading3']))
    story.append(Paragraph("• Variables and Data Types", body_style))
    story.append(Paragraph("• Control Structures (if/else, loops)", body_style))
    story.append(Paragraph("• Functions and Methods", body_style))
    story.append(Paragraph("• Object-Oriented Programming", body_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Essential Developer Tools", styles['Heading2']))
    story.append(Paragraph("""
    Every developer needs a reliable toolkit. Here are some essential tools that 
    will make your development journey smoother and more efficient.
    """, body_style))
    
    story.append(Paragraph("• Code Editor (VS Code, Sublime Text)", body_style))
    story.append(Paragraph("• Version Control (Git)", body_style))
    story.append(Paragraph("• Package Managers (npm, pip)", body_style))
    story.append(Paragraph("• Development Environment", body_style))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("Stay Connected", styles['Heading3']))
    story.append(Paragraph("""
    Follow us on social media for daily tech insights, tips, and updates. 
    Join our community of tech enthusiasts and never miss the latest developments 
    in the world of technology.
    """, body_style))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("© 2024 Byte-Sized Brilliance. All rights reserved.", 
                          ParagraphStyle('Footer', parent=styles['Normal'], 
                                        fontSize=10, textColor=HexColor('#71717a'))))
    
    # Build PDF
    doc.build(story)
    print("Sample PDF created: newsletters/sample-newsletter.pdf")

if __name__ == "__main__":
    create_sample_pdf() 