import socket
import time
import sys
import os
import math

DEBUG = 0
def errorMessage(terminate = True):
    print("The program neededs the following arguments \nServer Location (IP address) \"-w\" (if you wish to upload obmit for download) Filename")
    print("The command line command should look like \nclient serverLocation \"-w\" Filename")
    if terminate:
        exit(0)

def requestFile(filename, s):
    print("Request : ", filename)
    time.sleep(.1)
    responce = s.recv(64).decode('ascii')
    if responce != "FILE FOUND":
        print(responce)
        print("file not found")
        exit(0)
    file = open(filename, "wb")
    timeout = 0
    fileData = []
    data =''
    while timeout < 3:
        data = s.recv(1024)
        if(data):
            fileData.append(data)
            timeout = 0
        else:
            timeout += 1
            time.sleep(.1)
    for d in fileData:
        file.write(d)
    file.close()
    print("file received and saved")

def sendFile(filename, s, host):
    print("sending {} to {}".format(filename, host[0]))

    file = open(filename, 'rb')
    fileSize =  os.stat(filename).st_size
    tenth = math.ceil(fileSize/10)
    for i in range(10):
        fileData = file.read(tenth)
        s.send(fileData)
        print("Sent {}% of {}".format((i+1)*10, filename))
    print("Finished sending {} to {}".format(filename, host[0]))
    return 1

def requstBytes(filename, s, host, bs, be):
    time.sleep(.1)
    responce = s.recv(64).decode('ascii')
    if responce != "FILE FOUND":
        print("file not found")
        exit(0)
    msg = bs+"-"+be
    time.sleep(.5)
    if DEBUG == 1:
        print(msg)
    s.send(msg.encode())
    print("Request : ", filename)
    file = open(filename, "wb")
    timeout = 0
    fileData = []
    data =''
    while timeout < 3:
        data = s.recv(1024)
        if(data):
            fileData.append(data)
            timeout = 0
        else:
            timeout += 1
            time.sleep(.1)
    for d in fileData:
        file.write(d)
    file.close()

byteStart = 0
byteEnd = 0
if len(sys.argv) < 3:
    errorMessage()
host = sys.argv[1]
if(sys.argv[2] == "-w"):
    requestType = "w"
    filename = sys.argv[3]
elif(sys.argv[2] == "-s"):
    byteStart = sys.argv[3]
    if(sys.argv[4] == "-e"):
        byteEnd = sys.argv[5]
        requestType = 's'
        filename = sys.argv[6]
    else:
        errorMessage()
else:
    requestType = 'r'
    filename = sys.argv[2]
if int(byteEnd) < int(byteStart):
    errorMessage()
if DEBUG == 1:
    print("filename {}\nbyteStart {} byteEnd {}\nrequest type {}".format(filename, byteStart, byteEnd, requestType))
s = socket.socket()
port = 8080
s.connect((host,port))
request = filename + requestType
s.send(request.encode())

for i in range(len(filename)):
    if filename[len(filename) - i - 1] == "/":
        filename = filename[len(filename)-i:]
if requestType == "w":
    sendFile(filename, s, host)
elif requestType == "r":
    requestFile(filename, s)
elif requestType == "s":
    requstBytes(filename, s, host, byteStart, byteEnd)
