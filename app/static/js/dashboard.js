document.addEventListener('DOMContentLoaded', () => {
    // 1. Gather configuration details from DOM
    const dashboardMeta = document.getElementById('dashboard-meta');
    const refreshInterval = parseInt(dashboardMeta.getAttribute('data-refresh-interval')) * 1000 || 5000;
    
    // Remote device tracking
    let selectedUserId = '';
    let selectedHostname = '';
    
    // 2. Global instances to maintain Chart.js configurations
    let cpuChart = null;
    let ramChart = null;
    let diskChart = null;
    let netChart = null;

    // Helper to generate Chart.js line options
    function getChartOptions(yLabel, yMax = null) {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const gridColor = isDark ? '#334155' : '#e5e7eb';
        const textColor = isDark ? '#94a3b8' : '#64748b';

        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: textColor, font: { family: 'Outfit', size: 11 } }
                }
            },
            scales: {
                x: {
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { family: 'Outfit', size: 9 } }
                },
                y: {
                    min: 0,
                    max: yMax,
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { family: 'Outfit', size: 10 } },
                    title: { display: true, text: yLabel, color: textColor, font: { family: 'Outfit', size: 11 } }
                }
            }
        };
    }

    // 3. Initialize line charts with initial historical data
    async function initializeCharts() {
        try {
            // Destroy existing charts to prevent memory leaks/re-drawing bugs
            if (cpuChart) cpuChart.destroy();
            if (ramChart) ramChart.destroy();
            if (diskChart) diskChart.destroy();
            if (netChart) netChart.destroy();

            let url = '/api/charts';
            if (selectedUserId && selectedHostname) {
                url += `?user_id=${selectedUserId}&hostname=${encodeURIComponent(selectedHostname)}`;
            }
            const response = await fetch(url);
            const data = await response.json();

            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const labelColor = isDark ? '#ffffff' : '#1f2937';

            // CPU Chart
            const ctxCpu = document.getElementById('cpuHistoryChart').getContext('2d');
            cpuChart = new Chart(ctxCpu, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: data.cpu,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }]
                },
                options: getChartOptions('Percentage (%)', 100)
            });

            // RAM Chart
            const ctxRam = document.getElementById('ramHistoryChart').getContext('2d');
            ramChart = new Chart(ctxRam, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'RAM Usage (%)',
                        data: data.ram,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }]
                },
                options: getChartOptions('Percentage (%)', 100)
            });

            // Disk Chart
            const ctxDisk = document.getElementById('diskHistoryChart').getContext('2d');
            diskChart = new Chart(ctxDisk, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Disk Usage (%)',
                        data: data.disk,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }]
                },
                options: getChartOptions('Percentage (%)', 100)
            });

            // Network Chart
            const ctxNet = document.getElementById('networkHistoryChart').getContext('2d');
            netChart = new Chart(ctxNet, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Upload (KB/s)',
                            data: data.upload,
                            borderColor: '#ef4444',
                            backgroundColor: 'transparent',
                            tension: 0.3,
                            borderWidth: 2
                        },
                        {
                            label: 'Download (KB/s)',
                            data: data.download,
                            borderColor: '#06b6d4',
                            backgroundColor: 'transparent',
                            tension: 0.3,
                            borderWidth: 2
                        }
                    ]
                },
                options: getChartOptions('Speed (KB/s)')
            });

        } catch (err) {
            console.error('Failed to initialize charts: ', err);
        }
    }

    // 4. Update elements in dashboard via fetch
    async function updateDashboardMetrics() {
        const spinner = document.getElementById('metricsSpinner');
        if (spinner) spinner.classList.remove('d-none');

        try {
            let url = '/api/metrics';
            if (selectedUserId && selectedHostname) {
                url += `?user_id=${selectedUserId}&hostname=${encodeURIComponent(selectedHostname)}`;
            }
            const response = await fetch(url);
            if (!response.ok) throw new Error('API server returned error');
            const data = await response.json();

            // Check health status elements
            const badge = document.getElementById('overallHealthBadge');
            const statusBox = document.getElementById('healthStatusBox');
            const healthMsg = document.getElementById('healthMessage');
            if (badge && statusBox) {
                // Remove existing classes
                badge.className = 'badge px-3 py-2 fw-bold ';
                statusBox.className = 'metric-card ';

                if (data.health_status === 'HEALTHY') {
                    badge.classList.add('bg-success');
                    badge.innerText = 'Healthy';
                    statusBox.classList.add('border-success-subtle');
                } else if (data.health_status === 'WARNING') {
                    badge.classList.add('bg-warning', 'text-dark');
                    badge.innerText = 'Warning';
                    statusBox.classList.add('border-warning-subtle');
                } else {
                    badge.classList.add('bg-danger');
                    badge.innerText = 'Critical';
                    statusBox.classList.add('border-danger-subtle');
                }
            }

            if (healthMsg) {
                if (data.is_remote) {
                    healthMsg.innerHTML = `<span class="text-success fw-bold"><i class="fa-solid fa-circle-dot me-1 text-success"></i>Monitoring Laptop Telemetry: ${data.system.hostname}</span>`;
                } else {
                    healthMsg.innerHTML = `<span class="text-warning fw-semibold"><i class="fa-solid fa-triangle-exclamation me-1"></i>No laptop telemetry active. Showing Server Host metrics. Download <a href="/static/downloads/client_agent.py" download class="text-primary fw-bold text-decoration-underline mx-1">Agent Script</a> / <a href="/static/downloads/requirements.txt" download class="text-secondary fw-bold text-decoration-underline mx-1">Requirements</a> / <a href="/static/downloads/run_client.bat" download class="text-success fw-bold text-decoration-underline mx-1">One-Click Launcher</a> and run on your laptop.</span>`;
                }
            }

            // Update CPU Card
            document.getElementById('cpu-usage-val').innerText = `${data.cpu.usage}%`;
            document.getElementById('cpu-cores-val').innerText = `${data.cpu.cores} Cores`;
            document.getElementById('cpu-freq-val').innerText = `${data.cpu.frequency} GHz`;
            const cpuBar = document.getElementById('cpu-progress-bar');
            cpuBar.style.width = `${data.cpu.usage}%`;
            adjustProgressBarColor(cpuBar, data.cpu.usage);

            // Update Memory Card
            document.getElementById('ram-percent-val').innerText = `${data.memory.percent}%`;
            document.getElementById('ram-used-total').innerText = `${data.memory.used} GB / ${data.memory.total} GB`;
            const ramBar = document.getElementById('ram-progress-bar');
            ramBar.style.width = `${data.memory.percent}%`;
            adjustProgressBarColor(ramBar, data.memory.percent);

            // Update Disk Card
            document.getElementById('disk-percent-val').innerText = `${data.disk.percent}%`;
            document.getElementById('disk-used-total').innerText = `${data.disk.used} GB / ${data.disk.total} GB`;
            const diskBar = document.getElementById('disk-progress-bar');
            diskBar.style.width = `${data.disk.percent}%`;
            adjustProgressBarColor(diskBar, data.disk.percent);
            
            // Update prediction details
            const diskPred = document.getElementById('disk-prediction-val');
            if (diskPred && data.disk.prediction) {
                diskPred.innerText = data.disk.prediction;
                diskPred.className = 'fw-semibold text-' + (data.disk.prediction_level || 'secondary');
            }

            // Update Network speed cards
            document.getElementById('net-upload-val').innerText = `${data.network.upload_speed} KB/s`;
            document.getElementById('net-download-val').innerText = `${data.network.download_speed} KB/s`;
            document.getElementById('net-ip-val').innerText = data.network.ip;
            document.getElementById('net-mac-val').innerText = data.network.mac;

            // System uptime and accounts count
            document.getElementById('sys-uptime-val').innerText = data.system.uptime_str;
            document.getElementById('sys-os-val').innerText = data.system.os;
            document.getElementById('sys-hostname-val').innerText = data.system.hostname;
            document.getElementById('sys-boot-val').innerText = data.system.boot_time;
            document.getElementById('counts-users').innerText = data.active_counts.users;
            document.getElementById('counts-processes').innerText = data.active_counts.processes;

            // Processes table update
            const procBody = document.getElementById('processes-table-body');
            if (procBody) {
                procBody.innerHTML = '';
                const hasActions = Array.from(document.querySelectorAll('th')).some(th => th.innerText.trim() === 'Actions');
                data.processes.forEach(proc => {
                    let actionsCell = '';
                    if (hasActions) {
                        actionsCell = `
                            <td class="text-end">
                                <button class="btn btn-sm btn-outline-danger py-0 px-2 kill-process-btn" data-pid="${proc.pid}" data-name="${proc.name}" style="font-size: 0.7rem;">
                                    <i class="fa-solid fa-ban me-1"></i>Kill
                                </button>
                            </td>
                        `;
                    }
                    procBody.innerHTML += `
                        <tr>
                            <td><span class="badge bg-secondary">${proc.pid}</span></td>
                            <td class="fw-semibold text-truncate" style="max-width: 140px;" title="${proc.name}">${proc.name}</td>
                            <td>${proc.username}</td>
                            <td class="text-end fw-medium text-primary">${proc.cpu_percent}%</td>
                            <td class="text-end fw-medium text-info">${proc.memory_percent}%</td>
                            ${actionsCell}
                        </tr>
                    `;
                });

                // Attach click listeners to processes
                document.querySelectorAll('.kill-process-btn').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        const pid = btn.getAttribute('data-pid');
                        const name = btn.getAttribute('data-name');
                        if (!confirm(`Are you sure you want to terminate process ${name} (PID: ${pid})?`)) return;
                        try {
                            const res = await fetch('/api/process/kill', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ pid: parseInt(pid) })
                            });
                            const result = await res.json();
                            if (result.success) {
                                alert(result.message);
                                updateDashboardMetrics();
                            } else {
                                alert('Error: ' + result.message);
                            }
                        } catch (err) {
                            console.error('Failed to kill process:', err);
                            alert('Network error occurred.');
                        }
                    });
                });
            }
            // Update AI recommendations list
            const recContainer = document.getElementById('recommendations-container');
            const recCount = document.getElementById('recommendations-count');
            if (recContainer && recCount && data.recommendations) {
                recCount.innerText = `${data.recommendations.length} Active Insight${data.recommendations.length !== 1 ? 's' : ''}`;
                
                // Color recCount badge based on highest level
                let highestLevel = 'success';
                data.recommendations.forEach(r => {
                    if (r.level === 'danger') highestLevel = 'danger';
                    else if (r.level === 'warning' && highestLevel !== 'danger') highestLevel = 'warning';
                    else if (r.level === 'info' && highestLevel !== 'danger' && highestLevel !== 'warning') highestLevel = 'info';
                });
                recCount.className = `badge bg-${highestLevel === 'warning' ? 'warning text-dark' : highestLevel}`;

                recContainer.innerHTML = '';
                data.recommendations.forEach(rec => {
                    // Create list items for causes and actions
                    let causesHtml = '';
                    rec.causes.forEach(cause => {
                        causesHtml += `<li class="d-flex align-items-start gap-1"><i class="fa-solid fa-circle-exclamation text-secondary mt-1" style="font-size: 0.75rem;"></i><span>${cause}</span></li>`;
                    });
                    
                    let actionsHtml = '';
                    rec.actions.forEach(action => {
                        actionsHtml += `<li class="d-flex align-items-start gap-1"><i class="fa-solid fa-circle-check text-success mt-1" style="font-size: 0.75rem;"></i><span>${action}</span></li>`;
                    });

                    recContainer.innerHTML += `
                        <div class="col-lg-6 col-12">
                            <div class="card border-0 bg-secondary-subtle p-3 h-100" style="border-radius: 10px;">
                                <div class="d-flex justify-content-between align-items-start border-bottom pb-2 mb-3">
                                    <div>
                                        <span class="badge bg-${rec.level === 'warning' ? 'warning text-dark' : rec.level} mb-1 small">${rec.metric} Metric</span>
                                        <h6 class="fw-bold mb-0 text-dark-emphasis">${rec.title}</h6>
                                    </div>
                                    <span class="text-secondary small fw-bold">${rec.value}</span>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3 mb-md-0">
                                        <span class="text-secondary small fw-bold d-block mb-2 uppercase">Possible Causes:</span>
                                        <ul class="list-unstyled mb-0 text-secondary-emphasis small flex-column d-flex gap-2">
                                            ${causesHtml}
                                        </ul>
                                    </div>
                                    <div class="col-md-6">
                                        <span class="text-secondary small fw-bold d-block mb-2 uppercase">Recommended Actions:</span>
                                        <ul class="list-unstyled mb-0 text-secondary-emphasis small flex-column d-flex gap-2">
                                            ${actionsHtml}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });
            }

            // Update active line charts dynamically
            const timeStr = new Date().toLocaleTimeString();
            appendChartData(cpuChart, timeStr, data.cpu.usage);
            appendChartData(ramChart, timeStr, data.memory.percent);
            appendChartData(diskChart, timeStr, data.disk.percent);
            appendChartData(netChart, timeStr, [data.network.upload_speed, data.network.download_speed], true);

        } catch (err) {
            console.error('Failed fetching real-time metrics: ', err);
        } finally {
            if (spinner) spinner.classList.add('d-none');
        }
    }

    // Helper to color progress bars dynamically
    function adjustProgressBarColor(bar, percent) {
        bar.className = 'progress-bar ';
        if (percent > 90.0) {
            bar.classList.add('bg-danger');
        } else if (percent > 75.0) {
            bar.classList.add('bg-warning');
        } else {
            bar.classList.add('bg-success');
        }
    }

    // Helper to feed real-time coordinates to Chart.js
    function appendChartData(chart, label, value, isMulti = false) {
        if (!chart) return;
        
        // Push new label
        chart.data.labels.push(label);
        
        if (isMulti) {
            // value is array matching datasets
            chart.data.datasets.forEach((dataset, idx) => {
                dataset.data.push(value[idx]);
            });
        } else {
            chart.data.datasets[0].data.push(value);
        }

        // Shift old labels/data points if exceeding max size (20 coordinates)
        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets.forEach(dataset => {
                dataset.data.shift();
            });
        }

        chart.update('none'); // silent update (no slide animations to conserve CPU)
    }

    // Listen for theme change events to re-render chart grid lines properly
    document.getElementById('themeToggleBtn').addEventListener('click', () => {
        setTimeout(() => {
            if (cpuChart) { cpuChart.options = getChartOptions('Percentage (%)', 100); cpuChart.update(); }
            if (ramChart) { ramChart.options = getChartOptions('Percentage (%)', 100); ramChart.update(); }
            if (diskChart) { diskChart.options = getChartOptions('Percentage (%)', 100); diskChart.update(); }
            if (netChart) { netChart.options = getChartOptions('Speed (KB/s)'); netChart.update(); }
        }, 100);
    });

    // Bind Alerts Purging Action
    const clearAlertsBtn = document.getElementById('clearAlertsBtn');
    if (clearAlertsBtn) {
        clearAlertsBtn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to clear all RESOLVED alert records from the system history?')) return;
            try {
                const response = await fetch('/api/alerts/clear', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    // Update dashboard lists immediately
                    updateDashboardMetrics();
                    // Optional: reload page to update the server-rendered Alerts Feed block if no active alerts
                    window.location.reload();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (err) {
                console.error('Failed to clear logs:', err);
            }
        });
    }

    // Device Selector Dropdown Listener
    const deviceSelector = document.getElementById('deviceSelector');
    if (deviceSelector) {
        deviceSelector.addEventListener('change', (e) => {
            const val = e.target.value;
            if (val) {
                const parts = val.split('|');
                selectedUserId = parts[0];
                selectedHostname = parts[1];
            } else {
                selectedUserId = '';
                selectedHostname = '';
            }
            // Re-initialize charts and fetch immediate update
            initializeCharts().then(() => {
                updateDashboardMetrics();
            });
        });
    }

    // ==========================================
    // MonitorAI Diagnostic Chatbot Handler
    // ==========================================
    const chatbotLauncher = document.getElementById('chatbotLauncher');
    const chatbotPanel = document.getElementById('chatbotPanel');
    const chatbotCloseBtn = document.getElementById('chatbotCloseBtn');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSendBtn = document.getElementById('chatbotSendBtn');
    const chatbotBody = document.getElementById('chatbotBody');

    if (chatbotLauncher && chatbotPanel && chatbotCloseBtn) {
        // Toggle panel
        chatbotLauncher.addEventListener('click', () => {
            chatbotPanel.classList.toggle('active');
            chatbotLauncher.classList.toggle('active');
            if (chatbotPanel.classList.contains('active')) {
                chatbotInput.focus();
            }
        });

        chatbotCloseBtn.addEventListener('click', () => {
            chatbotPanel.classList.remove('active');
            chatbotLauncher.classList.remove('active');
        });

        // Input validation
        chatbotInput.addEventListener('input', () => {
            chatbotSendBtn.disabled = !chatbotInput.value.trim();
        });

        // Enter key to send
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && chatbotInput.value.trim()) {
                sendChatMessage(chatbotInput.value.trim());
            }
        });

        // Button click to send
        chatbotSendBtn.addEventListener('click', () => {
            if (chatbotInput.value.trim()) {
                sendChatMessage(chatbotInput.value.trim());
            }
        });

        // Suggested buttons click handler
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('chatbot-suggested-btn')) {
                const query = e.target.getAttribute('data-query');
                sendChatMessage(query);
            }
        });
    }

    function appendMessage(text, sender) {
        if (!chatbotBody) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `chatbot-message ${sender}`;
        
        if (sender === 'ai') {
            msgDiv.innerHTML = formatMarkdown(text);
        } else {
            msgDiv.innerText = text;
        }
        
        chatbotBody.appendChild(msgDiv);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }

    function showTypingIndicator() {
        if (!chatbotBody) return null;
        const indicator = document.createElement('div');
        indicator.className = 'chatbot-message ai typing-indicator-wrapper';
        indicator.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatbotBody.appendChild(indicator);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
        return indicator;
    }

    async function sendChatMessage(text) {
        if (!text) return;
        
        // Clear input
        chatbotInput.value = '';
        chatbotSendBtn.disabled = true;
        
        // Append user message
        appendMessage(text, 'user');
        
        // Show typing indicator
        const indicator = showTypingIndicator();
        
        try {
            // Build the payload
            const payload = {
                message: text,
                user_id: selectedUserId || null,
                hostname: selectedHostname || null
            };

            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            // Remove typing indicator
            if (indicator) indicator.remove();
            
            if (data.success) {
                appendMessage(data.response, 'ai');
            } else {
                appendMessage("Sorry, I encountered an issue querying the telemetry diagnostics system: " + data.message, 'ai');
            }
        } catch (err) {
            if (indicator) indicator.remove();
            console.error('Chat error:', err);
            appendMessage("Connection error. Could not connect to the MonitorAI backend.", 'ai');
        }
    }

    function formatMarkdown(text) {
        let html = text;
        // Escape HTML
        html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        // Title headers
        html = html.replace(/^### (.*?)$/gm, '<h6 class="fw-bold mt-2 mb-1 text-dark-emphasis">$1</h6>');
        // Bold tags
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Pre-formatted code blocks
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        // Inline code
        html = html.replace(/`(.*?)`/g, '<code>$1</code>');
        // List items
        html = html.replace(/^\* (.*?)$/gm, '<li class="small">$1</li>');
        html = html.replace(/^\d+\. (.*?)$/gm, '<li class="small">$1</li>');
        // Wrap lists
        html = html.replace(/<\/li>\n<li/g, '</li><li');
        html = html.replace(/(<li.*?>.*?<\/li>)/g, '<ul class="mb-1 text-secondary-emphasis ps-3">$1</ul>');
        html = html.replace(/<\/ul><ul class="mb-1 text-secondary-emphasis ps-3">/g, '');
        // Line breaks
        html = html.replace(/\n/g, '<br>');
        return html;
    }

    // 5. Bootstrapper execution
    initializeCharts().then(() => {
        updateDashboardMetrics();
        // Setup polling loop
        setInterval(updateDashboardMetrics, refreshInterval);
    });
});
