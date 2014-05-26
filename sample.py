import time
import bop

html = """
<html>
    <body>
        <script src="/sse.js"></script>

        <input type="text" id="name" placeholder="Anon">
        <button onclick="call('change_name', 'name')">Change name</button>

        <div id="chat"></div>

        <form onsubmit="call('say', 'message');" action="javascript:void(0);">
            <input type="text" id="message">
            <input type="submit" value="Send">
        </form>
    </body>
</html>
"""

class Page(object):
    def __init__(self, context):
        self.ctx = context
        try:
            self.ctx.page['name'] = self.ctx.user.name
        except AttributeError:
            pass

    def __str__(self):
        return html

    def get_name(self):
        try:
            return self.ctx.user.name
        except AttributeError:
            return 'Anon'

    def change_name(self, new_name):
        if not new_name:
            return

        self.ctx.user.name = new_name
        self.ctx.user['name'] = new_name

    def say(self, message):
        self.ctx.page['message'] = ''
        line = '<strong>{}</strong>: {}<br>'.format(self.get_name(), message)
        self.ctx.world['chat'] += line
                                                             

bop.App(Page)
