var currentColor = 0;
var colors = [ // from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
    "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000080", "#808080", "#FFFFFF", "#000000"
];

var chartData = null;
var request = new XMLHttpRequest();
request.open("GET", "data.json", false);
request.send(null);
chartData = JSON.parse(request.responseText);
request = new XMLHttpRequest();
request.open("GET", "../index.json", false);
request.send(null);
var date = JSON.parse(request.responseText);

$(document).ready(function () {
    $("#sub_title").text(chartData.title_sub);
    var i = 0;
    $("#collapsibleNavbar ul li a").each(function () {
        $( this ).text(date.date[i]);
        i++;
    });

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