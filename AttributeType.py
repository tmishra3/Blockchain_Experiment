import FileIO
import Encryption
import DevMessage

#This file contains information about every file attribute.
#It's important to note that fileName, fileSize, fileEncrypt, fileHash, and fileExt are
#the included ones. If you wish to include more, take the following steps:
#
#1) First define how the value is to be stored. As an int or a str.
#2) Define whether it is a toggled value (ie, like fileEncrypt)
#3) Define its return behavior in the action() function.
#4) Define its acceptable values in the validValue() function.

class AttributeType:

    max_fileName_length = 255
    min_fileName_length = 1

    max_fileSize = 209715200 #200 MB
    min_fileSize = 0 #0 Bytes.

    def __init__(self, name, kind):

        self.name = name
        self.setSymbol()
        self.kind = kind

    def __repr__(self):

        return str(self.name)

    def setSymbol(self):

        if self.name == 'fileName':
            self.symbol = '?'
        elif self.name == 'fileSize':
            self.symbol = '%'
        elif self.name == 'fileHash':
            self.symbol = '#'
        elif self.name == 'fileExt':
            self.symbol = '&'
        else:
            self.symbol = None

    #Define additional attributes by following the pattern below.
    def action(self, fileName):

        if FileIO.doesFileExist(fileName) == True:

            if self.name == 'fileName':
                return fileName
            elif self.name == 'fileSize':
                return FileIO.getFileSize(fileName)
            elif self.name == 'fileHash':
                return Encryption.calculateHashFromBytes(fileName.encode() + Encryption.fileToByteString(fileName))
            elif self.name == 'fileExt':
                return FileIO.returnFileExtension(fileName)
            else:
                DevMessage.printDev("Action for attribute name does not exist. Please define in file or check syntax.")
                return None
        else:
            DevMessage.printDev("Unable to pull file attribute as file does not exist.")
            return None

    def defaultOutput(self, input = ''):

        if self.kind == 'str':
            return str(input)
        elif self.kind == 'int':
            try:
                return int(input)
            except:
                return 0
        else:
            return None

    def validAttributeValue(self, attrValue):

        if self.name == 'fileName':

            return self.private_validFileName(attrValue)

        elif self.name == 'fileSize':

            return self.private_validFileSize(attrValue)

        elif self.name == 'fileHash':

            return self.private_validFileHash(attrValue)

        elif self.name == 'fileExt':

            return self.private_validFileExt(attrValue)
        else:

            return None

    def maximumCharLength(self, length):

        if self.name == 'fileName':
            return length <= 255
        elif self.name == 'fileSize':
            return length <= 9
        elif self.name == 'fileHash':
            return length <= 64
        elif self.name == 'fileExt':
            return length <= 256
        else:
            return None

########################################################################################################################
#                                                 PRIVATE FUNCTIONS
########################################################################################################################

    def private_isLetterOrNumber(self, myString, charExc=[]):

        for char in myString:
            if not char.isalpha() and not char.isdigit() and char not in charExc:
                return False

        return True

    def private_isLetter(self, myString):

        for char in myString:
            if not char.isalpha():
                return False

        return True

    def private_isNumber(self, myString, charExc=[]):

        for char in myString:
            if not char.isdigit():
                return False

        return True

    def private_charFreq(self, myString):

        charFreq = {}

        for char in myString:
            if char in charFreq:
                charFreq[char] = charFreq[char] + 1
            else:
                charFreq[char] = 1

        return charFreq

########################################################################################################################
#                                                 PRIVATE FUNCTIONS
########################################################################################################################

    def private_validFileName(self, attrValue):

        if len(attrValue) > AttributeType.min_fileName_length and attrValue!= None:
            return len(attrValue) <= AttributeType.max_fileName_length and \
                   self.private_isLetterOrNumber(attrValue, charExc=['_', '-', '(', ')', ' ', '.']) == True and \
                   attrValue[0:1] != '_' and self.private_isNumber(attrValue[0:1]) == False
        else:
            return False

    def private_validFileSize(self, attrValue):

        try:
            int(attrValue)
            if int(attrValue) >= 0:
                return True
            else:
                return False
        except:
            return False

    def private_validFileHash(self, attrValue):

        return len(attrValue) == 64

    def private_validFileExt(self, attrValue):

        if len(attrValue) > 0:
            return '.' in attrValue and len(attrValue) <= 256 and attrValue[0:1] == '.' and \
                   self.private_isLetterOrNumber(attrValue, ['.']) == True
        if len(attrValue) == 0:
            return True