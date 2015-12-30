import argparse

import logging
import logging.config

import imsdb.filehandlers
import imsdb.dataextraction
import imsdb.dataadjustment

from classMovieCharacter import *
from processMovieSingleScene import *
from plotCharacterTimeline import *
from extractCharacterGender import *

if __name__ == '__main__':
    # Process arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Name of the file containing the movie script')
    parser.add_argument('--nscenes', help='Number of scenes to process')
    args = parser.parse_args()

    if args.nscenes:
        nscenes = int(args.nscenes)
    else:
        nscenes = 0

    # Sets up the logging system
    logging.config.fileConfig('logging_config.ini', defaults={'logfilename': 'movienucleobase.log'})
    logger = logging.getLogger(__name__)

    # Loads the IMSDb movie script into a list
    # The script terminates if the script is empty
    imsdb_movie_script = imsdb.filehandlers.open_movie_script(args.filename)

    # Extract the movie characters
    movieCharactersList = imsdb.dataextraction.extract_movie_characters(imsdb_movie_script)

    # Resolve each character's name
    for l in movieCharactersList:
        l.real_name = imsdb.dataadjustment.resolve_movie_character_real_name("lotr" , l.name)

    # Return the list of the scenes in the movie
    movieScenesList = imsdb.dataextraction.extract_movie_scenes(imsdb_movie_script)

    # Draw the interactions
    for i, movieScene in enumerate(movieScenesList):
        logger.debug('\nNew scene...')
        logger.debug(re.sub('\s{2,}', '\n', movieScene))
        logger.debug(processMovieSingleScene(movieScene, movieCharactersList, i))

        if nscenes>0 and i==nscenes:
            break

    # List all info
    print 'The movie characters are:'
    for l in movieCharactersList:
        print '    - ' + l.real_name + ' (' + l.gender + ')'
        
    print ''
    for l in movieCharactersList:
        l.listCharactersInteractedWith()
        l.listMentionedCharacters()
        l.listAppearedScenes()
