$(function() {
  // Calendar.
  $('.calendar').datepicker({
    dateFormat: 'dd-mm-yy',
    onSelect: function(dateText, inst) {
      if ($('#meeting-table').length) {
        scrollToAnchor('meeting-table');
      } else if ($('#followup-table').length) {
        scrollToAnchor('followup-table');
      }

      $.get(eventsFilterByDateURI, {date: dateText}, function(resp) {
        if (resp.status == 'success') {
          var mContainer = $('#meeting-table tbody');
          var fContainer = $('#followup-table tbody');

          // Clear table content to fill up new.
          mContainer.html('');
          fContainer.html('');

          $('#date-heading').html(resp.date);

          $.each(resp.data, function() {
            var ob = $(this)[0];
            var row = "<tr>";

            if (ob.type == 'Meeting') row += "<td width=\"5%\" align=\"center\">" +
                                             ob.time + "</td>";

            row += "<td><a href=\"" + ob.url + "\">" + ob.subject + "</a></td>" +
                   "<td align=\"center\"><a href=\"" + ob.delete_url + "\" class=\"red\" title=\"Remove\">" +
                   "<i class=\"fa fa-times\"></i></a></td></tr>";

            if (ob.type == 'Meeting') mContainer.append(row);
            if (ob.type == 'FollowUp') fContainer.append(row);
          });

          var emptyRow = "<tr><td><p>No meeting created yet.</p></td><td></td>";

          if (!fContainer.has('tr').length) fContainer.html(emptyRow + "</tr>");
          if (!mContainer.has('tr').length) mContainer.html(emptyRow + "<td></td></tr>");
        }
      });
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
          }
        });
      }, 800);
    }
  });

  // Duration.
  fixMinutesDisplay();
});

$('.duration input[type="number"]').last().on('change', function() {
  fixMinutesDisplay();
});
