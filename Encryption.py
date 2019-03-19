from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
import random
import string

def generateRSAKeyPair(): #Generate a public key with a private key to send to someone. Returns the file name of the
    #public key.

    fileIndex = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    privateKey = "private" + fileIndex + ".pem"
    publicKey = "receiver" + fileIndex + ".pem"

    key = RSA.generate(2048)
    public_key = key.publickey().export_key()
    private_key = key.export_key()

    # generate private key.
    file_out = open(privateKey, "wb")
    file_out.write(private_key)

    # generate public key.
    file_out = open(publicKey, "wb")
    file_out.write(public_key)

    file_out.close()

    #self.publicKeys.update({publicKey: None})

    return publicKey

def fileToByteString(fileName):

    file_read = open(fileName,"rb")
    byteString = file_read.read()
    file_read.close()

    return byteString

def byteStringToFile(fileName, myBytes):

    file_read = open(fileName,"wb")
    file_read.write(myBytes)
    file_read.close()

def encryptBytesPublicKey(fileName, myBytes, publicKey): #Stores myBytes to fileName and uses publicKey to encrypt

    file_out = open(fileName, "wb")

    recipient_key = RSA.import_key(open(publicKey).read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(myBytes)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()

    return fileToByteString(fileName)

def decryptBytesPrivateKey(fileName, privateKey): #Takes fileName and decrypts using privateKey to myBytes.

    file_in = open(fileName, 'rb')

    private_key = RSA.import_key(open(privateKey).read())

    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    myBytes = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return myBytes

def calculateHashFromBytes(myBytes):

    hashFile = SHA256.new()
    hashFile.update(myBytes)
    return hashFile.hexdigest()

def calculateHashFromFile(fileName):

    myBytes = b''

    with open(fileName, 'rb') as open_file:
        myBytes = open_file.read()

    hashFile = SHA256.new()
    hashFile.update(myBytes)
    return hashFile.hexdigest()