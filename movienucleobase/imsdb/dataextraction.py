"""
.. module:: dataextraction
    :synopsis: A module to extract various kinds of movie data from the IMSDb HTML pages

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import re
import logging
import imsdb.datastructures
import imsdb.utilities


def extract_characters(imsdb_movie_script):
    """ Extract the movie characters from a movie script into a list.

    This function receives as a parameter a list containing the movie
    lines in the format of the IMSDb HTML page. The HTML page will be
    parsed using a regular expression which will extract all the possible
    candidates for movie characters.

    After the extraction of those candidates, the function will reject all
    false positives classified as such by the function valid_movie_character().

    Each character will be added to a new object from the
    class MovieCharacter.

    Each object will then be added to a list of objects to be returned in
    the end of the function.

    No repeated characters shall be added to the list.

    Args:
        imsdb_movie_script (list of strings): The file containing the
        IMSDb HTML page

    Returns:
        list of MovieCharacter: This list contains all the detected
        movie characters from the IMSDb movie script
    """

    logger = logging.getLogger(__name__)
    logger.info('Extracting the characters...')

    movie_characters_names_extracted = []
    movie_characters_list = []

    # *** Regex explanation ***
    # (1) First and second lines
    #   Match all text enclosed by the HTML tags:
    #       - "<b></b>"
    #   Except for the ones that start with the strings:
    #       - "EXT."
    #       - "INT."
    #       - "SUPER"
    #   And put them under the capturing group "movie_char"
    #
    # (2) Third line
    #   Match all text that comes after the previous HTML tags until
    #   the next "<b>" tag (which represents the next character) and
    #   put it under the captuing group "movie_text"
    regex = ur'<b>(?!EXT\.)(?!INT\.)(?!SUPER)' + \
            ur'(?P<movie_char>.*?)<\/b>' + \
            ur'(?P<movie_text>.*?)(?=<b>)'

    for m in re.finditer(regex , imsdb_movie_script):
        movie_characters_names_extracted.append(m.group('movie_char'))
    
    for name in movie_characters_names_extracted:
        if not imsdb.utilities.valid_movie_character(name):
            continue
        
        movie_character_name = imsdb.utilities.strip_unwanted_strings(name)

        # TODO: Remove this hack and fix the issue
        # The movie script as characters represented as "Merry & Pippin"
        # And the Regex code is extracting empty strings as characters
        if '&amp;' in movie_character_name or not movie_character_name:
            logger.debug('Rejecting possible invalid character: ' + movie_character_name)
            continue

        if imsdb.utilities.similar_character_already_added(movie_characters_list, movie_character_name):
            continue

        # Check if the character was already collected in the list
        for existent_movie_character in movie_characters_list:
            if movie_character_name in existent_movie_character.name:
                break
        else:
            logger.info('Adding character... ' + movie_character_name)
            movie_characters_list.append(imsdb.datastructures.MovieCharacter(movie_character_name))

    return movie_characters_list


def extract_scenes(imsdb_movie_script):
    """Parse the movie script and collect all movie scenes in the movie script.

    The function parses the HTML page using a regex code which considers
    a movie scene any text from the following list of tags until the next
    same list of tags:
        - BLACK SCREEN
        - EXT.
        - INT.

    Each scene will be stored as a string in a list of string.

    The scenes can, and should, contain:
        - Movie characters
        - Character's lines

    Args:
        imsdb_movie_script (list of strings): The file containing the
        IMSDb HTML page

    Returns:
        List of strings: The returned list contains each individual scene
        from the movie
    """
    logger = logging.getLogger(__name__)
    
    logger.info('Extracting all the scenes from the movie script...')

    # *** Regex explanation ***
    # (1) First line
    #   Start by matching the beginning of each scene. Every scene
    #   starts with one of these strings:
    #     - "<pre>BLACK SCREEN"
    #     - "<b>EXT."
    #     - "<b>INT."
    #   The "BLACK SCREEN" string is usually the very beginning
    #   of the movie script.
    #
    # (2) Second line
    #   Match all text starting from one of the previous strings
    #   and tag it under the capturing group "movie_text"
    #
    # (3) Third line
    #   Stop matching until the beginning of the next scene, which
    #   is given by the strings mentioned earlier.
    regex = ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)' + \
            ur'(?P<movie_text>.*?)' + \
            ur'(?=<b>(EXT\.|INT\.))'

    movie_scenes_list = []

    for m in re.finditer(regex, imsdb_movie_script):
        movie_scenes_list.append(m.group('movie_text'))
     
    return movie_scenes_list


def process_movie_single_scene(single_scene, movieCharactersList, scene_number):
    """Parse a single movie scene and extract the interactions between the
    characters.

    Args:
        single_scene (list of strings): A single movie scene
        movieCharactersList (list of MovieCharacter): list of all extracted
        characters
        scene_number (integer): The number of scene being analyzed.

    Returns:
        List of strings: The returned list returns the list of interactions
    """

    # *** Regex explanation ***
    # (1) First and second lines
    #   Match all text enclosed by the HTML tags:
    #       - "<b></b>"
    #   Except for the ones that start with the strings:
    #       - "EXT."
    #       - "INT."
    #       - "SUPER"
    #   And put them under the capturing group "movie_char"
    #
    # (2) Third line
    #   Match all text that comes after the previous HTML tags until
    #   the next "<b>" tag (which represents the next character) and
    #   put it under the captuing group "movie_text"
    regex = ur'<b>(?!EXT\.)(?!INT\.)(?!SUPER)' + \
            ur'(?P<movie_char>.*?)<\/b>' + \
            ur'(?P<movie_text>.*?)(?=<b>)'

    p = re.compile(regex, re.MULTILINE | re.DOTALL)
     
    # The elements of the list movie_lines are extracted in the
    # following manner:
    #   [Line 0] - [Character name, Character line]
    #   [Line 1] - [Character name, Character line]
    #   [Line 2] - [Character name, Character line]
    #       ...
    movie_lines = re.findall(p, single_scene)

    movieCharacterFromScene = ""
    charactersInteractedWith = []

    for line in movie_lines:
        # First step:
        #   - Detect new direct interactions

        movie_char_from_scene = line[0]

        # If the character was not a valid one (meaning that there is
        # some kind of meta information in the scene like, a description on
        # how the camera behave or similar), discard the current movie line
        # and move on to the next one

        if not imsdb.utilities.valid_movie_character(movie_char_from_scene):
            continue

        movie_char_from_scene = imsdb.utilities.strip_unwanted_strings(movie_char_from_scene)

        if movie_char_from_scene not in charactersInteractedWith: 
            charactersInteractedWith.append(movie_char_from_scene)

        # Second step:
        #   - Check for any mentioned characters
        #       For example: Frodo might talk about Gandalf even though
        #       Gandalf might not be in the scene

        movie_line_from_scene = line[1]

        imsdb.utilities.check_mentioned_characters(movie_char_from_scene,
                                                   movie_line_from_scene,
                                                   movieCharactersList)

    for l1 in movieCharactersList:
        for l2 in charactersInteractedWith:
            if l1.name==l2:
                l1.add_characters_interacted_with(charactersInteractedWith)
                l1.add_appeared_scene(scene_number)

    return charactersInteractedWith


