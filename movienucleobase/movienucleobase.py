import argparse

import logging
import logging.config

import imsdb.filehandlers
import imsdb.dataextraction
import imsdb.dataadjustment
import imsdb.datastructures

from processMovieSingleScene import *

if __name__ == '__main__':
    # Process arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='Name of the file containing the movie script')

    parser.add_argument('--nscenes',
                        help='Number of scenes to process')

    parser.add_argument('--movie_title',
                        help='The title of the movie')

    parser.add_argument('--sub_wikia',
                        help='The subwikia associated to the movie')

    args = parser.parse_args()

    if args.nscenes:
        nscenes = int(args.nscenes)
    else:
        nscenes = 0

    # Sets up the logging system
    logconfig = 'logging_config.ini'
    logfile = 'movienucleobase.log'
    logging.config.fileConfig(logconfig, defaults={'logfilename': logfile})
    logger = logging.getLogger(__name__)

    movie = imsdb.datastructures.MovieData(args.movie_title, args.sub_wikia)

    # Loads the IMSDb movie script into a list
    # The script terminates if the script is empty
    imsdb_movie_script = imsdb.filehandlers.open_movie_script(args.filename)

    # Extract the movie characters
    movie.characters = imsdb.dataextraction.extract_characters(imsdb_movie_script)

    # Retrieve each character's real name
    for character in movie.characters:
        character.real_name = imsdb.dataadjustment.retrieve_character_real_name(
            movie.sub_wikia,
            character.name)

    # Return the list of the scenes in the movie
    movie.scenes = imsdb.dataextraction.extract_scenes(imsdb_movie_script)

    # Draw the interactions
    for i, scene in enumerate(movie.scenes):
        logger.debug('\nNew scene: ' + str(i))
        logger.debug(re.sub('\s{2,}', '\n', scene))
        logger.debug(processMovieSingleScene(scene, movie.characters, i))

        if nscenes>0 and i==nscenes:
            break

    # List all info
    movie.print_info()
        
    print ''
    for character in movie.characters:
        character.listCharactersInteractedWith()
        character.listMentionedCharacters()
        character.listAppearedScenes()
