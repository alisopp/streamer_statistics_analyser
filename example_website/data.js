var chartData = null;
var request = new XMLHttpRequest();
request.open("GET", "data.json", false);
request.send(null);
chartData = JSON.parse(request.responseText);

$(document).ready(function () {

    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getLabels(),
            datasets: getData()
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0.1, // disables bezier curves
                },
                point: {radius: 0}
            },
            legend: {
                position: 'right',
            }
        }
    });
});

//alert(chartData);
function getData() {
    return chartData.chart_data
}

function getLabels() {
    return chartData.observation_date
}