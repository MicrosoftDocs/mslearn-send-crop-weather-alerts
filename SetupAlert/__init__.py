import logging
import azure.functions as func
import os
import json
import urllib
import time

from azure.cosmosdb.table.tableservice import TableService


def main(req: func.HttpRequest) -> func.HttpResponse:

    sender = req.form['From']
    message = req.form['Body']

    # We will try to parse the message into location, minimum temperature and maximum temperaturess
    try:
        message = message.strip()
        maxIndex = message.rindex(' ')
        minIndex = message.rindex(' ', 0, maxIndex)
        maxInput = message[maxIndex+1:]
        minInput = message[minIndex+1:maxIndex]
        location = message[:minIndex]
        maxTemp = float(maxInput.lower().strip('c'))
        minTemp = float(minInput.lower().strip('c'))

    except ValueError as err:
        return func.HttpResponse(f'INVALID FORMAT. USE: Location MinTemp MaxTemp. EXAMPLE: Platz der Republik 1, Berlin, Germany 3C 25C')
        

    MAPS_KEY = os.environ.get('AZURE_MAPS_SUBSCRIPTION_KEY')
    requesturl = f'https://atlas.microsoft.com/search/address/json?subscription-key={MAPS_KEY}&api-version=1.0&limit=1&query={urllib.parse.quote(location, safe="")}'

    res = urllib.request.urlopen(requesturl)
    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))

    # This is a standardized way the location's address is returned
    location_normalized = res_json['results'][0]['address']['freeformAddress']
    lat = res_json['results'][0]['position']['lat']
    lon = res_json['results'][0]['position']['lon']
    coordinates = f'{lat},{lon}'

    record = dict()
    record['max'] = maxTemp
    record['min'] = minTemp
    record['coordinates'] = coordinates
    record['location'] = location_normalized
    record['number'] = sender
    record['PartitionKey'] = f'{sender}'
    record['RowKey'] = f'{sender}:{coordinates}'

    try:
        STORAGE_CONNECTION_STRING = os.environ.get('AzureWebJobsStorage')
        service = TableService(connection_string=STORAGE_CONNECTION_STRING)
        service.insert_or_replace_entity('alerts', record)
    except Exception as err:
        logging.error(f'{err}')
        return func.HttpResponse('An error occurred saving your alert. Please try again later.')
    
    return func.HttpResponse(f'Alert for {location_normalized} at {coordinates} with Max:{maxTemp}C and Min:{minTemp}C saved.')