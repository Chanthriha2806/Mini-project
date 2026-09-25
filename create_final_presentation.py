import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Aspect Ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    DARK_BG = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)# Slate 400
    ACCENT_BLUE = RGBColor(59, 130, 246) # Blue 500
    ACCENT_CYAN = RGBColor(14, 165, 233) # Cyan 500
    ACCENT_GREEN = RGBColor(34, 197, 94) # Green 500
    ACCENT_RED = RGBColor(239, 68, 68)   # Red 500

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="MINI PROJECT REVIEW II"):
        # Header Banner Card
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.0))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide1)

    # Title Card Accent Box
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = ACCENT_BLUE
    card1.line.width = Pt(2)

    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.3), Inches(10.333), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "KGiSL INSTITUTE OF INFORMATION MANAGEMENT"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "DEPARTMENT OF COMPUTER SCIENCE | ODD SEMESTER 2026 - 2027"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "\nAI-ENABLED IT INFRASTRUCTURE MONITORING DASHBOARD"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "MINI PROJECT REVIEW II PRESENTATION\n"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.alignment = PP_ALIGN.CENTER

    # Student Details Grid
    p = tf.add_paragraph()
    p.text = "Submitted by: CHANTHRIHA J   |   Register No: 2538M0070"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "Under the Guidance of: Mrs. R. GOMATHI (Designation)"
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: OBJECTIVES & KEY FEATURES
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide2)
    add_header(slide2, "Project Objectives & Core Capabilities")

    features = [
        ("Centralized Real-Time Telemetry", "Live tracking of CPU core usage, physical RAM, Disk volume, and Network upload/download speeds using psutil & socket API."),
        ("Rule-Based AI Recommendation Engine", "Zero-latency expert decision matrix analyzing multi-metric states to generate instant diagnostic root causes and corrective steps."),
        ("Automated Threshold Alerting", "Monitors live hardware metrics against user settings; logs ACTIVE database alerts and dispatches async SMTP email warnings."),
        ("Remote Client Agent Network Monitoring", "Lightweight client_agent.py script streams JSON telemetry payloads over REST API from remote server nodes."),
        ("Process Control & Audit Reports", "Admin PID process inspection and safe termination; single-click export of compliance reports in PDF (ReportLab) and Excel (openpyxl).")
    ]

    top_pos = 1.6
    for title, desc in features:
        box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_BLUE
        
        tb = slide2.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.333), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"• {title}"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(12)
        p1.font.color.rgb = TEXT_MUTED
        
        top_pos += 1.08

    # ==========================================
    # SLIDE 3: COMPONENT 1 - MODULE DESCRIPTION
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide3)
    add_header(slide3, "Component 1: Module Description")

    modules = [
        ("1. User Authentication Module", "auth_controller.py & auth_routes.py", "Manages user registration, login authentication using PBKDF2-SHA256 password hashing, Flask-Login session management, and admin vs client role separation."),
        ("2. Telemetry Acquisition Module", "system_monitor.py & client_agent.py", "Extracts local host hardware metrics (CPU %, RAM, Disk, Net KB/s) via psutil, or ingests remote client JSON telemetry payloads via HTTP POST /api/metrics/report."),
        ("3. Threshold Audit & Alert Module", "dashboard_controller.py & mail_helper.py", "Audits live metrics against user-configured limits stored in database settings; logs ACTIVE alert records and triggers async SMTP email notifications on breach."),
        ("4. AI Recommendation Module", "ai_engine.py (RecommendationEngine)", "Rule-based expert diagnostic engine that analyzes combined metric bottlenecks (e.g. CPU saturation, memory leaks) to output structured causes and corrective actions."),
        ("5. Reporting & Process Control Module", "reports_controller.py & report_generator.py", "Enables safe PID process termination for administrators, and compiles historical time-series statistics into formatted PDF (ReportLab) and Excel (openpyxl) audit sheets.")
    ]

    top_pos = 1.5
    for m_name, m_file, m_desc in modules:
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(1.0))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_BLUE
        
        tb = slide3.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.333), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"{m_name}   [{m_file}]"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = m_desc
        p1.font.size = Pt(12)
        p1.font.color.rgb = TEXT_MUTED
        
        top_pos += 1.1

    # ==========================================
    # SLIDE 4: COMPONENT 2 - DFD LEVEL 0 (CONTEXT)
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide4)
    add_header(slide4, "Component 2: Data Flow Diagram (DFD Level 0 - Context Diagram)")

    # DFD Level 0 Visual Representation Card
    box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = ACCENT_BLUE

    tb = slide4.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LEVEL 0 CONTEXT DIAGRAM ARCHITECTURE"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    dfd0_text = """
  +-----------------------+   Login / Credentials    +----------------------------------+   Telemetry & Charts   +-----------------------+
  |    USER / ADMIN       |------------------------->|                                  |----------------------->|     ADMIN DASHBOARD   |
  |  (Web Browser User)   |<-------------------------|                                  |                        |  (Chart.js UI Views)  |
  +-----------------------+     Session State        |                                  |                        +-----------------------+
                                                     |   0.0 AI-ENABLED IT MONITORING   |
  +-----------------------+   JSON Telemetry Payload |              SYSTEM              |   Breach Email Alert   +-----------------------+
  |  REMOTE CLIENT AGENT  |------------------------->|   (Flask Central Server App)     |----------------------->|   SMTP MAIL GATEWAY   |
  |  (client_agent.py)    |                          |                                  |                        |   (Admin Inbox)       |
  +-----------------------+                          +----------------------------------+                        +-----------------------+
                                                               |              ^
  +-----------------------+   Raw Hardware Metrics             |              | SQL Queries / Time-series Logs
  |   HOST HARDWARE / OS  |------------------------------------+              v
  |   (psutil Sensor)     |                                      +----------------------------------+
  +-----------------------+                                      |      MYSQL / SQLITE DATABASE     |
                                                                 |         (it_monitor_db)          |
                                                                 +----------------------------------+
    """
    p2 = tf.add_paragraph()
    p2.text = dfd0_text
    p2.font.size = Pt(11)
    p2.font.name = "Courier New"
    p2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 5: COMPONENT 2 - DFD LEVEL 1 (MACRO FLOW)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide5)
    add_header(slide5, "Component 2: Data Flow Diagram (DFD Level 1 - Macro Flow)")

    box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = ACCENT_BLUE

    tb = slide5.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LEVEL 1 MACRO PROCESS DECOMPOSITION"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    dfd1_text = """
  [User / Admin] ---> ( 1.0 User Authentication ) =====> [ D1: users ]
                              |
                              v
  [Client Agent] ---> ( 2.0 Telemetry Ingestion ) =====> [ D2: monitoring_history ]
                              |
                              v
                      ( 3.0 Threshold Auditing  ) =====> [ D3: settings ] & [ D4: alerts ] ---> [ SMTP Mail ]
                              |
                              v
                      ( 4.0 AI Diagnostics Engine) ---> ( 5.0 UI Visualization & Process Kill )
                              |                                      |
                              v                                      v
                      [ Diagnostic Recommendations ]          [ Chart.js & Reports Export ]
    """
    p2 = tf.add_paragraph()
    p2.text = dfd1_text
    p2.font.size = Pt(12)
    p2.font.name = "Courier New"
    p2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 6: COMPONENT 2 - DFD LEVEL 2 (DETAILED ALERTS & AI)
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide6)
    add_header(slide6, "Component 2: Data Flow Diagram (DFD Level 2 - Sub-Processes)")

    box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = ACCENT_BLUE

    tb = slide6.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LEVEL 2 SUB-PROCESS FLOW: THRESHOLD ALERTING & AI DIAGNOSTICS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    dfd2_text = """
  --- SUB-PROCESS 3.0: THRESHOLD AUDITING & ALERTING ---
  [Live Telemetry] ---> ( 3.1 Fetch Threshold Limits D3: settings )
                             |
                             v
                        ( 3.2 Compare CPU/RAM/Disk Values )
                             |---> [ Normal ]  --> Update Healthy Status
                             |---> [ Exceeded ]--> ( 3.3 Create ACTIVE Alert D4: alerts )
                                                         |
                                                         v
                                                   ( 3.4 Dispatch Email via MailHelper )

  --- SUB-PROCESS 4.0: AI RECOMMENDATION ENGINE ---
  [Metrics Context] ---> ( 4.1 Evaluate Rules Matrix: CPU > 90%, RAM > 90%, Disk > 95%, Net > 10MB/s )
                             |
                             v
                        ( 4.2 Formulate Diagnostic Causes & Corrective Actions )
                             |
                             v
                        [ Render AI Troubleshooting Banners & Chat Responses ]
    """
    p2 = tf.add_paragraph()
    p2.text = dfd2_text
    p2.font.size = Pt(11)
    p2.font.name = "Courier New"
    p2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 7: COMPONENT 3 - TABLE DESIGN (DATABASE SCHEMA)
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide7)
    add_header(slide7, "Component 3: Table Design (Relational Schema)")

    tables = [
        ("users", "id (INT, PK, AI) | username (VARCHAR 50, UNQ) | email (VARCHAR 120, UNQ) | password_hash (VARCHAR 255) | is_admin (BOOL)"),
        ("settings", "id (INT, PK, AI) | user_id (INT, FK -> users.id) | cpu_threshold (FLOAT, 90.0) | ram_threshold (FLOAT, 90.0) | disk_threshold (FLOAT, 95.0) | email_address (VARCHAR 120)"),
        ("monitoring_history", "id (INT, PK, AI) | user_id (INT, FK) | hostname (VARCHAR 100) | cpu_usage (FLOAT) | ram_usage (FLOAT) | disk_usage (FLOAT) | upload_speed (FLOAT) | download_speed (FLOAT) | created_at (TIMESTAMP)"),
        ("alerts", "id (INT, PK, AI) | metric_type (VARCHAR 20) | message (VARCHAR 255) | value (FLOAT) | threshold (FLOAT) | status (VARCHAR 20: 'ACTIVE'/'RESOLVED') | created_at (TIMESTAMP)"),
        ("reports", "id (INT, PK, AI) | report_type (VARCHAR 20: 'DAILY'/'WEEKLY'/'MONTHLY') | file_path (VARCHAR 255) | created_at (TIMESTAMP)")
    ]

    top_pos = 1.5
    for t_name, t_fields in tables:
        box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_BLUE
        
        tb = slide7.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.333), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"TABLE: `{t_name}`"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = t_fields
        p1.font.size = Pt(11)
        p1.font.name = "Courier New"
        p1.font.color.rgb = TEXT_LIGHT
        
        top_pos += 1.08

    # ==========================================
    # SLIDE 8: COMPONENT 4 - INPUT DESIGN
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide8)
    add_header(slide8, "Component 4: Input Design (Forms & Control Interfaces)")

    inputs = [
        ("User Authentication Input (`auth/login.html`)", "Fields: Username/Email (Text), Password (Password field).\nValidation: Client-side required fields, server-side PBKDF2 hash verification."),
        ("Threshold & Notification Settings (`settings.html`)", "Fields: CPU Threshold (%, Slider 1-100), RAM Threshold (%), Disk Threshold (%), Refresh Rate (Seconds), Alert Email Address.\nValidation: Range validation [1.0 - 100.0], valid email regex format."),
        ("Remote Client Agent JSON Payload (`POST /api/metrics/report`)", "Schema: JSON payload containing cpu (usage, cores, freq), memory (total, used, percent), disk (total, used, percent), network (upload_speed, download_speed), and system (hostname).\nValidation: JSON content-type verification, numeric float type enforcement."),
        ("AI Diagnostic Assistant Chat Query (`dashboard.html`)", "Fields: User Question String input box.\nValidation: Text sanitization, non-empty query check."),
        ("Process Termination Request (`POST /api/process/kill`)", "Fields: Process ID (PID - Integer).\nValidation: Admin role verification, system PID protection check.")
    ]

    top_pos = 1.5
    for i_title, i_desc in inputs:
        box = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_BLUE
        
        tb = slide8.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.08), Inches(11.333), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"• {i_title}"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = i_desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_MUTED
        
        top_pos += 1.08

    # ==========================================
    # SLIDE 9: COMPONENT 5 - OUTPUT DESIGN
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide9)
    add_header(slide9, "Component 5: Output Design (Dashboards, Alerts & Reports)")

    outputs = [
        ("Real-Time Metric Status Cards & Gauges", "Renders percentage badges and dynamic progress rings for CPU, RAM, Disk, and Network speeds in real time (refreshed every 5s)."),
        ("Interactive Multi-Line Chart.js Graphs", "Renders time-series line charts tracking CPU %, RAM %, and Disk % trends over time with dynamic live push updates."),
        ("Active Alert Notification Feed", "Color-coded warning/danger alert banners displayed instantly when threshold limits are breached."),
        ("AI Diagnostic Recommendation Banners & Chat Modal", "Displays structured diagnostic causes (e.g., memory leak, runaway thread) and step-by-step resolution advice."),
        ("Top Processes Table & Admin Controls", "Displays top 10 CPU/RAM consuming tasks with process names, PIDs, and single-click 'Kill Process' action buttons."),
        ("Exported PDF & Excel Infrastructure Audit Reports", "Generates downloadable PDF diagnostic summaries (ReportLab) and Excel spreadsheets (openpyxl) over customizable date ranges.")
    ]

    top_pos = 1.5
    for o_title, o_desc in outputs:
        box = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.85))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_BLUE
        
        tb = slide9.shapes.add_textbox(Inches(1.0), Inches(top_pos + 0.06), Inches(11.333), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"• {o_title}"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        p1 = tf.add_paragraph()
        p1.text = o_desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_MUTED
        
        top_pos += 0.92

    # ==========================================
    # SLIDE 10: CONCLUSION & SUMMARY
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_background(slide10)
    add_header(slide10, "Conclusion & Future Enhancements")

    box = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.3))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = ACCENT_BLUE

    tb = slide10.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.133), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "PROJECT REVIEW II SUMMARY"
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN

    summary_bullets = [
        "Fully Implemented Components: Successfully presented Module Description, DFD (Level 0, 1, 2), Table Design, Input Design, and Output Design.",
        "Production-Ready Infrastructure Monitoring: Centralized platform for monitoring local and remote server metrics in real time.",
        "Zero-Latency Rule-Based AI Engine: Provides automated troubleshooting root causes and remediation steps.",
        "Proactive Alerting & Auditing: Instant SMTP email notifications on threshold breach and single-click PDF/Excel audit report exports.",
        "Future Roadmap: Integrating Machine Learning (LSTM models) for predictive failure forecasting and mobile app push notifications."
    ]

    for bullet in summary_bullets:
        p = tf.add_paragraph()
        p.text = f"\n✔ {bullet}"
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_LIGHT

    # Save to file
    out_path = r"e:\Mini_Project_Review_2_AI_IT_Infra_Dashboard_Final.pptx"
    prs.save(out_path)
    print(f"Successfully generated PowerPoint presentation at: {out_path}")

    # Overwrite the original file too so the user gets it in their existing PPTX
    orig_path = r"e:\Mini_Project_Review_2_AI_IT_Infra_Dashboard.pptx"
    prs.save(orig_path)
    print(f"Successfully updated original PowerPoint presentation at: {orig_path}")

if __name__ == '__main__':
    create_presentation()
