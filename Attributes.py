import os
import Encryption
import FileIO
from AttributeType import AttributeType
import Labeler
import DevMessage

#Does not deal with files. Only with byts and values.

class Attributes:

    def __init__(self, attrTypes=[]):

        self.attributes = {}
        self.fileName = None
        self.fileLoaded = False

        self.addAttribute(attrTypes)

    def addAttribute(self, attrTypes=[]):

        for attrType in attrTypes:

            if type(attrType) is AttributeType:

                if attrType in self.attributes:
                    pass
                else:
                    self.attributes[attrType] = attrType.defaultOutput()

                    if self.fileLoaded == True:
                        self.loadFileAttributes(self.fileName)

            else:
                DevMessage.printDev("One or more types not of Type: <AttributeType>")
                pass

    def removeAttribute(self, attrType):

        if type(attrType) is AttributeType:

            elementRemoved = True

            try:
                self.attributes.pop(attrType)
            except:
                elementRemoved = False
            else:
                if self.fileLoaded == True:
                    self.loadFileAttributes(self.fileName)
            finally:
                return elementRemoved

        else:
            return False

    def resetAttributes(self):

        for attr, value in self.attributes.items():
            self.attributes[attr] = attr.defaultOutput()

        self.fileName = None
        self.fileLoaded = False

    def pullFileAttributes(self, fileName):

        backUp = self.attributes
        returnValue = True

        for attr, values in self.attributes.items():

            value = attr.action(fileName)

            if value != None:
                self.attributes[attr] = value

            else:
                self.attributes = backUp
                returnValue = False
                break

        if returnValue == True:
            self.fileName = fileName
            self.fileLoaded = True

        return returnValue

    def setAttributeValueWhere(self, value, attrName = ''):

        for attrType, value in self.attributes.items():
            if attrType.name == attrName:
                self.attributes[attrType] = value
                return True

        return False

    def setAttributesValuesAll(self, attrValues=[]):

        counter = 0
        backUp = self.attributes

        try:

            for index, values in self.attributes.items():
                correctedValue = index.defaultOutput(attrValues[counter])
                self.attributes[index] = correctedValue
                counter += 1

            return True

        except:

            DevMessage.printDev("Failed to set attribute values.")
            self.attributes = backUp
            return False

    def returnAttributeValuesAll(self):

        listAttrValues = []

        for attrType, value in self.attributes.items():
            listAttrValues.append(value)

        return listAttrValues

    def returnAttributeValueWhere(self, attrName = 'fileName'): #Return attribute where attr = "some attribute"

        for attrType, value in self.attributes.items():

            if attrType.name == attrName:
                return value

        return None

    def returnNumberAttributes(self):

        return len(self.attributes)

    def returnAttributeKind(self, attrType):

        value = 0

        kind = attrType.kind
        if kind == 'str':
            value = ''
        if kind == 'int':
            value = 0

        return value

    def returnAttributeSymbols(self):

        listAttrSymbols = []

        for attrType, value in self.attributes.items():
            listAttrSymbols.append(attrType.symbol)

        return listAttrSymbols

    def returnAttributeList(self):

        listAttrType = []

        for attrType, value in self.attributes.items():

            listAttrType.append(attrType)

        return listAttrType