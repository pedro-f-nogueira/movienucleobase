"""
.. module:: utilities
    :synopsis: A module which contains multiple utilities to support the IMSDb API

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import logging
import difflib


def valid_movie_character(possible_movie_character_name):
    """ Detect if the movie character is valid or not.

    The function is needed because the regex used will parse the meta
    tags from the movie script, like 'INT', 'EXT' or 'CONTINUATION',
    as a movie character, as these tags are at bold in the HTML script
    like a normal movie character.

    A valid character is considered the one that it is a bold (already
    parsed by the script) and centered in the text.
    If the candidate string is not centered, it will be marked as invalid.

    Args:
        possible_movie_character_name (string): The name of the candidate
        string to movie character

    Returns:
        Bool: True if it is a valid character name, False otherwise
    """
    logger = logging.getLogger(__name__)

    # Consider valid characters the names that are centered
    numberWhitespaces = len(possible_movie_character_name) - len(possible_movie_character_name.lstrip(' '))

    if numberWhitespaces<20 or numberWhitespaces>30:
        logger.debug('Rejecting possible invalid character due to the number ' +
                     'of whitespaces at the start of the string ' +
                     '(' + str(numberWhitespaces) + '): ' + possible_movie_character_name)
        return False
    else:
        return True


def strip_unwanted_strings(movie_character_name):
    """This function removes any unwanted strings from the character's names.

    The unwanted strings are:
        - "(V.O.)"
        - "(CONT'D)"
        - Any multiple whitespaces

    Args:
        movie_character_name (string): The name of the movie character

    Returns:
        String: Returns a string clean from all unwanted strings
    """
    # Remove "(V.O.)" and "(CONT'D)" from characters' names
    stripped_movie_character_name = movie_character_name.split('(')[0]

    # Remove all of the unecessary whitespaces
    stripped_movie_character_name = " ".join(stripped_movie_character_name.split())

    return stripped_movie_character_name


def similar_character_already_added(movie_characters_list, movie_character_name):
    """Checks if a similar name was already added to the collected characters.
    
    The API assumes that the movie script has misspelled character names,
    so this function checks if the new candidate to movie character has a
    similar character name already added to the list.

    The function will reject names with 90% of similarity, or more, with any
    of the already present movie characters' name in the list.

    Args:
        movie_characters_list (list of MovieCharacter): List of all movie
        characters already collected
        movie_character_name (string): The name of the candidate to
        movie character

    Returns:
        Bool: True if already exists a character with a similar name,
        False otherwise
    """

    logger = logging.getLogger(__name__)

    # The "Fellowship of the Ring" script sometimes misspells "FRODO" as
    # "FRO DO" this function attempts to fix that
    for character in movie_characters_list:
        similarityRatio = difflib.SequenceMatcher(None,
                                                  movie_character_name.lower(),
                                                  character.name.split(' ')[0].lower())
        similarityRatio = similarityRatio.ratio()

        if similarityRatio>0.9 and similarityRatio<1.0:
            logger.debug('Possible character already added: ' + \
                         movie_character_name)
            return True
    else:
        return False


def check_mentioned_characters(char_from_scene, movie_line, characters_list):
    for mentioned_character in characters_list:
        # Find which characters are mentioned in the movie line
        if mentioned_character.name.lower() in movie_line.lower():
            # Add the mentioned characters to the list of the character that
            # it is mentioning them
            for mentioning_character in characters_list:
                if char_from_scene == mentioning_character.name:
                    mentioning_character.add_mentioned_character(mentioned_character.name)
                    break


