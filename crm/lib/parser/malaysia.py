"""Functions to fetch parsed data from yellowpages.com.my."""
import time
import urllib

from random import randint
from django.utils.text import slugify
from lib.parser.constants import INDUSTRIES, CITIES
from lib.parser.utils import istag, cleanstr, connect

DOMAIN = 'http://www.yellowpages.com.my'


def _fetch_details(url):
    """Fetch and parse company's details."""
    print("Connecting to {}".format(url))
    soup = connect(url)
    data = dict()
    # Get company name.
    cont = soup.find(id='result')
    if cont is not None:
        name_tag = cont.find('h2')
        if name_tag is not None:
            data['name'] = cleanstr(cont.find('h2').string)
        table = cont.find('table')
        if table is not None:
            rows = table.find_all('tr')
            if len(rows) > 1:
                row = rows[1]
                for col in row.children:
                    if istag(col):
                        s = str()
                        for el in col.contents:
                            if el.string is not None:
                                if istag(el):
                                    s += cleanstr(el.string)
                                else:
                                    s += cleanstr(el)
                        if 'Tel:' in s:
                            # Get phone number.
                            phone = ''
                            for d in s[5:17]:
                                if d.isdigit():
                                    phone += d
                            if len(phone) == 10:
                                data['phone'] = phone
                        else:
                            # Get city.
                            for city in CITIES:
                                if city.lower() in s.lower():
                                    data['city'] = city
    print("Result: {}".format(data))
    if 'name' in data and 'phone' in data and 'city' in data:
        return data
    return


def fetch(industry=None, limit=5):
    """Entry point for fetching company list."""

    def _parse(industry, delay=False, attempts=10):
        """Parse data for industry. Use recursive call when the page
        isn't available or we haven't receive enough data.
        """
        if not attempts:
            # Exceeded attempts, exiting recursion.
            return

        if delay:
            # In order to avoid ban.
            time.sleep(10)

        slug = slugify(industry)
        url_pattern = '{domain}/category/{category}/?p={page}'
        url = url_pattern.format(domain=DOMAIN, category=slug,
                                 page=randint(1, 10))
        try:
            soup = connect(url)
        except urllib.error.HTTPError:
            _parse(industry, True, attempts-1)

        list_ = list()
        ul = soup.find(id='result')
        if ul is not None:
            for li in ul.find_all(class_='listing'):
                if len(list_) == limit:
                    break
                if istag(li):
                    link = li.find('a')['href']
                    profile_url = '{domain}{link}'.format(
                        domain=DOMAIN, link=link)
                    try:
                        data = _fetch_details(profile_url)
                    except urllib.error.HTTPError:
                        continue
                    else:
                        if data is None:  # incomplete information
                            continue
                        data.update(dict(industry=industry,
                                         country='Malaysia'))
                        list_.append(data)
        else:
            # Probably we got banned.
            return []
        # Continue searching for records if we haven't got enough.
        if len(list_) < limit:
            _parse(industry, True, attempts-1)
        return list_

    if industry is not None:
        res = _parse(industry)
    else:
        res = list()
        for key, list_ in INDUSTRIES.items():
            for v in list_:
                if len(res) == limit:
                    break
                res.extend(_parse(v, True))
    return res
