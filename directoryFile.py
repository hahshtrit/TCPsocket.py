import os
import addHTMLdata
import webSockets

import newParse
import dataBases



class directory:
    def __init__(self, data):
        self.data = data
        # print(self.data.decode())

        self.textHi = '<h1> Hello World️!!<h1>'
        self.myHTML = addHTMLdata.indexHTMLCall(data)
        self.myCSS = open("sample_page /style.css", "r")
        self.myJS = open("sample_page /functions.js", "r")

        self.file_sizeHTML = os.path.getsize("sample_page /index.html")
        self.file_sizeCSS = os.path.getsize("sample_page /style.css")
        self.file_sizeJS = os.path.getsize("sample_page /functions.js")



        def sendImage(path):
            if os.path.exists(f"sample_page /{path}"):
                image = open(f"sample_page /{path}", "rb")
                imageSize = os.path.getsize(f"sample_page /{path}")
                return f"HTTP/1.1 200 OK\r\nContent-Length: {imageSize}\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + image.read()
            else:
                errorMessage = '<h2>ERROR 404😩<h2>'
                f"HTTP/1.1 404 Not Found\r\nContent-Length :{len(errorMessage.encode())}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{errorMessage}".encode()

        self.getDirectory = {
            '/': f"HTTP/1.1 200 OK\r\nContent-Length: {len(self.myHTML.encode())}\r\nContent-Type:text/html;charset=utf-8\r\nX-Content-Type-Options:nosniff\r\n\r\n{self.myHTML}".encode(),
            '/hello': f'HTTP/1.1 200 OK\r\nContent-Length: {len(self.textHi.encode())}\r\nContent-Type:text/html;charset=utf-8\r\nX-Content-Type-Options:nosniff\r\n\r\n{self.textHi}'.encode(),
            '/hi': "HTTP/1.1 301 Moved Permanently\r\nContent-Length:0\r\nLocation:/hello\r\n".encode(),
            '/style.css': f"HTTP/1.1 200 OK\r\nContent-Length: {(self.file_sizeCSS)}\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{self.myCSS.read()}".encode(),
            '/functions.js': f"HTTP/1.1 200 OK\r\nContent-Length: {(self.file_sizeJS)}\r\nContent-Type: text/javascript; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\n\r\n{self.myJS.read()}".encode(),
            '/users': dataBases.database(data).getAllUsers(),
            f'/users/{newParse.Request(data).parseUserID()}': dataBases.database(data).getSingleUser(),
            '/websocket': webSockets.websocket(data).websocketHandshake(),
            '/chat-history': webSockets.websocket(data).getChatHistory(),
        }

        path = newParse.Request(data).path
        if '/image/' in path:
            self.getDirectory[path] = sendImage(path)

        if addHTMLdata.getTotalId() != -1:
            for i in (range(1, (addHTMLdata.getTotalId()) + 1)):
                imagePath = f'userImages/image{i}.jpg'
                if os.path.exists(imagePath):
                    myImage = open(imagePath, "rb")
                    myImageSize = os.path.getsize(imagePath)

                    self.getDirectory[f'/userImages/image{i}.jpg'] = \
                        f"HTTP/1.1 200 OK\r\nContent-Length: {int(myImageSize)}\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + myImage.read()
                    myImage.close()
                else:
                    text = "<h2>Server might need docker compose down</h2>"
                    self.getDirectory[f'/userImages/image{i}.jpg'] = \
                        f"HTTP/1.1 200 OK\r\nContent-Length: {len(text.encode())}\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\n\r\n{text}".encode()

        self.postDirectory = {
            "/users": dataBases.database(data).postUserSend(),
            "/image-upload": f"HTTP/1.1 301 Moved Permanently\r\nContent-Length:0\r\nLocation:/\r\n".encode()

        }
        self.deleteDirectory = {
            f'/users/{newParse.Request(data).parseUserID()}': dataBases.database(data).deleteUser()
        }
        self.putDirectory = {f'/users/{newParse.Request(data).parseUserID()}': dataBases.database(data).updateUser()}

        self.requestDirectory = {"GET": self.getDirectory, "POST": self.postDirectory, "DELETE": self.deleteDirectory,
                                 "PUT": self.putDirectory}
