$(function() {
  if (!$('#id_first_name').val()) $('#id_first_name').focus();

  $('.edit').on('click', function() {
    var name = $(this).data('name');

    $(this).parent('.btn-container').hide();
    $('input[name="'+name+'"]').show();

    return false;
  });
});
