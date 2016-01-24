#!/bin/python
# coding: utf-8

"""
Python API to retrieve Caller ID from phone number using OpenCNAM api.
"""

import requests
from bs4 import BeautifulSoup
import json
import phonenumbers
from flask import Markup
from config import OPEN_CNAM_KEY, OPEN_CNAM_SECRET

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
        try:
            formatted_number = self.format_number(phone_number)
        except Exception:
            raise ValueError('Bad Input Phone')
        
        s = requests.Session()
        req = s.get('https://%s:%s@api.opencnam.com/v2/phone/%s?format=json' % (OPEN_CNAM_KEY, OPEN_CNAM_SECRET, formatted_number))
        soup = BeautifulSoup(req.content)
        json_result = json.loads(str(soup))

        dataJson = json.dumps(json_result)
        full_name = Markup('<a target="_blank" href="https://www.google.com/#q='+json_result['name']+'">'+json_result['name']+'</a>')
        phone_number = json_result['number']
        return {'dataJson': dataJson, 'full_name': full_name, 'phone_number': phone_number}
