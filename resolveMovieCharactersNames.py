import wikia
import logging

def resolveMovieCharactersNames(sub_wikia, characterName):
    resolvedCharacterName = wikia.search(sub_wikia, characterName)[0]

    logging.debug("resolveMovieCharactersNames(): Resolved " + characterName + " to " + resolvedCharacterName)

    return resolvedCharacterName
