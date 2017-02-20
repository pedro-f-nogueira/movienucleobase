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

    def __init__(self, sub_wikia):
        """This function initializes the movie information.
        
        Args:
            title (String): Movie title
            sub_wikia (String): The sub-wikia related to the movie

        Returns:
            None
        """

        #self._title = title
        self._sub_wikia = sub_wikia

    @property
    def title(self):
        """
        Returns the movie title
        """
        return self._title 

    @property
    def sub_wikia(self):
        """
        Returns the sub_wikia
        """
        return self._sub_wikia

    @property
    def characters(self):
        """Return the movie characters
        
        Returns:
            List of MovieCharacter: Movie characters
        """

        return self._characters

    @characters.setter
    def characters(self, argx):
        """Set the characters.
        
        Args:
             x (list of MovieCharacter): List of characters extracted
            from the movie script
        """

        self._characters = argx

    @property
    def scenes(self):
        """Return the movie scenes
        
        Returns:
            List of string: Movie scenes
        """

        return self._scenes

    @scenes.setter
    def scenes(self, argx):
        """Set the movie scenes.
        
        Args:
            argx (list of str): List of all scenes from the movie
        """

        self._scenes = argx

    def print_info(self):
        """Print the movie information:
            - Movie title
            - Sub-wikia
            - All of the characters' names
        """

        print 'Title of the movie:'
        print '    - ' + self.title
        print 'Sub-wikia:'
        print '    - ' + self.sub_wikia

        self.print_characters()

    def print_characters(self):
        """List the movie characters' names:
            - Movie script names
            - Real names
        """

        print 'Characters of the movie:'

        for character in self.characters:
            print '    - Name: ' + character.name + \
                  ' ; Real name: ' + character.real_name + \
                  ' ; Gender: ' + character.gender

    def clean_up_character_list(self):
        """
        Cleans the char list from some unwanted names
        """
        real_name_list = []

        for character in self.characters:
            if character.real_name not in real_name_list:
                real_name_list.append(character.real_name)
            else:
                self.characters.remove(character)

    def build_table_interactions(self):
        """
        Helps with the process of building the interations info
        Returns the info relative to char mentions in an id manner
        This way building the table is much easier
        returns ex:
        1 - Frodo
        2 - Sam
        3 - 1 -  Frodo id
        4 - 4 - Sam id
        5 - 6 - times they interacted
        """
        logger = logging.getLogger(__name__)

        source_name_list = []
        target_name_list = []
        source_id_list = []
        target_id_list = []
        weight_list = []
        interactions_list = ['']

        for source in self.characters:
            for target, value in source.characters_interacted_with.iteritems():
                for target_name in self.characters:

                    if len(source.appeared_scenes) > 1 and len(target_name.appeared_scenes) > 1 \
                            and target_name.name == target:
                        interaction = str(target) + str(source.name)
                        interaction_rev = str(source.name) + str(target)

                        if interaction not in interactions_list and interaction_rev not in interactions_list:
                            # Appends source and target names
                            source_name_list.append(source.name)
                            target_name_list.append(target)

                            # Appends source and target id's
                            source_id_list.append(source.id)

                            for char in self.characters:
                                if char.name == target:
                                    target_id_list.append(char.id)
                                    break

                            # Appends interaction weigth
                            weight_list.append(value)
                            interactions_list.append(interaction)

        logger.debug('Interaction:Source Name List\n' + ','.join(source_name_list))
        logger.debug('Interaction:Target Name List\n' + ','.join(target_name_list))
        logger.debug('Interaction:Source Id List\n' + ','.join(map(str, source_id_list)))
        logger.debug('Interaction:Target Id List\n' + ','.join(map(str, target_id_list)))
        logger.debug('Interaction:Weight List\n' + ','.join(map(str, weight_list)))

        return source_name_list, \
               target_name_list, \
               source_id_list, \
               target_id_list, \
               weight_list

    def build_table_mentions(self):
        """
        Helps with the process of building the mentions info
        Returns the info relative to char mentions in an id manner
        This way building the table is much easier
        returns ex:
        1 - Frodo
        2 - Sam
        3 - 1 -  Frodo id
        4 - 4 - Sam id
        5 - 6 - times they interacted
        """
        logger = logging.getLogger(__name__)

        source_name_list = []
        target_name_list = []
        source_id_list = []
        target_id_list = []
        weight_list = []

        for source in self.characters:
            for target, value in source.mentioned_characters.iteritems():
                for target_name in self.characters:
                    if len(source.appeared_scenes) > 1 and len(target_name.appeared_scenes) > 1 \
                            and target_name.name == target:
                        # Appends source and target names
                        source_name_list.append(source.name)
                        target_name_list.append(target)

                        # Appends source and target id's
                        source_id_list.append(source.id)

                        for char in self.characters:
                            if char.name == target:
                                target_id_list.append(char.id)
                                break

                        # Appends intereraction weigth
                        weight_list.append(value)

        logger.debug('Mention:Source Name List\n' + ','.join(source_name_list))
        logger.debug('Mention:Target Name List\n' + ','.join(target_name_list))
        logger.debug('Mention:Source Id List\n' + ','.join(map(str, source_id_list)))
        logger.debug('Mention:Target Id List\n' + ','.join(map(str, target_id_list)))
        logger.debug('Mention:Weight List\n' + ','.join(map(str, weight_list)))

        return source_name_list, \
               target_name_list, \
               source_id_list, \
               target_id_list, \
               weight_list

    def build_table_chars(self):
        """
        Helps with the process of building the chars info
        returns ex:
        1 - [1, 2, 3]
        2 - [Sam, Frodo, Legolas]
        3 - [Male, Male, Male]
        4 - [2, 3, 1] - Number of scenes appeared
        5 - [[1, 5], [2, 4, 6], [3]]
        """
        logger = logging.getLogger(__name__)

        df_id_1 = []
        df_names = []
        df_gender = []
        df_n_scenes_int = []
        df_scenes_int = []

        for char in self.characters:
            if len(char.appeared_scenes) > 1:
                df_id_1.append(char.id)
                df_names.append(char.name)
                df_gender.append(char.gender)
                df_n_scenes_int.append(len(char.appeared_scenes))
                df_scenes_int.append(char.appeared_scenes)

        logger.debug('Char Id \n' + ','.join(map(str, df_id_1)))
        logger.debug('Char Name\n' + ','.join(df_names))
        logger.debug('Char Gender\n' + ','.join(df_gender))
        logger.debug('N. Scenes appeared\n' + ','.join(map(str, df_n_scenes_int)))
        logger.debug('Scenes appeared\n' + ','.join(map(str, df_scenes_int)))

        return df_id_1, df_names, df_gender, df_n_scenes_int, df_scenes_int


class MovieCharacter:
    """
    Class with all the info relevant to the movie char
    """
    def __init__(self, name):
        """
        Iniates all the variables inerent to the movie char
        """
        self._id = id
        self._name = name
        self._real_name = ""
        self._gender = ""
        self._characters_interacted_with = {}
        self._mentioned_characters = {}
        self._appeared_scenes = []
        #missing appeared scenes relative to mentions

    @property
    def id(self):
        """
        Returns char id, ex: 1
        """
        return self._id

    @property
    def name(self):
        """
        Returns char name ex: Frodo
        """
        return self._name

    @property
    def real_name(self):
        """
        Returns char real name, ex: Frodo Baggins
        """
        return self._real_name

    @property
    def gender(self):
        """
        Returns char real name, ex: Male
        """
        return self._gender

    @property
    def appeared_scenes(self):
        """
        Returns a list of scenes in which the char appeared
        ex:[1, 6, 7, 8, 9, 11, 12, 13, 35, 86, 95]
        """
        return self._appeared_scenes

    @property
    def characters_interacted_with(self):
        """
        Returns a list of scenes in which the char appeared
        ex:[Frodo, Galadriel, Legolas]
        """
        return self._characters_interacted_with

    @property
    def mentioned_characters(self):
        """
        Returns a list of scenes in which the char was mentioned
        ex:[Frodo, Galadriel, Legolas]
        """
        return self._mentioned_characters

    @real_name.setter
    def real_name(self, argx):
        """
        Sets the char real name
        """
        self._real_name = argx

    @gender.setter
    def gender(self, argx):
        """
        Sets the char gender
        """
        self._gender = argx

    def add_characters_interacted_with(self, list_of_names, char_list):
        """
        The function will accept a list of characters that the present
        character interacted during a scene.

        It is desirable to add all of these characters to the list but
        the list will also contain the present character as well. So we
        need to make sure to exclude it from the list.

        But it is also possible that the character speaks with himself
        in the whole scene. This scenario also counts as well, so we
        only add the character if it is the only element in the list.
        """
        logger = logging.getLogger(__name__)

        # If the lists of names is empty, terminate the function immediately
        if len(list_of_names) <= 1:
            return False

        # Detect which characters were already added as interactions and
        # increase the respective counters of interactions
        for iter1 in set(list_of_names).intersection(self._characters_interacted_with):
            if iter1 in self._characters_interacted_with and iter1 != self.name:
                self._characters_interacted_with[iter1] += 1

        # Detect the characters that weren't added as interaction yet
        for iter2 in set(list_of_names).difference(self._characters_interacted_with):
            if iter2 in char_list and iter2 != self.name:
                added_character = iter2
                self._characters_interacted_with[iter2] = 1

        #logger.debug('The character ' + self.name + ' interacted with: ' + added_character)

        return True

    def add_appeared_scene(self, scene_number):
        """
        This function adds an appeared scene to the object movie char
        ex: Frodo appeared in scene 6
        """
        logger = logging.getLogger(__name__)

        logger.debug('The character ' + self.name + 
                     ' appears in the scene ' + str(scene_number))

        try:
            self._appeared_scenes.append(scene_number)
        except NameError:
            self._appeared_scenes = [scene_number]

    def add_mentioned_character(self, name):
        """
        This function adds an mentioned scene to the object movie char
        ex: Frodo mentioned Sam
        """
        logger = logging.getLogger(__name__)

        if name == self.name:
            return None

        if name in self.mentioned_characters:
            self._mentioned_characters[name] = \
                self._mentioned_characters[name] + 1
        else:
            self._mentioned_characters[name] = 1

        logger.debug('The character ' + self.name + ' mentioned ' + name)

    def list_characters_interacted_with(self):
        """
        Lists all the chars the char in question interacted with
        """
        if len(self._characters_interacted_with) > 0:
            print 'The character ' + self.name + ' interacted with:'

            for char in self._characters_interacted_with:
                print '    - ' + char + ' ' + \
                    str(self.characters_interacted_with[char]) + ' times'
        else:
            print 'The character ' + self.name + ' did\'t have any interactions'

    def list_mentioned_characters(self):
        """
        Lists all the chars the char mentioned
        """
        if len(self.mentioned_characters):
            print 'The character ' + self.name + ' mentioned the following characters:'

            for char in self.mentioned_characters:
                print '    - ' + char + ' ' + \
                    str(self.mentioned_characters[char]) + ' times'
        else:
            print 'The character did not mentioned anyone.'

    def list_appeared_scenes(self):
        """
        Lists all the scenes the char appeared in
        """
        if self.appeared_scenes:
            print 'The character ' + self.name + ' appeared in the following scenes: ' + \
                ', '.join(str(i) for i in self.appeared_scenes)
        else:
            print 'The character did not appear in any scenes.'




