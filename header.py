import secrets

import TCPsocket
import authenticate
import newParse
import parse
import dataBases
import directoryFile
from cookies import cookies

token = secrets.token_hex(16)


# def addCookies(data):
#     cookies.incrementCookies(data)

def htmlRendering(html_fileName, data, newData):
    with open(html_fileName) as html_file:
        template = html_file.read()
        template = replace_placeholders(template, data)
        template = render_loop(template, data)
        template = template.replace("{{token_valuex12}}", token)
        template = template.replace("{{cookieTracker}}", str(cookies().incrementCookies(newData)))
        template = template.replace("{{UserWelcome}}", "please register or login")
        if authenticate.addUsername(newData):
            template = template.replace("{{UserWelcome}}", authenticate.addUsername(newData))

        return template


def replace_placeholders(template, data):
    replace_template = template
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            replace_template = replace_template.replace("{{" + placeholder + "}}", data[placeholder])
    return replace_template


def render_loop(template, data):
    loop_start_tag = "{{loop}}"
    loop_end_tag = "{{end_loop}}"

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
