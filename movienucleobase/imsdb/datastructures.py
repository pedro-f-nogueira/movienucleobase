"""
.. module:: datastructures
    :synopsis: A module that provides the data structures to store movie data

.. moduleauthor:: Pedro Araujo <pedroaraujo@colorlesscube.com>
.. moduleauthor:: Pedro Nogueira <pedro.fig.nogueira@gmail.com>
"""

import logging


class MovieData:
    """This class contains all information related to the movie being analyzed.

    This class stores mostly characters and scenes and it provides a number of
    methods to access to these attributes.

    Attributes:
        title (str): Movie title
        sub_wikia (str): Sub-wikia related to the movie. Used for completing
        information about the movies' characters
        characters (list of MovieCharacter): List of all characters in the movie
        scenes (list of str): List of all scenes from the movie
    """

    def __init__(self, title, sub_wikia):
        """This function initializes the movie information.
        
        Args:
            title (String): Movie title
            sub_wikia (String): The sub-wikia related to the movie

        Returns:
            None
        """

        self.title = title
        self.sub_wikia = sub_wikia

    def set_characters(self, characters):
        """Set the characters.
        
        Args:
            characters (list of MovieCharacter): List of characters extracted
            from the movie script

        Returns:
            Bool: Always returns True.
        """

        self.characters = characters
        return True

    def set_scenes(self, scenes):
        """Set the movie scenes.
        
        Args:
            scenes (list of str): List of all scenes from the movie

        Returns:
            Bool: Always returns True.
        """

        self.scenes = scenes
        return True

    def get_title(self):
        """Return the movie title as a string.
        
        Returns:
            String: Movie title
        """

        return self.title

    def get_sub_wikia(self):
        """Return the movie sub-wikia
        
        Returns:
            String: Movie sub-wikia
        """

        return self.sub_wikia

    def get_characters(self):
        """Return the movie characters
        
        Returns:
            List of MovieCharacter: Movie characters
        """

        return self.characters

    def get_scenes(self):
        """Return the movie scenes
        
        Returns:
            List of string: Movie scenes
        """

        return self.scenes

    def print_info(self):
        """Print the movie information:
            - Movie title
            - Sub-wikia
            - All of the characters' names
        """

        print "Title of the movie:"
        print "    - " + self.title
        print "Sub-wikia:"
        print "    - " + self.sub_wikia

        self.print_characters()

    def print_characters(self):
        """List the movie characters' names:
            - Movie script names
            - Real names
        """

        print "Characters of the movie:"

        for character in self.characters:
            print "    - " + character.name + " ; " + character.real_name


class MovieCharacter:
    def __init__(self, name, real_name = '', gender = ''):
        self.name = name
        self.real_name = real_name
        self.gender = gender
        self.charactersInteractedWith = [[]]
        self.mentionedCharacters = [[]]
        self.appearedScenes = []

        self.charactersInteractedWith = filter(None, self.charactersInteractedWith)
        self.mentionedCharacters = filter(None, self.mentionedCharacters)
        self.appearedScenes = filter(None, self.appearedScenes)

    def set_real_name(self, real_name):
        self.real_name = real_name

        return True

    def get_real_name(self, real_name):
        return self.real_name

    def get_name(self, name):
        return self.name

    def addCharactersInteractedWith(self, nameList):
        addedCharacter = []
        nameListLength = len(nameList)

        if nameListLength==0:
            print "[Error][addCharactersInteractedWith()] Invalid nameList"
        else:
            for l1 in nameList:
                listElementFound = 0

                for l2 in self.charactersInteractedWith:
                    if l1!=self.name or l1==self.name and nameListLength==1:
                        if l2[0] in l1:
                            addedCharacter.append(l2[0])
                            l2[1] = l2[1] + 1
                            listElementFound = 1
                            break
                    else:
                        listElementFound = 1

                if listElementFound==0:
                    addedCharacter.append(l1)
                    self.charactersInteractedWith.append([l1, 1])

            logging.debug("The character " + self.name + " interacted with: " + ", ".join(addedCharacter))

    def addMentionedCharacter(self, name):
        listElementFound = 0

        for l in self.mentionedCharacters:
            if l[0]==name:
                l[1] = l[1] + 1
                listElementFound = 1
                break

        if listElementFound==0:
            self.mentionedCharacters.append([name, 1])

        logging.debug("The character " + self.name + " mentioned " + name)

    def addAppearedScene(self, nScene):
        logging.debug("The character " + self.name + " appears in the scene " + str(nScene))
        self.appearedScenes.append(nScene)

    def listCharactersInteractedWith(self):
        if len(self.charactersInteractedWith)>0:
            print "The character " + self.name + " interacted with:"

            for l in self.charactersInteractedWith:
                print "    - " + l[0] + " " + str(l[1]) + " times"
        else:
            print "The character " + self.name + " did not have any interactions."

    def listMentionedCharacters(self):
        if len(self.mentionedCharacters):
            print "The character " + self.name + " mentioned the following characters:"

            for l in self.mentionedCharacters:
                print "    - " + l[0] + " " + str(l[1]) + " times"
        else:
            print "The character did not mentioned anyone."

    def listAppearedScenes(self):
        if self.appearedScenes:
            print "The character " + self.name + " appeared in the following scenes: " + ", ".join(str(i) for i in self.appearedScenes)
        else:
            print "The character did not appear in any scenes."


