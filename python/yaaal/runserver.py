#!/usr/bin/env python
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

import logging
import argparse
import BaseHTTPServer

__path__ = os.path.dirname(__file__)
sys.path.insert(0, __path__)
sys.path.insert(0, os.path.join(__path__, 'libs'))

import yaaal
import yaaal.util
import yaaal.request_handler
import config

class YAAALRequestHandler(yaaal.RequestHandler):
    """ This class implements grabbing handlers from the configuration-file. """

    def on_init(self):
        self.add_handlers(config.HANDLERS)
        config.HANDLERS = self.handlers

    def handle_404(self, path, GET, POST):
        if config.HANDLE_404:
            request_o = yaaal.request_handler.Request(path, GET, POST, None)
            request_o.response = 404
            result = config.HANDLE_404(request_o)
            self._proc_request_object(request_o)
            return result
        else:
            return yaaal.RequestHandler.handle_404(self, path, GET, POST)

    def handle_exception(self, path, GET, POST, exc):
        if config.HANDLE_EXCEPTION:
            request_o = yaaal.request_handler.Request(path, GET, POST, None)
            request_o.response = 500
            result = config.HANDLE_EXCEPTION(request_o, exc)
            if request_o.invoked_404:
                return self.handle_404(path, GET, POST)
            else:
                self._proc_request_object(request_o)
            return result
        else:
            return yaaal.RequestHandler.handle_exception(self, path, GET, POST,
                                                         exc)


def main():
    parser = argparse.ArgumentParser(description='Run the YAAAL Server.')
    parser.add_argument('port', nargs='?', default=6150, type=int,
        help='the servers port. default is 6150.')
    parser.add_argument('-l', '--log-file', default='stderr',
        help='filename to put loggings in. stdout | stderr | none or a ' +
             'filename.')
    parser.add_argument('--log-level', default='DEBUG',
        help='the logging level. default is DEBUG.')
    args = parser.parse_args()


    if args.log_level not in 'DEBUG INFO WARNING ERROR CRITICAL'.split():
        parser.error('invalid log-level %s.' % args.log_level)

    max_port = 2**16
    if not (1024 < args.port < max_port):
        parser.error('port must in in range 1024 - %d.' % max_port)

    level = getattr(logging, args.log_level)

    if args.log_file == 'none':
        logger = None
    else:
        if args.log_file == 'stdout':
            handler = logging.StreamHandler(sys.stdout)
        elif args.log_file == 'stderr':
            handler = logging.StreamHandler(sys.stderr)
        else:
            handler = logging.FileHandler(args.log_file)

        formatter = yaaal.util.MultilineFormatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger('yaaal-server')
        logger.addHandler(handler)

        handler.setLevel(level)
        logger.setLevel(level)

    handler = YAAALRequestHandler(logger)
    httpd = BaseHTTPServer.HTTPServer(('', args.port), handler)
    httpd.serve_forever()

    return 0

if __name__ == "__main__":
    sys.exit(main())

