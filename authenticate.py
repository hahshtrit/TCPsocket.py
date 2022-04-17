import json

# import bcrypt
import secrets
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
                    cookieHash = crypt.crypt(cookie, 'qwertypoiu')
                    cl['cookie'] = cookieHash
                    # print(cl)
                    # print(cookieHash)

                    # dataBases.database.loginClient.({'usernmame': self.userName}, cl)
                    dataBases.database.loginClient.delete_one({'usernmame': userName})
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


def authMessage(data):
    addAuthMessage(data)
    return "HTTP/1.1 301 Moved Permanently\r\nContent-Length:0\r\nLocation:/\r\n".encode()


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
            dataBases.database.authMessages.insert_one(message)
            # print(message)
