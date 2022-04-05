import json


class parser:
    # request = ''
    def __init__(self, request, undecoded = None):
        self.request = request
        self.unDecoded = undecoded
        # self.request2 = self.request.decode()

    def parsePostContent(self, types):
        split2 = self.request.decode().split("\r\n\r\n")
        # print(len(split2))
        if len(split2) > 1:
            loaded = (split2[1])
            new = (json.loads(loaded))
            if types in new:
                return new[types]
            else:
                return 5



