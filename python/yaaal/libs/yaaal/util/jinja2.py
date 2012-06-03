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

from __future__ import absolute_import

import jinja2
import codecs


def load_template(filename):
    """ *Public*. Load a :class:`jinja2.Template` by filename. """

    with open(filename) as fl:
        return jinja2.Template(unicode(fl.read().encode('utf-8').decode('utf-8').encode('utf-8')))

def render_template(filename, context):
    """ *Public*. Render a :class:`jinja2.Template` by filename and context. """

    template = load_template(filename)
    return template.render(**context)


