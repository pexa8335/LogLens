// script.js - PHIÊN BẢN CUỐI CÙNG, SỬ DỤNG LOGIC ĐÚNG

// Điểm vào duy nhất, chạy khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Chạy code chung cho tất cả các trang ---
    renderNavbarButtons();

    // --- 2. Chạy code riêng cho từng trang ---

    // Nếu tìm thấy nút 'checkButton', ta biết đây là trang Detect Anomaly
    if (document.getElementById('checkButton')) {
        initializeDetectPage();
    }

    // Nếu tìm thấy 'trafficChart', ta biết đây là trang Dashboard
    if (document.getElementById('trafficChart')) {
        initializeDashboardPage();
    }
});


// =============================================================
//  CÁC HÀM TRỢ GIÚP
// =============================================================

/**
 * Hàm chung: Hiển thị nút Login/Logout trên thanh điều hướng.
 */
function renderNavbarButtons() {
    const navbarButtons = document.querySelector('.navbar-buttons');
    if (!navbarButtons) return;
    navbarButtons.innerHTML = '';
    const loggedInUserEmail = localStorage.getItem('loggedInUserEmail');
    if (loggedInUserEmail) {
        const logoutBtn = document.createElement('a');
        logoutBtn.textContent = 'Log Out';
        logoutBtn.className = 'navbar-btn-login';
        logoutBtn.style.cursor = 'pointer';
        logoutBtn.onclick = function() {
            localStorage.removeItem('loggedInUserEmail');
            window.location.href = '/';
        };
        navbarButtons.appendChild(logoutBtn);
    }
}


/**
 * Khởi tạo tất cả logic cho trang Detect Anomaly.
 */
function initializeDetectPage() {
    // Toàn bộ code cho trang Detect Anomaly của bạn ở đây...
    // (Phần này đã hoạt động tốt, không cần thay đổi)
    const checkButton = document.getElementById('checkButton');
    const logInput = document.getElementById('logInput');
    const resultContainer = document.getElementById('resultContainer');
    const explanationContainer = document.getElementById('explanationContainer');

    checkButton.addEventListener('click', async () => {
        const logLine = logInput.value.trim();
        if (!logLine) {
            resultContainer.innerHTML = '<p style="color: #ffcc00;">Please paste a log entry first.</p>';
            return;
        }
        resultContainer.innerHTML = '<p>Analyzing, please wait...</p>';
        explanationContainer.innerHTML = '';
        checkButton.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ log_line: [logLine] }),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error');
            }
            const results = await response.json();
            displayAnalysisResult(results[0]);
        } catch (error) {
            console.error('Error during analysis:', error);
            resultContainer.innerHTML = `<p style="color: #ff4d4d;"><strong>Error:</strong> ${error.message}</p>`;
        } finally {
            checkButton.disabled = false;
        }
    });

    function displayAnalysisResult(result) {
        if (!result) { return; }
        const isSuspicious = result.is_suspicious === 1;
        const score = (result.suspicion_score * 100).toFixed(2);
        const statusClass = isSuspicious ? 'suspicious' : 'normal';
        const statusText = isSuspicious ? 'Suspicious' : 'Normal';
        resultContainer.innerHTML = `<b class="result-title">Analysis Result:</b><div class="result-item">Log Entry: <span>${result.log_line}</span></div><div class="result-item">Status: <span class="${statusClass}">${statusText}</span></div><div class="result-item">Suspicion Score: <span>${score}%</span></div>`;
        if (isSuspicious) {
            const explainButton = document.createElement('button');
            explainButton.id = 'explainButton';
            explainButton.textContent = '🔍 Explain Anomaly';
            explainButton.style.cssText = "width: 100%; background: #0d6efd; color: white; font-weight: bold; font-size: 1.1em; padding: 12px 0; border: none; border-radius: 6px; margin-top: 15px; cursor:pointer;";
            resultContainer.appendChild(explainButton);
            explainButton.addEventListener('click', () => handleExplainClick(result.log_line));
        }
    }
    async function handleExplainClick(logLine) {
        explanationContainer.innerHTML = '<p>Generating explanation...</p>';
        try {
            const response = await fetch('/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ log_line: [logLine] }),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error');
            }
            const data = await response.json();
            displayExplanation(data);
        } catch (error) {
            console.error('Error during explanation:', error);
            explanationContainer.innerHTML = `<p style="color: #ff4d4d;"><strong>Error:</strong> ${error.message}</p>`;
        }
    }
    function displayExplanation(data) {
        let explanationHTML = '<b class="result-title">Feature Importance:</b>';
        explanationHTML += '<ul style="list-style: none; padding: 0;">';
        const features = data.feature_names.map((name, index) => ({
            name: name,
            value: data.feature_values[name],
            shap: data.shap_values[index]
        })).filter(f => Math.abs(f.shap) > 0.001); // Chỉ hiển thị các feature có ảnh hưởng
        
        features.sort((a, b) => Math.abs(b.shap) - Math.abs(a.shap));

        features.slice(0, 10).forEach(f => {
            const shapValue = f.shap.toFixed(4);
            const color = shapValue > 0 ? '#ff4d4d' : '#4dff88'; // Đỏ (tăng khả năng) hoặc Xanh (giảm khả năng)
            const sign = shapValue > 0 ? '+' : '';
            explanationHTML += `<li style="padding: 4px 0; border-bottom: 1px solid #333;"><b>${f.name}</b>: ${f.value} <span style="color:${color}; float: right; font-weight: bold;">(${sign}${shapValue})</span></li>`;
        });

        explanationHTML += '</ul>';
        explanationContainer.innerHTML = explanationHTML;
    }
}


/**
 * Khởi tạo tất cả logic cho trang Dashboard.
 */
function initializeDashboardPage() {
    
    async function fetchAndUpdateDashboard() {
        try {
            const response = await fetch('/dashboard_data');
            if (!response.ok) throw new Error(`Failed to fetch: ${response.statusText}`);
            const data = await response.json();
            
            updateOverviewCards(data.cards);
            updateAnomalyTable(data.table);
            // Gọi hàm cập nhật biểu đồ CHÍNH XÁC của bạn
            updateTrafficChart(data.chart);

        } catch (error) {
            console.error("Error updating dashboard:", error);
        }
    }

    function updateOverviewCards(cards) {
        document.getElementById('total-requests-value').textContent = cards.total_requests;
        document.getElementById('anomalies-detected-value').textContent = cards.anomalies_detected;
        document.getElementById('warnings-value').textContent = cards.warnings;
        const healthElement = document.getElementById('system-health-value');
        healthElement.textContent = cards.system_health;
        healthElement.classList.remove('overview-card-critical');
        if (cards.system_health === 'Critical') {
            healthElement.classList.add('overview-card-critical');
        }
    }

    function updateAnomalyTable(tableData) {
        const tbody = document.querySelector('.anomaly-table tbody');
        tbody.innerHTML = '';
        if (!tableData || tableData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No recent anomalies found.</td></tr>';
            return;
        }
        tableData.forEach(row => {
            let severity = 'Low';
            let severityClass = 'low';
            if (row.suspicion_score > 0.9) {
                severity = 'Critical';
                severityClass = 'critical';
            } else if (row.suspicion_score > 0.7) {
                severity = 'High';
                severityClass = 'high';
            }
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${row.timestamp}</td><td>${row.ip}</td><td>${row.url}</td><td>${row.status}</td><td class="${severityClass}">${severity}</td>`;
            tbody.appendChild(tr);
        });
    }

    /**
     * HÀM CẬP NHẬT BIỂU ĐỒ CHUYÊN NGHIỆP MÀ BẠN ĐÃ CUNG CẤP
     */
    function updateTrafficChart(chartData) {
        const canvas = document.getElementById('trafficChart');
        if (!canvas) return; // Thoát nếu không tìm thấy canvas

        // Lấy biểu đồ hiện tại đang gắn với canvas (nếu có)
        let chart = Chart.getChart(canvas);

        if (chart) {
            // Nếu biểu đồ đã tồn tại, chỉ cập nhật dữ liệu
            chart.data.labels = chartData.labels;
            chart.data.datasets[0].data = chartData.normal_data;
            chart.data.datasets[1].data = chartData.anomalies_data;
            chart.update(); // Vẽ lại biểu đồ với dữ liệu mới
        } else {
            // Nếu chưa có biểu đồ nào, tạo một cái mới
            new Chart(canvas.getContext('2d'), {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [
                        { label: 'Normal Traffic', data: chartData.normal_data, borderColor: '#2196f3', backgroundColor: 'rgba(33,150,243,0.08)', fill: true, tension: 0.4 },
                        { label: 'Anomalies Traffic', data: chartData.anomalies_data, borderColor: '#e57373', backgroundColor: 'rgba(229,115,115,0.08)', fill: true, tension: 0.4 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#E0EEF0' } },
                        y: { grid: { color: 'rgba(224, 238, 240, 0.1)' }, beginAtZero: true, ticks: { color: '#E0EEF0' } }
                    }
                }
            });
        }
    }

    // Chạy lần đầu khi trang tải và tự động cập nhật mỗi 10 giây
    fetchAndUpdateDashboard();
    setInterval(fetchAndUpdateDashboard, 10000);
}