#!/usr/bin/python
# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>

import os
import sys

#: Interface that must be implemented for the platforms.

def getApplications():
    """ Return a list of dictionaries where each of them contains information
        about and application on the system. Required keys are:

        :Index:         A unique index that identifies the application.
        :Name:          The applications name as it is displayed
        :Icon:          Path to an image-file, or ``None`` if not icon.
        :Categories:    A list of strings containing categories for the app.
        :Desc-Short:    A short description of the application.
        :Desc-Long:     A long description of the application.
        :User-rate:     A number between 0 and 5 for the users-rating.

        **Optional entries:**

        :Screenshots:   A list of paths to images of screenshots. """

    raise NotImplemented

def setApplicationData(app_index, name, value):
    """ Set custom data for an application identified with the index
        *app_index*. *value* will be associated with *name* and retrieved either
        via :func:`getApplications` or :func:`getApplicationData`. """

    raise NotImplemented

def getApplicationData(app_index, name, default=None):
    """ Read custom data from the application identified with the index
        *app_index*. The value assiciated with *name* is returned or *default*,
        if no such value was set. """

    raise NotImplemented



if os.name == 'posix':
    from model_posix import *
elif os.name == 'mac':
    from model_mac import *
elif os.name == 'win':
    from model_win import *
else:
    raise NotImplemented('The platform %r is not supported.' % os.name)




