import datetime as dt

from django.db.models import Sum
from django.shortcuts import render
from lib.date import LONG_MONTH_NAMES
from apps.customers.models import Customer, Amount


def index(request):
    ctx = dict()

    customers = Customer.objects.all()
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

    ctx['monthly_trend'] = get_monthly_trend()
    ctx['long_month_names'] = LONG_MONTH_NAMES
    ctx['title'] = "Reports"
    ctx['title_icon'] = 'bar-chart-o'
    return render(request, 'reports/index.html', ctx)


def get_monthly_trend():
    """Monthly Trend for Sales."""
    def _get_month_sales(month):
        now = dt.datetime.now()
        base = now - dt.timedelta(days=30*month)
        d = now - dt.timedelta(days=30*(month - 1))
        qs = Amount.objects.filter(date__range=(base, d))
        sum_ = qs.aggregate(Sum('value'))['value__sum'] or 0
        return sum_

    data = list()
    # basemonth = None
    # from_ = None
    # for month in range(1, 7):
    #     if month:
    #         basemonth = _get_month_sales(month)
    #         from_ = month
    # if basemonth is not None and from_ is not None:
    #     for month in range(from_, 7):
    #         mon = _get_month_sales(month)
    #         print(mon, basemonth)
    #         data.append((mon - basemonth)/basemonth)
    return data
