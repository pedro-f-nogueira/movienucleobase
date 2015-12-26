import re
import difflib

from classMovieCharacter import *

def extractMovieCharacters(movieScript):
    movieCharactersExtracted    = []
    movieCharactersList         = []
    movieCharacterAlreadyListed     = 0

    for m in re.finditer(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', movieScript):
        movieCharactersExtracted.append(m.group("movie_char"))
    
    for l1 in movieCharactersExtracted:
        movieCharacterAlreadyListed = 0

        # Consider valid characters the names that are centered
        numberWhitespaces = len(l1) - len(l1.lstrip(' '))

        if numberWhitespaces<20 or numberWhitespaces>30:
            continue
        
        # Remove "(V.O.)" and "(CONT'D)" from characters' names
        tmp = l1.split("(")[0]
        tmp = " ".join(tmp.split())
    
        # Check if the character was already collected in the list
        for l2 in movieCharactersList:

            # The "Fellowship of the Ring" script sometimes misspells "FRODO" as "FRO DO"
            # This function attempts to fix that
            similatityBetweenStrings = difflib.SequenceMatcher(None, tmp, l2.name).ratio()
            sameString = 0

            if similatityBetweenStrings>0.9 and similatityBetweenStrings<1.0:
                sameString = 1

            if tmp in l2.name and sameString==0:
                movieCharacterAlreadyListed = 1
                l2.n_scenes_real = l2.n_scenes_real + 1
    
        if movieCharacterAlreadyListed==0:
            print "Adding character... " + tmp
            movieCharactersList.append(classMovieCharacter(tmp, 0, [[]]))

    return movieCharactersList
