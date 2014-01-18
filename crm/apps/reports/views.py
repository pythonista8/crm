import calendar
import datetime as dt

from django.db.models import Sum
from django.shortcuts import render
from lib.date import LONG_MONTH_NAMES
from apps.customers.models import Customer, Amount


def index(request):
    ctx = dict()

    customers = Customer.objects.filter(user=request.user)
    oppdict = dict(color='#e0e4cb', label='Opportunities')
    windict = dict(color='#64d2e9', label='Closed-Win')
    lostdict = dict(color='#fa4444', label='Closed-Lost')

    # Total Number of Cases.
    opp = customers.filter(amounts__status=Amount.OPPORTUNITY)
    opp_number = oppdict.copy()
    opp_number['value'] = opp.count()

    win = customers.filter(amounts__status=Amount.WIN)
    win_number = windict.copy()
    win_number['value'] = win.count()

    lost = customers.filter(amounts__status=Amount.LOST)
    lost_number = lostdict.copy()
    lost_number['value'] = lost.count()

    if opp.count() or win.count() or lost.count():
        ctx['data_number'] = [opp_number, win_number, lost_number]

    # Total Income.
    opp_sum = opp.aggregate(
        Sum('amounts__value'))['amounts__value__sum'] or 0
    opp_amount = oppdict.copy()
    opp_amount['value'] = opp_sum

    win_sum = win.aggregate(
        Sum('amounts__value'))['amounts__value__sum'] or 0
    win_amount = windict.copy()
    win_amount['value'] = win_sum

    lost_sum = lost.aggregate(
        Sum('amounts__value'))['amounts__value__sum'] or 0
    lost_amount = lostdict.copy()
    lost_amount['value'] = lost_sum

    if opp_sum or win_sum or lost_sum:
        ctx['data_amount'] = [opp_amount, win_amount, lost_amount]

    ctx['monthly_win_trend'] = get_monthly_trend(Amount.WIN)
    ctx['monthly_lost_trend'] = get_monthly_trend(Amount.LOST)

    ctx['long_month_names'] = LONG_MONTH_NAMES
    ctx['title'] = "Reports"
    ctx['title_icon'] = 'bar-chart-o'
    return render(request, 'reports/index.html', ctx)


def get_monthly_trend(status):
    """Return list of values that determine percentage of sales
    trend between two month.
    """
    def _get_month_sales(month, status):
        """If `month` equals to zero, then treat as a previous month."""
        now = dt.datetime.now()
        if month == 0:
            yr = now.year - 1
            month = 12
        else:
            yr = now.year
        days = calendar.monthrange(yr, month)[1]
        begin = dt.datetime(yr, month, 1)
        end = begin + dt.timedelta(days=days - 1)
        qs = Amount.objects.filter(status=status, date__range=(begin, end))
        sum_ = qs.aggregate(Sum('value'))['value__sum'] or 0
        return sum_

    data = list()
    base = _get_month_sales(0, status)
    for month in range(1, 13):
        if base == 0:
            base = _get_month_sales(month, status)
        sales = _get_month_sales(month, status)
        try:
            diff = round(abs(sales - base) / base*100)
        except ZeroDivisionError:
            diff = 0
        data.append(diff)
    return data
