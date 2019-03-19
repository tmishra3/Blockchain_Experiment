import os
import random
import string
import Encryption
import Labeler
import FileIO
from AttributeType import AttributeType
from Attributes import Attributes
import DevMessage

class File:

    separator = b'%'

    def __init__(self, fileName=''):

        #Custom declaration for used attributes.

        self.attr = Attributes([AttributeType('fileName', 'str'),
                                AttributeType('fileSize', 'int'),
                                AttributeType('fileHash', 'str'),
                                AttributeType('fileExt', 'str')])

        self.generateLabels()
        self.generateContentFile()

        self.fileLoaded = False

        if fileName != '':
            self.ingestFile(fileName)

    def __str__(self):

        return self.contentFile

    def generateContentFile(self): #Generates the temporary file in which the file is stored along with the header.

        randomCharacters = 6

        try:
            if self.contentFile != "":
                os.remove(self.contentFile)
        except:
            pass

        self.contentFile = "Temp" + "".join(random.choices(string.ascii_uppercase + string.digits, k=randomCharacters)) \
                           + ".tmp"

        open(self.contentFile,'wb').close()

    def generateLabels(self):

        self.labels = Labeler.label(self.attr)

    def pullFileAttributes(self, fileName):

        success = self.attr.pullFileAttributes(fileName)
        self.generateLabels()
        return success

    def resetAttributes(self):

        self.Attr.resetAttributes()
        self.fileLoaded = False
        self.generateLabels()

    def returnAttributeValueWhere(self, attrName='fileName'):
        return self.attr.returnAttributeValueWhere(attrName=attrName)

    def returnFileLoaded(self):
        return self.fileLoaded

    def returnFileBundle(self):
        self.generateLabels()
        return self.labels

    def returnAttributes(self):
        return self.attr.returnAttributeValuesAll()

    def returnLabelsList(self):

        return Labeler.label(self.attr)


    def ingestFile(self, fileName): #Returns True if successful and false if not.

        if self.pullFileAttributes(fileName) == True: #If we were able to pull attributes from file.

            try:
                FileIO.bytesToFile(self.contentFile, #Destination file.
                                   self.labels[0] + FileIO.fileToBytes(fileName) + self.labels[1]) #Header + data + footer
            except:
                DevMessage.printDev("Couldn't write temporary file.")
                return False
            else:
                self.fileLoaded = True
                #os.remove(self.Attr.returnAttributeWhere(attr='fileName'))
                return True
        else:
            DevMessage.printDev("Unable to ingest file, " + fileName)
            return False

    def importExisting(self, importFile):  # Attempts to import file from existing exported file.

        unBundle = Labeler.unLabel(importFile, self.attr)

        if unBundle != None:

            backUp = self.attr
            newAttrValues = unBundle[0]
            self.attr.setAttributesValuesAll(newAttrValues)

            # Obtain hash for data read.
            readBytes = unBundle[1]
            fileName = self.attr.returnAttributeValueWhere(attrName='fileName')
            fileHash = self.attr.returnAttributeValueWhere(attrName='fileHash')

            hashCheck = Encryption.calculateHashFromBytes(fileName.encode() + readBytes)

            if fileHash == hashCheck:
                self.generateLabels()
                os.remove(self.contentFile)
                self.contentFile = importFile
                self.fileLoaded = True
                DevMessage.printDev(importFile + " sucessfully loaded. All integrity checks passed.")
                return True
            else:
                DevMessage.printDev("Hash calculation mismatch for " + fileName + ". File may be corrupted. Import failed.")
                self.attr = backUp
                return False
        else:
            DevMessage.printDev("Import failed.")
            return False

    def extractThis(self):

        if self.fileLoaded == True:

            destFile = self.attr.returnAttributeValueWhere('fileName')
            startIndex = len(self.labels[0])
            endIndex = len(self.labels[1])

            FileIO.copyFile(self.contentFile, #Source
                            destFile, #Destination
                            startIndex, #Starting index
                            -1*endIndex)#Ending index

        elif self.fileLoaded == False:
            DevMessage.printDev("No file has been loaded.")