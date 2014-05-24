import random
import bop

class User(object):
    def count(self, page):
        page['log'] = '<h1>{}</h1>'.format(random.randint(1, 100))

html = """
<html>
    <body>
        <script src="/sse.js"></script>

        <div id="log"></div>

        <button onclick="call('count')">New random!</button>
    </body>
</html>
"""

bop.start(html, User)
