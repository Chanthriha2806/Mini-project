class RecommendationEngine:
    """Rule-based engine generating troubleshooting causes and corrective actions for system bottlenecks."""

    @staticmethod
    def generate_recommendations(cpu, ram, disk, upload_speed, download_speed, health_status):
        """Audits live telemetry against engineering rules to formulate diagnostic recommendations."""
        recommendations = []

        # 1. CPU Rules
        if cpu > 90.0:
            recommendations.append({
                'title': 'Critical CPU Core Saturation',
                'metric': 'CPU',
                'value': f"{cpu}%",
                'level': 'danger',
                'causes': [
                    'Too many foreground applications running simultaneously.',
                    'A runaway thread or memory-leak loop locking the processor.',
                    'Active operating system update installation or background file indexing.',
                    'Malicious script or unauthorized cryptocurrency mining activity.'
                ],
                'actions': [
                    'Check the processes list below and kill high CPU-consuming processes.',
                    'Gracefully restart the host server to flush runaway threads.',
                    'Initiate a full system virus and malware scan.',
                    'Schedule hardware upgrade to more processor cores if loads are recurring.'
                ]
            })
        elif cpu > 75.0:
            recommendations.append({
                'title': 'High CPU Utilization Warning',
                'metric': 'CPU',
                'value': f"{cpu}%",
                'level': 'warning',
                'causes': [
                    'Multiple browser tabs or development environments open.',
                    'Non-critical background service updates.'
                ],
                'actions': [
                    'Close unused browser tabs and application windows.',
                    'Postpone heavy system builds or compiler scripts to off-peak hours.'
                ]
            })

        # 2. Memory (RAM) Rules
        if ram > 90.0:
            recommendations.append({
                'title': 'Critical Physical RAM Depletion',
                'metric': 'RAM',
                'value': f"{ram}%",
                'level': 'danger',
                'causes': [
                    'Active execution of heavy applications, IDEs, or virtual machines.',
                    'Severe memory leaks in long-running daemon processes.',
                    'Inflated database buffer cache allocations.'
                ],
                'actions': [
                    'End memory-hogging processes and container stacks.',
                    'Restart memory-leaking background applications.',
                    'Flush standby lists and disk caches using cleanup tools.',
                    'Install additional physical RAM modules immediately.'
                ]
            })
        elif ram > 75.0:
            recommendations.append({
                'title': 'High Memory Allocation Warning',
                'metric': 'RAM',
                'value': f"{ram}%",
                'level': 'warning',
                'causes': [
                    'High quantity of active background services running.',
                    'Over-allocated browser tab processes.'
                ],
                'actions': [
                    'Examine active memory footprints in detailed stats.',
                    'Disable unnecessary startup services and applications.'
                ]
            })

        # 3. Disk Rules
        if disk > 95.0:
            recommendations.append({
                'title': 'Critical Storage Space Depletion',
                'metric': 'DISK',
                'value': f"{disk}%",
                'level': 'danger',
                'causes': [
                    'Accumulation of raw diagnostic temporary log files.',
                    'Unemptied local Recycle Bin or Trash directories.',
                    'Large application crash dumps or core files.',
                    'Lack of secondary storage volumes for heavy media file dumps.'
                ],
                'actions': [
                    'Trigger a system-wide Disk Cleanup to purge temp files and update caches.',
                    'Purge old Docker containers, dangling images, and system volumes.',
                    'Empty the operating system recycle bin completely.',
                    'Transfer archive logs or bulky directories to secondary network storage.'
                ]
            })
        elif disk > 80.0:
            recommendations.append({
                'title': 'Low Disk Storage warning',
                'metric': 'DISK',
                'value': f"{disk}%",
                'level': 'warning',
                'causes': [
                    'Normal workspace accumulation over time.',
                    'Bulky package caches (npm, pip, maven) in user folders.'
                ],
                'actions': [
                    'Audit directory trees using size analyzer utilities.',
                    'Clean standard packet installer cache folders.'
                ]
            })

        # 4. Network Bandwidth Rules
        # Upload > 10MB/s (10240 KB/s) or Download > 20MB/s (20480 KB/s)
        if upload_speed > 10240.0:
            recommendations.append({
                'title': 'High Upload Network Throughput',
                'metric': 'NETWORK',
                'value': f"{round(upload_speed / 1024.0, 1)} MB/s",
                'level': 'info',
                'causes': [
                    'Active background file synchronization (OneDrive, GDrive, Dropbox).',
                    'Active file seeding, peer-to-peer uploads, or high volume file copies.',
                    'Potential local data exfiltration breach.'
                ],
                'actions': [
                    'Pause active cloud folders replication operations.',
                    'Check netstat socket listings to check active upload targets.',
                    'Ensure local firewalls rules block unsolicited outbound transfers.'
                ]
            })
        if download_speed > 20480.0:
            recommendations.append({
                'title': 'High Download Network Throughput',
                'metric': 'NETWORK',
                'value': f"{round(download_speed / 1024.0, 1)} MB/s",
                'level': 'info',
                'causes': [
                    'Active download of heavy installers or system update files.',
                    'Active media streams or high volume database replications.'
                ],
                'actions': [
                    'Confirm download is authorized and from a secure source.',
                    'Limit network bandwidth rates during active production hours.'
                ]
            })

        # 5. Overall System Health Rule
        if health_status in ['WARNING', 'CRITICAL']:
            recommendations.append({
                'title': 'Compromised Node Server Health',
                'metric': 'SYSTEM',
                'value': health_status,
                'level': 'danger' if health_status == 'CRITICAL' else 'warning',
                'causes': [
                    'One or more hardware threshold rules have been violated.',
                    'Local system state matches warning/critical alarms triggers.'
                ],
                'actions': [
                    'Investigate active violations in the Alerts Feed Panel.',
                    'Review detailed hardware parameters on the Specs page.',
                    'Ensure target system cooling fans are clean and operational.'
                ]
            })
        elif not recommendations:
            # Seed a default healthy recommendation if everything is normal
            recommendations.append({
                'title': 'All Systems Operational',
                'metric': 'SYSTEM',
                'value': 'HEALTHY',
                'level': 'success',
                'causes': [
                    'Resource consumption is well below configured thresholds.'
                ],
                'actions': [
                    'No troubleshooting action required. Maintain regular audits.'
                ]
            })

        return recommendations
