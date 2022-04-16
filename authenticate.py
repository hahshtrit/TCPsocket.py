import json

# import bcrypt
import crypt

from newParse import Request
# import bcrypt
import dataBases


def successRegister(data):
    P = (Request(data).parsePassUser('add'))
    password = None
    userName = None
    if 'Password' in P:
        if P['Password']:
            password = (Request(data).parsePassUser('add'))['Password'].decode()
    if 'Username' in P:
        if P['Username']:
            userName = (Request(data).parsePassUser('add'))['Username'].decode()
    if userName and password:
        salt = crypt.mksalt()
        password = crypt.crypt(password, salt)
        # salt = 'gge'
        # password = password
        build = {'username': userName, 'salt': salt, 'password': password}
        dataBases.database.loginClient.insert_one(build)
        # print(build)

        return "HTTP/1.1 301 Moved Permanently\r\nContent-Length:0\r\nLocation:/\r\n".encode()
    else:
        text = 'add valid username and password'
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
               f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()


class loginPassword:
    # ss = []
    def __init__(self, data):
        self.ss = []
        self.data = data
        P = (Request(self.data).parsePassUser('login'))
        self.password = None
        self.userName = None
        self.s = []

        if 'Password' in P:
            if P['Password']:
                self.password = (Request(self.data).parsePassUser('login'))['Password'].decode()
        if 'Username' in P:
            if P['Username']:
                self.userName = (Request(self.data).parsePassUser('login'))['Username'].decode()

    def successLogin(self):
        cl = dataBases.database.loginClient.find_one({"username": self.userName}, {"_id": 0})
        # print(cl)
        if cl:
            checker = crypt.crypt(self.password, cl['salt'])
            if (cl['password'] == checker):
                text = "Successfully Logged in"
                # print(cl)

                return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
                       f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()
            else:
                text = 'wrong password'
                return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
                       f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()
        else:
            text = 'invalid username or password'
            return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
                   f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()


def addUsername(data):
    P = (Request(data).parsePassUser('login'))

    if 'Password' in P and 'Username' in P:
        if P['Password'] and P['Username']:
            password = (Request(data).parsePassUser('login'))['Password'].decode()
            userName = (Request(data).parsePassUser('login'))['Username'].decode()
            cl = dataBases.database.loginClient.find_one({"username": userName}, {"_id": 0})
            if cl:
                checker = crypt.crypt(password, cl['salt'])
                if cl['password'] == checker:
                    return userName

