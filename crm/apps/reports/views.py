from django.db.models import Sum
from django.shortcuts import render
from apps.customers.models import Customer


def index(request):
    ctx = dict()
    customers = Customer.objects.all()
    oppdict = dict(color='#e0e4cb', label='Opportunities')
    windict = dict(color='#64d2e9', label='Closed Win')
    lostdict = dict(color='#fa4444', label='Closed Lost')

    opp = customers.filter(status=Customer.OPPORTUNITY)
    opp_number = oppdict.copy()
    opp_number['value'] = opp.count()
    win = customers.filter(status=Customer.WIN)
    win_number = windict.copy()
    win_number['value'] = win.count()
    lost = customers.filter(status=Customer.LOST)
    lost_number = lostdict.copy()
    lost_number['value'] = lost.count()
    if opp.count() or win.count() or lost.count():
        ctx['data_number'] = [opp_number, win_number, lost_number]

    opp_sum = opp.aggregate(Sum('amount'))['amount__sum'] or 0
    opp_amount = oppdict.copy()
    opp_amount['value'] = opp_sum
    win_sum = win.aggregate(Sum('amount'))['amount__sum'] or 0
    win_amount = windict.copy()
    win_amount['value'] = win_sum
    lost_sum = lost.aggregate(Sum('amount'))['amount__sum'] or 0
    lost_amount = lostdict.copy()
    lost_amount['value'] = lost_sum
    if opp_sum or win_sum or lost_sum:
        ctx['data_amount'] = [opp_amount, win_amount, lost_amount]

    ctx['title'] = "Reports"
    ctx['title_icon'] = 'bar-chart-o'
    return render(request, 'reports/index.html', ctx)
