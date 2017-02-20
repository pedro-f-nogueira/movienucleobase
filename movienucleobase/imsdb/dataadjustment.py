"""
.. module:: dataadjustment
    :synopsis: A module to adjust the data extracted the movie script before analyzing it

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import logging
import __builtin__
import json
import urllib
import wikia
import unidecode


def retrieve_character_real_name(sub_wikia, movie_character_name):
    """Retrieve the complete name of the movie character.
    
    The character's names in the movie script are often incomplete or
    shortened (for example, "Samwise Gamgee" appears as "Sam" in "The Lord
    of the Rings") so this function uses the movie's sub-wikia to detect
    the character's real name.

    The script will query the wikia search for the short name (for example,
    "Sam") and it will accept anything that shows up as the first result as
    the correct real name.

    It is likely that the movie script contains generic characters which do
    not properly exist in the wikia. For example, in "The Lord of the Rings:
    The Fellowship of the Ring":
        - Character name: "ORC OVERSEER"
        - Wikia search result: "List of unnamed original characters of the
        books and films"
    In cases in which the wikia search result returns "List of", the function
    will return None as the character's real name.

    Sometimes the search result will return something like this:
        - Character name: "HALDIR"
        - Wikia search result: "Haldir (disambiguation)"
    This might happen when there are multiple characters with the same name in
    the movie lore. The function will assume that the less important characters
    with the same name are irrelevant and it will automatically strip the
    substring "(disambiguation)".

    Args:
        sub_wikia (String): The sub-wikia to be queried
        movie_character_name (String): The character's 

    Returns:
        String: The character's real name
    """

    logger = logging.getLogger(__name__)

    black_list = ['List of']

    try:
        real_name = wikia.search(sub_wikia, movie_character_name)[0]  # here

        logger.info('Resolved ' + movie_character_name + ' to ' + real_name)

        if __builtin__.any(x in real_name for x in black_list):
            logger.info('Rejecting possible invalid character.' +
                        ' Name: ' + movie_character_name +
                        ' ; Real name: ' + real_name)
            real_name = None
        else:
            # Removing any "(disambiguation)" sub-strings
            real_name = real_name.split('(')[0].strip(' ')

        # Remove any special accents from the string
        real_name = unidecode.unidecode(unicode(real_name))

        return real_name

    except ValueError:
        return 'problematic character'


def retrieve_character_gender(real_name, api_key_path='api_key'):
    """Retrieve the character's gender from the Freebase database.

    This function will query the Freebase's database for the character's name
    and it will attempt to extract the gender from the first result found. The
    string that represents the gender is extracted as it is from Freebase in 
    lower case.

    If the character is not human, the page on Freebase might no contain
    any reference to the gender, so the function will return the
    string "nogender".

    The function accepts the character's real name resolved by the function
    "retrieve_character_real_name()".

    It is necessary to request a Google API enabled for Freebase and store it
    in a text file. The path to the text file shall be passed as an argument
    of the function, otherwise the script will look for a file name "api_key"
    in the current path of the shell.

    Args:
        real_name (String): The character's name to be queried on Freebase
        api_key_path (String): The path to the text file containing the 
        Google API's key

    Returns:
        String: The character's gender
    """

    logger = logging.getLogger(__name__)
    logger.debug('Attempting to get the gender from character: ' + real_name)

    nogender = "nogender"

    if real_name is None:
        return nogender

    freebase_search_url = 'https://www.googleapis.com/freebase/v1/search'
    freebase_topic_url = 'https://www.googleapis.com/freebase/v1/topic'
    freebase_json_gender = '/fictional_universe/fictional_character/gender'
    freebase_api_key = open(api_key_path).read()

    # First step: check if the character exists in freebase's database
    character_id = get_freebase_character_id(real_name,
                                             freebase_api_key,
                                             freebase_search_url)

    if not character_id:
        return nogender

    # Second step: look up for the character's gender
    freebase_topic_url = freebase_topic_url + character_id
    freebase_search_params = {
        'key': freebase_api_key,
        'filter': freebase_json_gender
        }
    url = freebase_topic_url + '?' + urllib.urlencode(freebase_search_params)
    logger.debug('Looking up ' + real_name + '\'s gender: ' + url)

    response = json.loads(urllib.urlopen(freebase_topic_url).read())

    if 'property' not in response:
        print 'Error retrieving data from freebase: ' + url
        print response

    if freebase_json_gender in response['property'].keys():
        gender = response['property'][freebase_json_gender]['values'][0]['text']
        
        return gender.lower()
    else:
        return nogender


def get_freebase_character_id(real_name, freebase_api_key, freebase_search_url):
    """Retrieve the character's ID associated to the Freebase database.
    
    This function retrives the character ID to be used by the 
    function retrieve_character_gender() in order to extract information
    related to the character.

    More info: https://developers.google.com/freebase/

    Args:
        real_name (String): The character's name to be queried on Freebase
        freebase_api_key (String): The Google API's key used to access Freebase
        freebase_search_url (String): The URL to be used to perform searches

    Returns:
        String: The character's ID on Freebase
    """
    logger = logging.getLogger(__name__)

    freebase_search_params = {
        'query': real_name,
        'key': freebase_api_key
    }

    url = freebase_search_url + '?' + urllib.urlencode(freebase_search_params)
    logger.debug('Looking up the character ' + real_name + ': ' + url)

    response = json.loads(urllib.urlopen(url).read())

    if len(response['result']) <= 0 or 'id' not in response['result'][0].keys():
        return
    else:
        return response['result'][0]['id']


