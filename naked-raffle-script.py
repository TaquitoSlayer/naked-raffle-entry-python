import requests
import json
import re
import bs4 as bs
import time
import calendar
from itertools import cycle
import traceback


"""

WHERE WERE YOU WHEN FUNKOFUCKED TOOK STOCK
https://twitter.com/FunkoFucked
https://twitter.com/FunkoFucked
https://twitter.com/FunkoFucked

"""

file_proxies = '/Users/OverpricedFruit/Desktop/proxies.txt' # direct file path
catchall = ''
country = 'Canada' # straight outta YEG
i = 50 # number of entries
password = 'naked12!'
r = requests.session()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
}

json_headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
}

def read_proxies(file_path):
    with open(file_path) as txt_file:
        proxies = txt_file.read().splitlines()
    return proxies

proxies = read_proxies(file_proxies)
proxy_swm = cycle(proxies)

def get_name():
    print('Generating random name')
    api = 'https://uinames.com/api/?gender=female&region=united%20states'
    gen_name = r.get(api, headers = json_headers)
    name_dump = json.loads(gen_name.text)
    fname = name_dump['name']
    lname = name_dump['surname']
    print('damn ' + fname + ' ' + lname + ', you cute!')
    return fname, lname

def get_csrf(proxy):
    url = 'https://www.nakedcph.com/auth/view?op=register'
    page = r.get(url, headers = headers, proxies={"http": proxy, "https": proxy})
    print(page.text)
    soup = bs.BeautifulSoup(page.text, 'lxml')
    print('Scraping csrf token')
    csrf = soup.find('input', {'name': '_AntiCsrfToken'}).get('value')
    print(csrf)
    return csrf

def register(miss_me):
    csrf = get_csrf(miss_me)
    fname, lname = get_name()
    email = fname + '@' + catchall
    headers_wcsrf = {
		'x-requested-with': 'XMLHttpRequest',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54',
		'x-anticsrftoken': csrf,
    }
    payload = { 
        '_AntiCsrfToken': '{}'.format(csrf),
        'firstName': '{}'.format(fname),
        'email': email,
        'password': password,
        'action': 'register'
   }
    print('Registering account')
    register = r.post('https://www.nakedcph.com/auth/submit', headers=headers_wcsrf, data=payload, proxies={"http": miss_me, "https": miss_me})
    jsondump = json.loads(register.text)
    if jsondump['StatusCode'] == 0:
        print('Account registered successfully')
    elif jsondump['StatusCode'] == 500:
        print('Account registration failed')
    return fname, lname, email

def raffle_entry(with_them_bans):
    print('Entering raffle')
    fname, lname, email = register(with_them_bans)
    raffle_token_request = 'https://nakedcph.typeform.com/app/form/result/token/PABKmQ/default'
    raffle_token = r.get(raffle_token_request, headers = headers, proxies={"http": with_them_bans, "https": with_them_bans})
    # not making this a string makes me nervous even though .text does that shit for you
    raffle_token = str(raffle_token.text)
    # i got problems sorry
    payload = {
        'form[language]': 'en',
        'form[textfield:FhF0pPr4gdHO]': fname,
        'form[textfield:HjWDPHuvQXDW]': lname,
        'form[email:xS8rv0ZpuFDg]': email,
        'form[dropdown:PzvBvJMvRXrd]': country,
        'form[landed_at]': '{}'.format(calendar.timegm(time.gmtime())),
        'form[token]': raffle_token,
    }
    raffle_url = 'https://nakedcph.typeform.com/app/form/submit/PABKmQ'
    submit = r.post(raffle_url, headers = headers, data=payload, proxies={"http": with_them_bans, "https": with_them_bans})
    print(submit.text)

def proxy_parse(proxy):
    # shout out to https://twitter.com/idontcop for the help over the years - little things like this save me time
    proxy_parts = proxy.split(':')

    if len(proxy_parts) == 2:
        ip, port = proxy_parts
        formatted_proxy = {
            'http': f'https://{ip}:{port}/',
        }
    elif len(proxy_parts) == 4:
        ip, port, user, password = proxy_parts
        formatted_proxy = {
            'http': f'https://{user}:{password}@{ip}:{port}/',
        }
    formatted_proxy = formatted_proxy['http']
    return formatted_proxy

for rafflesubmit in range(i):
    proxy = next(proxy_swm)
    proxy = proxy_parse(proxy)
    print('Using ' + proxy + ' for the registration and raffle entries')
    try:
        raffle_entry(proxy)
        r.cookies.clear()
        time.sleep(1)
    except:
        print('Proxy probably not working - trying again!')

