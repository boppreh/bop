import time
import bop

class User(object):
    def send_page(self, context, number):
        context.page['log'] = number

    def send_user(self, context, number):
        context.user['log'] = number

    def send_global(self, context, number):
        context.global_['log'] = number

    def long_action(self, context):
        for i in range(30):
            context.page['progress'] = '{}/{}'.format(i, 30)
            time.sleep(0.1)
        context.page['progress'] = 'Done!'

html = """
<html>
    <body>
        <input id="number" type="text" placeholder="Enter a number"</input>

        <button onclick="call('send_page', 'number')">Update page</button>
        <button onclick="call('send_user', 'number')">Update user</button>
        <button onclick="call('send_global', 'number')">Update global</button>

        <h1><span id="log">Nothing</span></h1>

        <button onclick="call('long_action');console.log(this);">Start long action</button>
        <h1><span id="progress"></span></h1>

        <script src="/sse.js"></script>
    </body>
</html>
"""

bop.start(html, User)
