document.addEventListener('DOMContentLoaded', function() {
    const velocityInput = document.getElementById('velocity');
    const angleInput = document.getElementById('angle');
    const simulateBtn = document.getElementById('simulate-btn');
    const ctx = document.getElementById('motionChart').getContext('2d');

    let chart = null;

    function renderChart(trajectory) {
        const dataPoints = trajectory.map(p => ({ x: p.x, y: p.y }));

        // Determine max range to keep aspect ratio somewhat consistent or just auto-scale
        // For physics, equal scaling is better, but Chart.js makes that tricky without plugins.
        // We will stick to standard scatter plot for now.

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Projectile Path',
                    data: dataPoints,
                    backgroundColor: 'rgba(54, 162, 235, 1)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    showLine: true,
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Distance (m)'
                        },
                        beginAtZero: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Height (m)'
                        },
                        beginAtZero: true
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    simulateBtn.addEventListener('click', () => {
        const v0 = velocityInput.value;
        const angle = angleInput.value;

        fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ v0: v0, angle: angle }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                renderChart(data.trajectory);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
