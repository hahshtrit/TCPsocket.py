import TCPsocket
import newParse
import dataBases
import header
import crypt
import addHTMLdata

def incrementCookies(data):
    dic = {}
    count = 1
    if 'Cookie' in newParse.Request(data).headers:
        parsed = newParse.Request(data).headers['Cookie']
        visits = parsed.split(';')
        for i in visits:
            split2 = i.split('=')
            if split2:
                dic[split2[0].strip()] = split2[1].strip()
        if 'visits' in dic:
            if (dic['visits']).isnumeric():
                count = int(dic['visits']) + 1

    return count


def addUsername(data):
    # P = (Request(data).parsePassUser('login'))

    dic = {}

    if 'Cookie' in newParse.Request(data).headers:
        parsed = newParse.Request(data).headers['Cookie']
        visits = parsed.split(';')
        for i in visits:
            split2 = i.split('=')
            if split2:
                dic[split2[0].strip()] = split2[1].strip()
        # print(dic)
        if 'userCookie' in dic:
            cookie1 = crypt.crypt(dic['userCookie'],'qwertypoiu')
            # print(cookie1)
            cl = dataBases.database.loginClient.find_one({"cookie": cookie1}, {"_id": 0})
            # print(cl)
            if cl:
                # print("yes cl")
                user = addHTMLdata.escapeHTML((cl['username']).encode()).decode()
                return f"Welcome: {user}, to our encrypted site!!"
    return "please register or login"







