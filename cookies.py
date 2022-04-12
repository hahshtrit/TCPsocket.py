import TCPsocket
import newParse


class cookies:
    def incrementCookies(self, data):
        dic = {}
        count = 1
        if 'Cookie' in newParse.Request(data).headers:
            parsed = newParse.Request(data).headers['Cookie']
            visits = parsed.split(';')
            for i in visits:
                split2 = i.split('=')
                dic[split2[0].strip()] = split2[1].strip()
            if 'visits' in dic:
                if (dic['visits']).isnumeric():
                    count = int(dic['visits']) + 1

        return count
