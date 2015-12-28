import argparse
import numpy as np
import pandas as pd
import os.path
import logging

from classMovieCharacter import *
from extractMovieCharacters import *
from extractMovieScenes import *
from processMovieSingleScene import *
from plotCharacterTimeline import *
from extractCharacterGender import *

if __name__ == '__main__':

    # Process arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Name of the file containing the movie script")
    parser.add_argument("--loglevel", help="Level of the logging messages")
    parser.add_argument("--nscenes", help="Number of scenes to process")
    args = parser.parse_args()

    filename = args.filename

    if args.nscenes:
        nscenes = int(args.nscenes)
    else:
        nscenes = 0

    # Load logging
    fileLog = "movienucleobase.log"
    if os.path.isfile(fileLog):
        os.remove(fileLog)

    if args.loglevel:
        numeric_value = getattr(logging, args.loglevel.upper(), None)
        logging.basicConfig(filename="movienucleobase.log", level=numeric_value)
        logging.getLogger(__name__)

    # Open movie script
    with open(filename, 'r') as myfile:
        movieScript = myfile.read().replace("\n", "").split("<br> <table width=\"100%\">")[1]

    # Extract movie characters
    movieCharactersList = extractMovieCharacters(movieScript, "lotr")

    # List all info
    print "The movie characters are:"
    for l in movieCharactersList:
        print "    - " + l.name + " (" + l.gender + ")"

    # Return the list of the scenes in the movie
    movieScenesList = extractMovieScenes(movieScript)

    # Draw the interactions
    i = 0

    for movieScene in movieScenesList:
        logging.debug("New scene...")
        logging.debug("   " + re.sub("\s{2,}", "\n", movieScene))
        logging.debug(processMovieSingleScene(movieScene, movieCharactersList, i))
        logging.debug("")

        if nscenes>0 and i==nscenes:
            break

        i = i + 1

    # List all info
    print "The movie characters are:"
    for l in movieCharactersList:
        print "    - " + l.real_name + " (" + l.gender + ")"
        
    print ""
    for l in movieCharactersList:
        l.listCharactersInteractedWith()
        l.listMentionedCharacters()
        l.listAppearedScenes()
