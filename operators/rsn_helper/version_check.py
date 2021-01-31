import requests
from html.parser import HTMLParser
import bpy

from ...preferences import get_pref
from ... import bl_info


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        # print('<%s>' % tag)
        if tag == "a" and len(attrs) != 0:
            for (variable, value) in attrs:
                if variable == "id" and value.startswith("user-content"):
                    self.links.append(value)


class RSN_OT_CheckUpdate(bpy.types.Operator):
    """Check latest version"""
    bl_idname = 'rsn.check_update'
    bl_label = 'Check Update'

    def execute(self, context):
        # get current version num
        pref = get_pref()
        v = bl_info['version']
        v = int(f'{v[0]}{v[1]}{v[2]}')
        # get latest version
        response = requests.get('https://github.com/atticus-lv/RenderStackNode/blob/main/README.md')
        html_code = response.text
        parser = MyHTMLParser()
        parser.feed(html_code)
        parser.close()
        new_v = int(parser.links[1][-3:])

        if v != new_v:
            pref.need_update = True
            pref.latest_version = new_v
        return {'FINISHED'}


def register():
    bpy.utils.register_class(RSN_OT_CheckUpdate)


def unregister():
    bpy.utils.unregister_class(RSN_OT_CheckUpdate)
