import datetime as dt

from django import test
from lib import date


class DateTestCase(test.TestCase):
    def test_parsedate(self):
        def _assertdate(string, hr, day, mon, min_=None, yr=None):
            res = date.parsedate(string)
            hrs = '0' + str(hr) if hr < 10 else str(hr)
            self.assertEqual(res['hours'], hrs)
            days = '0' + str(day) if day < 10 else str(day)
            self.assertEqual(res['day'], days)
            mons = '0' + str(mon) if mon < 10 else str(mon)
            self.assertEqual(res['month'], mons)
            if min_ is not None:
                mins = '0' + str(min_) if min_ < 10 else str(min_)
                self.assertEqual(res['minutes'], mins)
            if yr is not None:
                self.assertEqual(res['year'], str(yr))

        today = dt.date.today()
        _assertdate("Coffee at 15.30 @12 Aug", 15, 12, 8, 30, today.year + 1)
        _assertdate("Coffee at 3pm @10 Aug", 15, 10, 8, 0, today.year + 1)
        _assertdate("Meet Jay at 31/12/17 at 8am", 8, 31, 12, 0, 2017)
        _assertdate("Meet Jay at 3/5/17 at 4pm", 16, 3, 5, 0, 2017)
        _assertdate("Meet Jay at 1th December at 3am", 3, 1, 12, 0, today.year)
        _assertdate("Afternoon 1.30 @ 5 Jan 2014 @ No 6", 13, 5, 1, 30, 2014)
        _assertdate("Evening 12.30 @ 5 Jan 2014 @ No 6", 0, 5, 1, 30, 2014)
        _assertdate("Noon 2 @ 1st Jan @ No 8", 14, 1, 1)
        _assertdate("Noon 3 @ 2nd Jan @ No 8", 15, 2, 1)
        _assertdate("Noon 4 @ 3rd Jan @ No 8", 16, 3, 1)
        _assertdate("Meet Jay at 18.20 on July 7th 2014", 18, 7, 7, 20, 2014)
