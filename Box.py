from File import File
import Packager
import FileIO
import random
import string
import Encryption
import os
import time
import DevMessage

class Box:

    def __init__(self, blockNumber=-1): #FINE

        self.blockNumber = blockNumber
        self.files = []
        self.packaged = False

    def __contains__(self, fileName):

        return self.fileInBox(fileName)

    def __str__(self):
        return str(self.returnFileNames())

    def __add__(self, fileName):

        if type(fileName) is File:
            self.files.append(fileName)

        if type(fileName) is str:
            newFile = File(fileName)
            if newFile.returnFileLoaded():
                self.files.append(newFile)
            else:
                self.deleteFileObject(newFile)

        return self

    def __sub__(self, fileName):

        if type(fileName) is str:
            self.removeFile(fileName=fileName)

        return self

    def addFile(self, fileName = ''): #FINE

        if type(fileName) is str:

            if self.fileInBox(fileName) == False:

                newFile = File()

                if fileName != '':

                    successfulIngest = newFile.ingestFile(fileName)

                    if successfulIngest == True:

                        self.files.append(newFile)
                    else:
                        FileIO.deleteFile(newFile)
                else:
                    self.files.append(newFile)

            else:

                DevMessage.printDev("File with name already exists.")
        else:
            DevMessage.printDev("You are attempting to load a non-file.")

    def addLabeledFile(self, fileName): #FINE

        newFile = File()

        try:
            successfulImport = newFile.importExisting(str(fileName))

            if successfulImport:

                self.files.append(newFile)
                return True

            else:

                DevMessage.printDev("Failed to import file.")
                FileIO.deleteFile(newFile)
                return False

        except:

            DevMessage.printDev("File with name does not exist.")
            return False

    def removeFile(self, fileName = ''):

        index = self.returnFileIndex(fileName)

        if index != None:
            FileIO.deleteFile(self.files[index])
            self.files.pop(index)
            return True

        return False

    def dump(self):

        for files in self.files:
            FileIO.deleteFile(files)

        self.files = []
        self.packaged = False

    def bundle(self):

        packageContents = Packager.package(self.files)

        thisBox = "Box_" + str(self.blockNumber) + ".dat"
        success = FileIO.bytesOrFilesToFile(thisBox,packageContents)

        if success == True:
            DevMessage.printDev("Box is bundled.")
        if success == False:
            DevMessage.printDev("Couldn't bundle box.")

    def fileInBox(self, fileName):

        if fileName in self.returnFileNames():
            return True
        else:
            return False

    def returnFile(self, fileName = ''):

        index = self.returnFileIndex(fileName)
        return self.files[index]

    def returnFileNames(self):

        fn = []
        for files in self.files:
            fn.append(files.returnAttributeValueWhere(attrName='fileName'))

        return fn

    def returnFileIndex(self, fileName):

        try:
            return self.returnFileNames().index(str(fileName))
        except:
            return None

    def returnFileLabels(self):

        hf = []

        for files in self.files:
            hf.append(files.returnLabelsList())

        return hf

    def deleteFileObject(self, fileObj):

        FileIO.deleteFile(str(fileObj))
