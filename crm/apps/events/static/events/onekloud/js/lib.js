// Add `beforeShow` option to jQuery Datepicker.
(function ($) {
  $.extend($.datepicker, {
    // Reference the orignal function so we can override it and call it
    // later.
    _inlineDatepicker2: $.datepicker._inlineDatepicker,

    // Override the _inlineDatepicker method.
    _inlineDatepicker: function(target, inst) {

      // Call the original method.
      this._inlineDatepicker2(target, inst);

      var beforeShow = $.datepicker._get(inst, 'beforeShow');

      if (beforeShow) {
        beforeShow.apply(target, [target, inst]);
      }
    }
  });
}(jQuery));

function setCalendarEvents() {
  $.get(eventsDatesURI, function(resp) {
    if (resp.status == 'success') {
      for (var i = 0; i < resp.data.length; i++) {
        var date = resp.data[i].split('-');

        var day = date[0];
        if (day[0] == '0') day = day[1];

        var mon = date[1] - 1;
        var yr = date[2];

        // We find elements that match date criteria.
        var elems = $('.calendar').find('[data-month='+mon+'][data-year='+yr+'] a');

        $.each(elems, function() {
          if ($(this).html() == day) $(this).addClass('has-events');
        });
      }
    }
  });
}

// Display minutes as two digit value.
function fixMinutesDisplay() {
  var minsInput = $('#duration input[type="number"]').last();
  if (minsInput.length) {
    var minsInputVal = minsInput.val();
    if (minsInputVal.length == 1) minsInput.val('0' + minsInputVal);
  }
}

// Take Tour.
function startTour() {
  var tour = introJs();

  tour.setOptions({
    showBullets: false,
    showStepNumbers: false,
    doneLabel: 'Continue',
    steps: [
      {
        element: '#step-1',
        intro: "Create new meetings or follow-ups. Meetings have exact date \
                and time, while follow-ups only have date.",
        position: 'bottom'
      },
      {
        element: '#step-2',
        intro: "Add new meeting or follow-up. Example: Call Bill today, or \
                Meet Sam tomorrow at 3pm.",
        position: 'right'
      },
      {
        element: '#step-3',
        intro: "This is what you get.",
        position: 'right'
      },
      {
        element: '#step-4',
        intro: "Browse events by clicking on dates.",
        position: 'left'
      },
      {
        element: '#step-5',
        intro: "Here you will see all events on selected date.",
        position: 'top'
      }
    ]
  });

  // Go to the next page.
  tour.oncomplete(function() {
    window.location.href = customersListURI + '?tour';
  });

  tour.start();
}

function fillWithSampleData() {
  $('.input-event').val('Meet Sam tomorrow at 3pm').trigger('keypress');
}
