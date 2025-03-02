document.addEventListener('DOMContentLoaded', function() {
    var chartData = JSON.parse(document.getElementById('chartData').textContent);
    if (chartData) {
        Plotly.newPlot('stockChart', chartData.data, chartData.layout);
    }
}); 