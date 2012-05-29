# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

import re
import cgi
import copy
import logging
import urlparse
import traceback
import cStringIO
import BaseHTTPServer

import util
stderr_logger = util.stderr_logger()

class FakedRequestHandler(object):
    """ This class is passed to a handler-function registered to an instance
        of :class:`RequestHandler`. The handler should use it to send the
        response and headers.

        It supports the following methods and and attributes that are normally
        accessed via the original request-handler:

        + ``send_response(int response)`` *method*
        + ``send_header(str name, str value)`` *method*
        + ``end_headers()`` *method*
        + ``wfile`` *attribute*
        """

    def __init__(self):
        self.response = -1
        self.headers = {}
        self.wfile = cStringIO.StringIO()

    #: FakedRequestHandler

    def send_response(self, response):
        self.response = int(response)

    def send_header(self, name, value):
        self.headers[name] = value

    def end_headers(self):
        pass

    def default_response(self, code=200,
                         headers={'Content-type': 'text/html'}):
        """ *Public*. Send a response with *code* and *headers* to the
            client. """

        self.send_response(code)
        for k, v in headers.iteritems():
            self.send_header(k, v)
        self.end_headers()

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ The :class:`RequestHandler` class implements matching regular
        expressions against the request-URI and call associated
        handler-functions (similar with Django).

        This class does not behave the same way it's parent-class
        :class:`BaseHTTPRequestHandler<BaseHTTPServer.BaseHTTPRequestHandler>`
        does. When using the latter directly, or by another subclass that does
        not change the behaviour, the class itself must be passed to a
        server-constructor (e.g. :class:`HTTPServer<BaseHTTPServer.HTTPServer>`
        or :class:`TCPServer<SocketServer.TCPServer>`).  
        Instead of passing the class of the RequestHandler to a server, one
        passes an instance of it. This enables to pass arguments on construction
        that will influence the way the handler will work (subclasses can of
        course accept new arguments and change their behaviour likewise).

        .. attribute:: logger

            This class overwrites the
            :meth:`BaseHTTPServer.BaseHTTPRequestHandler.log_message` method.
            By passing a logger to the constructor, the request-handler will log
            messages in it. By default, it is a logger to stderr.

            .. note::

                :class:`BaseHTTPServer.BaseHTTPRequestHandler` does some logging
                operations by default.

        .. attribute:: make_copies

            As already mentioned, instead of the class itself, an instance of
            this (sub-) class should be passed to a server. As a constructor
            is invoked via :meth:`__call__` of a class-object, we can simulate
            an instance of this class actually *being* a class. When the
            server wants to create a new instance of the passed request-handler,
            the :meth:`__call__` implementation acts properly.

            When this slot is set to ``True``, :func:`copy.copy` is called on
            the current instance of this class, otherwise the current instance
            itself will be returned.

            .. warning::

                You usually don't want to set this to ``False`` as it is very
                likely to crash your application when multiple threads that are
                handling a request from a client are using the same
                request-handler object.

        .. attribute:: handlers

            A list of ``(regex, handler_function)`` pairs. Rather call
            :meth:`add_handler` or :meth:`add_handlers` than modifieng this
            list directly.
        """

    def __init__(self, logger=stderr_logger, make_copies=True):
        """ Constructor. See the attributes of this class to get a clue of what
            arguments this constructor expects. """

        self.logger = logger
        self.make_copies = make_copies
        self.handlers = []

        self.on_init()

    def __call__(self, *args, **kwargs):
        """ Object-calling. For more information, see :attr:`make_copies`. """

        if self.make_copies:
            new = copy.copy(self)
        else:
            new = self

        # Whoever did implement that, it doesn't seem like he didn't make his
        # head around the design. Why the heck is the request-handling done
        # within the constructor?!
        # However, know you know why we call the constructor on the
        # request-handler object here..
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(new, *args, **kwargs)

        return new

    #: BaseHTTPServer.BaseHTTPRequestHandler

    def log_message(self, format, *args):
        if self.logger:
            self.logger.info(format % args)

    def log_error(self, format, *args):
        if self.logger:
            self.logger.error(format % args)

    def do_GET(self, postvars=None):
        # :arg:`postvars` is passed via do_POST() as both procedures are
        # similiar, but do_GET() will fail if it wants to obtain POST-vars.

        path = self.get_PATH()
        getvars = self.get_GET()

        if postvars is None:
            postvars = {}

        # Go through each registered handler and match the regular-expression
        # against the requested path.
        for regex, handler in self.handlers:
            match = regex.match(path)
            if match:
                fake_handler = FakedRequestHandler()

                # Well, the regular-expression did match. But the
                # handler-function could throw an exception, so we have to
                # encapsulate it in try-except and handle it properly.
                try:
                    result = handler(fake_handler, path, getvars, postvars,
                                     match)
                    self._proc_fake_handler(fake_handler)
                except Exception as exc:
                    result = self.handle_exception(path, getvars, postvars, exc)

                if result:
                    self._proc_result(result)

                return True

        # Seems like no handler did match the requested path ...
        result = self.handle_404(path, getvars, postvars)
        if result:
            self._proc_result(result)

        return False

    def do_POST(self):
        postvars = self.get_POST()
        return self.do_GET(postvars=postvars)

    #: RequestHandler

    def _proc_fake_handler(self, fake_handler):
        """ *Private*. Processes an instance of :class:`FakedRequestHandler` to
            send the headers and it's content to the client. """

        self.send_response(fake_handler.response)
        for type, value in fake_handler.headers.iteritems():
            self.send_header(type, value)

        self.end_headers()

        fake_handler.wfile.seek(0)
        self.wfile.write(fake_handler.wfile.read())

    def _proc_result(self, result):
        """ *Private*. Handles the result returned from a handle, either
            registered or `:meth`handle_404` or :meth:`handle_exception`. """

        if hasattr(result, 'read'):
            result = result.read()

        self.wfile.write(result)

    def add_handler(self, regex, handler, flags=0):
        """ *Public*. Associate a regular-expression passed via *regex* with a
            function *handler*. One can specify flags to the compilation of
            the regular-expressions via *flags*.

            Such a function has to take 5 arguments:

            1. An instance of :class:`FakedRequestHandler`
            2. The request-URI (without GET)
            3. GET-vars
            4. POST-vars
            5. The match returned by the regular expression

            The response and it's headers must be sent via the request-handler
            instance. After that, one can either write directly to
            :attr:`wfile<BaseHTTTPServer.HTTPServer.wfile>` or return a string
            or a file-like object. If the latter is returned, it's ``close()``
            method is not called.

            Raises ``TypeError`` in case *handler* is not callable.

            .. note::

                The request-handler is not passed directly to a handler,
                because it can lead to (to the (api-) user) fatal errors when
                a response and headers have already been sent and an exception
                occures afterwards. :meth:`handle_exception` would then send
                a response and headers again and this text would be sent with
                the content of the error-message. """

        if not hasattr(handler, '__call__'):
            raise TypeError('handler is not callable.')
        
        regex = re.compile(regex, flags)

        self.handlers.append((regex, handler))

    def add_handlers(self, handlers):
        """ *Public*. Elements in the sequence *handlers* must support the
            iterator-interface to be extracted to :meth:`add_handler`.

            Add multiple handlers to this request-handler. """

        for item in handlers:
            self.add_handler(*item)

    def get_GET(self):
        """ *Public*. Return the GET vars passed to the current request. Will
            always succeed and return a dictionary. """

        request_uri = self.path
        index = request_uri.find('?')
        if index >= 0:
            return urlparse.parse_qs(request_uri[index + 1:])
        else:
            return {}

    def get_POST(self):
        """ *Public*. Return the POST vars passed to the current request. """
        # http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        return postvars

    def get_PATH(self):
        """ *Public*. Return the request path without GET-vars. """

        request_uri = self.path
        index = request_uri.find('?')
        if index >= 0:
            request_uri = request_uri[:index]
        return request_uri

    def on_init(self):
        """ *Override*. Called on initialization of this instance. This is just
            for convenience so one doesn't have to override :meth:`__init__`.
            """

        pass

    def handle_404(self, path, GET, POST):
        """ *Override*. This method is called in case no registered handler
            did match with the requested path. The default implementation
            sends a simple 404 error in HTML format. """

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('<DOCTYPE html><html><body>' +
            '<h1>404 Page Not Found</h1>' +
            '<span id=msg>The requested page could not be found.' +
            '</span></body></html>')

    def handle_exception(self, path, GET, POST, exc):
        """ *Override*. This method is called in case a registered handler
            throws an exception, i.e. it was not implemented properly. The
            default implementation shows a simple 500 error in HTML format
            and prints the exception. """

        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('<DOCTYPE html><html><body>' +
            '<h1>500 Internal Server Error</h1>' +
            '<span id=msg>An error occurred, please contact the domain-host.' +
            '</span></body></html>')

        full_msg = 'Exception on handling request to %r.\n' % path
        full_msg = full_msg + traceback.format_exc()
        self.log_error(full_msg)


