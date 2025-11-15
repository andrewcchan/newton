function drawChart(data) {
    const ctx = document.getElementById('trajectoryChart').getContext('2d');
    if (window.myChart) {
        window.myChart.destroy();
    }
    window.myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Trajectory',
                    data: data.x.map((val, index) => ({ x: val, y: data.y[index] })),
                    borderColor: 'blue',
                    showLine: true
                },
                {
                    label: 'Target',
                    data: [{ x: data.target.x, y: data.target.y }],
                    backgroundColor: 'red',
                    pointRadius: data.target.radius * 5,
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Distance (m)'
                    }
                },
                y: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Height (m)'
                    }
                }
            }
        }
    });

    const message = document.getElementById('message');
    if (data.hit) {
        message.textContent = 'Congratulations, it was a hit!';
        message.style.color = 'green';
    } else {
        message.textContent = 'Sorry, you missed. Try again!';
        message.style.color = 'red';
    }
}

document.getElementById('launch').addEventListener('click', () => {
    const velocity = document.getElementById('velocity').value;
    const angle = document.getElementById('angle').value;
    const gravity = (Math.random() * 10) + 5; // Random gravity between 5 and 15

    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ velocity, angle, gravity })
    })
    .then(response => response.json())
    .then(drawChart);
});

document.getElementById('solve').addEventListener('click', () => {
    const gravity = (Math.random() * 10) + 5;

    fetch('/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ gravity })
    })
    .then(response => response.json())
    .then(drawChart);
});
