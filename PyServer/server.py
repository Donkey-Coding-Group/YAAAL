# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>
""" YAAAL.server
    ~~~~~~~~~~~~ """

import os
import sys
import urlparse
import traceback
import SocketServer
import BaseHTTPServer

class BasicRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.base_path = os.environ.get('RQH_BASEPATH', os.getcwd())
        self.handles = {}
        self.filehandles = {}
        self.on_init()

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    # BaseHTTPServer.BaseHTTPRequestHandler

    def do_GET(self):
        path  = self.get_path()
        query = self.get_GET()

        if not path:
            self.handle_index(query)
            return

        handle = self.match_handles(self.handles, path)
        if handle:
            handle[1](path, query)
            return

        handle = self.match_handles(self.filehandles, path)
        if handle:
            self.cgifile(handle[1], path, query)
            return

        self.handle_404(path, query)

    # BaseRequestHandler

    def match_handlesequence(self, sequence, path):
        matches = True 
        for h, p in zip(sequence, path):
            if h != p:
                matches = False
                break
        return matches

    def match_handles(self, handles, path):
        longines = [-1, None]
        for handle, func in handles.iteritems():
            if len(handle) < longines[0]:
                continue

            if self.match_handlesequence(handle, path):
                longines[0] = len(handle)
                longines[1] = handle, func

        return longines[1]

    def cgifile(self, filename, path=(), query={}, globals={}, locals=None):
        filename = os.path.join(self.base_path, filename).replace('~', os.environ['HOME'])
        if not os.path.exists(filename):
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('404: File %r does not exist.' % filename)
            return

        globals = globals.copy()
        if locals is None:
            locals = globals

        globals['request'] = self
        globals['path'] = path
        globals['query'] = query
        globals['__file__'] = filename
        globals['__name__'] = '__main__'

        stdout = sys.stdout
        stdin  = sys.stdin
        sys.stdout = self.wfile
        sys.stdin  = self.rfile

        try:
            with open(filename) as fl:
                code = compile(fl.read(), filename, 'exec')
                exec code in globals
        except:
            self.wfile.write('\n')
            self.wfile.write(traceback.format_exc())
            return False
        finally:
            sys.stdout = stdout
            sys.stdin  = stdin

        return True


    def on_init(self):
        pass

    def get_path(self):
        path = self.path
        if '?' in path:
            path = path[:path.find('?')]
        return filter(lambda x: not not x, map(lambda x: x.strip(), path.split('/')))

    def get_GET(self):
        query = self.path
        if '?' in query:
            query = query[query.find('?') + 1:]
            query = urlparse.parse_qs(query)
        else:
            query = {}
        return query

    def handle_index(self, query):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('404')

    def handle_404(self, path, query):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('404')

class YAAALRequestHandler(BasicRequestHandler):

    def on_init(self):
        self.filehandles.update({
            ('api',):               'api.py',
            ('api', 'get-files'):   'api-getfiles.py',
        })

    def handle_index(self, query):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write("Hello, this is the index file.")

    def handle_404(self, path, query):
        self.send_response(404)
        self.end_headers()
        self.wfile.write("404: %s" % path)


    # YAAALRequestHandler

    def respond(self):
        self.send_response(200)
        self.send_header('Content-type:', 'text/json')
        self.end_headers()


    def handle_api(self, path, query):
        self.respond()
        print "api"

    def handle_api_getfiles(self, path, query):
        self.respond()
        print "api-getfiles"

def YAAALServer(host='', port=6150):
    return BaseHTTPServer.HTTPServer((host, port), YAAALRequestHandler)







