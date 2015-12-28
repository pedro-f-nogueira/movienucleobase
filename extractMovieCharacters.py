import re
import difflib
import logging
import unidecode

from classMovieCharacter import *
from resolveMovieCharactersNames import *

def extractMovieCharacters(movieScript, sub_wikia):
    logging.debug("extractMovieCharacters(): Extracting the characters...")

    movieCharactersExtracted    = []
    movieCharactersList         = []
    movieCharacterAlreadyListed = 0

    for m in re.finditer(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', movieScript):
        movieCharactersExtracted.append(m.group("movie_char"))
    
    for l1 in movieCharactersExtracted:
        # Consider valid characters the names that are centered
        numberWhitespaces = len(l1) - len(l1.lstrip(' '))

        if numberWhitespaces<20 or numberWhitespaces>30:
            logging.debug("extractMovieCharacters(): Rejecting possible invalid character due to the number of whitespaces at the start of the string (" + str(numberWhitespaces) + "): " + l1)
            continue
        
        # Remove "(V.O.)" and "(CONT'D)" from characters' names
        tmp = l1.split("(")[0]
        tmp = " ".join(tmp.split())

        if "&amp;" in tmp or not tmp:
            logging.debug("extractMovieCharacters(): Rejecting possible invalid character: " + tmp)
            continue

        characterAlreadyAdded = 0
        for l2 in movieCharactersList:
            # The "Fellowship of the Ring" script sometimes misspells "FRODO" as "FRO DO"
            # This function attempts to fix that
            similatityBetweenStrings = difflib.SequenceMatcher(None, tmp.lower(), l2.name.split(" ")[0].lower()).ratio()

            if similatityBetweenStrings>0.9 and similatityBetweenStrings<1.0:
                logging.debug("extractMovieCharacters(): Possible character already added: " + tmp)
                characterAlreadyAdded = 1

        if characterAlreadyAdded==1:
            continue

        tmp2 = resolveMovieCharactersNames(sub_wikia, tmp)

        if "List of" in tmp2:
            logging.debug("extractMovieCharacters(): Rejecting possible invalid character: " + tmp2)
            tmp2 = "none"
        else:
            tmp2 = tmp2.split("(")[0].strip(" ")

        tmp = unidecode.unidecode(tmp)

        movieCharacterAlreadyListed = 0

        # Check if the character was already collected in the list
        for l2 in movieCharactersList:
            if tmp in l2.name:
                movieCharacterAlreadyListed = 1
                l2.n_scenes_real = l2.n_scenes_real + 1
    
        if movieCharacterAlreadyListed==0:
            logging.debug("extractMovieCharacters(): Adding character... " + tmp)
            movieCharactersList.append(classMovieCharacter(tmp, tmp2, "", 0, [[]], [[]], []))

    return movieCharactersList
