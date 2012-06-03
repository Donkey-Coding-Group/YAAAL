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
import json

from __main__ import __file__ as mainfile
maindir = os.path.dirname(mainfile)

import models.applications as apps


def add_app(request):
    """ Adds an application by index (sent per URI) to the registered
        applications. """

    found_apps = apps.get_found_apps()
    index = int(request.match.group(1))

    if index not in found_apps:
        return '{"status": "INVALID_INDEX"}'

    id = apps.register_application(found_apps.pop(index))
    return '{"status": "OK"}'


def rm_app(request):
    """ Removes an entry from the registered applications. """

    index = int(request.match.group(1))
    appdata = apps.unregister_application(index)
    if not appdata:
        return '{"status": "INVALID_INDEX"}'

    apps.put_app_back(appdata)
    return '{"status": "OK"}'




