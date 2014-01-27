"""Context processors for all apps."""


def tour(request):
    ctx = dict(take_tour=False, manual_tour=False)
    in_session = request.session.pop('take_tour', False)
    if request.method == 'GET' and (in_session or 'tour' in request.GET):
        ctx['take_tour'] = True
        if 'manual' in request.GET:
            ctx['manual_tour'] = True
    return ctx
