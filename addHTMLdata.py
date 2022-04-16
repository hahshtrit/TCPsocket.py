import dataBases
import header

import newParse
from dataBases import database
from header import htmlRendering
import directoryFile
import secrets

from parse import parser

track = 0
commentsData = []
imagesPath = {}


def getNextId():
    id_object = database.image_id_collection.find_one()
    if id_object:
        next_id = int(id_object["last_id"]) + 1
        database.image_id_collection.update_one({}, {"$set": {"last_id": next_id}})
        return next_id
    else:
        database.image_id_collection.insert_one({'last_id': 1})
        return 1


def getTotalId():
    id_object = database.image_id_collection.find_one()
    if id_object:
        return int(id_object["last_id"])
    return -1


def add_user_posts(data):
    database.image_collection.insert_one(data)


def escapeHTML(text):
    text = text.replace(b"&", b'&amp')
    text = text.replace(b"<", b'&lt')
    text = text.replace(b">", b'&gt')
    return text


def token_exist(newData):
    webBody = newParse.Request(newData).parseWebBody()
    if webBody:
        if webBody['token']:
            if header.token != webBody['token'].decode():
                return False

    return True


def add_data(data):
    global track
    global commentsData
    webBody = newParse.Request(data).parseWebBody()
    perCaption = {}
    id = 0
    if webBody:
        # print(webBody)
        if 'comment' in webBody:
            text = escapeHTML(webBody["comment"])

            perCaption["comment"] = text.decode()
        else:
            perCaption['comment'] = ''

        if 'contentType' in webBody:
            if 'image/jpeg' in webBody['contentType']:
                track += 1
                id = getNextId()
                # id = track
                with open(f"userImages/image{id}.jpg", "wb") as f:
                    f.write(webBody['bytes'])
                    f.close()
                perCaption[
                    'image_filenameRoute'] = f'<img src="userImages/image{id}.jpg" class = "imagesUsers"/><br/>'
            else:
                perCaption['image_filenameRoute'] = ''

        else:
            perCaption['image_filenameRoute'] = ''

        if token_exist(data):
            add_user_posts(perCaption)


def indexHTMLCall(data):
    # print(1)
    add_data(data)
    commentsData = list(database.image_collection.find({}, {"_id": 0}))
    # print(3)
    return htmlRendering("sample_page /index.html", {'loop_data': commentsData}, data)
