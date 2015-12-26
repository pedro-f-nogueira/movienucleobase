import logging

class classMovieCharacter:
    def __init__(self, name, n_scenes_real, charactersInteractedWith, mentionedCharacters):
        self.name = name
        self.n_scenes_real = n_scenes_real
        self.charactersInteractedWith = charactersInteractedWith
        self.mentionedCharacters = mentionedCharacters

        self.charactersInteractedWith = filter(None, self.charactersInteractedWith)
        self.mentionedCharacters = filter(None, self.mentionedCharacters)

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
