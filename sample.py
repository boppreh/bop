import random
import bop

class User(object):
    def send_page(self, context, number):
        context.page['log'] = number

    def send_user(self, context, number):
        context.user['log'] = number

    def send_global(self, context, number):
        context.global_['log'] = number

html = """
<html>
    <body>
        <input id="number" type="text" placeholder="Enter a number"</input>

        <button onclick="call('send_page', 'number')">Update page</button>
        <button onclick="call('send_user', 'number')">Update user</button>
        <button onclick="call('send_global', 'number')">Update global</button>

        <h1><span id="log"></span></h1>

        <script src="/sse.js"></script>
    </body>
</html>
"""

bop.start(html, User)
