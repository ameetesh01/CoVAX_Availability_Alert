# CoVAX_Availabilty_Alert
This is a simple python script that can give regular vaccination availability updates through email alerts so that we do not miss out on our only hope in fighting this pandemic. This script is run as a corn job. The users can specify how regularly and at which time they want to get the updates. Before running the script, some initial setup might be required. We will be using the APIs provided by [API Setu](https://apisetu.gov.in/public/marketplace/api/cowin). 

## Initial Set-ups
Since we are using "requests" module which isn't a default module in python, we have to install it.

For Linux and Mac users:

    pip3 install requests
    
For Windows users (assuming you have installed python and are in the python directory):

    > python -m pip3 install requests
    
Since we are using "Appointment Availability APIs - find_by_district", we must know the state code and district code. For this also we use the APIs provided in API Setu.

#### For State id
For Linux and Mac users:

    curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/states" -H  "accept: application/json" -H  "Accept-Language: en_US"
    
For Windows users:
  For running cURL commands in command prompt follow these [steps](https://stackoverflow.com/questions/2710748/run-curl-commands-from-windows-console)
  
#### For District id
After running the command for state id, check your state id and note it down.
Now, using the state id, we will be finding the district id where you wanna know the availability.

For Linux and Mac users:

    curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/[enter_your_state_id]" -H  "accept: application/json" -H  "Accept-Language: en_US"
    
For Windows users:
  For running cURL commands in command prompt follow these [steps](https://stackoverflow.com/questions/2710748/run-curl-commands-from-windows-console)   
    
After noting down the district id, change the 'district_id' in line number 43 of the script:

    https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=[Enter_district_id]&date=
    
For example, Angul is a district in Odisha with district id = 445, so the request will be as follows:

    https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=445&date=02-05-2021
    
In the 'email_alert' function in the script, add the recepient email id in the 'to' parameter.

## Auto Scheduling the python script
We donot want to manually run the program everytime we need to know the availability of vaccines. For that we need to use it as a [cron](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjq7NHFtKvwAhU7xzgGHX0OAkgQmhMwHHoECD4QAg&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCron&usg=AOvVaw0wfcpwkKkcbyApDzmGV-rD) job. For this we use crontab feature.

For Linux and Mac users:

Follow the steps:

    export EDITOR=nano
    crontab -e
    
Add the following line at the end of the crontab file:
    
    0,10,20,30,40,50 * * * * cd/path/to/the_file && python3 vax_alert.py
    
Here, it will run after every 10 mins, it can be changed accordingly. To learn more about cron, refer [here](https://crontab.guru/crontab.5.html).

For Windows users:
Follow these [steps](https://datatofish.com/python-script-windows-scheduler/).

## Function of the driver.py file
The extra functionality that it has over the vax_alert.py file is reading the text file containing the details of the subscribers to get the state, district, and email, and reading the states.json file.
The text file contains the details of the subscribers in the following format - State : District : email1 email2 ... For example if there are 3 subscribers from North Delhi with email ids e1@abc.com, e2@abc.com and e3@abc.com, then the content of the file will be as following:

    Delhi : North Delhi : e1@abc.com e2@abc.com e3@abc.com

As we saw previously how to get the state details using cURL, hence, it was called prior and the response was stored in a file called states.json. Hence, calling this api isn't required at all. The state id can be assigned just by using the state entered in the text file.

Then a request is sent to retrieve the district id of the subscriber using the state id and using this district id, 7 requests are sent for the coming 7 days about available slots at vaccination centres in the subscriber's district.

If there are any available slots (let's say 2), the subscribers receive an email alert in the following format:

    from: availvax@gmail.com
    subject: Vaccine Available

    Available at: Vaccination Centre1 on dd-mm-yyyy
    Available at: Vaccination Centre2 on dd-mm-yyyy
