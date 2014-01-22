"""Context processors for Accounts app."""


def users(request):
    ctx = dict(TRIAL=False, IS_HEAD=False)
    user = request.user
    if user.is_authenticated():
        if user.is_trial:
            ctx['TRIAL'] = True  # Trial user
        if user.is_head:
            ctx['IS_HEAD'] = True  # Head of Department
    return ctx
