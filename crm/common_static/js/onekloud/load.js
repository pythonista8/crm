$(function() {
  // Slowly fade out messages.
  var msgContainers = [$('.messages'), $('.errorlist')];
  $.each(msgContainers, function() {
    if ($(this).length > 0) $(this).delay(3000).fadeOut(8000);
  });
});
