import requests
import json
import re
import bs4 as bs
import time


catchall = 'pewpw.pw'
country = 'Canada' # straight outta YEG
i = 50 # number of entries

r = requests.session()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
}

json_headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
}


def get_name():
    print('Generating random name')
    api = 'https://uinames.com/api/?gender=female&region=united%20states'
    gen_name = r.get(api, headers = json_headers)
    name_dump = json.loads(gen_name.text)
    fname = name_dump['name']
    lname = name_dump['surname']
    print('damn ' + fname + ' ' + lname + ', you cute!')
    return fname, lname

def get_csrf():
    url = 'https://www.nakedcph.com/auth/view?op=register'
    page = r.get(url, headers = headers)
    soup = bs.BeautifulSoup(page.text, 'lxml')
    print('Scraping csrf token')
    csrf = soup.find('input', {'name': '_AntiCsrfToken'}).get('value')
    print(csrf)
    return csrf

def register():
    csrf = get_csrf()
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
        'password': 'naked12!',
        'action': 'register'
   }
    print('Registering account')
    register = r.post('https://www.nakedcph.com/auth/submit', headers=headers_wcsrf, data=payload)
    jsondump = json.loads(register.text)
    if jsondump['StatusCode'] == 0:
        print('Account registered successfully')
    elif jsondump['StatusCode'] == 500:
        print('Account registration failed')

    return fname, lname, email

def raffle_entry():
    print('Entering raffle')
    fname, lname, email = register()
    raffle_token_request = 'https://nakedcph.typeform.com/app/form/result/token/PABKmQ/default'
    raffle_token = r.get(raffle_token_request, headers = headers)
    # not making this a string makes me nervous even though .text does that shit for you
    raffle_token = str(raffle_token.text)
    # i got problems sorry
    payload = {
        'form[language]': 'en',
        'form[textfield:FhF0pPr4gdHO]': fname,
        'form[textfield:HjWDPHuvQXDW]': lname,
        'form[email:xS8rv0ZpuFDg]': email,
        'form[dropdown:PzvBvJMvRXrd]': 'Canada',
        'form[landed_at]': '1532468223',
        'form[token]': raffle_token,
    }
    raffle_url = 'https://nakedcph.typeform.com/app/form/submit/PABKmQ'
    submit = r.post(raffle_url, headers = headers, data=payload)
    print(submit.text)

for rafflesubmit in range(i):
    raffle_entry()
    r.cookies.clear()
    time.sleep(4)

