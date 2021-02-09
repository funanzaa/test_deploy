$(function () {

  //Datemask dd/mm/yyyy
  $('#datemask').inputmask('dd/mm/yyyy', {
    'placeholder': 'dd/mm/yyyy'
  })
  //Datemask2 mm/dd/yyyy
  $('#datemask2').inputmask('dd/mm/yyyy', {
    'placeholder': 'dd/mm/yyyy'
  })

  //Date range picker
  $('#reservationdate').datetimepicker({
    format: 'L'
  });
  //Date range picker
  $('#reservation').daterangepicker({
    locale: {
      format: 'DD/MM/YYYY'
    }
  })

  //Bootstrap Duallistbox
  $('.duallistbox').bootstrapDualListbox()

})