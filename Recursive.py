import os
import FileIO
import time

def package(myPath):

    default_dir = os.getcwd()
    myDataFile = b''
    dataFile = myDataFile
    os.chdir(myPath)
    current = os.listdir()

    for something in current:

        if os.path.isdir(os.path.join(myPath,something)):
            print("Directory Found: " + something)

            dataFile += b"[" + something.encode() + b"]"
            dataFile += package(myPath + '/' + something + '/')
            dataFile += b"[/" + something.encode() + b"]"

        if os.path.isfile(os.path.join(myPath,something)):
            print("File Found: " + something)

            dataFile += b"(" + something.encode() + b")"
            dataFile += b"{" + str(os.path.getsize(os.path.join(myPath,something))).encode() + b"}"
            dataFile += open(myPath+'/'+something,'rb').read()

    os.chdir(default_dir)

    return dataFile

def unPackage(fileName, folderName):

    with open(fileName,'rb') as open_file:

        slow = 0
        currentPath = os.getcwd() + '/' + folderName + '/'
        os.makedirs(folderName)
        os.chdir(currentPath)

        readByte = b''
        temp = b''
        currentFile = b''

        while True:

            readByte = open_file.read(1)
            time.sleep(slow)

            if readByte == b'':
                break

            if readByte == b'[': #working with folder.

                while True:

                    readByte = open_file.read(1)
                    time.sleep(slow)

                    if readByte != b']':

                        temp += readByte
                    else:

                        if temp[0:1] != b'/':
                            print("Folder " + temp.decode('utf-8') + ' detected.')
                            os.mkdir(os.path.join(currentPath,temp.decode('utf-8')))
                            currentPath += '/' + temp.decode('utf-8')
                            print("Making Folder: " + temp.decode('utf-8') + " and moving into it.")
                            os.chdir(currentPath)
                            temp = b''
                            break

                        if temp[0:1] == b'/':
                            print("Folder termination detected. Moving one directory up.")
                            os.chdir('..')
                            currentPath = os.getcwd()
                            temp = b''
                            break

            if readByte == b'(':

                while True:

                    readByte = open_file.read(1)
                    time.sleep(slow)

                    if readByte != b')':

                        temp += readByte
                    else:
                        if not os.path.isdir(os.path.join(currentPath, temp.decode('utf-8'))):
                            print("File " + temp.decode('utf-8') + ' detected.')
                            open(os.path.join(currentPath, temp.decode('utf-8')), 'wb').close()
                            currentFile = temp.decode('utf-8')
                            temp = b''
                        break
            if readByte == b'{':

                while True:

                    readByte = open_file.read(1)
                    time.sleep(slow)

                    if readByte != b'}':

                        temp += readByte
                    else:

                        print("Creating file " + currentFile + "...")
                        with open(os.path.join(currentPath, currentFile), 'wb') as write_file:
                            write_file.write(open_file.read(int(temp)))
                        print("Data printed to " + currentFile)
                        temp = b''
                        break

        print("Process complete.")

myBytes = package(os.getcwd())
FileIO.bytesToFile('Package.dat',myBytes)
#unPackage('Package.dat','verify')
