import sys
sys.path.append('../server-sent-events')
from sse import Publisher

import flask
from urllib.parse import quote
from uuid import uuid4

class Channel(object):
    def __init__(self, publisher, channel):
        self.publisher = publisher
        self.channel = channel

    def __setitem__(self, element_id, value):
        event = '{} {}'.format(element_id, quote(value))
        self.publisher.publish(event, self.channel)

class Context(object):
    def __init__(self, publisher, user, pageid):
        self.publisher = publisher
        self.user = user
        self.pageid = pageid

        self.global_ = Channel(publisher, 'global')
        self.user = Channel(publisher, user.id)
        self.page = Channel(publisher, pageid)


def start(html, user_cls):
    app = flask.Flask(__name__)

    publisher = Publisher()
    user_by_id = {}

    def get_user():
        userid = flask.request.cookies.get('userid') or str(uuid4())

        try:
            return user_by_id[userid]
        except KeyError:
            user = user_cls()
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

    @app.route('/sse/subscribe/<pageid>')
    def subscribe(pageid):
        user = get_user()
        subscription = publisher.subscribe(['global', user.id, pageid])
        response = flask.Response(subscription,
                                  content_type='text/event-stream')
        if flask.request.cookies.get('userid') is None:
            response.set_cookie('userid', user.id)
        return response

    @app.route('/<method_name>', methods=['POST'])
    def action(method_name):
        user = get_user()
        params = [value for key, value in sorted(flask.request.form.items())
                  if key != 'pageid']
        context = Context(publisher, user, flask.request.form['pageid'])
        method = getattr(user, method_name)
        return method(context, *params) or ''

    app.run(debug=True, threaded=True)
