"""Utility functions to fetch and parse data from URL."""
import urllib

from bs4 import BeautifulSoup as Soup
from bs4.element import Tag


def istag(el):
    """Check whether an element is instance of Tag class. This is used
    to differentiate from NavigableString class."""
    if isinstance(el, Tag):
        return True
    return False


def cleanstr(s):
    """Capitalize and remove whitespace from a string."""
    return s.replace('\n', '').strip().capitalize()


def connect(url):
    """Connect to URL and return BeautifulSoup instance."""
    headers = {'User-agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return Soup(resp)
