$(function() {
  // Mobile menu link.
  var layout   = $('#layout'),
      menu     = $('#menu'),
      menuLink = $('#menu-link');

  menuLink.on('click', function(event) {
    var active = 'active';

    event.preventDefault();
    layout.toggleClass(active);
    menu.toggleClass(active);
    menuLink.toggleClass(active);
  });

  // Slowly fade out messages.
  var msgContainers = [$('.messages'), $('.errorlist')];
  $.each(msgContainers, function() {
    if ($(this).length > 0) $(this).delay(3000).fadeOut(8000);
  });
});
