import argparse
import re
import numpy as np
import pandas as pd

class classMovieCharacter:
    def __init__(self, name, n_scenes_real, otherCharactersInteracted):
        self.name = name
        self.n_scenes_real = n_scenes_real
        self.otherCharactersInteracted = otherCharactersInteracted

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
             if tmp in l2.name:
                movieCharacterAlreadyListed = 1
                l2.n_scenes_real = l2.n_scenes_real + 1
    
        if movieCharacterAlreadyListed==0:
            print "Adding character... " + tmp
            movieCharactersList.append(classMovieCharacter(tmp, 0, [[]]))

    return movieCharactersList

def extractMovieScenes(movieScript):
    p = re.compile(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', re.MULTILINE | re.DOTALL)
    text = []

    for m in re.finditer(ur'(<pre>BLACK SCREEN|<b>EXT\.|<b>INT\.)(?P<movie_text>.*?)(?=<b>(EXT\.|INT\.))', movieScript):
        text.append(m.group("movie_text"))
     
    return text

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

def processing_stuff():
    print "\n###########################################"
    print "###  Extracting characters      "
    print "###########################################\n"
    
    characters_extracted = []
    characters_list = []
    
    for m in re.finditer(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', movieScript):
        characters_extracted.append(m.group("movie_char"))
    
    print "Printing characters without post-processing..."
    
    for l in characters_extracted:
        print l
    
        # Remove "(V.O.)" and "(CONT'D)" from characters' names
        tmp = l.split("(")[0]
    
        # Check if the character was already collected in the list
        if tmp not in characters_list:
            characters_list.append(tmp)
    
    print "\nPrinting characters with post-processing..."
    
    for l in characters_list:
        print l
    
    print "\n###########################################"
    print "###  Associating characters to the lines"
    print "###########################################\n"
    
    lines_extracted = []
    
    for m in re.finditer(ur'<b>(?!EXT)(?!SUPER)(?P<movie_char>.*?)<\/b>(?P<movie_text>.*?)(?=<b>)', movieScript):
        str = m.group("movie_text")
        # The join(str.split()) will remove all the extra spaces from the extracted movie line
        lines_extracted.append(' '.join(str.split()))
    
    for line in lines_extracted:
        for char in characters_list:
            if char in line:
                print "The character '" + char + "' appears in the following line:\n" + line

if __name__ == '__main__':
    movieScript = ""
    movieScenesList = []

    # Process arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of the file containing the movie script")
    args = parser.parse_args()
    
    if not args.filename:
        filename = "lotr.html"
    else:
        filename = args.filename

    print filename

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
