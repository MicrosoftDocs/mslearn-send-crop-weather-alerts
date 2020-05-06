import logging
import azure.functions as func
import os
import json
import urllib

def main(msg: func.QueueMessage, twilioMessage: func.Out[str]) -> func.HttpResponse:

    MAPS_KEY = os.environ.get('AZURE_MAPS_SUBSCRIPTION_KEY')

    alert = json.loads(msg.get_body().decode('utf-8'))
    
    alertMax = alert['max']
    alertMin = alert['min']
    coordinates = alert['coordinates']
    location = alert['location']
    number = alert['number']

    requesturl = f'https://atlas.microsoft.com/weather/forecast/daily/json?subscription-key={MAPS_KEY}&api-version=1.0&unit=metric&duration=5&query={coordinates}'

    res = urllib.request.urlopen(requesturl)
    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))


    message = f"Temperature alert for {location} at {coordinates}. "
    sendAlert = False

    for i in range(0,5):
        maxTemp = res_json['forecasts'][i]['temperature']['maximum']['value']
        minTemp = res_json['forecasts'][i]['temperature']['minimum']['value']

        maxnotify = (alertMax <= maxTemp)
        minnotify = (alertMin >= minTemp)

        if minnotify or maxnotify:
            sendAlert = True

        if maxnotify and minnotify:
            message+= f'In {str(i)} days: Min is {str(minTemp)}C Max is {str(maxTemp)}C. '
        elif maxnotify:
            message+= f'In {str(i)} days: Max is {str(maxTemp)}C. '
        elif minnotify:
            message+= f'In {str(i)} days: Min is {str(minTemp)}C. ' 

    if sendAlert:
        value = {
        "from": os.environ.get('TWILIO_PHONE_NUMBER'),
        "body": message,
        "to": number
        }

        logging.info(f'Sending message to {number}: {message}')
        twilioMessage.set(json.dumps(value))

    return
