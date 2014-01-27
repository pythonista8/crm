// Customer form.
$(function() {
  if (!$('#id_first_name').val()) $('#id_first_name').focus();

  $('.edit').on('click', function() {
    var name = $(this).data('name');

    $(this).parent('.btn-container').hide();
    $('input[name="'+name+'"]').show();

    return false;
  });
});

// Take Tour.
if (takeTour) {
  if (!$('#id_first_name').length) {
    // CustomerList.
    startTourForList();
  } else {
    // CustomerCreate.
    startTourForCreate();

    // Prepare sample data for fields.
    $('#id_salutation').val('mr');
    $('#id_first_name').val('Michael');
    $('#id_last_name').val('Jackson');
    $('#id_amounts-0-value').val('15600');
    $('#id_amounts-0-status').val('win');
  }
}
