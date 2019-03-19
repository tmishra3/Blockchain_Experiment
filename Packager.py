from Attributes import Attributes
from AttributeType import AttributeType
from File import File
import FileIO
import Encryption
import time
import DevMessage

packageSymbol = b'&'

def package(listFiles=[]):

    packageHeader = packageSymbol

    packageContents = []

    for file in listFiles:
        if file.returnFileLoaded() == True and type(file) is File:

            packageContents += [str(file)]
            fileSize = FileIO.getFileSize(file)
            packageHeader += str(fileSize).encode() + packageSymbol

    packageEnd = packageSymbol

    packageContents = [packageHeader] + packageContents + [packageEnd]

    return packageContents

def unPackage(self, fileName):

    if FileIO.doesFileExist(fileName):

        try:
            open_file = open(fileName, 'rb')
        except:
            return False

        fileStart = 0
        sepIndex = []
        headerFile = b''
        charRead = b''

        while True:

            fileStart += 1
            charRead = open_file.read(1)

            if FileContainer.separator == charRead:
                sepIndex.append(fileStart)
            if FileContainer.headerStartEnd == charRead:
                break
            if charRead == b'':
                break

            headerFile += charRead

        open_file.close()

    try:
        headerData = []
        for i in range(0, len(sepIndex) - 1):
            headerData.append(int(headerFile[sepIndex[i]:sepIndex[i + 1] - 1].decode('utf-8')))
    except:
        print("Header file in data file is corrupted.")
        return False

    if len(headerData) > 0:

        offset = len(headerFile) + 1

        for i in range(0, len(headerData)):
            # try:
            self.addFile()

            file_open = open(str(self.files[i]), 'wb')
            open_file = open(fileName, 'rb')

            file_open.write(open_file.read()[offset:headerData[i] + offset])

            file_open.close()
            open_file.close()

            self.files[i].importExisting(str(self.files[i]))

            if self.files[i].returnFileLoaded() == True:
                pass
            else:
                del self.files[-1]

            offset += headerData[i]
        # except:
        # print("Issue with parsing files in data file.")
        # return False

        self.packaged = True
        return True

    else:
        os.remove(fileName)

