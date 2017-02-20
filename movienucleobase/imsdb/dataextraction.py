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

    movie_chars_names_extracted = []
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

    for char in re.finditer(regex, imsdb_movie_script):
        movie_chars_names_extracted.append(char.group('movie_char'))
    
    for name in movie_chars_names_extracted:
        if not imsdb.utilities.valid_movie_character(name):
            continue
        
        movie_character_name = imsdb.utilities.strip_unwanted_strings(name)

        # TODO: Remove this hack and fix the issue
        # The movie script as characters represented as "Merry & Pippin"
        # And the Regex code is extracting empty strings as characters
        if '&' in movie_character_name or not movie_character_name:
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

    for mscene in re.finditer(regex, imsdb_movie_script):
        movie_scenes_list.append(mscene.group('movie_text'))
     
    return movie_scenes_list


def process_movie_single_scene(single_scene, movie_characters_list, scene_number):
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

    process = re.compile(regex, re.MULTILINE | re.DOTALL)
     
    # The elements of the list movie_lines are extracted in the
    # following manner:
    #   [Line 0] - [Character name, Character line]
    #   [Line 1] - [Character name, Character line]
    #   [Line 2] - [Character name, Character line]
    #       ...
    movie_lines = re.findall(process, single_scene)

    characters_interacted_with = []

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

        if movie_char_from_scene not in characters_interacted_with:
            characters_interacted_with.append(movie_char_from_scene)

        # Second step:
        #   - Check for any mentioned characters
        #       For example: Frodo might talk about Gandalf even though
        #       Gandalf might not be in the scene

        movie_line_from_scene = line[1]

        imsdb.utilities.check_mentioned_characters(movie_char_from_scene,
                                                   movie_line_from_scene,
                                                   movie_characters_list)

    char_list = []
    for char in movie_characters_list:
        char_list.append(char.name)

    for char1 in movie_characters_list:
        for char2 in characters_interacted_with:
            if char1.name == char2:
                char1.add_characters_interacted_with(characters_interacted_with, char_list)
                char1.add_appeared_scene(scene_number)

    return characters_interacted_with


def get_real_name_and_id(characters, movie):
    """
    Gets the real name of the char from the wikia
    Adds an id to that char
    """
    identi = 0

    for character in characters:
        character.real_name = imsdb.dataadjustment.retrieve_character_real_name(
            movie.sub_wikia,
            character.name)

        character.id = identi
        identi = identi +1

    # Clean up list
    real_name_list = []

    for character in characters:
        if character.real_name not in real_name_list:
            real_name_list.append(character.real_name)
        else:
            movie.characters.remove(character)


def get_gender(characters, args):
    """
    Gets the gender for each char and adds it to the object
    Gender can be:
    male
    female
    no gender
    """
    for character in characters:
        if not args.bypass_gender_retrieval:
            character.real_name = imsdb.dataadjustment.retrieve_character_gender(character.real_name)
        else:
            dict_gender = imsdb.filehandlers.load_config_file(args.config, 'gender')
            character.gender = dict_gender[character.name.lower()]
