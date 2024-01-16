import asyncio
from typing import Awaitable, Optional, Union
import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import time
from event_parser import parseEvents
import json, copy

funcs = {}
globalApp = None

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open success")
        self.uri = self.get_argument("path", default="/")
        # timer that sends data to the front end once per second
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1000)
        self.timer.start()

    def on_close(self):
        self.timer.stop()

    def send_data(self, message = ""):
        # send the current time to the front end
        self.write_message(message)
    
    def on_message(self, message: str | bytes) -> Awaitable[None] | None:
        doc = funcs[self.uri]()
        data = parseEvents(doc, message)
        changes = doc.changed
        if data == None:
            self.send_data({"changes": changes})
        else:
            self.send_data({"changes": changes, "id": data[0].id, "effect": data[1]})
        doc.resetChanged()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        file = open("index.html", "rb")
        self.write(file.read())

def make_app(routes):
    return tornado.web.Application(routes)
    

def server(port):
    global globalApp
    class Serve:
        def __init__(self):
            self.routes= [
                (r"/websocket", WebSocketHandler)
            ]
            self.port = port
        
        def route(self, path, method, func = None, file = None):
            if(file):
                class Handler(tornado.web.RequestHandler):
                    def get(self):
                        f = open(file, "rb")
                        self.write(f.read())
                self.routes.append((path, Handler))
            else:
                if(method == "get"):
                    class Handler(tornado.web.RequestHandler):
                        def get(self):
                            func().resetChanged()
                            self.write(str(func()))
                    self.routes.append((path, Handler))
                elif method == "post":
                    class Handler(tornado.web.RequestHandler):
                        def post(self):
                            func().resetChanged()
                            self.write(str(func()))
                    self.routes.append((path, Handler))
                funcs[path] = func
            
                    
        async def start(self):
            app = make_app(self.routes)
            app.listen(self.port)
            await asyncio.Event().wait()
        
    app = Serve()
    globalApp = app
    return app