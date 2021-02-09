$(document).ready(function(){
  // getsubproject()
  let dropdown = document.getElementById('locality-dropdownUpdate');
  $("#project2").change(function(){
    getsubproject()
  })
  function getsubproject(){
    document.getElementById('locality-dropdownUpdate').disabled = false;
    var x = document.getElementById("project2").value;
    let dropdown_subproject = $('#locality-dropdownUpdate');
    dropdown_subproject.empty();
    var endpoint = 'http://bkk.hospital-os.com/crm/api/List_Subproject/'+ x + '/'
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
