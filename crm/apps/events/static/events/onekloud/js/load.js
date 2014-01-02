$(function() {
  $('.calendar').datepicker({
    onSelect: function(dateText, inst) {
      if ($('#events').length > 0) scrollToAnchor('events');
    }
  });
  $('.datepicker').datepicker();
  fixMinutesDisplay();
});

$('.duration input[type="number"]').last().on('change', function() {
  fixMinutesDisplay();
});
