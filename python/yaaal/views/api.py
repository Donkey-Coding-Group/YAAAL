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

from views import _path_

import models

import json

OK = 'OK'
WRONG_ARGUMENT = 'WRONG_ARGUMENT'

def registered_apps(request):
    """ *View*. Returns the registered apps in JSON format. """

    request.headers['Content-type'] = 'text/plain'

    apps = models.Applications.get_registered_apps()
    return json.dumps(apps)

def find_apps(request):
    """ *View*. Returns alls apps that can be found on the users system in JSON
        format. """

    request.headers['Content-type'] = 'text/plain'
    data = {}

    try:
        indent = int(request.GET['indent'][0])
    except ValueError:
        data['status'] = WRONG_ARGUMENT
        data['message'] = 'Argument `index` is not convertable to int.'
        data['apps'] = None
        return json.dumps(data)
    except KeyError:
        indent = 0

    data['status'] = OK
    data['apps'] = models.Applications.find_all_apps()


    return json.dumps(data, indent=indent)
        




