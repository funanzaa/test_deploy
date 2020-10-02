$(document).ready(function() {
    var endpoint4 = 'api/MonthlyRecap/data/'
    var defaultData = []
    var labels = [];
    $.ajax({
        method: "GET",
        url: endpoint4,
        success: function(data) {
            labels = data.labels
            defaultData = data.default
            // console.log(data)
            setChart()
        },
        error: function(error_data) {
            console.log('error')
            console.log(error_data)
        }
    })

    function setChart() {
        var caseChartCannvas = $('#caseMonthChart').get(0).getContext('2d')

        var casesChartData = {
            // labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],
            labels: labels,
            datasets: [{
                label: 'Cases',
                backgroundColor: 'rgba(60,141,188,0.9)',
                borderColor: 'rgba(60,141,188,0.8)',
                pointRadius: false,
                pointColor: '#3b8bba',
                pointStrokeColor: 'rgba(60,141,188,1)',
                pointHighlightFill: '#fff',
                pointHighlightStroke: 'rgba(60,141,188,1)',
                // data: ['21', '12', '3', '41', '5', '6', '7', '3', '9', '10', '11', '12', '13', '14', '51', '16', '17', '18', '19', '24', '21', '21', '3', '24', '25', '26', '27', '28', '29', '30'],
                data: defaultData,
            }, ]
        }

        var caseChartOptions = {
            maintainAspectRatio: false,
            responsive: true,
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false,
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false,
                    }
                }]
            }
        }

        // This will get the first returned node in the jQuery collection.
        var salesChart = new Chart(caseChartCannvas, {
            type: 'bar',
            data: casesChartData,
            options: caseChartOptions
        })
    }

})
