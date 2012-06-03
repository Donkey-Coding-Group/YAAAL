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

from __main__ import __file__ as mainfile
maindir = os.path.dirname(mainfile)

import appfind


# This dictionary keeps track of the registered applications.
last_index = 0
registered_apps = {}
last_index_f = 0
found_apps = None

def new_index():
    """ Get a new index for the next application. """
    global last_index
    try:
        return last_index
    finally:
        last_index += 1

def new_index_f():
    """ Get a new index for the next application in found_apps. """
    global last_index_f
    try:
        return last_index_f
    finally:
        last_index_f += 1

def register_application(appdata):
    """ Register an application. Returns the applications index. Also modifies
        the *appdata* a little, first setting the index and second filling out
        missing data (such as user-rating, e.g.). """

    if not isinstance(appdata, dict):
        raise TypeError('appdata must be dictionary.')

    appdata['index'] = new_index()
    registered_apps[appdata['index']] = appdata

    if not appdata.has_key('rating'):
        appdata['rating'] = 0

    return appdata['index']

def unregister_application(index):
    """ Unregister an application by index. Returns None if no such applications
        was available, the app-dict otherwise. """

    if not index in registered_apps:
        return None

    appdata = registered_apps.pop(index)
    del appdata['index']
    return appdata

def get_application(index):
    """ Get an application by index or return `None` if not such application
        is registered. """

    return registered_apps.get(index, None)

def get_registered_applications():
    """ Returns all registered applications. """

    dct = registered_apps.copy()
    return dct

def get_found_apps():
    """ Return the found apps (from cache). """

    global found_apps
    if not found_apps:
        reload_found_apps()

    return found_apps

def reload_found_apps():
    """ Re-search for applications and return them. """

    global found_apps
    global last_index_r

    found_apps = dict(((i, e) for i, e in enumerate(appfind.find())))
    reg_apps = [v['name'] for v in registered_apps.values()]
    for k, v in found_apps.items():
        if v['name'] in reg_apps:
            del found_apps[k]
        else:
            last_index_r = k
            v['index'] = k

    return found_apps

def put_app_back(appdata):
    """ Put back an application to the found apps. """

    appdata['index'] = new_index_f()
    found_apps[appdata['index']] = appdata
    return appdata



