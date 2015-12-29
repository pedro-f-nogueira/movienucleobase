import logging
import wikia
import unidecode

def resolveMovieCharactersNames(sub_wikia, characterName):
    resolvedCharacterName = wikia.search(sub_wikia, characterName)[0]

    logging.debug("resolveMovieCharactersNames(): Resolved " + characterName + " to " + resolvedCharacterName)

    return resolvedCharacterName

def resolve_real_movie_character_name(sub_wikia, movie_character_name):
    logger = logging.getLogger(__name__)

    movie_character_real_name = resolveMovieCharactersNames(sub_wikia, movie_character_name)

    if "List of" in movie_character_real_name:
        logger.debug("Rejecting possible invalid character: " + movie_character_real_name)
        movie_character_real_name = "none"
    else:
        movie_character_real_name = movie_character_real_name.split("(")[0].strip(" ")

    movie_character_real_name = unidecode.unidecode(unicode(movie_character_real_name))

    return movie_character_real_name
