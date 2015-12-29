import json
import urllib
import logging

def extractCharacterGender(name):
    logging.debug("extractCharacterGender(): Attempting to get gender from character: " + name)

    api_key = open("api_key").read()

    query = name
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    if len(response['result'])<=0 or "id" not in response['result'][0].keys():
        return "nogender"

    #print "Name: " + response['result'][0]['name'] + " ; id: " + response['result'][0]['id']
    #print ""

    query = response['result'][0]['id']
    service_url = 'https://www.googleapis.com/freebase/v1/topic' + query
    params = {
        'query': query,
        'key': api_key
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    if '/fictional_universe/fictional_character/gender' in response['property'].keys():
        gender = response['property']['/fictional_universe/fictional_character/gender']['values'][0]['text'].lower()
    else:
        gender = "nogender"

    return gender
