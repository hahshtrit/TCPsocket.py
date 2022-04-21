import json

# import bcrypt
import secrets
import crypt
from newParse import Request
# import bcrypt
from header import find_token
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
    # print(P)
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
        text = 'Please remove any invalid cookies'
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
               f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()


# class loginPassword:
#     # ss = []
#     def __init__(self, data):
#         self.data = data

def successLogin(data):
    P = (Request(data).parsePassUser('login'))
    if 'Password' and 'Username' in P:
        if P['Password'] and P['Username']:
            password = (Request(data).parsePassUser('login'))['Password'].decode()
            userName = (Request(data).parsePassUser('login'))['Username'].decode()
            cl = dataBases.database.loginClient.find_one({"username": userName}, {"_id": 0})

            if cl:
                checker = crypt.crypt(password, cl['salt'])
                if cl['password'] == checker:
                    text = "Successfully Logged in"
                    cookie = secrets.token_hex(32)
                    token = secrets.token_hex(16)
                    cookieHash = crypt.crypt(cookie, 'qwertypoiu')
                    cl['cookie'] = cookieHash
                    cl['XSRF_token'] = token
                    # print(cl)
                    # print(cookieHash)

                    # dataBases.database.loginClient.({'usernmame': self.userName}, cl)
                    dataBases.database.loginClient.delete_one({'username': userName})
                    dataBases.database.loginClient.insert_one(cl)

                    # print(dataBases.database.loginClient.find_one({"cookie": cookieHash}, {"_id": 0}))
                    # print(cl)
                    return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
                           f"text/plain\r\nX-Content-Type-Options: nosniff\r\nSet-Cookie: userCookie={cookie}; " \
                           f"HttpOnly;  Max-Age=7200; SameSite=Strict" \
                           f"\r\n\r\n{text}".encode()

        # text = 'wrong username or password'
        # return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
        #                    f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()

    text = 'invalid username or password'
    return f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: " \
           f"text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()


def escapeHTML(text):
    text = text.replace("&", '&amp')
    text = text.replace("<", '&lt')
    text = text.replace(">", '&gt')
    return text


def user_token_exists(newData):
    token = Request(newData).parseAuthMessage()

    if token:
        if token['token']:
            if 'pip' != token['token'].decode():
                return False

    return True


def authMessage(data):
    if addAuthMessage(data):
        return "HTTP/1.1 301 Moved Permanently\r\nContent-Length:0\r\nLocation:/\r\n".encode()
    forbidden = '403 Access Denied'
    return f"HTTP/1.1 403 Forbidden\r\nContent-Length :{len(forbidden.encode())}\r\nContent-Type: " \
           f"text/html; charset=utf-8\r\n\r\n{forbidden}".encode()

def addAuthMessage(data):
    message = (Request(data).parseAuthMessage())
    if message:

        UserName = message['Username']
        if 'Welcome' in UserName:
            st = UserName.find(': ')
            nd = UserName.rfind(",")
            UserName = UserName[st + 2:nd]
            message['authorizedUser'] = UserName
            message.pop('Username')
            if 'token' in message:
                if message['token'].decode() != find_token(data):
                    return False
                else:
                    dataBases.database.authMessages.insert_one(message)
                    return True
    return True
