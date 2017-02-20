"""
.. module:: movienucleobase.py
   :synopsis: The main module

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import argparse
import re

import logging
import logging.config

import imsdb.filehandlers
import imsdb.dataextraction
import imsdb.dataadjustment
import imsdb.datastructures
import imsdb.gen_database
import imsdb.gen_dataframe
import imsdb.social_net as social_net

if __name__ == '__main__':
    # Process arguments from the command line
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument('filename',
                        help='Name of the file containing the movie script')

    PARSER.add_argument('--config',
                        help='Name of the configuration file')

    PARSER.add_argument('--nscenes',
                        help='Number of scenes to process')

    PARSER.add_argument('--sub_wikia',
                        help='The subwikia associated to the movie')

    PARSER.add_argument('--bypass_gender_retrieval',
                        help='Bypass the retrieval of gender from freebase',
                        action='store_true')

    ARGS = PARSER.parse_args()

    if ARGS.nscenes:
        NSCENES = int(ARGS.nscenes)
    else:
        NSCENES = 0

    # Setup the logging system
    LOGCONFIG = 'logging_config.ini'
    LOGFILE = 'movienucleobase.log'

    logging.config.fileConfig(LOGCONFIG, defaults={'logfilename': LOGFILE})
    LOGGER = logging.getLogger(__name__)

    MOVIE = imsdb.datastructures.MovieData(ARGS.sub_wikia)

    # Loads the IMSDb movie script into a list
    # The script terminates if the script is empty
    IMSDB_MOVIE_SCRIPT, MOVIE.title = imsdb.filehandlers.open_movie_script(ARGS.filename)

    if not IMSDB_MOVIE_SCRIPT:
        print "Error: Empty movie script."
        quit()

    # Extract the movie characters
    MOVIE.characters = imsdb.dataextraction.extract_characters(IMSDB_MOVIE_SCRIPT)

    # Retrieve each character's real name and adding id
    imsdb.dataextraction.get_real_name_and_id(MOVIE.characters, MOVIE)

    # Clean up list
    MOVIE.clean_up_character_list()

    # Identify the gender of each character
    # imsdb.dataextraction.get_gender(MOVIE.characters, ARGS)

    # Return the list of the scenes in the movie
    MOVIE.scenes = imsdb.dataextraction.extract_scenes(IMSDB_MOVIE_SCRIPT)

    # Draw the interactions
    for i, scene in enumerate(MOVIE.scenes):
        LOGGER.debug('\nNew scene: ' + str(i))
        LOGGER.debug(re.sub('\s{2,}', '\n', scene))
        LOGGER.debug(imsdb.dataextraction.process_movie_single_scene(scene
                                                                     , MOVIE.characters
                                                                     , i))

        if NSCENES > 0 and i == NSCENES:
            break

    # List all info
    #movie.print_info()

    #for character in movie.characters:
        #character.list_characters_interacted_with()
        #character.list_mentioned_characters()
        #character.list_appeared_scenes()

    # --- This part  of the main script if for data purposes ---

    # Builds dataframes
    df_chars = imsdb.gen_dataframe.build_df_chars(MOVIE)
    df_interactions = imsdb.gen_dataframe.build_df_interactions(MOVIE)
    df_mentions = imsdb.gen_dataframe.build_df_mentions(MOVIE)

    # Outputting to excel / database
    # wdata.write_df(df_chars, 'chars')
    # wdata.write_df(df_interactions, 'interactions')
    # wdata.write_df(df_chars, 'mentions')

    df_metrics = social_net.return_metrics(df_chars, df_interactions)

    # Creating a JSON for the social network
    imsdb.gen_dataframe.write_nodes_edges_to_json(df_metrics, df_interactions, 'ARGS.filename')

    #Builds database
    imsdb.gen_database.build_database(MOVIE)
