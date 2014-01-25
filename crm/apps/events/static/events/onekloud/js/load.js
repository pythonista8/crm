$(function() {
  // Calendar.
  $('.calendar').datepicker({
    dateFormat: 'dd-mm-yy',
    onSelect: function(dateText, inst) {
      var mTable = $('#meeting-table');
      var mContainer = mTable.find('tbody');
      var mEmpty = $('#meetings-empty');

      var fTable = $('#followup-table');
      var fContainer = fTable.find('tbody');
      var fEmpty = $('#followups-empty');

      if (mEmpty.length) mEmpty.remove();
      if (fEmpty.length) fEmpty.remove();

      // Clear table content to fill up new.
      mContainer.html('');
      fContainer.html('');

      scrollToAnchor('date-heading');

      $.get(eventsFilterByDateURI, {date: dateText}, function(resp) {
        if (resp.status == 'success') {
          $('#date-heading').html(resp.date);

          $.each(resp.data, function() {
            var ob = $(this)[0];
            var row = "<tr>";

            if (ob.type == 'Meeting') row += "<td width=\"5%\" align=\"center\">" +
                                             ob.time + "</td>";

            row += "<td><a href=\"" + ob.url + "\">" + ob.subject + "</a></td>";

            if (isHead) row += "<td>" + ob.user + "</td>";

            row += "<td align=\"center\"><a href=\"" + ob.delete_url + "\" class=\"red\" title=\"Remove\">" +
                   "<i class=\"fa fa-times\"></i></a></td>";
            row += "</tr>";

            if (ob.type == 'Meeting') mContainer.append(row);
            if (ob.type == 'FollowUp') fContainer.append(row);
          });

          if (mContainer.has('tr').length) {
            mTable.show();
          } else {
            mTable.hide().after("<p id=\"meetings-empty\">No meetings created yet.</p>");
          }

          if (fContainer.has('tr').length) {
            fTable.show();
          } else {
            fTable.hide().after("<p id=\"followups-empty\">No follow-ups created yet.</p>");
          }
        }
      });
    }
  });
  $('.datepicker').datepicker();

  // New event.
  $('.input-event').on('keypress keyup', function() {
    var s = $(this).val();
    if (s.length > 10) {
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
            $('#event-type').removeClass('gray').html("Meeting");
            $('#duration input[type="number"]').removeAttr('disabled');
          } else {
            $('#event-type').removeClass('gray').html("Follow-Up");
            $('#duration input[type="number"]').attr('disabled', 'disabled');
          }
          $('#event-date').removeClass('gray').html(html);
        }
      });
    }
  });

  // Duration.
  fixMinutesDisplay();
});

$('#duration input[type="number"]').last().on('change', function() {
  fixMinutesDisplay();
});

// Offer to take a tour.
if (offerTour) {
  var modal = $('#offer-tour-modal');

  modal.dialog({
    autoOpen: true,
    modal: true,
    resizable: false,
    closeOnEscape: true,
    width: 340,
    draggable: false,
    title: "Take a Tour",
    buttons: {
      Yes: function() {
        $(this).dialog('close');
        startTour();
        $('.input-event').val('Meet Sam tomorrow at 3pm').trigger('keypress');
      },
      No: function() {
        $(this).dialog('close');
      }
    }
  });
}
