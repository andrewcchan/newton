document.addEventListener('DOMContentLoaded', () => {
    const velocitySlider = document.getElementById('velocity');
    const angleSlider = document.getElementById('angle');
    const velocityValue = document.getElementById('velocity-value');
    const angleValue = document.getElementById('angle-value');

    const trajectoryCanvas = document.getElementById('trajectoryChart');
    const kinematicsCanvas = document.getElementById('kinematicsChart');

    let trajectoryChart;
    let kinematicsChart;
    let animationFrameId;

    function fetchDataAndUpdate() {
        const velocity = velocitySlider.value;
        const angle = angleSlider.value;

        velocityValue.textContent = velocity;
        angleValue.textContent = angle;

        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ velocity, angle }),
        })
        .then(response => response.json())
        .then(data => {
            createOrUpdateCharts(data);
        });
    }

    function createOrUpdateCharts(data) {
        const trajectoryData = data.x.map((x_val, i) => ({ x: x_val, y: data.y[i] }));
        const angleVectorData = data.angle_vector.x.map((x_val, i) => ({ x: x_val, y: data.angle_vector.y[i] }));

        if (trajectoryChart) {
            trajectoryChart.destroy();
        }
        trajectoryChart = new Chart(trajectoryCanvas, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Full Trajectory',
                        data: trajectoryData,
                        borderColor: '#cccccc',
                        showLine: true,
                        fill: false,
                        pointRadius: 0,
                    },
                    {
                        label: 'Projectile',
                        data: [trajectoryData[0]],
                        backgroundColor: 'blue',
                        pointRadius: 5,
                    },
                    {
                        label: 'Launch Angle',
                        data: angleVectorData,
                        borderColor: 'red',
                        showLine: true,
                        fill: false,
                        pointRadius: 0,
                    }
                ]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: { display: true, text: 'x (m)' }
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        title: { display: true, text: 'y (m)' }
                    }
                },
                animation: false // We will handle animation manually
            }
        });

        if (kinematicsChart) {
            kinematicsChart.destroy();
        }
        kinematicsChart = new Chart(kinematicsCanvas, {
            type: 'line',
            data: {
                labels: data.t,
                datasets: [
                    { label: 'x Position', data: [], borderColor: 'red', yAxisID: 'y', pointRadius: 0 },
                    { label: 'y Position', data: [], borderColor: 'green', yAxisID: 'y', pointRadius: 0 },
                    { label: 'x Velocity', data: [], borderColor: 'purple', yAxisID: 'y1', pointRadius: 0 },
                    { label: 'y Velocity', data: [], borderColor: 'orange', yAxisID: 'y1', pointRadius: 0 }
                ]
            },
            options: {
                scales: {
                    x: { title: { display: true, text: 'Time (s)' } },
                    y: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Position (m)' } },
                    y1: { type: 'linear', display: true, position: 'right', title: { display: true, text: 'Velocity (m/s)' }, grid: { drawOnChartArea: false } }
                },
                animation: false
            }
        });

        // Cancel any previous animation frame
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }
        animate(data, trajectoryData);
    }

    function animate(data, trajectoryData) {
        const duration = 2000; // 2 seconds
        let startTime = null;

        function animationStep(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = (timestamp - startTime) / duration;
            const frameIndex = Math.min(Math.floor(progress * data.t.length), data.t.length - 1);

            // Update projectile position
            trajectoryChart.data.datasets[1].data = [trajectoryData[frameIndex]];
            trajectoryChart.update('none'); // 'none' for no animation from chart.js

            // Update kinematic graphs
            kinematicsChart.data.datasets[0].data = data.x.slice(0, frameIndex + 1);
            kinematicsChart.data.datasets[1].data = data.y.slice(0, frameIndex + 1);
            kinematicsChart.data.datasets[2].data = data.vx_t.slice(0, frameIndex + 1);
            kinematicsChart.data.datasets[3].data = data.vy_t.slice(0, frameIndex + 1);
            kinematicsChart.update('none');

            if (progress < 1) {
                animationFrameId = requestAnimationFrame(animationStep);
            }
        }
        animationFrameId = requestAnimationFrame(animationStep);
    }

    velocitySlider.addEventListener('input', fetchDataAndUpdate);
    angleSlider.addEventListener('input', fetchDataAndUpdate);

    fetchDataAndUpdate();
});
