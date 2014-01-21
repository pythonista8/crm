"""Context processors for Accounts app."""


def users(request):
    ctx = dict()
    # Trial user?
    ctx['TRIAL'] = True if request.user.is_trial else False
    # Head of Department?
    ctx['IS_HEAD'] = True if request.user.is_head else False
    return ctx
