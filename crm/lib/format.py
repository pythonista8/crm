
def format_phone(string):
    """Return nicely formatted phone number. If invalid characters 
    are found, omit them."""
    res = ''
    for i in list(string):
        if i.isdigit() or i.lower() == 'x':
            res += i
    if res.startswith('0'):
        if res.startswith('00'):
            res = res[2:]
        else:
            res = res[1:]
    return res
