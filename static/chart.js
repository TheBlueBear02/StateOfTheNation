var ctx = document.getElementById('lineChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ lables | safe }},
        datasets: [{
            label: 'Example Dataset',
            data: {{ values | safe }},
            fill: true, 
            borderColor: '#4890FD',
            borderWidth: 2,
            lineTension: 0.5,
            backgroundColor: 'rgb(208, 226, 252)',
            pointRadius: 0,
        }]
    },
    options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }  
        },
    
        animations: {
            tension: {
                duration: 1000,
                easing: 'linear',
                from: 1,
                to: 0.3,
                loop: true
                }
        },
        scales: {
            x: {
            grid: {
                display: false,
                }
            }
        }
    }
});