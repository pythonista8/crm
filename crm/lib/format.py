"""Functions to work with stings."""


def format_phone(string):
    """Return nicely formatted phone number. If invalid characters
    are found, omit them."""
    res = ''
    for i in list(string):
        if i.isdigit() or i.lower() == 'x':
            res += i
    return res
