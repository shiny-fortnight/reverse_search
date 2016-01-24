#!/bin/python
# coding: utf-8

"""
Python API to retrieve Caller ID from phone number using OpenCNAM api.
"""

import requests
from bs4 import BeautifulSoup
import json
import phonenumbers


class OpenCNAMAPI(object):

    """
        OpenCNAMAPI Main Handler
    """

    _instance = None
    _verbose = False

    def __init__(self, arg=None):
        pass

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(OpenCNAMAPI, cls).__new__(
                cls, *args, **kwargs)
            if (args and args[0] and args[0]['verbose']):
                cls._verbose = True
        return cls._instance

    def display_message(self, s):
        if (self._verbose):
            print('[verbose] %s' % s)

    def format_number(self, phone_number):
        parsed_number = phonenumbers.parse(phone_number, 'US')
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    def get(self, phone_number):
        formatted_number = self.format_number(phone_number)
        s = requests.Session()
        req = s.get('https://ACc8aa48a044604425ba66940a2f6bdb54:AUfb0f7a1fd66f489c9f9e6d22426ccaa9@api.opencnam.com/v2/phone/%s?format=json' % formatted_number)
        soup = BeautifulSoup(req.content)
        json_result = json.loads(str(soup))

        dataJson = json.dumps(json_result)
        full_name = json_result['name']
        phone_number = json_result['number']
        return {'dataJson': dataJson, 'full_name': full_name, 'phone_number': phone_number}
