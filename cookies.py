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
        # print(visits)
        for i in visits:
            # print(i)
            split2 = i.find('=')
            first = i[:split2]
            second = i[split2 + 1:]
            # print(first, second)
            if first.strip() == 'visits':
                count = int(second.strip()) + 1
                break

    return count


def addUsername(data):
    if 'Cookie' in newParse.Request(data).headers:
        parsed = newParse.Request(data).headers['Cookie']
        visits = parsed.split(';')
        for i in visits:
            split2 = i.find('=')
            first = i[:split2]
            second = i[split2 + 1:]
            # print('-------')
            # print(i)
            # print(first,second)
            # if split2:
            #     print(split2)
            #     dic[first.strip()] = second.strip()
            # if 'userCookie' in dic:
            if first.strip() == 'userCookie':
                cookie1 = crypt.crypt(second.strip(), 'qwertypoiu')
                # print(cookie1)
                cl = dataBases.database.loginClient.find_one({"cookie": cookie1}, {"_id": 0})
                # print(cl)
                if cl:
                    user = addHTMLdata.escapeHTML((cl['username']).encode()).decode()
                    return f"Welcome: {user}, to our encrypted site!!"
    return "please register or login"
