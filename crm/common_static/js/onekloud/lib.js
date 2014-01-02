// Smoothly scroll browser window to the anchor. Pass element's id
// without `#`.
function scrollToAnchor(id){
  var anchor = $('#' + id);
  $('html, body').animate({
    scrollTop: anchor.offset().top
  }, {
    duration: 1000,
    easing: 'easeOutQuart'
  });
}
