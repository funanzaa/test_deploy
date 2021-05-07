

var labels = [];
domain = 'http://localhost:8000'
// domain = 'http://bkk.hospital-os.com'
// var objId = document.getElementById("project").value;
// var objDate = document.getElementById("reservation").value;
var dataURLOpbkkWeb = domain + `/crm/report/ReportSubProjectHos`
// var dataURLOpbkkClient = domain + `/crm/report/ReportSubProjectOpbkkClient`
$.ajax({
    method:'GET',
    url: dataURLOpbkkWeb,
    success:function(response){
        console.log(response)
        for (var i in response){    
          console.log(response)      
            labels = response.labelsHos
            defaultData_m1 = response.data_m1
            defaultData_m2 = response.data_m2
            defaultData_m3 = response.data_m3
            defaultData_m4 = response.data_m4
            defaultData_m5 = response.data_m5
            // opbkkclinet
            labelOpbkkClient = response.labelsHosAdmin
            opbkkclient_m1 = response.hosAdmin_m1
            opbkkclient_m2 = response.hosAdmin_m2
            opbkkclient_m3 = response.hosAdmin_m3
            opbkkclient_m4 = response.hosAdmin_m4
            opbkkclient_m5 = response.hosAdmin_m5
            // console.log(opbkkclient_m1)


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
      text: 'Hospital-OS',
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
      item: {"font-angle":-15},
      maxItems: 999,
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
      },
      {
        // Plot 2 values, linear data
        values:defaultData_m4,
        text: 'เมษายน'
      },
      {
        // Plot 2 values, linear data
        values:defaultData_m5,
        text: 'พฤษภาคม'
      }
    ]
  };

  // OpbkkClinet
  let OpbkkClinet = {
    type: 'bar',
    globals: {
      fontFamily:"Sarabun",
      },
    title: {
      text: 'Hospital-Admin',
      fontSize: 20,
    },
    legend: {
      draggable: true,
    },
    scaleX: {
      // values: ['Archery - Female', 'Archery - Male', 'Athletics - Male', 'Boxing - Male', 'Cycling - Male', 'Diving - Male', 'Fencing - Male', 'Figure Skating - Female', 'Figure Skating - Male', 'Football - Male', 'Gymnastics - Male', 'Hockey - Male', 'Jeu De Paume - Male', 'Lacrosse - Male', 'Motorboating - Male', 'Polo - Male', 'Racquets - Male', 'Rowing - Male', 'Rugby - Male', 'Sailing - Male', 'Shooting - Male', 'Swimming - Male', 'Tennis - Female', 'Tennis - Male', 'Tug-Of-War - Male', 'Water Polo - Male', 'Wrestling - Male'],
      // values : ['ติดตั้งโปรแกรม', 'ประมวลผลข้อมูล', 'การใช้งานโปรแกรม','เข้าใช้งาน<br>OPBKKClaimClient', 'นำเข้าข้อมูล','ร้องขอข้อมูลล่าสุด','ตรวจสอบข้อมูล','สถานะข้อมูล<br>ไม่ตรงกับหน้าเว็บ','ส่งข้อมูล','UpdatePatch'],
      values : labelOpbkkClient,
      item: {
        angle: -15,
        fontSize: '10px'
      },
      // itemsOverlap: true,
      // lineColor: '#0079C4',
      maxItems: 999,
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
        // values: [23,5,27,29,25,17,15],
        values:opbkkclient_m1,
        text: 'มกราคม',
      },
      {
        // Plot 2 values, linear data
        // values: [23,20,27,5,25,17,15],
        values:opbkkclient_m2,
        text: 'กุมภาพันธ์'
      },
      {
        values:opbkkclient_m3,
        text: 'มีนาคม'
      },
      {
        values:opbkkclient_m4,
        text: 'เมษายน'
      },
      {
        values:opbkkclient_m5,
        text: 'พฤษภาคม'
      }
    ]
  };
  // Render Method[3]
  zingchart.render({
    id: 'ChartOpbkkWeb',
    data: OpbkkWeb,
  });
  zingchart.render({
    id: 'ChartOpbkkClient',
    data: OpbkkClinet,
  });
}

