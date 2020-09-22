$(document).ready(function(){
        var endpoint3 = 'api/chart_case/data/'
        var defaultData = []
        var labels = [];
        $.ajax({
        method:"GET",
        url: endpoint3,
        success: function(data){
            labels = data.labels
            defaultData = data.default
            // console.log(data)
            setChart()
        },
        error: function(error_data){
          console.log('error')
          console.log(error_data)
        }
      })
      function setChart(){
        let myChart = document.getElementById('case-chart').getContext('2d');
        // Global Options
        Chart.defaults.global.defaultFontFamily = 'Lato';
        Chart.defaults.global.defaultFontSize = 18;
        Chart.defaults.global.defaultFontColor = '#777';
        let massPopChart = new Chart(myChart, {
          type:'line', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
          data:{
            labels: labels,
            datasets:[{
              label:'Case',
              data: defaultData,
              backgroundColor: '#007bff',
              backgroundColor : 'transparent',
              borderWidth:4,
              borderColor : '#007bff',
              pointBorderColor : '#007bff',
              pointBackgroundColor: '#007bff',
              fill : false
              // hoverBorderWidth:3,
              // hoverBorderColor:'#000'
            }]
          },
          options:{
            maintainAspectRatio: false,
            title:{
              display:false,
              text:'month',
              fontSize:20
            },
            legend : {
              display: false
            },
            layout:{
              padding:{
                left:50,
                right:0,
                bottom:0,
                top:0
              }
            },
            tooltips:{
              enabled:true
            }
          }
        });
      }
  }) //end document
