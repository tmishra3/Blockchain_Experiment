import Encryption
from Box import FileContainer
from File import File
import os

firstBlock = FileContainer()
firstBlock.unPackage('Block_-1.dat')

def addFile():
    fileName = input("Enter File to Add: ")
    firstBlock.addFile(fileName=fileName)

def importFile():
    fileName = input("Enter ingested file to import: ")
    firstBlock.importFile(fileName)

def removeFile():
    fileName = input("Enter File to Remove: ")
    firstBlock.removeFile(fileName=fileName)

def extractFile():
    fileName = input("Enter File to Extract: ")
    firstBlock.extractWhere(fileName=fileName)

def packageFile():
    firstBlock.package()
    print("Packaged.\n")

def generateRSA():
    print("Generating RSA Key Pair")
    print(Encryption.generateRSAKeyPair())
    print()

def encryptFile():
    getKey = input("Enter Public Key: ")
    getInput = input("Enter File to Encrypt: " )
    firstBlock.encryptWhere(getKey,fileName=getInput)

def decryptFile():
    getKey = input("Enter Private Key: ")
    getInput = input("Enter File to Decrypt: " )
    firstBlock.decryptWhere(getKey,fileName=getInput)

def printFiles():
    #name, size, encrypt

    listFiles = firstBlock.returnFileHeaders()
    numFiles = len(listFiles)
    contentFiles = firstBlock.returnFileExtensions()

    counter = 1
    for files in listFiles:
        if contentFiles != '.pem':
            isEnc = (files[2]=="No")*"" + (files[2]=="Yes")*"[E] "
            print(str(counter) + ". " + isEnc + "["+ files[0] + toBytes(files[1]) + "] Hash:[" + files[3][:7] + "...]")
        counter += 1
    print()

def toBytes(bytes):

    value = ''

    if bytes < 1024:
        value = str(bytes) + " B)"
    if bytes >= 1024 and bytes < 1048576:
        value = str(round(bytes/1024,2)) + " KB)"
    if bytes >= 1048576:
        value = str(round(bytes/1024/1024,2)) + " MB)"

    return " (" + value

while True:

    #os.system('cls' if os.name == 'nt' else 'clear')
    print()
    printFiles()

    print("(1) Ingest New File")
    print("(2) Remove File")
    print("(3) Extract File")
    print("(4) Encrypt File (Public Key)")
    print("(5) Decrypt File (Private Key)")
    print("(6) Generate RSA Key Pair")
    print("(7) Package File")
    print("(8) Import Ingested File")
    print("(9) Exit\n")

    getInput = int(input("Choice: "))

    if getInput == 1:
        addFile()
    if getInput == 2:
        removeFile()
    if getInput == 3:
        extractFile()
    if getInput == 4:
        encryptFile()
    if getInput == 5:
        decryptFile()
    if getInput == 6:
        generateRSA()
    if getInput == 7:
        packageFile()
    if getInput == 8:
        importFile()
    if getInput == 9:
        break
