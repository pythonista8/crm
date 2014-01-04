$(function() {
  // Calendar.
  $('.calendar').datepicker({
    onSelect: function(dateText, inst) {
      if ($('#events').length > 0) scrollToAnchor('events');
    }
  });
  $('.datepicker').datepicker();

  // New event.
  $('.input-event').on('keypress keyup', function() {
    var s = $(this).val();
    if (s.length > 10) {
      setTimeout(function() {
        $.get(eventDetailsURI, {s: s}, function(resp) {
          if (resp.status == 'success') {
            var isMeeting = false;
            if (resp.data.hours) isMeeting = true;

            var day = resp.data.day;
            var month = resp.data.month;
            var year = resp.data.year;
            var html = month + " " + day + ", " + year;

            if (isMeeting) {
              var hrs = resp.data.hours;
              var mins = resp.data.minutes;
              html += " @ " + hrs + ":" + mins;
              $('#event-type').html("Meeting");
            } else {
              $('#event-type').html("Follow-Up");
            }
            $('#event-date').html(html);
            $('#event-details').hide().fadeIn();
          } else {
            $('#event-details').fadeOut();
          }
        });
      }, 500);
    }
  });

  // Duration.
  fixMinutesDisplay();
});

$('.duration input[type="number"]').last().on('change', function() {
  fixMinutesDisplay();
});
