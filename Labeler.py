#Bundles attribute objects into header and footer data describing the file attributes.
#Unbundles header footer data from already bundled file and returns validated attributes. Returns None if fails.

from Attributes import Attributes
from AttributeType import AttributeType
import FileIO
import Encryption
import time
import DevMessage

separators_top = b'*'
separators_bottom = b'*'

def label(attr): #Returns [header top, header bottom]

    if type(attr) is Attributes:

        # Format of header.
####################################

        listAttr = attr.returnAttributeValuesAll()
        listSymbol = attr.returnAttributeSymbols()

        top = b''
        counter = 0

        for values in listAttr:
            top += listSymbol[counter].encode()
            top += str(values).encode()
            counter += 1

        top += separators_top

        # Format of footer.
####################################

        bottom = separators_bottom

        #Return header and footer as a list.

        return [top, bottom]

    else:
        return None

def unLabel(fileName, attr): #Returns ([header attributes], bytes from file, header_bottom] or none if error.

    fileExists = FileIO.doesFileExist(fileName)

    if fileExists and type(attr) is Attributes: #if file actually exists and the other
        #included file is of type attribute.

        #Here, we're obtaining a list of attributeType objects and the respective symbols. This could be
        #one (just listAttr). Probably something to clean up later.

        listAttr = attr.returnAttributeList()
        listSymbol = attr.returnAttributeSymbols()

        #Adding the end '%' symbol for the sake of convenience of searching.
        listSymbol.append(separators_top.decode('utf-8')) #Adding the last symbol to find as the separator.

        open_file = open(fileName,'rb')

        #Will store value of header here.
        headerFile = b''

        #Which symbol are we looking for?
        symbolCount = 0 #number of symbols.
        currentSymbol = listSymbol[symbolCount] #current symbol we are searching for.
        symbolIndex = [] #index of symbols.

        validHeader = True #Do we have a valid header? If certain conditions fail, our header file is either
        #corrupted or of the incorrect format.
        attributes = [] #Stores the parsed attributes.
        currentIndex = 0 #Current index of byte being read.

        attributeLength = -1 #Starting from -1 because the first char doesn't count in the data, it's the symbol.

        while True:

            currentIndex += 1 #basic iterator. Keeps track of each bit read.
            attributeLength += 1 #keeps track of stream of attribute characters coming in. If they exceed a value that
            #they should not be close to (such as a hash stream reading without terminating), it will automatically
            #quit out.
            byteRead = open_file.read(1) #Read one byte.
            headerFile += byteRead #Save that one byte to the header file.

            if byteRead == b'': #If we've reached the end of our file and we haven't parsed, we're fucked.
                validHeader = False
                break

            #First element must be first symbol.
            if currentIndex == 1:

                if listSymbol[symbolCount].encode() != byteRead: #If the first element is not the identifier for
                    #anything.
                    validHeader = False
                    break
                else: #otherwise, we have found a symbol that corresponds to an attribute.
                    symbolIndex.append(currentIndex) #Save its index into the symbolIndex list.
                    symbolCount += 1 #Mark number of symbols "found" as 1.
                    currentSymbol = listSymbol[symbolCount] #Current symbol is the next symbol in the list.
                    attributeLength = -1 #Starting back at -1.

            if currentIndex > 1: #if we're looking at an index greater than 1.

                #If our stream of characters after picking up a symbol exceeds a value that it should not,
                #we've failed. For example, if we are reading more than 9 characters for the stream of information
                #coming in for the file size, we've probably exceeded the worst case scenario and have bad data.
                if listAttr[symbolCount - 1].maximumCharLength(attributeLength) == False:
                    DevMessage.printDev("Failure...Value for " + str(listAttr[symbolCount-1]) + " is out of bounds.")
                    validHeader = False
                    break

                #TEMP FOR TESTING.
                #print("Length of " + str(listSymbol[symbolCount - 1]) + ": " + str(attributeLength) +
                #      ' / Byte Read: ' + byteRead.decode('utf-8'))
                #time.sleep(.07)

                if listSymbol[symbolCount].encode() == byteRead: #If we detect the symbol we "should" detect.

                    attributeLength = -1

                    #Now that we have 2 symbols, we can look at what's between and take that as an attribute.
                    attributes.append(headerFile[symbolIndex[symbolCount - 1]:currentIndex - 1].decode())

                    #Verify that the attribute is what it should be.
                    validValue = listAttr[symbolCount-1].validAttributeValue(attributes[symbolCount-1])

                    if validValue != True: #if our verification value is false, we need to quit.
                        DevMessage.printDev("Header validation failed for " + listAttr[symbolCount-1].name)
                        validHeader = False
                        break

                    symbolCount += 1 #Otherwise, we succeeded. Incremement # of symbols by 1.
                    symbolIndex.append(currentIndex) #Put in the current symbols's index and move on to the next symbol.

                    if symbolCount < len(listSymbol): #If we've not reached the end, set the next symbol in there.
                        currentSymbol = listSymbol[symbolCount]
                    else:
                        break #Otherwise, we've found everything. Break out.

        counter = 0
        fileSizeHeader = False

        for list in listAttr:
            if str(list) == 'fileSize':
                fileSizeHeader = True
                try:
                    if int(attributes[counter]) == FileIO.getFileSize(fileName) - len(headerFile) - len(separators_bottom):
                        break
                except:
                    validHeader = False
                    break
                else:
                    DevMessage.printDev("File size mismatch.")
                    validHeader = False
                    break
            else:
                pass
            counter += 1

        fileBytes = FileIO.fileToBytes(fileName,len(headerFile),-1*len(separators_bottom))

        if fileSizeHeader == False:
            validHeader = False
            DevMessage.printDev("No file size header found.")
        if validHeader == False:
            DevMessage.printDev("Invalid header file.")

        if validHeader == True and fileSizeHeader == True:
            return (attributes, fileBytes, separators_bottom)
        else:
            return None
    else:
        DevMessage.printDev("File does not exist.")

########################################################################################################################
#                                                 PRIVATE FUNCTIONS
########################################################################################################################

def private_isStringType(myString, type = 'int'):

    try:
        if type == 'int':
            int(myString)
        if type == 'encBool':
            if myString != 'No' and myString != 'Yes':
                raise ValueError
    except ValueError:
        return False
    else:
        return True
    finally:
        pass

def private_calculateFileSize(fileName, headerFile):

    return FileIO.getFileSize(fileName) - len(headerFile) - len(separators_bottom)

def private_encodeList(strValue=[]):

    returnList = []

    for values in strValue:
        returnList.append(values.encode())

    return returnList