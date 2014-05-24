import sys
sys.path.append('../server-sent-events')
from sse import Publisher

import flask
from collections import defaultdict
from urllib.parse import quote
from uuid import uuid4

def start():
    app = flask.Flask(__name__)

    publisher_by_user = defaultdict(Publisher)

    @app.route('/sse.js')
    def server_sse():
        return flask.Response(open('sse.js').read(),
                              content_type='application/javascript')

    @app.route('/')
    def root():
        try:
            userid = flask.request.cookies['userid']
        except KeyError:
            userid = str(uuid4())

        resp = flask.make_response("""
    <html>
        <body>
            <script src="/sse.js"></script>

            <div id="log"></div>

            <button onclick="post('/action')">Do action</button>
        </body>
    </html>
    """)
        resp.set_cookie('userid', userid)
        return resp

    @app.route('/subscribe')
    def subscribe():
        userid = flask.request.cookies['userid']
        return flask.Response(publisher_by_user[userid].subscribe(),
                              content_type='text/event-stream')

    @app.route('/action', methods=['POST'])
    def action():
        userid = flask.request.cookies['userid']
        event = 'log ' + quote('<h1>Test!</.h1')
        publisher_by_user[userid].publish(event)
        return ''

    app.run(debug=True, threaded=True)
