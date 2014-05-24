import sys
sys.path.append('../server-sent-events')
from sse import Publisher

import flask
from urllib.parse import quote
from uuid import uuid4

class Page(object):
    def __init__(self, publisher, data=None):
        self.publisher = publisher
        self.data = data or {}

    def __setitem__(self, element_id, value):
        self.data[element_id] = value
        event = '{} {}'.format(element_id, quote(value))
        self.publisher.publish(event)

    def __getitem__(self, element_id):
        return self.data[element_id]


def start(html, user_cls):
    app = flask.Flask(__name__)

    user_by_id = {}

    def get_user():
        userid = flask.request.cookies.get('userid') or str(uuid4())

        try:
            return user_by_id[userid]
        except KeyError:
            user = user_cls()
            user.publisher = Publisher()
            user.id = userid
            user_by_id[userid] = user
            return user


    @app.route('/sse.js')
    def server_sse():
        return flask.Response(open('sse.js').read(),
                              content_type='application/javascript')

    @app.route('/')
    def root():
        return html

    @app.route('/sse/subscribe')
    def subscribe():
        user = get_user()
        response = flask.Response(user.publisher.subscribe(),
                                  content_type='text/event-stream')
        if flask.request.cookies.get('userid') is None:
            response.set_cookie('userid', user.id)
        return response

    @app.route('/<method>', methods=['POST'])
    def action(method):
        user = get_user()
        return getattr(user, method)(Page(user.publisher)) or ''

    app.run(debug=True, threaded=True)
