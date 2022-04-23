import secrets

from cookies import incrementCookies
from cookies import addUsername
# from newParse import Request
import dataBases
token = secrets.token_hex(16)
user_token = ''


# def addCookies(data):
#     cookies.incrementCookies(data)
def find_token(newData):
    message = addUsername(newData)
    # print(newData.decode())
    if 'Welcome' in message:
                # print(message)

                UserName = message
                st = UserName.find(': ')
                nd = UserName.rfind(",")
                UserName = UserName[st + 2:nd]

                stored_token = dataBases.database.loginClient.find_one({"username": UserName}, {"_id": 0})
                # print(stored_token)
                if stored_token:
                    if 'XSRF_token' in stored_token:
                        # print(stored_token)
                        new_token = stored_token['XSRF_token']
                        return new_token
    return 'None Error'

def htmlRendering(html_fileName, data, message, newData):
    with open(html_fileName) as html_file:
        template = html_file.read()
        template = replace_placeholders(template, data)
        template = replace_placeholders(template, message)

        template = render_loop(template, data, 0)
        template = render_loop(template, message, 1)
        # find_token(newData)
        template = template.replace("{{token_valuex12}}", token)
        template = template.replace("{{token_value123}}", find_token(newData))

        template = template.replace("{{cookieTracker}}", str(incrementCookies(newData)))
        template = template.replace("{{UserWelcome}}", addUsername(newData))
        # html_file.write(template)

        return template


def replace_placeholders(template, data):
    replace_template = template
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            replace_template = replace_template.replace("{{" + placeholder + "}}", data[placeholder])
    return replace_template


def render_loop(template, data, type):
    loop_start_tag = "{{loop}}"
    loop_end_tag = "{{end_loop}}"
    if type == 1:
        loop_start_tag = "{{loop2}}"
        loop_end_tag = "{{end_loop2}}"

    start_index = template.find(loop_start_tag)
    end_index = template.find(loop_end_tag)

    loop_template = template[start_index + len(loop_start_tag): end_index]
    loop_content = ""

    if "loop_data" in data:
        loop_data = data["loop_data"]

        for single_piece_of_content in loop_data:
            loop_content += replace_placeholders(loop_template, single_piece_of_content)

    final_content = template[:start_index] + loop_content + template[end_index + len(loop_end_tag):]

    return final_content
