import socket
import time
import os
import math

DEBUG = 0

def sendFile(filename, conn, host):
    print("sending {} to {}".format(filename, host[0]))
    file = open(filename, 'rb')
    fileSize =  os.stat(filename).st_size
    tenth = math.ceil(fileSize/10)
    for i in range(10):
        fileData = file.read(tenth)
        conn.send(fileData)
        print("Sent {}% of {}".format((i+1)*10, filename))
    print("Finished sending {} to {}".format(filename, host[0]))
    return 1

def receiveFile(filename, conn, addr):
    file = open(filename, "wb")
    timeout = 0
    fileData = []
    data =''
    while timeout < 3:
        data = conn.recv(1024)
        if(data):
            fileData.append(data)
            timeout = 0
        else:
            timeout += 1
            time.sleep(.1)
    for d in fileData:
        file.write(d)
    file.close()
    print("{} uploaded from {}".format(filename, host))
    return 1
def sendBytes(filename, conn, addr):
    msg = conn.recv(64).decode("ascii")
    bs = -1
    be = -1
    for i in range(len(msg)):
        if msg[i-1] == "-":
            bs = msg[:i-1]
            be = msg[i:]
    if DEBUG == 1:
        print("msg: ", msg)
        print("bs", bs, "be", be)

    print("sending {} to {}".format(filename, host[0]))
    file = open(filename, 'rb')
    fileSize =  os.stat(filename).st_size
    fileData = file.read(int(bs))
    fileData = file.read(int(be)-int(bs))
    conn.send(fileData)

    print("Finished sending {} to {}".format(filename, host[0]))

s = socket.socket()
host = socket.gethostname()
port = 8080
if DEBUG == 1:
    print(host)
s.bind((host,port))
while True:
    s.listen(1)
    conn, addr = s.accept()
    data = conn.recv(1024).decode("ascii")
    filename = data[:len(data)-1]
    requestType = (data[len(data)-1])
    for i in range(len(filename)):
        if filename[len(filename) - i - 1] == "/":
            localDir = filename[:len(filename) - i - 1]
            if(not os.path.isdir(localDir)):
                if DEBUG == 1:
                    print("dir not found makeing ", localDir)
                os.mkdir(localDir)

    if requestType == "r":
        if(os.path.exists(filename)):
            conn.send("FILE FOUND".encode())
            time.sleep(.1)
            sendFile(filename, conn, addr)
        else:
            print(host[0], "requested file that does not exist")
    elif requestType == "w":
        receiveFile(filename, conn, addr)
    elif requestType == "s":
        if(os.path.exists(filename)):
            conn.send("FILE FOUND".encode())
            time.sleep(.1)
            sendBytes(filename, conn, addr)
        else:
            conn.send("FILE FOUND".encode())
            print(host[0], "requested file that does not exist")
    conn.close()
