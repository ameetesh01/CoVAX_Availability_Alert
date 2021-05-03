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
