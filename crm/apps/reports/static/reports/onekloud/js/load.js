var options = {
  // Boolean - Whether we should show a stroke on each segment.
  segmentShowStroke : true,

  // String - The colour of each segment stroke.
  segmentStrokeColor : '#fff',

  // Number - The width of each segment stroke.
  segmentStrokeWidth : 2,

  // The percentage of the chart that we cut out of the middle.
  percentageInnerCutout : 50,

  // Boolean - Whether we should animate the chart.
  animation : true,

  // Number - Amount of animation steps.
  animationSteps : 25,

  // String - Animation easing effect.
  animationEasing : 'easeOutQuad',

  // Boolean - Whether we animate the rotation of the Doughnut.
  animateRotate : true,

  // Boolean - Whether we animate scaling the Doughnut from the centre.
  animateScale : true,

  // Function - Will fire on animation completion.
  onAnimationComplete : null
}

var ctxNumber = $('#chart-number').get(0).getContext('2d');
new Chart(ctxNumber).Pie(dataNumber, options);

var ctxAmount = $('#chart-amount').get(0).getContext('2d');
new Chart(ctxAmount).Pie(dataAmount, options);
