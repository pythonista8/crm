"""Functions to fetch parsed data from LinkedIn."""
import string
import urllib

from random import randint
from lib.parser.utils import istag, cleanstr, connect


def _fetch_details(url):
    """Fetch and parse person's details. User profile's URL must be
    provided.
    """
    soup = connect(url)
    data = dict()
    # Get full name.
    data['first_name'] = cleanstr(soup.find(class_='given-name').string)
    data['last_name'] = cleanstr(soup.find(class_='family-name').string)
    title_tag = soup.find(class_='headline-title')
    if title_tag is not None:
        list_ = title_tag.string.split(' at ')
        # Get company name.
        if len(list_) == 2:
            data['company'] = cleanstr(list_[1])
        # Get position.
        position = cleanstr(list_[0])
        if position != '--':
            data['position'] = position
    # Get location.
    location_tag = soup.find(class_='locality')
    if location_tag is not None:
        location_list = location_tag.string.split(',')
        if len(location_list) == 2:
            data['city'] = cleanstr(location_list[0])
        data['country'] = cleanstr(location_list[-1])
    # Get industry.
    industry = soup.find(class_='industry')
    if industry is not None:
        data['industry'] = cleanstr(industry.string)
    return data


def fetch(country_code, industry=None, limit=5):
    """Entry point for fetching contact list."""
    domain = 'http://{country}.linkedin.com'.format(country=country_code)
    url_pattern = '{domain}/directory/people-{letter}-{cat_1}-{cat_2}'
    contact_list = list()
    for letter in string.ascii_lowercase:
        # We generate random URL.
        url = url_pattern.format(domain=domain,
                                 letter=letter,
                                 cat_1=randint(1, 100),
                                 cat_2=randint(1, 100))
        try:
            soup = connect(url)
        except urllib.error.HTTPError:
            continue  # go to the next page if we got 404

        ul = soup.find('ul', class_='directory')
        if ul is not None:
            for li in ul.children:
                if len(contact_list) == limit:
                    break
                if istag(li):
                    link = li.a['href']
                    profile_url = '{domain}{link}'.format(
                        domain=domain, link=link)
                    try:
                        data = _fetch_details(profile_url)
                    except urllib.error.HTTPError:
                        continue
                    else:
                        if not 'company' in data:  # must be provided
                            continue
                        contact_list.append(data)
    return contact_list
