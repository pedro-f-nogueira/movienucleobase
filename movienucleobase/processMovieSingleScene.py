import re
import logging

from classMovieCharacter import *

def processMovieSingleScene(movieScene, movieCharactersList, nScene):
    p = re.compile(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', re.MULTILINE | re.DOTALL)
     
    movieSceneElements = re.findall(p, movieScene)

    n = 0
    movieCharacterFromScene = ""
    charactersInteractedWith = []

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
                nWhitespacesinStartOfString = len(l1) - len(l1.lstrip(' '))

                if nWhitespacesinStartOfString<20 or nWhitespacesinStartOfString>30:
                    n = n + 1
                    continue

                movieCharacterFromScene = l1.split("(")[0]
                movieCharacterFromScene = " ".join(movieCharacterFromScene.split())

                if movieCharacterFromScene not in charactersInteractedWith and movieCharacterFromScene != "":
                    charactersInteractedWith.append(movieCharacterFromScene)
            else:
                for l2 in movieCharactersList:
                    if l2.name.lower() in l1.lower():
                        #print movieCharacterFromScene + " is mentioning " + l2.name

                        for l3 in movieCharactersList:
                            if l3.name==movieCharacterFromScene:
                                l3.add_mentioned_character(l2.name)
                                break

            n = n + 1

    for l1 in movieCharactersList:
        for l2 in charactersInteractedWith:
            if l1.name==l2:
                l1.add_characters_interacted_with(charactersInteractedWith)
                l1.add_appeared_scene(nScene)

    return charactersInteractedWith
