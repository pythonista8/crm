import csv
import calendar
import datetime as dt

from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.shortcuts import render, redirect
from lib.date import LONG_MONTH_NAMES
from apps.customers.models import Customer, Amount


def index(request):
    ctx = dict()
    user = request.user
    customers = Customer.objects.filter(user=user)

    # TODO: Move to separate function.
    oppdict = dict(color='#ffb553', label='Opportunities')
    windict = dict(color='#3ebfbe', label='Closed-Win')
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

    # Total Amount.
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

    # Monthly Sales Trend.
    ctx['monthly_win_trend'] = _get_monthly_trend(user, Amount.WIN)
    ctx['monthly_lost_trend'] = _get_monthly_trend(user, Amount.LOST)

    # Monthly statistics.
    ctx['monthly_opportunities'] = _get_avg_stats(user, Amount.OPPORTUNITY)
    ctx['monthly_win'] = _get_avg_stats(user, Amount.WIN)
    ctx['monthly_lost'] = _get_avg_stats(user, Amount.LOST)

    # For CSV download buttons - whether to show them or not.
    if customers.exists():
        ctx['customers_exist'] = True
    if Amount.objects.filter(customer__user=user).exists():
        ctx['amounts_exist'] = True

    ctx['long_month_names'] = LONG_MONTH_NAMES
    ctx['title'] = "Reports"
    ctx['title_icon'] = 'bar-chart-o'
    return render(request, 'reports/index.html', ctx)


def _get_monthly_trend(user, status):
    """Return list of values that determine percentage of sales
    trend between two month.
    """
    now = dt.datetime.now()

    def _get_month_sales(month, status):
        # If `month` equals to zero, then treat as a previous month.
        if month == 0:
            yr = now.year - 1
            month = 12
        else:
            yr = now.year
        days = calendar.monthrange(yr, month)[1]
        begin = dt.datetime(yr, month, 1)
        end = begin + dt.timedelta(days=days - 1)
        qs = Amount.objects.filter(customer__user=user, status=status,
                                   date__range=(begin, end))
        sum_ = qs.aggregate(Sum('value'))['value__sum'] or 0
        return sum_

    data = list()
    base = _get_month_sales(0, status)
    for month in range(1, 13):
        if now.month >= month:
            if base == 0:
                base = _get_month_sales(month, status)
            sales = _get_month_sales(month, status)
            try:
                diff = round(abs(sales - base) / base*100)
            except ZeroDivisionError:
                diff = 0
        else:
            diff = 0
        data.append(diff)
    return data


def _get_avg_stats(user, status):
    """Return list of monthly amount values."""
    qs = Amount.objects.filter(customer__user=user, status=status)
    dict_ = dict()
    # Prepare data for convenience.
    for amount in qs:
        mon = amount.date.month
        sum_ = qs.aggregate(Sum('value'))['value__sum'] or 0
        if mon in dict_:
            dict_[mon].append(sum_)
        else:
            dict_[mon] = [sum_]
    return [v for k, v in dict_.items()]


ERROR_MSG = "Sorry, you can't download reports in Trial version."


def export_customers(request):
    """Export customers data in a CSV format."""
    user = request.user
    if user.is_trial:
        messages.error(request, ERROR_MSG)
        return redirect(reverse('reports:index'))

    # Create the HttpResponse object with the appropriate CSV header.
    fname = "{model}_{user}_{date}.csv".format(
        model=Customer._meta.verbose_name_plural, user=user,
        date=dt.date.today())
    resp = http.HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="{file}"'.format(
        file=fname)

    writer = csv.writer(resp)
    headers = ['ID',
               'Created',
               'Salutation',
               'First name',
               'Last name',
               'Position',
               'Company',
               'Cell phone',
               'Main phone',
               'Email',
               'Skype',
               'Address',
               'City',
               'State',
               'Country',
               'Website',
               'Facebook',
               'Twitter',
               'LinkedIn',
               'Notes']

    writer.writerow(headers)
    qs = Customer.objects.filter(user=user)
    for ob in qs:
        address = "{street} {postcode}".format(street=ob.street,
                                               postcode=ob.postcode or '')
        row = [ob.id,
               ob.date_created.strftime('%d/%m/%Y'),
               ob.get_salutation_display(),
               ob.first_name,
               ob.last_name,
               ob.position,
               ob.company,
               "'{}'".format(ob.cell_phone) if ob.cell_phone else '',
               "'{}'".format(ob.main_phone) if ob.main_phone else '',
               ob.email,
               ob.skype,
               address,
               ob.city,
               ob.state,
               ob.country,
               ob.website,
               ob.facebook,
               ob.twitter,
               ob.linkedin,
               ob.notes]
        writer.writerow(row)
    return resp


def export_amounts(request):
    """Export amounts data in a CSV format."""
    user = request.user
    if user.is_trial:
        messages.error(request, ERROR_MSG)
        return redirect(reverse('reports:index'))

    fname = "{model}_{user}_{date}.csv".format(
        model=Amount._meta.verbose_name_plural, user=user,
        date=dt.date.today())
    resp = http.HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="{file}"'.format(
        file=fname)

    writer = csv.writer(resp)
    headers = ['Date',
               'Customer ID',
               'First name',
               'Last name',
               'Amount',
               'Product',
               'Status']

    writer.writerow(headers)
    qs = Amount.objects.filter(customer__user=user)
    for ob in qs:
        row = [ob.date.strftime('%d/%m/%Y'),
               ob.customer.id,
               ob.customer.first_name,
               ob.customer.last_name,
               ob.value,
               ob.product,
               ob.get_status_display()]
        writer.writerow(row)
    return resp
