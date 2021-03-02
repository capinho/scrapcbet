from requests_html import HTMLSession
import pandas as pd
from nexmo import *
from pprint import pprint
from twilio.rest import Client 
import schedule
import time
from datetime import datetime
import os
from os import environ


def dec(a):
    decimal = str(a).split('.')
    return int(decimal[1])

def endwith5(number):
    return str(dec(number)).endswith('5')



def job():
    account_sid = environ['account_sid']
    auth_token = environ['auth_token']
    client = Client(account_sid, auth_token) 



    url = 'https://cbet.gg/sportwide/index.html?lang=en&brand=16#/virtual'

    s = HTMLSession()
    r = s.get(url)



    r.html.render(timeout=20,sleep=10)

    match_list = []
    print(r.status_code)
    for i in range(1,9):     
        heure = r.html.find("li:nth-of-type("+str(i)+") div.start-time",first=True)
        match = r.html.find("li:nth-of-type("+str(i)+") div.match-name", first=True)
        cote1 = r.html.find("li:nth-of-type("+str(i)+") div.odd-rect:nth-of-type(1)",first=True)
        cote2 = r.html.find("li:nth-of-type("+str(i)+") div.odd-rect:nth-of-type(2)",first=True)
        cote3 = r.html.find("li:nth-of-type("+str(i)+") div.odd-rect:nth-of-type(3)",first=True)

        if ((float(cote1.text)==1.95 and endwith5(cote2.text)==0 and endwith5(cote3.text)==0) or (float(cote3.text)==1.95 and endwith5(cote2.text)==0 and endwith5(cote1.text)==0)):
                message = client.messages.create( 
                    from_='whatsapp:+14155238886',  
                    body="Match: "+match.text+" merci",    
                    to='whatsapp:+221776206063',
                ) 
        match_item = {
            'heure':heure.text,
            'match':match.text,
            'cote1':cote1.text,
            'cote2':cote2.text,
            'cote3':cote3.text
        }
        match_list.append(match_item)
    df = pd.DataFrame(match_list)
    print(df)

schedule.every(2).minutes.do(job)
#schedule.every().minute.at(":30").do(job)

while True:
    schedule.run_pending()
    time.sleep(2.4) # wait one minute
