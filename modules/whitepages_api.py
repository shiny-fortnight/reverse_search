#!/usr/bin/env python
import requests as r
import sys, json, re
import StringIO as StringIO

API_KEY = 'ea04b1f16b56a1b1a21b0159b8b1990e'


def _getPhoneNumber(inPhone):
    re.sub("\D", "", inPhone)
    inPhone = inPhone.replace('-', '')
    if inPhone[0] == '1':
        inPhone = inPhone[1:]
    assert len(inPhone) == 10
    return inPhone


def makeAPIRequest(inPhone):
    """
    Returns the results of the whitepages requests as a list:
        name, streetaddr, carrier, phoneType, cleaned
    """
    try:
        cleaned = _getPhoneNumber(inPhone)
    except AssertionError:
        raise ValueError('Bad Input Phone')

    req = 'https://proapi.whitepages.com/2.1/phone.json?api_key=%s&phone_number=%s' % (API_KEY, cleaned)
    result = r.get(req)

    asDict = json.loads(result.text)

    nameValues = asDict['results'][0]['belongs_to']
    if len(nameValues) > 0:
        nameValues = nameValues[0]
        if nameValues['best_name']:
            fname = nameValues['best_name']
        elif nameValues['best_name']['first_name'] or nameValues['best_name']['last_name']:
            nameKeys = ['first_name', 'middle_name', 'last_name']
            fname = ''
            for name in nameKeys:
                fname += nameValues['names'][name] if nameValues['names'][name] else ''
    else:
        fname = None

    locationValues = asDict['results'][0]['best_location']
    carrier = asDict['results'][0]['carrier']
    phoneType = asDict['results'][0]['line_type']

    locKeys = ['standard_address_line1', 'standard_address_line2', 'city', 'standard_address_location']
    streetAddr = ''
    for name in locKeys:
        streetAddr += locationValues[name]+' ' if locationValues[name] else ''

    return [fname, streetAddr, carrier, phoneType, cleaned]
