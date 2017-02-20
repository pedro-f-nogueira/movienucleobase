# coding=utf-8

"""
.. module:: utilities
    :synopsis: A module which contains multiple utilities to support the IMSDb API

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import logging
import difflib
import pandas as pd
import sqlalchemy as sql
import re


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
    number_whitespaces = len(possible_movie_character_name) - \
                        len(possible_movie_character_name.lstrip(' '))

    if number_whitespaces < 20 or number_whitespaces > 30:
        logger.debug('Rejecting possible invalid character due to the number ' +
                     'of whitespaces at the start of the string ' +
                     '(' + str(number_whitespaces) + '): ' + possible_movie_character_name)
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

    # Remove additional V/O
    stripped_movie_character_name = re.sub('\V/0$', '', stripped_movie_character_name)
    stripped_movie_character_name = re.sub('\O.S$', '', stripped_movie_character_name)

    # Remove non-letters
    stripped_movie_character_name = re.sub("[.,“”/#!?$%\^&\*;:{}=\-_`~()'\"]",  # The pattern to search for
                                           "",  # The pattern to replace it with
                                           stripped_movie_character_name)  # The text to search

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

    # This step is done because of names like apis mistakes, for example
    # The api returns 'Minas Tirith' when sent FRO
    if len(movie_character_name.split(' ')[0]) <= 3:
        name_to_be_used = ''.join(movie_character_name.split(' '))
    else:
        name_to_be_used = movie_character_name

    max_similarity_ratio = 0

    for character in movie_characters_list:
        similarity_ratio = difflib.SequenceMatcher(None,
                                                   name_to_be_used.lower(),
                                                   character.name.split(' ')[0].lower())

        similarity_ratio = similarity_ratio.ratio()

        if max_similarity_ratio < similarity_ratio:
            max_similarity_ratio = similarity_ratio

    if max_similarity_ratio > 0.9 and max_similarity_ratio <= 1.0:
        logger.info('Possible character already added: ' + \
                     movie_character_name)
        return True
    else:
        return False


def check_mentioned_characters(char_from_scene, movie_line, characters_list):
    """
    Checks for mentioned movies characters and adds them to the list
    """
    for mentioned_character in characters_list:
        # Find which characters are mentioned in the movie line
        if mentioned_character.name.lower() in movie_line.lower():
            # Add the mentioned characters to the list of the character that
            # it is mentioning them
            for mentioning_character in characters_list:
                if char_from_scene == mentioning_character.name:
                    mentioning_character.add_mentioned_character(mentioned_character.name)
                    break


def get_df_from_conn(i_query):
    """
    This function creates a connection to the database
    Returns a df according to the input query

    i_query -> query to be returned to the dataframe
    """

    engine = sql.create_engine(
        'mysql://root:girafa@127.0.0.1:3306/movies?charset=utf8&use_unicode=True',
        pool_size=100,
        pool_recycle=3600,
        )
    db = engine.connect()
    my_df = pd.read_sql(i_query, con=db)
    db.close()

    return my_df


def write_table_to_my_sql(i_df, i_table_name, i_command):
    """
    This function writes the df created to the database
    It will also execute a command according to the input

    i_df -> Input dataframe that will be written to the database
    i_table_name -> Table that will contain that dataframe
    i_command -> SQL command to be executed
    """

    engine = sql.create_engine(
        'mysql://root:girafa@127.0.0.1:3306/movies?charset=utf8&use_unicode=True',
        pool_size=100,
        pool_recycle=3600)
    db = engine.connect()

    db.execute('DROP TABLE IF EXISTS ' + i_table_name)

    i_df.to_sql(i_table_name,
                con=engine,
                if_exists='replace',
                chunksize=1000,
                index=False)

    if i_command != '':
        db.execute(i_command)

    return
