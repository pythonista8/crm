"""Functions to fetch parsed data from yellowpages.com.my."""
import time
import urllib

from random import randint
from lib.parser.utils import istag, cleanstr, connect

DOMAIN = 'http://www.yellowpages.com.my'

CATEGORIES = (
    'Packaging Materials',
    'Secretarial Services',
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
                            data['phone'] = phone
                        else:
                            # Get city.
                            for city in CITIES:
                                if city.lower() in s.lower():
                                    data['city'] = city
    if 'name' in data and 'phone' in data and 'city' in data:
        return data
    return None


def fetch(category=None, limit=10):
    """Entry point for fetching company list."""
    def _parse(category, delay=False):
        """Parse data for category. Use recursive call when the page
        isn't available or we haven't receive enough data.
        """
        if delay:
            time.sleep(10)  # in order to avoid ban

        catslug = category.lower().replace(' ', '-')
        url_pattern = '{domain}/category/{category}/?p={page}'
        url = url_pattern.format(domain=DOMAIN, category=catslug,
                                 page=randint(1, 10))
        try:
            soup = connect(url)
        except urllib.error.HTTPError:
            _parse(category, delay=True)

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
                        data.update(dict(industry=category,
                                         country='Malaysia'))
                        list_.append(data)
        else:
            # Probably we got banned.
            return []
        # Continue searching for records if we haven't got enough.
        if len(list_) < limit:
            _parse(category, delay=True)
        return list_

    if category is not None:
        return _parse(category)
    else:
        res = list()
        for c in CATEGORIES:
            res.extend(_parse(c, delay=True))
        return res[:limit]
