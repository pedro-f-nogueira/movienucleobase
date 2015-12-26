import argparse
import numpy as np
import pandas as pd
import os.path
import logging

from classMovieCharacter import *
from extractMovieCharacters import *
from extractMovieScenes import *
from processMovieSingleScene import *

if __name__ == '__main__':

    # Process arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Name of the file containing the movie script")
    parser.add_argument("--loglevel", help="Level of the logging messages")
    parser.add_argument("--nscenes", help="Number of scenes to process")
    args = parser.parse_args()
    
    if not args.filename:
        print "Error: No input file specified."
        quit()

    filename = args.filename

    if not os.path.isfile(filename):
        print "Error: The file " + filename + " does not exist."
        quit()

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

    # Open movie script
    with open(filename, 'r') as myfile:
        movieScript = myfile.read().replace("\n", "").split("<br> <table width=\"100%\">")[1]

    logging.debug("#####################################################")
    logging.debug("####")
    logging.debug("#### Extracting the characters")
    logging.debug("####")
    logging.debug("#####################################################")

    # Extract movie characters
    movieCharactersList = extractMovieCharacters(movieScript)

    logging.debug("")
    logging.debug("#####################################################")
    logging.debug("####")
    logging.debug("#### Establishing interactions between characters")
    logging.debug("####")
    logging.debug("#####################################################")

    # Return the list of the scenes in the movie
    movieScenesList = extractMovieScenes(movieScript)

    # Draw the interactions
    i = 0

    for movieScene in movieScenesList:
        logging.debug("New scene...")
        logging.debug("   " + re.sub("\s{2,}", "\n", movieScene))
        logging.debug(processMovieSingleScene(movieScene, movieCharactersList))
        logging.debug("")

        if nscenes>0 and i==nscenes:
            break

        i = i + 1

    for l in movieCharactersList:
        l.listCharactersInteractedWith()
        l.listMentionedCharacters()

    quit()

    # Draw the interactions
    n = 1
    MovieInteractions = []
    for movieScene in movieScenesList:
        print "Changing scene..."
        print "   " + re.sub("\s{2,}", "\n", movieScene)
        print processMovieSingleScene(movieScene, movieCharactersList)

        MovieInteractions.append(processMovieSingleScene(movieScene, movieCharactersList))
        MovieInteractions.append(n)
        n += 1

        print ""

        if n==3:
            break

    quit()

    Df_Id = []
    Df_Names = []
    Df_N_scenes_real = []
    Df_Chars_Int = [[]]
    Df_Scenes_Int = [[]]
    id = 0

    for l in movieCharactersList:
        Df_Id.append(id)
        Df_Names.append(l.name)
        Df_N_scenes_real.append(l.n_scenes_real)

        for scene in range(len(MovieInteractions) - 1):
            if scene % 2 == 0:
                #Get chars interacted
                if l.name in MovieInteractions[scene]:
                    for char in MovieInteractions[scene]:
                        if l.name != char and char not in Df_Chars_Int[id]:
                            Df_Chars_Int[id].append(char)
            else:
                #Get Scene Numbers
                if l.name in MovieInteractions[scene-1] and l.name not in Df_Scenes_Int[id]:
                    Df_Scenes_Int[id].append(scene)

        id = id + 1
        Df_Chars_Int.append([])
        Df_Scenes_Int.append([])

    DataFrameMovie = {
                      'Id' : pd.Series(Df_Id),
                      'Name' : pd.Series(Df_Names),
                      'N_Scene_Appearances' : pd.Series(Df_N_scenes_real),
                      'Chars_Interacted' : pd.Series(Df_Chars_Int),
                      'Scene_Appearances' : pd.Series(Df_Scenes_Int)
                      }

    df = pd.DataFrame(DataFrameMovie)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
