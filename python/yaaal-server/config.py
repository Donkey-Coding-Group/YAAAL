#!/usr/bin/python
# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>

import views

# HANDLERS - Specify the handlers as a dictionary, while the keys are
# regular-epressions that will be matched against the request URI, and the
# values are callable objects accepting 4 arguments.
HANDLERS = {
}

# HANDLE_404 - Give a function to be able to handle requests that do not match
# with any of the patterns above.
HANDLE_404 = None

# HANDLE_EXCEPTION - Give a function to be able to handle exceptions that might
# occure within any of the above handlers.
HANDLE_EXCEPTION = None


