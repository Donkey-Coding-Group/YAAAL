# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>
""" YAAAL - Python Server for YAAAAL
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

import server

def main():
    host = 'localhost'
    port = 6150

    httpd = server.YAAALServer(host, port)
    httpd.handle_request()

main()

