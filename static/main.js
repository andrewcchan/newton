document.addEventListener('DOMContentLoaded', () => {
    const velocitySlider = document.getElementById('velocity');
    const angleSlider = document.getElementById('angle');
    const velocityValue = document.getElementById('velocity-value');
    const angleValue = document.getElementById('angle-value');

    const trajectoryCanvas = document.getElementById('trajectoryChart');
    const kinematicsCanvas = document.getElementById('kinematicsChart');

    let trajectoryChart;
    let kinematicsChart;

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
            updateCharts(data);
        });
    }

    function updateCharts(data) {
        const trajectoryData = data.x.map((x_val, i) => ({ x: x_val, y: data.y[i] }));

        if (trajectoryChart) {
            trajectoryChart.destroy();
        }
        trajectoryChart = new Chart(trajectoryCanvas, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Trajectory',
                    data: trajectoryData,
                    borderColor: 'blue',
                    showLine: true,
                    fill: false,
                }]
            },
            options: {
                animation: {
                    duration: 2000,
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'x (m)'
                        }
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'y (m)'
                        }
                    }
                }
            }
        });

        if (kinematicsChart) {
            kinematicsChart.destroy();
        }
        kinematicsChart = new Chart(kinematicsCanvas, {
            type: 'line',
            data: {
                labels: data.t,
                datasets: [{
                    label: 'x Position',
                    data: data.x,
                    borderColor: 'red',
                    yAxisID: 'y'
                }, {
                    label: 'y Position',
                    data: data.y,
                    borderColor: 'green',
                    yAxisID: 'y'
                }, {
                    label: 'x Velocity',
                    data: data.vx_t,
                    borderColor: 'purple',
                    yAxisID: 'y1'
                }, {
                    label: 'y Velocity',
                    data: data.vy_t,
                    borderColor: 'orange',
                    yAxisID: 'y1'
                }]
            },
            options: {
                animation: {
                    duration: 2000,
                    easing: 'linear'
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time (s)'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Position (m)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Velocity (m/s)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    velocitySlider.addEventListener('input', fetchDataAndUpdate);
    angleSlider.addEventListener('input', fetchDataAndUpdate);

    fetchDataAndUpdate();
});
