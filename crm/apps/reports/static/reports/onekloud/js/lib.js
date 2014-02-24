// Take Tour.
function startTour() {
  var tour = introJs();

  tour.setOptions({
    showBullets: false,
    showStepNumbers: false,
    steps: [
      {
        element: '#step-1',
        intro: "This chart shows the total number of deals.",
        position: 'right'
      },
      {
        element: '#step-2',
        intro: "This chart shows how much income have you received.",
        position: 'left'
      }
    ]
  });

  tour.start();
}
