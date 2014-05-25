import time
import bop

class User(object):
    def add(self, page, a, b):
        a, b = int(a), int(b)

        page['result'] = "Hmmm..."
        time.sleep(1)
        page['result'] = "{} plus {}...".format(a, b)
        time.sleep(2)
        page['result'] = "{}?".format(a + b + 1)
        time.sleep(2)
        page['result'] = "No no, wait."
        time.sleep(2)
        page['result'] = "It's {}!".format(a + b)
        time.sleep(2)
        page['result'] = "{} + {} = {}".format(a, b, a + b)

html = """
<html>
    <body>
        <script src="/sse.js"></script>

        <input id="a" type="text" placeholder="Number A"</input>
        <input id="b" type="text" placeholder="Number B"</input>

        <button onclick="call('add', 'a', 'b')">Add them!</button>

        <h2><span id="result">A + B = ?</span></h2>
    </body>
</html>
"""

bop.App(html, User)
