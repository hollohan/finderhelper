from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app
from json import loads

crt = '../creds/server.crt'
key = '../creds/server.key'

http_server = HTTPServer(WSGIContainer(app), ssl_options={'certfile':crt, 'keyfile':key})
http_server.listen(443)
IOLoop.instance().start()
