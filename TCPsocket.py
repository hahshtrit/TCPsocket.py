import json
import socketserver
import _sha1
import sys
# import os
import random

import addHTMLdata
import header
import parse
import directoryFile
# from pymongo import MongoClient
import dataBases
import newParse
# from cookies import cookies
from webSockets import initateWebsocket
from webSockets import websocket
import webSockets
from webSockets import webSocketParse
import base64


class MyTCPHandler(socketserver.BaseRequestHandler):
    clients = []
    new = []

    def handle(self) -> None:
        # while True:
        received_data = self.request.recv(1024)

        # newData = []
        client_id = self.client_address[0] + " :is sending data."  # + self.client_address[1]
        self.clients.append(self.client_address)
        # print(self.clients)
        # self.new.append(self)
        # print(self)
        # print(self.new)
        newData = received_data
        # decoded = received_data.decode()
        sys.stdout.flush()
        sys.stderr.flush()
        # print(decoded)
        errorMessage = '<h2>ERROR 404😩<h2>'
        print("\n\n")

        sys.stdout.flush()
        sys.stderr.flush()
        root = newParse.Request(newData).path
        requestType = newParse.Request(newData).method
        parseBody = newParse.Request(newData).body
        # =======================================================================================================================================================================
        lengthCalled = 0

        dict = newParse.Request(newData).headers
        if "Content-Length" in dict:
            # print("in dictionary")
            lengthCalled = int(dict["Content-Length"])

        lengthCalled -= len(parseBody)

        sys.stdout.flush()
        sys.stderr.flush()
        # print(newData)

        while lengthCalled > 0:
            data = self.request.recv(1024)
            newData = newData + data
            # print(len(data), " this is len of buffered data")
            lengthCalled -= len(data)
            sys.stdout.flush()
            sys.stderr.flush()
        # dict = newParse.Request(newData).headers
        # print(newData)

        sys.stdout.flush()
        sys.stderr.flush()
        requestDirectory = directoryFile.directory(newData).requestDirectory

        webBody = newParse.Request(newData).parseWebBody()
        id = (newParse.Request(newData))
        # print(id.path)
        # print(newParse.Request(newData).body)

        # print(newData.decode())
        # print(webBody)
        # print(newParse.Request(newData))
        # if 'POST' in newData.decode():
        #     print(newData.decode())
        # print(newParse.Request(newData).path)
        # print(newParse.Request(newData).headers)

        # =======================================================================================================================================================================
        if requestType in requestDirectory:
            if not addHTMLdata.token_exist(newData):
                forbidden = '<h1>403 Forbidden Access: Request Denied</h1>'
                self.request.sendall(
                    f"HTTP/1.1 403 Forbidden\r\nContent-Length :{len(forbidden.encode())}\r\nContent-Type: "
                    f"text/html; charset=utf-8\r\n\r\n{forbidden}".encode())

            if root in requestDirectory[requestType]:
                self.request.sendall((requestDirectory[requestType])[root])
            else:
                self.request.sendall(
                    f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: "
                    f"text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()
                )
        else:
            self.request.sendall(
                f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: "
                f"text/html; charset=utf-8\r\n\r\n{errorMessage}".encode())

        if initateWebsocket(newData):
            self.new.append(self)
            username = "User: " + str(random.randint(0, 1000))
            # data = None
            # data2 = None

            while 1:

                frame = self.request.recv(1024)
                maskFrom = webSockets.maskFrom(frame)
                payloadLength = webSockets.PayLoadLen(frame)
                newFrame = frame

                while 1:
                    if len(newFrame[maskFrom:]) >= payloadLength:
                        break
                    newFrame += self.request.recv(1024)

                parser1 = webSocketParse(newFrame, username)
                if parser1.Opcode == 8:
                    self.new.remove(self)
                    break

                for i in self.new:
                    if 'messageType' in parser1.message and 'webRTC' in parser1.message['messageType']:
                        if i != self:
                            print('sent')
                            # print(parser1.packedMessage)
                            i.request.sendall(parser1.packedMessage)
                    else:
                        i.request.sendall(parser1.packedMessage)
                        # print(parser1.packedMessage)
                        sys.stdout.flush()
                        sys.stderr.flush()

                sys.stdout.flush()
                sys.stderr.flush()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
