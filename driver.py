import requests
import json 
import datetime
import smtplib
from email.message import EmailMessage

#Function to send mail
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

#Function to make the json file more readable
def jprint(obj):
    text = json.dumps(obj,sort_keys=True,indent=4)
    return text

f = open("dist_data.txt","r") #Opens a file containing the details of the subscribers in State : District : email1 email2 .. format
lines = f.readlines()

for line in lines:
    lst = line.split()
    state = ""
    district = ""
    email = ""
    cn = 0
    elist = []
    sn = ""
    for j in lst:
        if(cn == 0 and j == ":"):
            state = sn
            cn = cn + 1
            sn = ""
        elif(cn == 1 and j == ":"):
            district = sn
            cn = cn + 1
            sn = ""
        elif(cn == 2):
            elist.append(j)
        else:
            ind = lst.index(j)
            if(lst[ind+1] == ":"):
                sn = sn + j
            else:
                sn = sn + j + " "

    stid = 0 #variable to store state id
    distid = 0 #variable to store district id
    district.strip()

    #The json file obtained from calling the state api is stored so that further api calls to get the state id is not required
    f1 = open("states.json","r")  #opens the states.json file which contains the details of every state of India
    dict1 = json.load(f1)
    for i1 in dict1['states']:
        if(i1['state_name'] == state):
            stid = i1['state_id']
            break
    f1.close()

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive'}

    req_dist_id = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"  #request to get the district id
    req_dist_id = req_dist_id + str(stid)
    resp2 = requests.get(req_dist_id,headers=headers)
    st2 = str(jprint(resp2.json()))
    file2  = open("districts.json",'w')
    file2.write(st2)
    file2.close()
    f2 = open("districts.json","r")
    dict2 = json.load(f2)
    for i2 in dict2['districts']:
        if(i2['district_name'] == district):
            distid = i2['district_id']
            break
    f2.close()

    t = datetime.datetime.now()
    day = t.day + 1
    month = t.month
    year = t.year
    count = 0
    sent = ""
    while count < 7:
        if(day > 31):
            day = 1
            month = month + 1
            if(month > 12):
                month = 1
                year = year + 1
        
        date = str(day) + '-' + str(month) + '-' + str(year)
        req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + str(distid) + "&date=" + date #request to get the available vaccine slot details
        response = requests.get(req,headers=headers)
        fname = "data" + str(count) + ".json"
        try:
            st = str(jprint(response.json()))
            file  = open(fname,'w')
            file.write(st)
            file.close()
        
        except:
            print(response)

        f = open(fname,'r')
        dict = json.load(f)
        for i in dict['sessions']:
            if(i['min_age_limit'] == 18): #If minimum age limit is 18 then only the details are stored. This can be changed accordingly
                stri = ""
                stri = stri + "Available at: " + i['name'] + " on " + date + "\n"
                sent = sent + stri
                print("Available at: " + i['name'] + " on " + date)
        f.close()

        day = day + 1
        count = count + 1
    
    if(len(sent)):
            for x in elist:
                email_alert("Vaccine Available", sent, x)
    else:
        print("Vaccine unavailable at " + district + " " + str(distid))
    

