## Import neccessary libraries

import requests
from requests import Session
from datetime import datetime
import json
import time
import twilio
from twilio.rest import Client
from requests.sessions import Session
import smtplib
import yaml

## Reading config file

with open("configfile.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Read successful")

date = datetime.now()
date = date.strftime('%d.%m.%Y %H:%M')
date = str(date)

## API to get current bitcoin price:

def get_bitcoin_price():
    url = data[0]['Details']['url']

    parameters = {'start':'1',
             'limit':'1',
             'convert':'INR'
             }

    headers = {'Accepts':'application/json',
          'X-CMC_PRO_API_KEY':data[0]['Details']['X-CMC_PRO_API_KEY']}
    session = Session()
    session.headers.update(headers)
    respone = session.get(url,params = parameters)
    output = json.loads(respone.text)
    price = output['data'][0]['quote']['INR']['price']
    return int(price)

print(get_bitcoin_price())

price = get_bitcoin_price()  ## Current price of bit coin using API
# price = 3696899

def twilio_setup(messg_body):               ## Function to send sms using twilio
    account_sid = data[0]['Details']['account_sid']
    auth_token = data[0]['Details']['auth_token']
    to_number = data[0]['Details']['to_number']
    client = Client(account_sid,auth_token)
    client.messages.create(to= to_number,from_= '(205) 236-6835',body=messg_body)
    print('successfully sent sms')

def mail_setup(mail_body):
    sender_email = data[0]['Details']['sender_email']
    rec_email = data[0]['Details']['rec_email']
    password = data[0]['Details']['password']
    message = 'Subject: {}\n\n{}'.format('BitCoin Status mail', mail_body)


    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender_email,password)


    print('login successfull')
    server.sendmail(sender_email,rec_email,message)
    print('Sent mail')


threshold_low = 3500000
threshold_high = 5000000
# date = datetime.now()
# date = date.strftime('%d.%m.%Y %H:%M')

if price < threshold_low:
    print(f'Hello Ganesh bitcoin price is lesser than {threshold_low} alert!!!')
    twilio_setup(f'Hello Ganesh bitcoin price is lesser than {threshold_low} alert!!!')
    mail_setup(f'Hello Ganesh bitcoin price is lesser than {threshold_low} alert!!!')

elif price > threshold_high:
    print(f'Hello Ganesh bitcoin price crossed {threshold_high} alert!!!')
    twilio_setup(f'Hello Ganesh bitcoin price crossed {threshold_high} alert!!!')
    mail_setup(f'Hello Ganesh bitcoin price crossed {threshold_high} alert!!!')
else:
    print(f'Hello Ganesh Bitcoin price at {date} is {price} INR')
    twilio_setup(f'Hello Ganesh Bitcoin price at {date} is {price} INR')
    mail_setup(f'Hello Ganesh bitcoin price at {date} is {price} ')



