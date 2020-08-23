$(document).ready(function () {
    $.validator.setDefaults({
      submitHandler: function () {
        alert( "From successful submitted!" );
      }
    });
    $('#quickForm').validate({
      rules: {
        name: {
          required: true,
          remote: "{% url 'add_project_save' %}"
        }
      },
      messages: {
        name: {
          required: "Please enter a Project"
        }
      },
      errorElement: 'span',
      errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.closest('.form-group').append(error);
      },
      highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      }
    });
  });