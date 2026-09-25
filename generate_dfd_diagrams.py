import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_dfd_level0(out_path):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(6, 6.6, "DFD LEVEL 0: CONTEXT DIAGRAM", fontsize=16, fontweight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(6, 6.3, "AI-Enabled IT Infrastructure Monitoring System", fontsize=11, ha='center', va='center', color='#475569')

    # Central System Process (Circle/Ellipse)
    center_circle = patches.Ellipse((6, 3.5), 3.8, 2.2, facecolor='#1E3A8A', edgecolor='#0EA5E9', linewidth=2.5, zorder=3)
    ax.add_patch(center_circle)
    ax.text(6, 3.7, "0.0", fontsize=14, fontweight='bold', color='#0EA5E9', ha='center', va='center', zorder=4)
    ax.text(6, 3.3, "AI-ENABLED IT INFRASTRUCTURE\nMONITORING SYSTEM", fontsize=10, fontweight='bold', color='white', ha='center', va='center', zorder=4)

    # Entities (Rectangles)
    entities = [
        ("USER / ADMIN\n(Web Browser)", (0.8, 4.8), "#E0F2FE", "#0284C7"),
        ("REMOTE CLIENT AGENT\n(client_agent.py)", (0.8, 1.2), "#E0F2FE", "#0284C7"),
        ("HOST HARDWARE / OS\n(psutil Sensor)", (4.5, 5.3), "#F3E8FF", "#7E22CE"),
        ("ADMIN DASHBOARD\n(Chart.js UI)", (8.5, 4.8), "#DCFCE7", "#15803D"),
        ("SMTP MAIL GATEWAY\n(Admin Inbox)", (8.5, 1.2), "#FEE2E2", "#B91C1C"),
        ("MYSQL / SQLITE DB\n(it_monitor_db)", (4.5, 0.4), "#FEF3C7", "#D97706")
    ]

    for name, (x, y), fill, border in entities:
        rect = patches.FancyBboxPatch((x, y), 2.7, 1.1, boxstyle="round,pad=0.1", facecolor=fill, edgecolor=border, linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + 1.35, y + 0.55, name, fontsize=9, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

    # Arrows & Flow Text
    arrow_props = dict(arrowstyle="->", color="#334155", lw=1.8, mutation_scale=15)
    
    # 1. User -> Center
    ax.annotate("", xy=(4.1, 3.8), xytext=(3.5, 5.2), arrowprops=arrow_props)
    ax.text(3.3, 4.7, "Login & Queries", fontsize=8, fontweight='bold', color='#0369A1', rotation=-30)

    # 2. Center -> User
    ax.annotate("", xy=(3.5, 5.5), xytext=(4.2, 4.2), arrowprops=arrow_props)
    ax.text(4.2, 4.9, "Session State", fontsize=8, fontweight='bold', color='#0369A1', rotation=-30)

    # 3. Remote Agent -> Center
    ax.annotate("", xy=(4.1, 3.2), xytext=(3.5, 1.8), arrowprops=arrow_props)
    ax.text(3.0, 2.3, "JSON Telemetry Payload", fontsize=8, fontweight='bold', color='#0369A1', rotation=25)

    # 4. Host Hardware -> Center
    ax.annotate("", xy=(6.0, 4.6), xytext=(6.0, 5.3), arrowprops=arrow_props)
    ax.text(6.1, 4.9, "Raw System Metrics", fontsize=8, fontweight='bold', color='#6B21A8')

    # 5. Center -> Admin Dashboard
    ax.annotate("", xy=(8.5, 5.2), xytext=(7.9, 3.8), arrowprops=arrow_props)
    ax.text(8.0, 4.7, "Live Telemetry & Charts", fontsize=8, fontweight='bold', color='#15803D', rotation=25)

    # 6. Center -> SMTP Mail
    ax.annotate("", xy=(8.5, 1.8), xytext=(7.9, 3.2), arrowprops=arrow_props)
    ax.text(8.0, 2.3, "Breach Email Alerts", fontsize=8, fontweight='bold', color='#B91C1C', rotation=-25)

    # 7. Center <-> DB
    ax.annotate("", xy=(6.0, 1.5), xytext=(6.0, 2.4), arrowprops=arrow_props)
    ax.text(6.1, 2.0, "Time-Series SQL Logs", fontsize=8, fontweight='bold', color='#B45309')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved DFD Level 0 to {out_path}")

def draw_dfd_level1(out_path):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(6, 6.6, "DFD LEVEL 1: MACRO PROCESS FLOW", fontsize=16, fontweight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(6, 6.3, "Decomposition of Major System Functions and Data Stores", fontsize=11, ha='center', va='center', color='#475569')

    processes = [
        ("1.0\nUser Authentication", (0.5, 3.8), "#1E3A8A"),
        ("2.0\nMetric Collection", (2.8, 3.8), "#1E3A8A"),
        ("3.0\nThreshold Auditing", (5.1, 3.8), "#1E3A8A"),
        ("4.0\nAI Diagnostics", (7.4, 3.8), "#1E3A8A"),
        ("5.0\nVisualization & Export", (9.7, 3.8), "#1E3A8A")
    ]

    for name, (x, y), fill in processes:
        rect = patches.FancyBboxPatch((x, y), 1.8, 1.6, boxstyle="round,pad=0.1", facecolor=fill, edgecolor='#0EA5E9', linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + 0.9, y + 0.8, name, fontsize=9, fontweight='bold', ha='center', va='center', color='white', zorder=4)

    stores = [
        ("D1: users", (0.5, 1.2), "#FEF3C7"),
        ("D2: monitoring_history", (2.8, 1.2), "#FEF3C7"),
        ("D3: settings\nD4: alerts", (5.1, 1.2), "#FEF3C7"),
        ("Rule Evaluation\nMatrix", (7.4, 1.2), "#F3E8FF"),
        ("Chart.js & PDF/Excel\nReports", (9.7, 1.2), "#DCFCE7")
    ]

    arrow_props = dict(arrowstyle="->", color="#0284C7", lw=1.8, mutation_scale=15)

    for name, (x, y), fill in stores:
        rect = patches.Rectangle((x, y), 1.8, 1.2, facecolor=fill, edgecolor='#D97706', linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x + 0.9, y + 0.6, name, fontsize=8, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)

        # Connect process to data store
        ax.annotate("", xy=(x + 0.9, y + 1.2), xytext=(x + 0.9, y + 2.6), arrowprops=arrow_props)

    # Horizontal Flow Arrows between processes
    for i in range(4):
        ax.annotate("", xy=(processes[i+1][1][0], 4.6), xytext=(processes[i][1][0] + 1.8, 4.6), arrowprops=arrow_props)

    # External Inputs/Outputs
    ax.text(0.2, 5.8, "[User Login Credentials]", fontsize=8, fontweight='bold', color='#0369A1')
    ax.annotate("", xy=(1.4, 5.4), xytext=(0.8, 5.7), arrowprops=arrow_props)

    ax.text(2.5, 5.8, "[Raw Telemetry / JSON]", fontsize=8, fontweight='bold', color='#0369A1')
    ax.annotate("", xy=(3.7, 5.4), xytext=(3.1, 5.7), arrowprops=arrow_props)

    ax.text(6.0, 5.8, "[SMTP Email Gateway]", fontsize=8, fontweight='bold', color='#B91C1C')
    ax.annotate("", xy=(6.0, 5.7), xytext=(6.0, 5.4), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved DFD Level 1 to {out_path}")

def draw_dfd_level2(out_path):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(6, 6.6, "DFD LEVEL 2: DETAILED SUB-PROCESS FLOW", fontsize=16, fontweight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(6, 6.3, "Sub-Processes for Threshold Auditing (3.0) and AI Diagnostic Engine (4.0)", fontsize=11, ha='center', va='center', color='#475569')

    # Section 1: Process 3.0 Breakdown
    rect_3 = patches.FancyBboxPatch((0.5, 0.5), 5.3, 5.5, boxstyle="round,pad=0.1", facecolor='#F8FAFC', edgecolor='#0284C7', linewidth=2)
    ax.add_patch(rect_3)
    ax.text(3.15, 5.7, "SUB-PROCESS 3.0: THRESHOLD AUDITING & ALERTING", fontsize=10, fontweight='bold', color='#0369A1', ha='center')

    steps_3 = [
        "3.1 Read Thresholds (D3: settings)",
        "3.2 Compare Telemetry vs Limits",
        "3.3 Record ACTIVE Alert (D4: alerts)",
        "3.4 Trigger Async SMTP Breach Email"
    ]

    arrow_props = dict(arrowstyle="->", color="#0284C7", lw=1.5, mutation_scale=12)

    for i, step in enumerate(steps_3):
        y = 4.7 - (i * 1.1)
        sb = patches.FancyBboxPatch((1.0, y), 4.3, 0.7, boxstyle="round,pad=0.05", facecolor='#1E3A8A', edgecolor='#0EA5E9')
        ax.add_patch(sb)
        ax.text(3.15, y + 0.35, step, fontsize=9, fontweight='bold', color='white', ha='center', va='center')
        if i < 3:
            ax.annotate("", xy=(3.15, y - 0.4), xytext=(3.15, y), arrowprops=arrow_props)

    # Section 2: Process 4.0 Breakdown
    rect_4 = patches.FancyBboxPatch((6.2, 0.5), 5.3, 5.5, boxstyle="round,pad=0.1", facecolor='#F8FAFC', edgecolor='#7E22CE', linewidth=2)
    ax.add_patch(rect_4)
    ax.text(8.85, 5.7, "SUB-PROCESS 4.0: AI RECOMMENDATION ENGINE", fontsize=10, fontweight='bold', color='#7E22CE', ha='center')

    steps_4 = [
        "4.1 Multi-Variable Telemetry Audit",
        "4.2 Identify Diagnostic Causes",
        "4.3 Formulate Actionable Remediation",
        "4.4 Render AI Banners & Chat Payload"
    ]

    for i, step in enumerate(steps_4):
        y = 4.7 - (i * 1.1)
        sb = patches.FancyBboxPatch((6.7, y), 4.3, 0.7, boxstyle="round,pad=0.05", facecolor='#581C87', edgecolor='#C084FC')
        ax.add_patch(sb)
        ax.text(8.85, y + 0.35, step, fontsize=9, fontweight='bold', color='white', ha='center', va='center')
        if i < 3:
            arrow_purple = dict(arrowstyle="->", color="#A855F7", lw=1.5, mutation_scale=12)
            ax.annotate("", xy=(8.85, y - 0.4), xytext=(8.85, y), arrowprops=arrow_purple)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved DFD Level 2 to {out_path}")

if __name__ == '__main__':
    img_dir = r"e:\Mini project 2\dfd_images"
    os.makedirs(img_dir, exist_ok=True)
    draw_dfd_level0(os.path.join(img_dir, "dfd_level0.png"))
    draw_dfd_level1(os.path.join(img_dir, "dfd_level1.png"))
    draw_dfd_level2(os.path.join(img_dir, "dfd_level2.png"))
