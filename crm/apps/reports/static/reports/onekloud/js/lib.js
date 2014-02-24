// Take Tour.
function startTour() {
  var tour = introJs();

  tour.setOptions({
    showBullets: false,
    showStepNumbers: false,
    steps: [
      {
        element: '#step-1',
        intro: "Chart shows the total number of deals.",
        position: 'right'
      },
      {
        element: '#step-2',
        intro: "Chart shows how much income have you received.",
        position: 'left'
      },
      {
        element: '#step-3',
        intro: "Chart shows sales trend data and the comparison between \
                Closed-Win and Closed-Lost.",
        position: 'top'
      },
      {
        element: '#step-4',
        intro: "You may easily download your data in a CSV format.",
        position: 'top'
      }
    ]
  });

  tour.start();
}
