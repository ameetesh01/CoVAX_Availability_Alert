import requests
import json 
import datetime
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "availvax@gmail.com"
    msg['from'] = user
    pwd = "iuokhukohdxqbrrh"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,pwd)
    server.send_message(msg)
    server.quit()

def jprint(obj):
    text = json.dumps(obj,sort_keys=True,indent=4)
    return text

t = datetime.datetime.now()
day = t.day + 1
month = t.month
year = t.year

count = 0
sent = ""
while count < 20:
    if(day > 31):
        day = 1
        month = month + 1
        if(month > 12):
            month = 1
            year = year + 1
    
    date = str(day) + '-' + str(month) + '-' + str(year)
    req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=445&date=" + date
    response = requests.get(req)
    st = str(jprint(response.json()))
    file  = open("data.json",'w')
    file.write(st)
    file.close()

    f = open('data.json','r')
    dict = json.load(f)
    for i in dict['sessions']:
        if(i['min_age_limit'] == 18):
            stri = ""
            stri = stri + "Available at: " + i['name'] + " on " + date + "\n"
            sent = sent + stri
            print("Available at: " + i['name'] + " on " + date)
    f.close()

    day = day + 1
    count = count + 1

if(len(sent)):
        email_alert("Vaccine Available", sent, "ameetesh01@gmail.com")
