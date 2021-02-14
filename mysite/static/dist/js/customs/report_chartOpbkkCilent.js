var defaultData_m1 = []
var defaultData_m2 = []
var defaultData_m3 = []
var labels = [];
domain = 'http://localhost:8000'
// domain = 'http://bkk.hospital-os.com'
// var objId = document.getElementById("project").value;
// var objDate = document.getElementById("reservation").value;
var dataURL = domain + `/crm/report/ReportSubProjectOpbkkWeb`
$.ajax({
    method:'GET',
    url:dataURL,
    success:function(response){
        // console.log(response)
        for (var i in response){
            // console.log(response)            
            labels = response.labels
            defaultData_m1 = response.data_m1
            defaultData_m2 = response.data_m2
            defaultData_m3 = response.data_m3
        }
        buildChartOpbkkWeb()

    }

})

function buildChartOpbkkWeb(){
  let OpbkkWeb = {
    type: 'bar',
    globals: {
      fontFamily:"Sarabun",
      },
    title: {
      text: 'OPBKKClaim - Web',
      fontSize: 20,
    },
    legend: {
      draggable: true,
    },
    scaleX: {
      // Set scale label
      // label: { text: 'Subgroup Project' },
      // Convert text on scale indices
      // labels: [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]
      labels:labels,
      item: {"font-angle":-15}
    },
    scaleY: {
      // Scale label with unicode character
      // label: { text: 'Temperature (°F)' }
    },
    plot: {
      // Animation docs here:
      // https://www.zingchart.com/docs/tutorials/styling/animation#effect
      animation: {
        effect: 'ANIMATION_EXPAND_BOTTOM',
        method: 'ANIMATION_STRONG_EASE_OUT',
        sequence: 'ANIMATION_BY_NODE',
        speed: 275,
      }
    },
    series: [
      {
        // Plot 1 values, linear data
        // values: [23,20,27,29,25,17,15],
        values:defaultData_m1,
        text: 'มกราคม',
      },
      {
        // Plot 2 values, linear data
        values:defaultData_m2,
        text: 'กุมภาพันธ์'
      },
      {
        // Plot 2 values, linear data
        values:defaultData_m3,
        text: 'มีนาคม'
      }
    ]
  };
  // Render Method[3]
  zingchart.render({
    id: 'ChartOpbkkClient',
    data: OpbkkWeb,
  });
// zingchart.render({
//   id: 'ChartOpbkkClient',
//   data: OpbkkWeb,
// });
}
