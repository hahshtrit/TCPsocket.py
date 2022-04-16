import json
import sys
from pymongo import MongoClient
import TCPsocket
import newParse
import parse
import directoryFile


class database:
    mongo_client = MongoClient("mongo")
    # mongo_client = MongoClient()

    db = mongo_client["cse312"]
    user_collection = db['ids']
    id_collection = db["users_id"]
    image_id_collection = db["image_id"]
    image_collection = db["images"]
    tokens_collection = db["tokens"]
    websocket_collection = db['webSocket']
    loginClient = db['clientLogin']

    def __init__(self, request):
        self.request = request

    def getNextId(self):
        id_object = self.id_collection.find_one()
        if id_object:
            next_id = int(id_object["last_id"]) + 1
            self.id_collection.update_one({}, {"$set": {"last_id": next_id}})
            return next_id
        else:
            self.id_collection.insert_one({'last_id': 1})
            return 1

    def addUser(self):
        if (parse.parser(self.request).parsePostContent("username")) == 5:
            return 5
        if (parse.parser(self.request).parsePostContent("email")) == 5:
            return 5
        username = (parse.parser(self.request).parsePostContent("username"))
        email = (parse.parser(self.request).parsePostContent("email"))
        dict = {"id": self.getNextId(), "email": email, "username": username}
        self.user_collection.insert_one(dict)
        # print(dict)
        dict.pop("_id")
        return json.dumps(dict)

    def postUserSend(self):
        errorMessage = '<h2>ERROR 404😩<h2>'
        errorMessage2 = '<h2> Enter a valid username and email😩<h2>'

        if "POST" in newParse.Request(self.request).method:
            if '/users' in newParse.Request(self.request).path:
                # if "POST /users" in (parse.parser(self.request).parseAt(0)):
                file = (self.addUser())
                # print(file)
                if file == 5:
                    # print("enters")
                    return f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage2.encode())}\r\nContent-Type: " \
                           f"text/html; charset=utf-8\r\n\r\n{errorMessage2}".encode()

                sending = f'HTTP/1.1 201 Created\r\nContent-Length :{len(file.encode())}\r\nContent-Type: ' \
                          f'application/json; charset=utf-8\r\n\r\n{file}'.encode()
                return sending
        else:
            f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: text/html; " \
            f"charset=utf-8\r\n\r\n{errorMessage}".encode()

    def getAllUsers(self):
        allUsers = self.user_collection.find({}, {"_id": 0})
        allData = json.dumps(list(allUsers))
        # print(allData)
        sending = f'HTTP/1.1 200 OK\r\nContent-Length :{len(allData.encode())}\r\nContent-Type: text/html; ' \
                  f'charset=utf-8\r\n\r\n{allData}'.encode()

        return sending

    def getSingleUser(self):
        id = newParse.Request(self.request).parseUserID()
        singleUser = self.user_collection.find_one({"id": id}, {"_id": 0})
        if singleUser:
            allData = json.dumps(singleUser)

            return f'HTTP/1.1 200 OK\r\nContent-Length :{len(allData.encode())}\r\nContent-Type: text/html; ' \
                   f'charset=utf-8\r\n\r\n{allData}'.encode()
        else:
            errorMessage = '<h2>ENTER A VALID ID😩<h2>'
            return f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: " \
                   f"text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()

    def updateUser(self):
        id = newParse.Request(self.request).parseUserID()

        if "PUT" in newParse.Request(self.request).method:
            if f'/users/{id}' in newParse.Request(self.request).path:
                # if f"PUT /users/{id}" in (parse.parser(self.request).parseAt(0)):
                username = (parse.parser(self.request).parsePostContent("username"))
                email = (parse.parser(self.request).parsePostContent("email"))
                singleUser = self.user_collection.find_one({"id": id}, {"_id": 0})
                if singleUser:
                    self.user_collection.update_one({"id": id}, {"$set": {"email": email, "username": username}})
                    allData = json.dumps(self.user_collection.find_one({"id": id}, {"_id": 0}))

                    return f'HTTP/1.1 200 OK\r\nContent-Length :{len(allData.encode())}\r\nContent-Type: text/html; ' \
                           f'charset=utf-8\r\n\r\n{allData}'.encode()
                else:
                    errorMessage = '<h2>ENTER A VALID ID😩<h2>'
                    return f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: " \
                           f"text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()

    def deleteUser(self):
        # print('heellosfdfd')
        id = newParse.Request(self.request).parseUserID()

        if "DELETE" in newParse.Request(self.request).method:
            if f'/users/{id}' in newParse.Request(self.request).path:
                # if f"DELETE /users/{id}" in (parse.parser(self.request).parseAt(0)):
                singleUser = self.user_collection.find_one({"id": id}, {"_id": 0})
                if singleUser:
                    self.user_collection.delete_one({"id": id})
                    # allData = json.dumps(self.user_collection.find_one({"id": id}, {"_id": 0}))

                    return f'HTTP/1.1 204 No Content response code\r\nContent-Length :0\r\nContent-Type: text/html; ' \
                           f'charset=utf-8\r\n\r\n'.encode()
                else:
                    errorMessage = '<h2>ENTER A VALID ID TO DELETE 😤<h2>'
                    return f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: " \
                           f"text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()
