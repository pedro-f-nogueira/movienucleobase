import argparse
import re

import logging
import logging.config

import imsdb.filehandlers
import imsdb.dataextraction
import imsdb.dataadjustment
import imsdb.datastructures

if __name__ == '__main__':
    # Process arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='Name of the file containing the movie script')

    parser.add_argument('--config',
                        help='Name of the configuration file')

    parser.add_argument('--nscenes',
                        help='Number of scenes to process')

    parser.add_argument('--movie_title',
                        help='The title of the movie')

    parser.add_argument('--sub_wikia',
                        help='The subwikia associated to the movie')

    parser.add_argument('--bypass_gender_retrieval',
                        help='Bypass the retrieval of gender from freebase',
                        action='store_true')

    args = parser.parse_args()

    if args.nscenes:
        nscenes = int(args.nscenes)
    else:
        nscenes = 0

    # Setup the logging system
    logconfig = 'logging_config.ini'
    logfile = 'movienucleobase.log'
    logging.config.fileConfig(logconfig, defaults={'logfilename': logfile})
    logger = logging.getLogger(__name__)

    movie = imsdb.datastructures.MovieData(args.movie_title, args.sub_wikia)

    # Loads the IMSDb movie script into a list
    # The script terminates if the script is empty
    imsdb_movie_script = imsdb.filehandlers.open_movie_script(args.filename)

    if not imsdb_movie_script:
        print "Error: Empty movie script."
        quit()

    # Extract the movie characters
    movie.characters = imsdb.dataextraction.extract_characters(imsdb_movie_script)

    # Retrieve each character's real name
    for character in movie.characters:
        character.real_name = imsdb.dataadjustment.retrieve_character_real_name(
            movie.sub_wikia,
            character.name)

    # Clean up list
    real_name_list = []

    for character in movie.characters:
        if character.real_name not in real_name_list:
            real_name_list.append(character.real_name)
        else:
            movie.characters.remove(character)

    # Identify the gender of each character
    for character in movie.characters:
        if not args.bypass_gender_retrieval:
            character.real_name = imsdb.dataadjustment.retrieve_character_gender(character.real_name)
        else:
            dict_gender = imsdb.filehandlers.load_config_file(args.config, 'gender')
            character.gender = dict_gender[character.name.lower()]

    # Return the list of the scenes in the movie
    movie.scenes = imsdb.dataextraction.extract_scenes(imsdb_movie_script)

    # Draw the interactions
    for i, scene in enumerate(movie.scenes):
        logger.debug('\nNew scene: ' + str(i))
        logger.debug(re.sub('\s{2,}', '\n', scene))
        logger.debug(imsdb.dataextraction.process_movie_single_scene(scene, movie.characters, i))

        if nscenes>0 and i==nscenes:
            break

    # List all info
    movie.print_info()
        
    print ''
	
    for character in movie.characters:
        character.list_characters_interacted_with()
        character.list_mentioned_characters()
        character.list_appeared_scenes()

	# Builds Excel with 5 columns
    # 1 - Id
    # 2 - Character name
    # 3 - Character gender
    # 4 - Number of scenes in which he appeared
    # 5 - Character he interacted with

    #imsdb.DataFrame.build_1st_excel(movie.characters)

    # Builds Excel with 4 columns relative to interactions
    # 1 - Id
    # 2 - Character 1
    # 3 - Character 2
    # 4 - Number of Interactions
    #imsdb.DataFrame.build_2nd_excel(movie.characters)