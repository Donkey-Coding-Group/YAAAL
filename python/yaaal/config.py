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

import views
import views.api

# HANDLERS - Associate regular-expressions with a handler-function here.
# Note: This list is modified on server-startup, where it is exchanged
#       with the list that is in the request-handlers slot. One can
#       modify it at runtime, however, make sure to only insert
#       compiled regular-expressions, not in raw-string format.
HANDLERS = (

    # API
    ('^/api/registered-apps$',      views.api.registered_apps),
    ('^/api/find-apps$',            views.api.find_apps),
)

# HANDLE_404 - Handle 404 errors here. It takes a yaaal.request_handler.Request
# instance as single argument. Note that it's match-slot will be None always.
HANDLE_404 = None

# HANDLE_EXCEPTION - Handle an exception that may occure within a
# handler-function. It takes a yaaal.request_handler.Request instance and the
# occured exception as arguments. Note that the request's match-slot will be
# always None. 
HANDLE_EXCEPTION = None


    


