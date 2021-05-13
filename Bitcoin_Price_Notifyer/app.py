import requests
from requests import Session
from datetime import datetime
import json
import time
import twilio
from twilio.rest import Client
from requests.sessions import Session

import smtplib


def get_bitcoin_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {'start':'1',
             'limit':'1',
             'convert':'INR'
             }

    headers = {'Accepts':'application/json',
          'X-CMC_PRO_API_KEY':'54533a9c-e9d3-4c4d-8704-993ad1a88e8d'}
    session = Session()
    session.headers.update(headers)
    respone = session.get(url,params = parameters)
    data = json.loads(respone.text)
    price = data['data'][0]['quote']['INR']['price']
    return int(price)

def price_date():
    price = get_bitcoin_price()
    date = datetime.now()
    date = date.strftime('%d.%m.%Y %H:%M')
    details = []
    details.append({'price':price,'date':date})
    return details

print(price_date())

output = price_date()

# output = [{'price': 4095503, 'date': '11.05.2021 20:34'}]


current_price = output[0]['price']
curr_date = output[0]['date']


account_sid = "ACc32f2b5878fe1b90bb7da03759ec1a3e"
auth_token = '39f74fda1805cc1ea5a92131272e962c'

client = Client(account_sid,auth_token)
to_number = '+919941716217'



client.messages.create(to='+919941716217',from_= '(205) 236-6835',body=f'Hi Ganesh,Bitcoin price is {current_price} at {curr_date}')
print('successfully sent sms')