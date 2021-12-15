from requests_html import HTMLSession
import pandas as pd
import schedule
import time
from datetime import datetime
import requests 


def dec(a):
    decimal = str(a).split('.')
    return int(decimal[1])

def endwith5(number):
    return str(dec(number)).endswith('5')



def job():
    
    url = 'https://www.nairabet.com/virtuals'

    s = HTMLSession()
    r = s.get(url)



    r.html.render(timeout=40,sleep=20)

    match_list = []
    print(r.status_code)
    for i in range(2,9):     
        match = r.html.find("li:nth-of-type("+str(i)+") div.StyledVirtual__EventsName-dEYouo",first=True)
        cote1 = r.html.find("li:nth-of-type("+str(i)+") div:nth-of-type(2) li:nth-of-type(1) button",first=True)
        cote2 = r.html.find("li:nth-of-type("+str(i)+") div:nth-of-type(2) li:nth-of-type(2) button",first=True)
        cote3 = r.html.find("li:nth-of-type("+str(i)+") div:nth-of-type(2) li:nth-of-type(3) button",first=True)

        if ((float(cote1.text)==1.95 and endwith5(cote2.text)==0 and endwith5(cote3.text)==0) or (float(cote3.text)==1.95 and endwith5(cote2.text)==0 and endwith5(cote1.text)==0)):
            requests.get("https://api.callmebot.com/whatsapp.php?phone=+221776206063&text=%s&apikey=534546" %(match.text))
        match_item = {
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
    time.sleep(1) # wait one minute
