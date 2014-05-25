import time
import bop

class User(object):
    def __init__(self):
        self.name = 'Anon'

    def change_name(self, page, new_name):
        self.name = new_name or 'Anon'
        page.user['name'] = new_name

    def say(self, page, message):
        page['message'] = ''
        page.world['chat'] += '<strong>{}</strong>: {}<br>'.format(self.name,
                                                                   message)

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

bop.App(html, User)
