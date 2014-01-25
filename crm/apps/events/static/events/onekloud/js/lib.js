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
    //doneLabel: 'Next page',
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

  tour.start();
}
