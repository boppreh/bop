import sys
sys.path.append('../server-sent-events')
from sse import Publisher

import flask
from urllib.parse import quote
from uuid import uuid4

class _Dummy(object):
    def __init__(self, element_id):
        self.element_id = element_id
        self.prepend = []
        self.append = []

    def __add__(self, other):
        self.append.append(other)
        return self

    def __radd__(self, other):
        self.prepend.append(other)
        return self


class _Channel(object):
    js_set = 'set("{}", decodeURIComponent("{}"))'
    js_surround = 'set("{}", decodeURIComponent("{}") + get("{}") + decodeURIComponent("{}"))'

    def __init__(self, publisher, channel):
        self.publisher = publisher
        self.channel = channel
        self.data = {}

    def __getitem__(self, element_id):
        return _Dummy(element_id)

    def __setitem__(self, element_id, value):
        if isinstance(value, _Dummy):
            prepend = ''.join(reversed(value.prepend))
            append = ''.join(value.append)
            self.eval(_Channel.js_surround.format(element_id,
                                                 quote(prepend),
                                                 value.element_id,
                                                 quote(append)))
        else:
            self.eval(_Channel.js_set.format(element_id, quote(value)))

    def eval(self, script):
        self.publisher.publish(script, self.channel)

class _Context(object):
    def __init__(self, page_channel, user_channel, world_channel, subscription):
        self.page = page_channel
        self.user = user_channel
        self.world = world_channel
        self.subscription = subscription


class App(object):
    def __init__(self, page_cls, port=5000):
        self.flask = flask.Flask(__name__)

        self.page_cls = page_cls

        self.publisher = Publisher()
        self.context_by_pageid = {}
        self.user_by_id = {}
        self.page_by_id = {}
        self.world = _Channel(self.publisher, 'world')

        @self.flask.route('/sse.js')
        def server_sse():
            return flask.Response(open('sse.js').read(),
                                  content_type='application/javascript')

        @self.flask.route('/sse/subscribe/<pageid>')
        def subscribe(pageid):
            context = self.context_by_pageid[pageid]
            response = flask.Response(context.subscription,
                                      content_type='text/event-stream')
            return response

        @self.flask.route('/call/<method_name>', methods=['POST'])
        def action(method_name):
            pageid = flask.request.form['pageid']
            page = self.page_by_id[pageid]

            params = [value
                      for key, value in sorted(flask.request.form.items())
                      if key != 'pageid']

            method = getattr(page, method_name)
            return method(*params) or ''

        @self.flask.route('/')
        @self.flask.route('/<resource>')
        def root(resource='/'):
            pageid = str(uuid4())
            page = self._get_page(pageid)

            response = flask.make_response(str(page))
            response.set_cookie('pageid', pageid)
            if flask.request.cookies.get('userid') is None:
                response.set_cookie('userid', self._get_user_channel().id)

            return response

        self.flask.run(debug=True, threaded=True, port=port)

    def _get_user_channel(self):
        userid = flask.request.cookies.get('userid') or str(uuid4())

        try:
            return self.user_by_id[userid]
        except KeyError:
            user = _Channel(self.publisher, userid)
            user.id = userid
            self.user_by_id[userid] = user
            return user

    def _get_page(self, pageid):
        try:
            return self.context_by_pageid[pageid]
        except KeyError:
            page_channel = _Channel(self.publisher, pageid)
            user_channel = self._get_user_channel()
            world_channel = self.world


            channel_names = ['world', user_channel.id, pageid]
            subscription = self.publisher.subscribe(channel_names)

            context = _Context(page_channel, user_channel, world_channel,
                               subscription)

            page = self.page_cls(context)

            self.context_by_pageid[pageid] = context
            self.page_by_id[pageid] = page
            return page
