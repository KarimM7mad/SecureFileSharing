from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import random as rnd
import string, csv, os


# generate key
def generateRandomEncryptionKey():
    key = ""
    for i in range(0, 16, 1):
        key += rnd.choice(string.ascii_letters)
    return key


# create file to encapsulate Encrypted file
def createFileData(plainTxt, filename, creatorID="14p6004", creatorEmail="14p6004@eng.asu.edu.eg"):
    key = generateRandomEncryptionKey()
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    # create file Header
    originalMsgSize = str(len(plainTxt))
    fileHeader = originalMsgSize + "," + creatorID + "," + creatorEmail
    # encrypt the plainTxt
    cipherTxt = iv + cipher.encrypt(plaintext=plainTxt)
    # store the data in a new file
    f = open(file=filename, mode="w+")
    f.write(fileHeader + "\n")
    f.write(bytes(cipherTxt).decode(encoding="latin-1"))
    f.close()
    # CSV to store information about file
    recordsFile = open(file="records.csv", mode="a+")
    fileFields = ['dataFilename', 'key', 'iv']
    writerObj = csv.DictWriter(recordsFile, fieldnames=fileFields)
    # if the file is empty
    if os.stat("records.csv").st_size == 0:
        writerObj.writeheader()
    writerObj.writerow({'dataFilename': filename, 'key': key, 'iv': bytes(iv).decode(encoding="latin-1")})
    recordsFile.close()


# decrypt the file and get original File content
def retrieveFileContent(filename, decryptionKey):
    desiredRecord = None
    try:
        tmpfr = open("records.csv", newline='')
    except FileNotFoundError:
        return False
    reader = csv.DictReader(tmpfr)
    for row in reader:
        if row['dataFilename'] == filename and row['key'] == decryptionKey:
            desiredRecord = row
            break
    tmpfr.close()
    if desiredRecord is None:
        print("no Match found")
        return
    dataFile = open(file=desiredRecord['dataFilename'], mode="r")
    dataFileContent = dataFile.read()
    dataFile.close()
    dataFileContent = dataFileContent.split("\n")
    # create the cipher
    cipher = AES.new(desiredRecord['key'], AES.MODE_CFB, bytes(desiredRecord['iv'], 'latin-1'))
    # obtain bytes , from string array and decrypt
    decryptedDataContentInFile = str(cipher.decrypt(bytes(dataFileContent[1], 'latin-1')))
    headerData = dataFileContent[0]
    originalPlainTxtLength = int(headerData.split(",")[0])
    originalPlainTxtCreatorID = headerData.split(",")[1]
    originalPlainTxtEmail = headerData.split(",")[2]
    plainTxtItself = decryptedDataContentInFile[(decryptedDataContentInFile.__len__() - originalPlainTxtLength - 1):decryptedDataContentInFile.__len__() - 1]
    print(plainTxtItself)


# encrypt the AES key of the file desired using public key recieved
def encryptAESKey(requesterPublicKey, filename):
    try:
        tmpfr = open("records.csv", newline='')
    except FileNotFoundError:
        return False
    reader = csv.DictReader(tmpfr)
    for row in reader:
        if row['dataFilename'] == filename:
            desiredRecord = row
            break
    tmpfr.close()
    if desiredRecord is None:
        print("no Match found")
        return
    print(desiredRecord)
    return requesterPublicKey.encrypt(desiredRecord['key'].encode('latin-1'), 32)[0]


# key1 = RSA.generate(2048)
# f = open('myPrivateKey.pem','w')
# f.write((key1.exportKey('PEM')).decode(encoding='latin-1'))
# f.close()
# f = open('myPublicKey.pem','w')
# f.write((key1.publickey().exportKey('PEM')).decode(encoding='latin-1'))
# f.close()
# stamp for creating a file and adding content to it
# plainTxt = "This is a demo3 for data for testing"
# filename = "tstFile3.txt"
# createFileData(plainTxt, filename)

print("----------------------------------------------")
xx = input("enter 1 for reciever and 0 for sender: ")

if xx == "0":
    filename = input("enter the filename that u wish to access=>")
    publicKeyfileName = input("enter the public key file(.pem)=>")
    ff = open(publicKeyfileName, 'r')
    key = ff.read()
    key = bytes(key, 'latin-1')
    keyObj = RSA.importKey(key)
    enc_data = encryptAESKey(requesterPublicKey=keyObj, filename=filename)
    fx = open(file="encKey.txt", mode="wb+")
    fx.write(enc_data)
    fx.close()
# requester part , sending a request reaction
elif xx == "1":
    filename = input("enter the filename that u wish to access=>")
    privateKeyFileName = input("enter the private key file(.pem)=>")
    recievedKeyfileName = input("Enter the Encrypted Key recieved filename=>")
    ff = open(privateKeyFileName, 'r')
    key = ff.read()
    key = bytes(key, 'latin-1')
    keyObj = RSA.importKey(key)
    fff = open(recievedKeyfileName, 'rb')
    key2 = fff.read()
    decKey = (keyObj.decrypt(key2)).decode('latin-1')
    print("the File Decryption Key is =>"+str(decKey))
    retrieveFileContent(filename, decKey)
