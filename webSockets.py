import json
import sys
import TCPsocket
import addHTMLdata
import newParse
import socketserver
import header
import dataBases
import hashlib
from base64 import b64encode


def initateWebsocket(data):
    if websocket(data).websocketHandshake():
        if "101 Switching Protocols".encode() in websocket(data).websocketHandshake():
            return True
    return False


class websocket:
    frame = None

    def __init__(self, data):
        self.data = data

    def websocketHandshake(self):
        path = newParse.Request(self.data).path
        headers = newParse.Request(self.data).headers
        if path == '/websocket':
            if "Sec-WebSocket-Key" in headers:
                SecKey = headers['Sec-WebSocket-Key']
                SecKey += "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                hashKey = hashlib.sha1(SecKey.encode()).digest()
                encodedkey = b64encode(hashKey)

                return f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {encodedkey.decode()}\r\n\r\n".encode()

        errorMessage = 'Something went wrong ...'
        return f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()

    def getChatHistory(self):
        allUsers = dataBases.database.websocket_collection.find({}, {"_id": 0})
        allData = json.dumps(list(allUsers))
        return f'HTTP/1.1 200 OK\r\nContent-Length :{len(allData.encode())}\r\nContent-Type: application/json; ' \
               f'charset=utf-8\r\n\r\n{allData}'.encode()


class webSocketParse:
    # payload = getPayload()
    def __init__(self, frame: bytes, username):
        self.frame = frame
        self.userName = username
        self.payloadLength = PayLoadLen(self.frame)
        self.Opcode = OpCode(self.frame)
        self.mask = getMask(self.frame)
        self.maskFrom = maskFrom(self.frame)
        self.message = self.addUserName()
        self.addToDataBase()

    def pay(self):
        if self.Opcode == 8:
            return None
        maskFrom = 0
        maskingKey = self.frame[2:6]

        if self.frame[1] & 127 < 126:
            maskFrom = 6
            maskingKey = self.frame[2:6]
        elif self.frame[1] & 127 == 126:
            maskFrom = 8
            maskingKey = self.frame[4:8]
        elif self.frame[1] & 127 == 127:
            maskFrom = 14
            maskingKey = self.frame[10:14]
        byte = bytearray()

        #
        message = self.frame[maskFrom: maskFrom + self.payloadLength]
        for i in range(self.payloadLength):
            byte.append(message[i] ^ maskingKey[i % 4])
        return json.loads(byte.decode())

    def addUserName(self):
        m = self.pay()
        if m:
            # if 'username' in m:
            if 'comment' in m:
                m['username'] = self.userName

                m['comment'] = addHTMLdata.escapeHTML(m['comment'].encode()).decode()
                # print(m)
                return m
            else:
                return m
        else:
            # print(m)
            return m

    def addToDataBase(self):
        data = self.addUserName()
        if data:
            if 'comment' in data:
                if 'username' in data:
                    dic = {'username': data["username"], 'comment': data['comment']}
                    dataBases.database.websocket_collection.insert_one(dic)

    def pack(self):
        useOpcode = [129]
        payLoadSize = 0
        payLoad = bytearray(json.dumps(self.message).encode())
        # print(self.message)
        # if 'comment' in self.message:
        # if True:
        # print(payLoad)
        size = (bin(len(payLoad))[2:])
        # print(size)
        lenS = len(size)
        # print(format(len(payLoad), 'b'))
        # print(payLoad)

        if lenS % 8 != 0:
            for i in range(8 - lenS % 8):
                size = '0' + size

        if self.payloadLength < 126:
            payLoadSize = [len(payLoad)]
            arr = int(bin(len(payLoad)), 2)
            print(arr)
            return bytearray(useOpcode) + ((len(payLoad)).to_bytes(1, 'big')) + payLoad

        elif self.frame[1] & 127 == 126:
            bin1 = format(len(payLoad), 'b')
            # bin1
            sizeOfBin = len(bin1)
            byt1 = bin1[:(sizeOfBin - 8)]
            byt2 = bin1[(sizeOfBin - 8):]
            print(int(bin(len(payLoad)), 2))
            one = (int(bin(len(payLoad))[:sizeOfBin - 8], 2))
            two = (int(bin(len(payLoad))[sizeOfBin - 8:], 2))

            return bytearray(useOpcode + [126]) + (len(payLoad)).to_bytes(2,'big') + payLoad

        elif self.frame[1] & 127 == 127:
            if len(size) != 64:
                for i in range(64 - len(size)):
                    size = '0' + size

            byt1 = [int(size[:8], 2)]
            byt2 = [int(size[8:16], 2)]
            byt3 = [int(size[16:24], 2)]
            byt4 = [int(size[24:32], 2)]
            byt5 = [int(size[32:40], 2)]
            byt6 = [int(size[40:48], 2)]
            byt7 = [int(size[48:56], 2)]
            byt8 = [int(size[56:], 2)]
            bytT = bytearray(byt1 + byt2 + byt3 + byt4 + byt5 + byt6 + byt7 + byt8)
            return bytearray(useOpcode + [127]) + (len(payLoad)).to_bytes(8,'big') + payLoad

        new = bytearray(useOpcode + [payLoadSize])
        return new + payLoad


def convert(frame, num):
    a = bin(frame[num])[2:]
    if len(a) < 8:
        for i in range(8 - len(a)):
            a = '0' + a
    return a


def PayLoadLen(frame):
    payLoadLen = frame[1] & 127
    if payLoadLen == 126:
        a = convert(frame, 2)
        b = convert(frame, 3)
        m = int(a + b, 2)

        return m

    elif payLoadLen == 127:

        new = ''
        for i in range(2, 10):
            new += convert(frame, i)
        return int(new, 2)

    return payLoadLen


def OpCode(frame):
    code = frame[0] & 15
    return code


# #
def getMask(frame):
    return frame[1] & 1


def maskFrom(frame):
    if frame[1] & 127 < 126:
        return 6
    elif frame[1] & 127 == 126:
        return 8
    elif frame[1] & 127 == 127:
        return 12
    return 0
