var chartContext = document.querySelector('#votesOnChart').getContext('2d');
var endpoint = $('#votesOnChart').attr('endpoint-url');

function renderChart(data) {
    new Chart(chartContext, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'number of votes',
                data: data.votes,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function handleError(error) {
    console.error(error)
}

$.ajax({
    method: 'get',
    url: endpoint,
    success: renderChart,
    error: handleError
})
