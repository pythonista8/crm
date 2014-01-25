"""Context processors for Accounts app."""


def users(request):
    ctx = dict()
    user = request.user
    if user.is_authenticated():
        # Trial user
        ctx['IS_TRIAL'] = True if user.is_trial else False
        # Head of Department
        ctx['IS_HEAD'] = True if user.is_head else False
    return ctx
