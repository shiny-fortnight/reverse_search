#!/bin/python
# coding: utf-8

import requests
import sys


def call_calleridservice(phone):
    #The username and key are required for the API and should be hardcoded.
    username = 'httrafficking'
    key = '807e9e3d6d1ce424a1fe65a4fbc62425e731eb1f'
    url = 'http://cnam.calleridservice.com/query?u=' \
    + username + '&k=' + key + '&n=' + phone

    try:
        response = requests.get(url)
        return response.text
    except:
        return str(sys.exc_info()[1]).split('BadStatusLine(')[1].split(',')[0]
