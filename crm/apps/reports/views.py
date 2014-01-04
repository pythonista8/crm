from django.db.models import Sum
from django.shortcuts import render
from apps.customers.models import Customer


def index(request):
    customers = Customer.objects.all()
    opp = customers.filter(status=Customer.OPPORTUNITY)
    oppdict = dict(color='#e0e4cb', label='Opportunities', value=opp.count())
    win = customers.filter(status=Customer.WIN)
    windict = dict(color='#64d2e9', label='Closed Win', value=win.count())
    lost = customers.filter(status=Customer.LOST)
    lostdict = dict(color='#fa4444', label='Closed Lost', value=opp.count())
    ctx = dict(data_number=[oppdict, windict, lostdict])

    opp_sum = opp.aggregate(Sum('amount'))['amount__sum'] or 0
    oppdict['value'] = opp_sum
    win_sum = win.aggregate(Sum('amount'))['amount__sum'] or 0
    windict['value'] = win_sum
    lost_sum = lost.aggregate(Sum('amount'))['amount__sum'] or 0
    lostdict['value'] = lost_sum
    ctx['data_amount'] = [oppdict, windict, lostdict]
    ctx['title'] = "Reports"
    ctx['title_icon'] = 'bar-chart-o'
    return render(request, 'reports/index.html', ctx)
