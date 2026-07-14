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
    story.append(Paragraph("MonitorAI: Multi-Device Infrastructure Setup Guide", title_style))
    story.append(Paragraph("This PDF manual outlines the folder structures and instructions required to test and monitor standard client laptops using the MonitorAI platform.", body_style))
    story.append(Spacer(1, 5))

    # Server-Side Setup Section
    story.append(Paragraph("1. Server-Side Directory Structure (Host Dashboard)", h2_style))
    story.append(Paragraph("The server hosts the primary Flask dashboard database, PDF/Excel reports repository, alerts logger, and the dynamic interactive AI Diagnostics assistant.", body_style))
    
    server_structure = """Server_Project/ (Main Project Root)
├── run.py                 # Launches Flask server & triggers browser
├── initialize_database.py # Prepares and seeds the local SQLite database
├── config.py              # Main configurations & thresholds definition
├── requirements.txt       # Dependencies manifest (Flask, SQLAlchemy, PyMySQL)
├── it_monitor_db.db       # SQLite local database binary file
├── client_agent.py        # Client reporting agent executable script
├── app/                   # Primary MVC package folder
│   ├── models/            # Database schema models (User, Alert, Report)
│   ├── controllers/       # Dashboard, metrics, auth, and reports controllers
│   ├── routes/            # Blueprint routes declarations
│   ├── templates/         # UI layout templates (dashboard, detailed specs)
│   ├── static/            # Stylesheets (style.css), JS scripts, images
│   └── utilities/         # AI recommendations, system specs, mail helper
└── tests/                 # Unittest diagnostics packages"""
    
    story.append(Paragraph(server_structure.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # Client-Side Setup Section
    story.append(Paragraph("2. Client-Side Directory Structure (Other Laptops)", h2_style))
    story.append(Paragraph("To gather telemetry data from other client laptops, copy only the following directory structure to a folder on the other machine:", body_style))
    
    client_structure = """Client_Telemetry/
├── client_agent.py        # Gathers system metrics and posts them to server
└── requirements.txt       # Minimised client dependencies listing (psutil, requests)"""
    
    story.append(Paragraph(client_structure.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 5))

    # Connecting Clients Section
    story.append(Paragraph("3. Step-by-Step Connection Instructions", h2_style))
    
    steps = [
        "<b>Step A: Identify Server Network Address</b><br/>Start the web dashboard on the host computer. Observe the console startup log to get the LAN IP address (e.g. <i>http://192.168.1.6:5000</i>).",
        "<b>Step B: Copy & Setup Agent</b><br/>Copy the client folder to the target laptop, open a terminal (PowerShell or Command Prompt) in that folder, and install dependencies:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<font color='#b91c1c'>pip install requests psutil</font>",
        "<b>Step C: Run Telemetry Reporting Agent</b><br/>Start the client agent pointing to the server's IP address:<br/>&nbsp;&nbsp;&nbsp;&nbsp;<font color='#b91c1c'>py client_agent.py http://&lt;your-server-ip&gt;:5000</font>",
        "<b>Step D: Authenticate with Dashboard Credentials</b><br/>Input the standard user credentials (Default: Username: <b>client</b> / Password: <b>client123</b>, or register a new user on the dashboard). The agent will print successful authentication and begin polling.",
        "<b>Step E: View Live Diagnostics</b><br/>Log in to the web dashboard on the host machine as <b>admin</b> / <b>admin123</b>. Use the <b>\"Select Remote Machine to Monitor\"</b> dropdown menu at the top of the page to toggle display specs to the remote laptop."
    ]
    for s in steps:
        story.append(Paragraph(f"• {s}", body_style))
        story.append(Spacer(1, 2))

    doc.build(story)
    print("[+] PDF setup manual generated successfully!")

if __name__ == '__main__':
    make_pdf("Setup_Instructions.pdf")
