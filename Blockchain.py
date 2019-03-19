import hashlib
import datetime
import sqlite3
import cryptography
from cryptography.fernet import Fernet


class block:

    def __init__(self, blockNumber, prevHash, blockLogic, blockData, isEncrypted = False):

        #The values a block will contain:
        self.blockNumber = blockNumber
        self.thisHash = ""
        self.prevHash = prevHash #as a string
        self.blockLogic = blockLogic #as a string (TEMPORARILY UNTIL ACTUAL LOGIC OBJECT PASSED)
        self.blockData = blockData #as a string
        self.isEncrypted = isEncrypted

        if self.isEncrypted == True:

            blockFileName = 'Block_Number_' + str(self.blockNumber) + '_Encryption_Key.txt'
            blockFile = open(blockFileName, "wb")

            self.blockKey = Fernet.generate_key()
            self.blockEnc = Fernet(self.blockKey)

            dataHash = self.findHash(self.blockData)
            logicHash = self.findHash(self.blockLogic)

            #blockFile.write(self.blockNumber)
            blockFile.write(self.blockKey)
            #blockFile.write(dataHash)
            #blockFile.write(logicHash)
            blockFile.close()

            self.encryptBlockValues()

        self.BlockCreation = ""#as a string (stores date/time of block creation)
        self.BlockModification = ""
        self.blockCreation = self.setTimeMod() #set date/time of block creation.
        self.blockModification = self.blockCreation #set modification date to creation date/time.

        self.calculateHash() #Calculate the hash of current block.

    def findHash(self, myString):

        return str(hashlib.sha256(myString.encode('utf-8')).hexdigest())

    def encryptBlockData(self):

        self.blockData = self.blockEnc.encrypt(self.blockData.encode())

    def encryptBlockLogic(self):

        self.blockLogic = self.blockEnc.encrypt(self.blockLogic.encode())

    def encryptBlockValues(self):

        self.encryptBlockData()
        self.encryptBlockLogic()

    def calculateHash(self):

        cumulativeData = self.prevHash + self.returnBlockLogic() + self.returnBlockData()
        self.thisHash = self.findHash(cumulativeData)

    def returnIsEncrypted(self):
        return int(self.isEncrypted)

    def returnBlockNumber(self):
        return self.blockNumber

    def returnHash(self):
        return self.thisHash

    def returnPrevHash(self):
        return self.prevHash

    def returnBlockLogic(self):
        if self.isEncrypted == True:
            return self.blockLogic.decode('utf-8')
        else:
            return self.blockLogic

    def returnBlockData(self):

        if self.isEncrypted == True:
            return self.blockData.decode('utf-8')
        else:
            return self.blockData

    def returnBlockCreation(self):
        return self.BlockCreation

    def modifyBlockData(self, newData): #modify this block's data.

        self.blockData = newData
        self.encryptBlockData()
        self.BlockModification = self.setTimeMod()

    def modifyBlockLogic(self, newLogic): #modify this block's logic.

        self.blockLogic = newLogic
        self.encryptBlockLogic()
        self.BlockModification = self.setTimeMod()

    def modifyPrevHash(self, newPrevHash): #modify the value of the previous hash

        self.prevHash = newPrevHash
        self.BlockModification = self.setTimeMod()

    def setTimeMod(self):

        return str(datetime.datetime.now()) #return current time and date..

    def __str__(self): #overloaded function to print a block in string return form.

        return (self.returnPrint())

    def __repr__(self): #Overloaded function to represent the block.

        return (self.returnPrint())

    def returnPrint(self): #the way a certain block will print.

        return "THIS HASH: " + self.returnHash() + "\nPREV HASH: " + self.returnPrevHash() + "\nCODE: " + self.returnBlockLogic() + "\nDATA: " + self.returnBlockData()
########################################################################################################################


class blockDataBase:

    def __init__(self, nameDataBase):

        self.nameDataBase = nameDataBase
        self.conn = sqlite3.connect(self.nameDataBase)

        self.c = self.conn.cursor()

        try:
            self.c.execute("""CREATE TABLE blockChain (
                                    id integer PRIMARY KEY,
                                    prev text,
                                    curr text,
                                    logic text,
                                    data text,
                                    cryp integer
                                    )""")
        except sqlite3.Error as er:
            print("\nLoading information from database " + self.nameDataBase + "\n as it already exists.\n")

        self.conn.close()


    def addBlockDB(self, myBlock, printConfirm = False):

        self.conn = sqlite3.connect(self.nameDataBase)

        self.c = self.conn.cursor()


        myBlockN = myBlock.returnBlockNumber()
        myPrev = myBlock.returnPrevHash()
        myHash = myBlock.returnHash()
        myLogic = myBlock.returnBlockLogic()
        myData = myBlock.returnBlockData()
        isEncr = myBlock.returnIsEncrypted()

        try:
            self.c.execute("INSERT INTO blockChain (id,prev,curr,logic,data,cryp) VALUES (?, ?, ?, ?, ?, ?)",
                           (myBlockN, myPrev, myHash, myLogic, myData, isEncr))

            self.conn.commit()

            if printConfirm == True:
                print("\nNew block with ID=" + str(myBlockN) + " added to table blockChain in Database: " + self.nameDataBase)


        except sqlite3.Error as er2:
            print("\nBlock with unique ID=" + str(myBlockN) + " already exists in table blockChain of Database: " + self.nameDataBase)

        self.conn.close()

    def printDatabase(self):

        self.conn = sqlite3.connect(self.nameDataBase)
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM blockChain")

        rows = self.c.fetchall()

        for row in rows:
            print(row)

        self.conn.close()

    def returnIsEncrypted(self, primaryKey):

        self.conn = sqlite3.connect(self.nameDataBase)
        self.c = self.conn.cursor()

        self.c.execute("SELECT cryp FROM blockChain WHERE id = %d" % (primaryKey))

        isEnc = int((self.c.fetchone())[0]) #convert tuple to integer.

        self.conn.close()

        return isEnc

    def returnLogic(self, primaryKey):

        self.conn = sqlite3.connect(self.nameDataBase)
        self.c = self.conn.cursor()

        self.c.execute("SELECT logic FROM blockChain WHERE id = %d" % (primaryKey))

        logicAtId = self.c.fetchall()
        logicAtId = ''.join(logicAtId[0])

        self.conn.close()

        return logicAtId.encode()

    def returnData(self, primaryKey):

        self.conn = sqlite3.connect(self.nameDataBase)
        self.c = self.conn.cursor()

        self.c.execute("SELECT data FROM blockChain WHERE id = %d" % (primaryKey))

        dataAtId = self.c.fetchall()
        dataAtId = ''.join(dataAtId[0])

        self.conn.close()

        return dataAtId.encode()


    def decryptBlock(self, keyFile, primaryKey, destinationFile):

        if (self.returnIsEncrypted(primaryKey) == 1):

            try:
                loadFile = open(keyFile,"rb") #Obtain key from keyFile and load.
                key = loadFile.read()
                loadFile.close()

                #Obtain encrypted data and logic from SQL table at primary key value.
                myData = self.returnData(primaryKey)
                myLogic = self.returnLogic(primaryKey)

                try: #Try to use key from file to decrypt logic and data.

                    cryptoEngine = Fernet(key)  # Create a Fernet process with Key from file.
                    decryptData = cryptoEngine.decrypt(myData)
                    decryptLogic = cryptoEngine.decrypt(myLogic)

                    writeFile = open(destinationFile,"w")
                    writeFile.write("Block "+str(primaryKey)+'\n')
                    writeFile.write("Data: " + decryptData.decode('utf-8')+'\n')
                    writeFile.write("Logic: " + decryptLogic.decode('utf-8'))
                    writeFile.close()

                    print("\nSUCCESS: " + keyFile + " has been decrypted and the output has been stored to " + destinationFile)

                except:

                    print("\nERROR: Unable to decrypt. Key or Data has been corrupted.")

            except IOError:

                print("\nERROR: Unable to either find or read " + keyFile)
        else:

            print("\nERROR: Block " + str(primaryKey) + " is not encrypted.")

