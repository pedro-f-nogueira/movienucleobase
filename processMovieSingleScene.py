import re

from classMovieCharacter import *

def processMovieSingleScene(movieScene, movieCharactersList):
    p = re.compile(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', re.MULTILINE | re.DOTALL)
     
    movieSceneElements = re.findall(p, movieScene)

    n                   = 0
    movieCharacterFound = ""
    CENAS = []

    for l1_tmp in movieSceneElements:
        for l1 in l1_tmp:
            # The elements of the list movieSceneElements are extracted in the following manner:
            #   [0] - Character name
            #   [1] - Character line
            #   [2] - Character name
            #   [3] - Character line
            #       ...
            if n%2==0:
                # Consider valid characters the names that are centered
                numberWhitespaces = len(l1) - len(l1.lstrip(' '))

                if numberWhitespaces<20 or numberWhitespaces>30:
                    n = n + 1
                    continue

                movieCharacterFound = l1.split("(")[0]
                movieCharacterFound = " ".join(movieCharacterFound.split())
                if movieCharacterFound not in CENAS and movieCharacterFound != "":
                    CENAS.append(movieCharacterFound)
            else:
                for l2 in movieCharactersList:
                    if l2.name.lower() in l1.lower():
                        print movieCharacterFound + " is interacting with " + l2.name

            n = n + 1
