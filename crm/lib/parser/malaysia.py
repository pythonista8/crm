"""Functions to fetch parsed data from yellowpages.com.my."""
import re
import urllib

from random import randint
from lib.parser.utils import istag, cleanstr, connect

DOMAIN = 'http://www.yellowpages.com.my'

CATEGORIES = (
    'Packaging Materials',
)

CITIES = (
    'Kuala Lumpur',
    'Shah Alam',
    'Petaling Jaya',
    'Subang Jaya',
    'Pulau Pinang',
    'Johor Bahru',
    'Pasir Gudang',
    'Kajang',
    'Cheras',
    'Ampang',
    'Klang',
    'Ipoh',
    'Batu Gajah',
    'Selayang',
    'Rawang',
    'Kuching',
    'Seremban',
    'Georgetown',
    'Malacca',
    'Kota Bahru',
    'Kota Kinabalu',
    'Kuantan',
    'Sungai Petani',
    'Batu Pahat',
    'Tawau',
    'Sandakan',
    'Bukit Mertajam',
    'Alor Setar',
    'Kuala Terengganu',
    'Taiping',
    'Miri',
    'Kluang',
    'Butterworth',
    'Kulim',
    'Kulai',
    'Sibu',
    'Muar',
    'Sitiawan',
    'Kangar',
    'Banting',
    'Jitra',
    'Sepang',
    'Kuala Selangor',
    'Teluk Intan',
    'Lahad Datu',
    'Bayan Lepas',
    'Kuala Kubu Bharu',
    'Kota Tinggi',
    'Segamat',
    'Pasir Mas',
    'Bintulu',
    'Alor Gajah',
    'Parit Buntar',
    'Tanjung Malim',
    'Tapah',
    'Keningau',
    'Chukai',
    'Nibong Tebal',
    'Sungai Jawi',
    'Temerioh',
)


def _fetch_details(url):
    """Fetch and parse company's details."""
    soup = connect(url)
    data = dict()
    # Get company name.
    cont = soup.find(id='result')
    data['name'] = cleanstr(cont.find('h2').string)
    # Get address.
    row = cont.find('table').find_all('tr')[1]
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
                end = s.find('Fax') or len(s)
                phone = ''
                for d in cleanstr(s[5:end]):
                    if d.isdigit():
                        phone += d
                data['phone'] = phone
            else:
                for city in CITIES:
                    if city.lower() in s.lower():
                        data['city'] = city
    # Get industry.
    # industry = soup.find(class_='industry')
    # if industry is not None:
    #     data['industry'] = cleanstr(industry.string)
    return data


def fetch(industry, limit=5):
    """Entry point for fetching company list."""
    url_pattern = '{domain}/category/{category}/?p={page}'
    list_ = list()
    for cat in CATEGORIES:
        # We generate random URL.
        catslug = cat.lower().replace(' ', '-')
        url = url_pattern.format(domain=DOMAIN, category=catslug,
                                 page=randint(1, 10))
        try:
            soup = connect(url)
        except urllib.error.HTTPError:
            continue  # go to the next page if we got 404

        ul = soup.find(id='result')
        if ul is not None:
            for li in ul.find_all(class_='listing'):
                if len(list_) == limit:
                    break
                if istag(li):
                    link = li.find(class_='nameFL').a['href']
                    profile_url = '{domain}{link}'.format(
                        domain=DOMAIN, link=link)
                    try:
                        data = _fetch_details(profile_url)
                    except urllib.error.HTTPError:
                        continue
                    else:
                        if 'phone' not in data:  # must be provided
                            continue
                        list_.append(data)
    return list_
