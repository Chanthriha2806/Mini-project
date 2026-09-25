import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def make_pdf(filepath):
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Styles setup
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1e3a8a'), # Premium Indigo
        spaceAfter=15
    )
    h2_style = ParagraphStyle(
        'SecHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#0f766e'), # Premium Teal
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor('#1f2937'),
        leading=14,
        spaceAfter=8
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        textColor=colors.HexColor('#b91c1c'),
        backColor=colors.HexColor('#f3f4f6'),
        borderPadding=8,
        spaceAfter=8
    )

    # Document Flowables
    story.append(Paragraph("MonitorAI Setup & User Guide", title_style))
    story.append(Paragraph("This manual provides step-by-step instructions to register a user account, download client files, run the telemetry agent on any laptop, and view real-time performance on the admin dashboard.", body_style))
    story.append(Spacer(1, 10))

    # Steps Table / Section
    story.append(Paragraph("Step-by-Step Setup Instructions", h2_style))
    
    steps = [
        "<b>1. Open the Website:</b><br/>Visit the live dashboard URL: <font color='#1e3a8a'><b>https://mini-project-phi-green.vercel.app/</b></font>",
        
        "<b>2. Register a New Account:</b><br/>Go to <font color='#1e3a8a'><b>https://mini-project-phi-green.vercel.app/auth/register</b></font> and create a new user account (e.g. Username: <b>Aishwarya</b> / Password: <b>Aishu@123</b>).",
        
        "<b>3. Download the Required Files:</b><br/>After logging in, download the following three files from the dashboard header links:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>1. Agent Script</b> (<code>client_agent.py</code>)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>2. Requirements</b> (<code>requirements.txt</code>)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>3. One-Click Launcher</b> (<code>run_client.bat</code>)",
        
        "<b>4. Create a Folder:</b><br/>Create a new folder on your computer named <b>MonitorAI</b> and move all three downloaded files into this folder.",
        
        "<b>5. Run the Client Telemetry Agent:</b><br/>Open the <b>MonitorAI</b> folder and double-click <b>run_client.bat</b>. When the Command Prompt window appears, enter the following details when prompted:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Server URL:</b> <code>https://mini-project-phi-green.vercel.app</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Username:</b> <code>Aishwarya</code> <i>(or your registered username)</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Password:</b> <code>Aishu@123</code> <i>(or your registered password)</i>",
        
        "<b>6. Register a Test Account (Optional):</b><br/>Open <code>https://mini-project-phi-green.vercel.app/auth/register</code> to register additional test user accounts.",
        
        "<b>7. View Connected Client Performance (Admin Dashboard):</b><br/>Open your web browser and go to <b>https://mini-project-phi-green.vercel.app/</b>.<br/>Log in using the administrator credentials:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Admin Username:</b> <code>admin</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Admin Password:</b> <code>admin123</code><br/>"
        "Select your connected laptop from the <b>Select Remote Machine</b> dropdown menu to monitor live CPU, Memory, Disk, and Network telemetry."
    ]
    for s in steps:
        story.append(Paragraph(f"• {s}", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print("[+] PDF setup manual generated successfully!")

if __name__ == '__main__':
    make_pdf("Setup_Instructions.pdf")
