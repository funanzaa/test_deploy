$(document).ready(function(){
  // getsubproject()
  let dropdown = document.getElementById('locality-dropdownUpdate');
  $("#project2").change(function(){
    // document.getElementById('locality-dropdownUpdate').disabled = false;
    // var x = document.getElementById("project2").value;
    getsubproject()
    // var endpoint = 'http://localhost:8000/crm/api/List_Subproject/'+ x + '/'
    // $.ajax({
    //     method:"GET",
    //     url: endpoint,
    //     success: function(data){
    //          var mydata = JSON.parse(data);
    //          let option;
    //         // console.log(mydata)
    //         //  console.log(mydata.length)
    //         let dropdown_subproject = $('#locality-dropdownUpdate');
    //         dropdown_subproject.empty();
    //          for (let i = 0; i < mydata.length; i++) {
    //           option = document.createElement('option');
    //           // console.log(data[i])
    //           option.text = mydata[i].name;
    //           option.value = mydata[i].id;
    //           dropdown.add(option);
    //           dropdown.selectedIndex = 0;
    //           }
    //     },
    //     error: function(error_data){
    //       console.log('error')
    //       console.log(error_data)
    //     }
    //   })
    
    // dropdown.options[ dropdown.selectedIndex ].value
    // let dropdown2 = $('#locality-dropdown2')
      // dropdown2.empty()
      // console.log("test")
  })
  function getsubproject(){
    document.getElementById('locality-dropdownUpdate').disabled = false;
    var x = document.getElementById("project2").value;
    let dropdown_subproject = $('#locality-dropdownUpdate');
    dropdown_subproject.empty();
    var endpoint = 'http://localhost:8000/crm/api/List_Subproject/'+ x + '/'
    $.ajax({
        method:"GET",
        url: endpoint,
        success: function(data){
             var mydata = JSON.parse(data);
             let option;
            // console.log(mydata)
            //  console.log(mydata.length)
            // let dropdown_subproject = $('#locality-dropdownUpdate');
            // dropdown_subproject.empty();
             for (let i = 0; i < mydata.length; i++) {
              option = document.createElement('option');
              // console.log(data[i])
              option.text = mydata[i].name;
              option.value = mydata[i].id;
              dropdown.add(option);
              dropdown.selectedIndex = 0;
              }
        },
        error: function(error_data){
          console.log('error')
          console.log(error_data)
        }
      })
  }
})
