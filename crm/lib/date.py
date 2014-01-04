import re
import datetime

LONG_MONTH_NAMES = ("January", "February", "March",
                    "April", "May", "June", "July",
                    "August", "September", "October",
                    "November", "December")

SHORT_MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr",
                     "May", "Jun", "Jul", "Aug",
                     "Sep", "Oct", "Nov", "Dec")


def parsedate(string, month_as_str=False):
    """Get date and time (if exists) from passed string and return a
    dict of strings.

    Convenient for futher conversion to DateTime or Date object using
    `strptime`. If a string does not contain date, function will return
    an empty dict.

    Set `month_as_str` to get month value as a long month name, e.g.
    September.
    """
    today = datetime.date.today()
    cyr = today.year

    def _year(s):
        if len(s) == 2:
            cyrs = str(cyr)
            if s == cyrs[2:]:
                yr = cyrs[:2] + s
            else:
                yr = '20' + s
        else:
            return s
        return yr

    def _monthval(s):
        # Check whether string contains short month name or long one,
        # i.e. `Dec` or `December`. If not in both, treat month as a
        # number. Returns zero padded decimal number: 01, 02, ..., 12.
        try:
            int(s)
        except ValueError:
            s = s.capitalize()
            if s in SHORT_MONTH_NAMES:
                mon = SHORT_MONTH_NAMES.index(s) + 1
            elif s in LONG_MONTH_NAMES:
                mon = SHORT_MONTH_NAMES.index(s[:3]) + 1
        else:
            if int(s) in range(13):
                mon = int(s)
            else:
                raise ValueError("Month value not in range")
        mons = str(mon)
        if mon < 10:
            mons = '0' + mons
        return mons

    res = dict()
    s = string
    lower = s.lower()

    if "today" in lower:
        res['day'] = today.day
        res['month'] = today.month
        res['year'] = today.year
    elif "tomorrow" in lower:
        tmr = today + datetime.timedelta(days=1)
        res['day'] = tmr.day
        res['month'] = tmr.month
        res['year'] = tmr.year
    else:
        # I.e. 19-12-2013
        date = re.search(r'(?P<day>\d{1,2})[\.\-/ ](?P<month>\d{1,2})[\.\-/ ]'
                         r'(?P<year>(\d{2})(\d{2})?)', s, re.IGNORECASE)
        if not date:
            monnames = '|'.join(LONG_MONTH_NAMES + SHORT_MONTH_NAMES)
            # I.e. 15 Dec 2014
            date = re.search(
                r'(?P<day>\d{1,2})(th|st|nd|rd)?[\.\-/ ](?P<month>(%s))'
                r'([\.\-/ ](?P<year>(\d{2})(\d{2})?))?' % monnames, s,
                re.IGNORECASE)
            if not date:
                # I.e. Dec 8 2014
                date = re.search(
                    r'(?P<month>(%s))[\.\-/ ](?P<day>\d{1,2})(th|st|nd|rd)?'
                    r'([\.\-/ ](?P<year>(\d{2})(\d{2})?))?' % monnames, s,
                    re.IGNORECASE)
        if date:
            day = date.group('day')
            if day:
                res['day'] = str(int(day))
                if int(day) < 10:
                    res['day'] = '0' + res['day']
            else:
                raise ValueError("Cannot parse day value")

            mon = date.group('month')
            if mon:
                res['month'] = _monthval(mon)
            else:
                raise ValueError("Cannot parse month value")

            yr = date.group('year')
            if yr:
                res['year'] = _year(date.group('year'))
            else:
                cmon = today.month
                cday = today.day
                day = int(res['day'])
                mon = int(res['month'])
                if cmon <= mon and cday >= day:
                    res['year'] = str(cyr)
                else:
                    res['year'] = str(cyr + 1)

            # Avoid possible further parsing errors by removing date.
            s = string.replace(date.group(), '')
        else:
            raise ValueError("Could not parse date")
    if month_as_str:
        res['month'] = LONG_MONTH_NAMES[int(res['month'])-1]

    time = re.search(
        r'(?P<hours>\d{1,2})'
        r'([:\-\.](?P<minutes>\d{2}))?[\- ]*(?P<period>(AM|PM))?', s,
        re.IGNORECASE)
    if time:
        hr = time.group('hours')
        pr = time.group('period')
        if hr and int(hr) in range(25):
            h = int(hr)
            if (h <= 12 and (pr is not None and pr.lower() == "pm") or
                    'noon' in lower or 'evening' in lower):
                h += 12
            if h == 24:
                h = 0
            res['hours'] = str(h)
            if h < 10:
                res['hours'] = '0' + str(h)
        min_ = time.group('minutes')
        if min_ and int(min_) in range(61):
            res['minutes'] = str(int(min_))
            if int(min_) < 10:
                res['minutes'] = '0' + res['minutes']
        else:
            res['minutes'] = '00'
    return res
