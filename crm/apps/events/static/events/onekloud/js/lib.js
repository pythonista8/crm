// Display minutes as two digit value.
function fixMinutesDisplay() {
  var minsInput = $('.duration input[type="number"]').last();
  var minsInputVal = minsInput.val();
  if (minsInputVal.length == 1) minsInput.val('0' + minsInputVal);
}
