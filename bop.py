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
        self.data = {}

    def __setitem__(self, element_id, value):
        event = '{} {}'.format(element_id, quote(value))
        self.publisher.publish(event, self.channel)

class App(object):
    def __init__(self, html, user_cls, port=5000):
        self.flask = flask.Flask(__name__)

        self.html = html
        self.user_cls = user_cls

        self.publisher = Publisher()
        self.user_by_id = {}
        self.page_by_id = {}
        self.world = Channel(self.publisher, 'world')

        @self.flask.route('/sse.js')
        def server_sse():
            return flask.Response(open('sse.js').read(),
                                  content_type='application/javascript')

        @self.flask.route('/')
        def root():
            return self.html

        @self.flask.route('/sse/subscribe/<pageid>')
        def subscribe(pageid):
            response = flask.Response(self._subscribe(pageid),
                                      content_type='text/event-stream')
            if flask.request.cookies.get('userid') is None:
                response.set_cookie('userid', self.get_user().id)
            return response

        @self.flask.route('/<method_name>', methods=['POST'])
        def action(method_name):
            user = self.get_user()
            pageid = flask.request.form['pageid']
            params = [value
                      for key, value in sorted(flask.request.form.items())
                      if key != 'pageid']
            return self.call(method_name, self._get_page(pageid), params) or ''

        self.flask.run(debug=True, threaded=True, port=port)

    def get_user(self):
        userid = flask.request.cookies.get('userid') or str(uuid4())

        try:
            return self.user_by_id[userid]
        except KeyError:
            user = self.user_cls()
            user.id = userid
            self.user_by_id[userid] = user
            return user

    def _get_page(self, pageid):
        try:
            return self.page_by_id[pageid]
        except KeyError:
            page = Channel(self.publisher, pageid)
            page.id = pageid
            page.user = self.get_user()
            page.world = self.world
            self.page_by_id[pageid] = page
            return page

    def _subscribe(self, pageid):
        user = self.get_user()
        page = self._get_page(pageid)
        return self.publisher.subscribe(['world', user.id, page.id])

    def call(self, method_name, page, params):
        user = self.get_user()
        method = getattr(user, method_name)
        return method(page, *params)
