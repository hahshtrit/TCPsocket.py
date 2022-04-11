import TCPsocket
import newParse


class cookies:
    def __init__(self, data):
        self.data = data

    def incrementCookies(self):
        dic = {}
        parsed = newParse.Request(self.data).headers['Cookie']
        visits = parsed.split(';')
        for i in visits:
            split2 = i.split('=')
            dic[split2[0]] = split2[1]
        return dic[' visits']
