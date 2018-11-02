#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 17:00
# @Author  : Fred Yang
# @File    : app.py
# @Role    : 事件提醒

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import define, options
from controller.event import EventHandler
from database import init_db

define("port", default=8888, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/event', EventHandler)
        ]

        settings = dict(
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            # xsrf_cookies=True,
            # login_url="/login",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    init_db()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
