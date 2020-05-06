import datetime
import azure.functions as func
import os
import logging
import json
from typing import List

from azure.cosmosdb.table.tableservice import TableService


def main(mytimer: func.TimerRequest, msg: func.Out[List[str]]) -> func.HttpResponse:

    alerts = list()
    
    STORAGE_CONNECTION_STRING = os.environ.get('AzureWebJobsStorage')
    service = TableService(connection_string=STORAGE_CONNECTION_STRING)
    items = service.query_entities('alerts')
    for item in items:
        alert = dict()
        alert['max'] = item['max']
        alert['min'] = item['min']
        alert['coordinates'] = item['coordinates']
        alert['location'] = item['location']
        alert['number'] = item['number']
        alerts.append(json.dumps(alert))

    # write queue
    msg.set(alerts)

    return
