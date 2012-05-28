#!/usr/bin/python

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>


""" yaaal.server
    ~~~~~~~~~~~~ """

import os
import re
import sys
import copy
import urllib
import urlparse
import traceback
import BaseHTTPServer

class BaseRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Public. This class implements basic high-level request-handling
        based on regular-expressions associated with functions. For more
        information, see :meth:`__init__`. """

    def __init__(self, logging=True, make_copies=True):
        """ Override. The constructor totally overrides the constructor of
            the base-class and reimplements the behaviour of a request handler.
            Instead of handling the request on initialization, which is done
            within the base-class constructor, the ``__call__`` method is
            implemented, which makes it possible to pass an **instance** of
            this request-handler to a TCPServer instead of it's class.

            + *logging*: Toggles logging.
            + *make_copies*: Whether to make a copy of this instance on
              :meth:`__call__` or not. """
        self.handlers = []
        self.logging = logging
        self.make_copies = make_copies
        self.on_init()


    def __call__(self, *args, **kwargs):
        """ This method is implemented to be able to pass an instance of a
            request-handler to a TCPServer instead of it's class. Depending
            on the :attr:`make_copies` slot, it creates a copy of the current
            instance or uses the actual instance and calls the base-classes'
            constructor. """
        if self.make_copies:
            new = copy.copy(self)
        else:
            new = self
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(new, *args, **kwargs)
        return new

    #: BaseHTTPServer.BaseHTTPRequestHandler

    def log_message(self, *args, **kwargs):
        if self.logging:
            BaseHTTPServer.BaseHTTPRequestHandler.log_message(self, *args,
                                                              **kwargs)

    def do_GET(self):
        path = self.get_requestpath()
        getvars = self.get_getvars()
        postvars = self.get_postvars()

        for regex, function in self.handlers:
            match = regex.match(path)
            if match:
                try:
                    result = function(path, getvars, postvars, match)
                except Exception as exc:
                    self.handle_exception(path, getvars, postvars, exc)
                else:
                    self.process_result(result)
                return

        self.handle_404(path, getvars, postvars, None)

    do_POST = do_GET

    #: BaseRequestHandler

    def process_result(self, result):
        """ Private. Process *result* which was returned from a
            handler-function. Extract the content (if neccessary, e.g. file-like
            objects) and send it to the client. """

        if not result:
            return

        if isinstance(result, basestring):
            pass
        elif hasattr(result, 'read'):
            result = result.read()
        else:
            raise TypeError('This type of result is not supported.')

        self.wfile.write(result)

    def add_handler(self, regex, function, flags=0):
        """ Public. Add a handler (a regular-expression that will be
            matched against the HTTP request-path) and associate it
            with *function*. *\*args* is optional for adding flags to
            the re-compilation. Raises ``TypeError`` in case *function*
            is not a callable object. Raises any exception :func:`re.compile`
            could raise.

            **About Handlers:**

            A handler is a function taking five arguments:

            1. The :class:`BaseRequestHandler` instance it was called from.
            2. A string containing the requested URI without GET-vars
            3. A :class:`dict` of GET variables
            4. A :class:`dict` of POST variables
            5. A SRE_Match object that was returned from the compiled pattern
               when matching the URI

            This function can either return a string or a file-like object
            (which is indicated wether the object has a ``read()`` method) or
            ``None``.
            The content will be (unpacked and) sent to the client. Response and
            headers must be sent with the appropriate methods of the
            request-handler. """

        if not hasattr(function, '__call__'):
            raise TypeError('arg function is not callable.')

        regex = re.compile(regex, flags)

        self.handlers.append((regex, function))

    def add_handlers(self, *handlers):
        """ Public. Call :meth::`add_handler` for each element in *\*
            """

        for handler in handlers:
            self.add_handler(handler)

    def get_requestpath(self):
        """ Public. Return the requested path of the server. This is the
            requested URI without GET vars. """

        query = self.path
        index = query.find('?')
        if index >= 0:
            path = query[:index]
        else:
            path = query
        return path

    def get_getvars(self):
        """ Public. Return a dictionary of variables defined in GET via the
            request URI. """

        query = self.path
        index = query.find('?')
        if index >= 0:
            query = query[index + 1:]
            query = urlparse.parse_qs(query)
        else:
            query = {}
        return query

    def get_postvars(self):
        """ Public. Returns a dictionary of variables defined in GET
            via the sent headers. """

        # TODO: implements BaseRequestHandler.get_postvars()
        pass

    def on_init(self):
        """ Override. Called on initialization. Handlers should be
            added here. """
        pass

    def handle_404(self, path, getvars, postvars, match):
        """ Override. Called in case no registered handler did match. The
            standard-implementation outputs a basic HTML with information.
            Response and headers must be sent. Just like handlers, this method
            can return either a string or a file-like object or ``None``.
            Note that *match* will be always ``None``. """

        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('<!DOCTYPE html><html><body><h1>404 Not Found</h1>' +
            '<span>The page you were looking for could not be found.' +
            '</span></body></html>')

    def handle_exception(self, path, getvars, postvars, exception):
        """ Override. Called in case a handler-function throwed an exception.
            While the first 3 arguments equal the ones passed to a
            handler-function, the last is not. Instead of a SRE_Match object,
            it is the exception that was raised.

            The default implementation respondes a 501 Internal Server Error and
            prints the traceback to stderr. """

        self.send_response(501)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write('<!DOCTYPE html><html><body><h1>501 Internal Server '
            'Error</h1><span>An internal error occured. Please contact the ' +
            'host.</span></body></html>')

        print
        print >> sys.stderr, "Exception in handling request to %r." % path
        print >> sys.stderr, traceback.format_exc()
        print



def main():
    httpd = BaseHTTPServer.HTTPServer(('', 8080), BaseRequestHandler())
    httpd.handle_request()

main()
