    $(document).ready(function(){
            // var endpoint = 'http://61.19.253.23/api/model5HospSendClaimCode/data/'
            var endpoint = 'http://bkk.hospital-os.com/api/model5HospSendClaimCode/data/'
            var defaultData = []
            var labels = [];
            $.ajax({
            method:"GET",
            url: endpoint,
            success: function(data){
                labels = data.labels
                defaultData = data.default
                setChart()
            },
            error: function(error_data){
              console.log('error')
              console.log(error_data)
            }
          })
          function setChart(){
            let myChart = document.getElementById('pieChart').getContext('2d');
            // Global Options
            Chart.defaults.global.defaultFontFamily = 'Lato';
            Chart.defaults.global.defaultFontSize = 18;
            Chart.defaults.global.defaultFontColor = '#777';
            let massPopChart = new Chart(myChart, {
              type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
              data:{
                labels: labels,
                datasets:[{
                  label:'Case',
                  data: defaultData,
                  formatter: labelFormatter,
                  // backgroundColor:'green',
                  backgroundColor:['#4cd137', '#e84118'],
                  // backgroundColor: [
                  // 'rgba(255, 99, 132, 0.7)',
                  // 'rgba(54, 162, 235, 0.7)',
                  // 'rgba(255, 206, 86, 0.7)',
                  // 'rgba(75, 192, 192, 0.7)',
                  // 'rgba(153, 102, 255, 0.7)',
                  // 'rgba(255, 159, 64, 0.7)',
                  // 'rgba(241, 196, 15,0.7)',
                  // 'rgba(44, 62, 80,0.7)'
                  // ],
                  borderWidth:1,
                  borderColor:'#777',
                  hoverBorderWidth:3,
                  hoverBorderColor:'#000'
                }]
              },
              options:{
                title:{
                  display:false,
                  text:'month',
                  fontSize:20
                },
                legend:{
                  display:false,
                  position:'right',
                  labels:{
                    fontColor:'#000'
                  }
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
      function labelFormatter(label, series) {
        return '<div style="font-size:13px; text-align:center; padding:2px; color: #fff; font-weight: 600;">'
          + label
          + '<br>'
          + Math.round(series.percent) + '%</div>'
      }
