$(function() {
  // Mobile menu link.
  var menu     = $('#menu'),
      menuLink = $('#menu-link');

  menuLink.on('click', function() {
    var active = 'active';

    menu.toggleClass(active);
    menuLink.toggleClass(active);
    return false;
  });

  // Slowly fade out messages.
  var msgContainers = [$('.messages'), $('.errorlist')];
  $.each(msgContainers, function() {
    if ($(this).length > 0) $(this).delay(3000).fadeOut(8000);
  });
});
