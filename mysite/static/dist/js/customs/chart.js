    $(document).ready(function(){
            var endpoint = 'api/chart/data/'
            var defaultData = []
            var labels = [];
            $.ajax({
            method:"GET",
            url: endpoint,
            success: function(data){
                labels = data.labels
                defaultData = data.default
                console.log(data)
                setChart()
            },
            error: function(error_data){
              console.log('error')
              console.log(error_data)
            }
          })
          function setChart(){
            let myChart = document.getElementById('myChart').getContext('2d');
            // Global Options
            Chart.defaults.global.defaultFontFamily = 'Lato';
            Chart.defaults.global.defaultFontSize = 18;
            Chart.defaults.global.defaultFontColor = '#777';
            let massPopChart = new Chart(myChart, {
              type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
              data:{
                labels: labels,
                datasets:[{
                  label:'Case',
                  data: defaultData,
                  backgroundColor:'green',
                  backgroundColor:[
                    'rgba(102, 154, 50, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(221, 148, 14, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(173, 11, 11, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(53, 50, 154, 0.2)',
                  ],
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
//chart-2
      $(document).ready(function(){
              var endpoint2 = 'api/chart_service/data/'
              var defaultData = []
              var labels = [];
              $.ajax({
              method:"GET",
              url: endpoint2,
              success: function(data){
                  labels = data.labels
                  defaultData = data.default
                  console.log(data)
                  setChart()
              },
              error: function(error_data){
                console.log('error')
                console.log(error_data)
              }
            })
            function setChart(){
              let myChart = document.getElementById('myChart2').getContext('2d');
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
                    backgroundColor:'green',
                    backgroundColor:[
                      'rgba(102, 154, 50, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(221, 148, 14, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(173, 11, 11, 0.2)',
                    ],
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
                    display:true,
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
