document.addEventListener('DOMContentLoaded', () => {

    // Helper to get CSS variables for chart colors
    const style = getComputedStyle(document.body);
    const primaryBlue = style.getPropertyValue('--primary-blue').trim() || '#007BFF';
    const accentBlue = style.getPropertyValue('--accent-blue').trim() || '#00d2ff';
    const dangerRed = style.getPropertyValue('--danger').trim() || '#ff0055';
    const successGreen = style.getPropertyValue('--success').trim() || '#00ff88';
    const textColor = style.getPropertyValue('--text-primary').trim() || '#ffffff';
    const gridColor = style.getPropertyValue('--card-border').trim() || 'rgba(0, 210, 255, 0.2)';

    Chart.defaults.color = textColor;
    Chart.defaults.font.family = "'Inter', sans-serif";

    if (window.chartType === 'identity' && window.resultData) {
        const ctx = document.getElementById('identityRadarChart');
        if (ctx) {
            // Generate mock radar data based on risk and confidence
            const d = window.resultData;
            const r = d.risk_score || 50;
            const c = d.confidence || 50;
            
            new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Surface Web', 'Deep Web', 'Social Graph', 'Breach Data', 'Metadata'],
                    datasets: [{
                        label: 'Threat Footprint Matrix',
                        data: [c, r/2, c*0.8, r, c*0.6],
                        backgroundColor: 'rgba(0, 210, 255, 0.2)',
                        borderColor: accentBlue,
                        pointBackgroundColor: dangerRed,
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: dangerRed,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: gridColor },
                            grid: { color: gridColor },
                            pointLabels: { color: textColor, font: { size: 11 } },
                            ticks: { display: false, min: 0, max: 100 }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
    }

    if (window.chartType === 'domain' && window.resultData) {
        const ctx = document.getElementById('domainBarChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['HSTS', 'X-Frame', 'CSP', 'XSS-Protect', 'Content-Type'],
                    datasets: [{
                        label: 'Security Posture',
                        data: [20, 80, 10, 90, 100], // Mock scores
                        backgroundColor: [dangerRed, successGreen, dangerRed, successGreen, successGreen],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: gridColor },
                            ticks: { display: false }
                        },
                        x: {
                            grid: { display: false }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
    }

});
