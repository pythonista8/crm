$(function() {
  // Calendar.
  $('.calendar').datepicker({
    dateFormat: 'dd-mm-yy',
    beforeShow: function(input, inst) {
      setCalendarEvents();
    },
    onSelect: function(dateText, inst) {
      window.open(eventsURI + '?filter=' + dateText, '_self');
    }
  });
  $('.datepicker').datepicker();
});

$(function() {
  // Offer to take a tour.
  if (takeTour) {
    if (!isManualTour) {
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
          },
          No: function() {
            $(this).dialog('close');
          }
        }
      });
    } else {
      // Tour triggered by user manually.
      startTour();
    }
  }
});
