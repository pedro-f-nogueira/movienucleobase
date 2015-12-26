import argparse
import numpy as np
import pandas as pd
import os.path

from classMovieCharacter import *
from extractMovieCharacters import *
from extractMovieScenes import *
from processMovieSingleScene import *

if __name__ == '__main__':
    movieScript = ""
    movieScenesList = []

    # Process arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Name of the file containing the movie script")
    args = parser.parse_args()
    
    if not args.filename:
        filename = "lotr.html"
    else:
        filename = args.filename


    if not os.path.isfile(filename):
        print "Error: The file " + filename + " does not exist."
        quit()

    # Open movie script
    with open(filename, 'r') as myfile:
        movieScript = myfile.read().replace("\n", "").split("<br> <table width=\"100%\">")[1]

    print "#####################################################"
    print "####"
    print "#### Extracting the characters"
    print "####"
    print "#####################################################"

    # Extract movie characters
    movieCharactersList = extractMovieCharacters(movieScript)

    print ""
    print "#####################################################"
    print "####"
    print "#### Establishing interactions between characters"
    print "####"
    print "#####################################################"

    # Return the list of the scenes in the movie
    movieScenesList = extractMovieScenes(movieScript)

    # Draw the interactions
    n = 1
    MovieInteractions = []
    for movieScene in movieScenesList:
        MovieInteractions.append(processMovieSingleScene(movieScene, movieCharactersList))
        n += 1

    Df_Id = []
    Df_Names = []
    Df_N_scenes_real = []
    Df_Chars_Int = [[]]
    Df_Scenes_Int = [[]]
    id = 0
    for l in movieCharactersList:
        Df_Id.append(n)
        Df_Names.append(l.name)
        Df_N_scenes_real.append(l.n_scenes_real)

        n = 1
        for scene in MovieInteractions:
            if n % 2 == 0:
                #Get chars interacted
                if l.name in scene:
                    for char in scene:
                        if l.name != char and char not in Df_Chars_Int[id]:
                            Df_Chars_Int[id].append(char)
            else:
                #Get Scene Numbers
                if l.name in scene and l.name not in Df_Scenes_Int[id]:
                    Df_Scenes_Int[id].append(scene)

            n = n + 1

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

    print df
