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

        self._title = title
        self._sub_wikia = sub_wikia

    @property
    def title(self):
        return self._title 

    @property
    def sub_wikia(self):
        return self._sub_wikia

    @property
    def characters(self):
        """Return the movie characters
        
        Returns:
            List of MovieCharacter: Movie characters
        """

        return self._characters

    @characters.setter
    def characters(self, x):
        """Set the characters.
        
        Args:
             x (list of MovieCharacter): List of characters extracted
            from the movie script
        """

        self._characters = x

    @property
    def scenes(self):
        """Return the movie scenes
        
        Returns:
            List of string: Movie scenes
        """

        return self._scenes

    @scenes.setter
    def scenes(self, x):
        """Set the movie scenes.
        
        Args:
            x (list of str): List of all scenes from the movie
        """

        self._scenes = x

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
    def __init__(self, name):
        self.name = name
        self.charactersInteractedWith = [[]]
        self.mentionedCharacters = [[]]
        self.appearedScenes = []

        self.charactersInteractedWith = filter(None, self.charactersInteractedWith)
        self.mentionedCharacters = filter(None, self.mentionedCharacters)
        self.appearedScenes = filter(None, self.appearedScenes)

    @property
    def name(self):
        return self._name

    @property
    def real_name(self):
        return self._real_name

    @real_name.setter
    def real_name(self, x):
        self._real_name = x

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, x):
        self._gender = x

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


