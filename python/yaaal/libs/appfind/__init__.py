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
""" appfind - Find applications and icons on a Linux installation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Basic Usage
    -----------

    >>> import appfind
    >>> apps = appfind.find()
    >>> len(apps)
    149
    >>> for app in apps:
    ...     if 'python' in app['name'].lower():
    ...         print app['name']
    ...
    Python 2.7

    """

__author__  = 'Niklas Rosenstein <rosensteinniklas@googlemail.com>'
__version__ = (0, 1, 0)

import os
import sys

import re
import glob
import numbers
import ConfigParser

APPLICATION_PATHS   = ['/usr/share/applications',
                       '$HOME/.local/share/applications']
ICON_PATHS          = ['/usr/share/pixmaps',
                       '/usr/share/app-install/icons',
                       '/usr/share/icons/']

# Regular expression for substituting Exec-code flags in Desktop Entries.
DKENTRY_EXECREPL    = re.compile('(?<!%)%[fFuUnNickvm]')

# Regular expression to extract icon-size from a path.
PATHEXTRCT_ICONSIZE = re.compile('/\s*(\d+)(?:\s*x\s*(\d+)\s*)?/.+')


# Process application paths to substitute $HOME with the environment value.
for index, path in enumerate(APPLICATION_PATHS):
    path = path.replace('$HOME', os.environ['HOME'])
    APPLICATION_PATHS[index] = path


class Size(object):
    """ *Public*. This class is used as a container for a width and height slot.
    """

    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def __bool__(self):
        return self.width < 0 or self.height < 0

    def __cmp__(self, other):
        if isinstance(other, Size):
            if self.width < other.width and self.height < other.height:
                return -1
            elif self.width == other.width and self.height == other.height:
                return 0
            else:
                return 1
        else:
            if self.width < other and self.height < other:
                return -1
            elif self.width == other and self.height == other:
                return 0
            else:
                return 1

class PixmapRef(object):
    """ *Public*. This class associates a filename and a :class:`Size` object.
        On initialization, it can automatically extract a suffix from the
        filename. """

    def __init__(self, size, filename, suffix=None):
        self.fullname = filename

        if suffix is None:
            suffix = filename.rfind('.')
            if not suffix < 0:
                suffix, filename = filename[suffix + 1:], filename[:suffix]
            else:
                suffix = ''

        self.size = size
        self.filename = os.path.basename(filename)
        self.suffix = suffix

def _ff_split(elements, rel_dir=None):
    """ *Private*. Split up list a list of mixed file- and folernames and
        return two lists respectively. It will ignore any elements that are
        neither files nor folders. """

    files = []
    folders = []

    for elm in elements:
        if rel_dir:
            check = os.path.join(rel_dir, elm)
        else:
            check = elm

        if os.path.isdir(check):
            folders.append(elm)
        elif os.path.isfile(check):
            files.append(elm)

    return files, folders

def _filter_bool(sequence):
    """ *Private*. Filter a sequence by it's elements truth-value. """

    return filter(lambda x: not not x, sequence)

def process_pixmap_name(pixmap, to_dct):
    """ *Public, Low-level*. Processes the name of *pixmap* and inserts some
        entries into the dictionary *to_dct*. This function is used by
        :func:`find_all_pixmaps`. """

    match = PATHEXTRCT_ICONSIZE.search(pixmap)
    if match:
        w, h = match.groups()
        w = int(w)
        if h is not None:
            h = int(h)
        else:
            h = w
    else:
        w = h = -1
    size = Size(w, h)
    pref = PixmapRef(size, pixmap)
    name = os.path.basename(pref.filename)

    to_dct.setdefault(name, []).append(pref)
    if pref.suffix:
        to_dct.setdefault(name + '.' + pref.suffix, []).append(pref)

    return pref
    

def find_pixmap(pixname, search_dirs=None, max_depth=-1, allow_sufx=(),
                deny_sufx=(), isufx=True, match_cb=lambda v,n: v.startswith(n)):
    """ *Public*. Search for a pixmap/icon by name passed via *pixname* in all
        directories listed in *search_dirs*. If omitted, it defaults to the
        paths defined on module-level (:attr:`appfind.ICON_PATHS`). *max_depth*
        defines the maxmimum recursion-level for searching for the pixmap,
        while `-1` indicates no limit.

        One can allow or deny suffices with the respectively named arguments
        *allow_sufx* and *deny_suffx*. Note that they will still fall into
        account in case *pixmap* does already have a suffix. When *isufx* is
        `True`, the case of the suffix will be converted to lower-case, i.e.
        the case is completely ignored (expecting that all suffices in
        *allow_sufx* are already lower-cased).

        With *match_cb*, one can define a callback that is used to determine
        wether a filename matches the pixname. It accepts two arguments, the
        filename and the requested name for the pixmap.
        By default, this searches 

        This function is an recursive generator. """

    if not search_dirs:
        search_dirs = ICON_PATHS

    for folder in search_dirs:
        files, subdirs = _ff_split(os.listdir(folder), rel_dir=folder)
        files = filter(lambda x: x.startswith(pixname), files)
        subdirs = map(lambda x: os.path.join(folder, x), subdirs)

        for file_ in files:
            suffix = file_.rfind('.')
            if not suffix < 0:
                suffix = file_[suffix + 1:]
            else:
                suffix = ''

            if (suffix not in allow_sufx and allow_sufx) or suffix in deny_sufx:
                continue

            yield os.path.join(folder, file_)

        if max_depth != 0 and subdirs:
            values = find_pixmap(pixname, subdirs, max_depth - 1, allow_sufx,
                                 deny_sufx, isufx, match_cb)
            for v in values:
                yield v

def find_all_pixmaps(search_dirs=None, max_depth=-1, to_dct=None,
                     match_cb=lambda v: True):
    """ *Public*. Return a dictionary of all pixmaps than can be found in
        folders passed via the iterable *search_dirs*. If omitted, it defaults
        to the paths defined on module-level (:attr:`appfind.ICON_PATHS`). The
        icons are stored the way a `*.desktop` file would specify it. Define
        the maximum recursion-level via *max_depth* (`-1` indicates no limit).

        One can specify the dictionary to put the results in by passing a
        subscriptable object to *to_dct*. With *match_cs*, one can specify a
        callback function which is used to determine wether the found file
        matches a pixname or not. It takes the filename as single argument.

        The keys stored in the dicionary are stored once **with** the suffix
        and once without, but always only by filename. The values are lists
        full of :class:`PixmapRef` instances.

        A pixmap's size is determined as good as possible (by
        :func:`process_pixmap_name`), but most time it can not be retrieved.
        However, the implementation of the :class:`Size` class allows one to
        extract the biggest pixmap from the available ones using the built-in
        function :func:`max`.

        >>> import appfind
        >>> pixmaps = appfind.find_all_pixmaps()
        >>> print max(pixmaps['boot'], key=lambda).fullname
        /usr/share/icons/Humanity/apps/48/boot.svg
        """

    if to_dct is None:
        to_dct = {}

    if not search_dirs:
        search_dirs = ICON_PATHS

    for folder in search_dirs:
        files, subdirs = _ff_split(os.listdir(folder), folder)
        subdirs = map(lambda x: os.path.join(folder, x), subdirs)

        for file_ in files:
            if match_cb(file_):
                process_pixmap_name(os.path.join(folder, file_), to_dct)

        if max_depth != 0 and subdirs:
            find_all_pixmaps(subdirs, max_depth - 1, to_dct, match_cb)

    return to_dct
    
def parse_desktop_file(filename, pixmaps, ):
    """ *Public*. Parse a single `*.desktop` file and return a dictionary with
        the relevant data. Raises `TypeError` in case the file is not valid.
        This method requires a dictionary of pixmaps that it can access which
        is passed via *pixmaps*. It's keys must be associated with instances
        of :class:`PixmapRef`.

        When this function returns `None`, it means that the `*.desktop` file
        specifies the value *NoDisplay* with *true*. This will only happen
        when *allow_nodisplay* is set to `False`.

        Entries the dictionary is guarantued to own:

        * name
        * exec
        * type

        Entries the dictionary may have default values:

        ==============================
        key             default
        ==============================
        version         1.0
        encoding        utf-8
        comment         None
        icon            None
        categories      []
        mime-types      []
        nodisplay       false
        ============================== """

    parser = ConfigParser.ConfigParser()
    parser.read([filename])

    if not parser.has_section('Desktop Entry'):
        raise TypeError('file is not a valid *.desktop file.')

    data = dict(parser.items('Desktop Entry'))

    try:
        encoding = data.get('encoding', 'utf-8')
        result = {
            'name':       data['name'].decode(encoding),
            'exec':       DKENTRY_EXECREPL.sub('', data['exec']).decode(encoding),
            'type':       data['type'].decode(encoding),
            'version':    float(data.get('version', 1.0)),
            'encoding':   encoding,
            'comment':    data.get('comment', '').decode(encoding) or None,
            'categories': _filter_bool(data.get('categories', '').
                                            decode(encoding).split(';')),
            'mimetypes':  _filter_bool(data.get('mimetype', '').
                                            decode(encoding).split(';')),
        }
    except KeyError as exc:
        raise TypeError('file is not a valid *.desktop file. missing item ' +
                        '%s.' % exc.message)
    except ValueError as exc:
        raise TypeError('file is not a valid *.desktop file. value for ' +
                        'Version can not be converted to integer.')

    nodisplay = data.get('nodisplay', 'false').strip().lower()
    if nodisplay == 'true':
        nodisplay = True
    elif nodisplay == 'false':
        nodisplay = False
    else:
        raise TypeError('file is not a valid *.desktop file. value for ' +
                        'NoDisplay is not true/false but %r.' % nodisplay)

    icon = data.get('icon', '').decode(encoding) or None
    if icon:
        if os.path.isabs(icon):
            pass
        else:
            pixmap = pixmaps.get(icon.strip())
            if pixmap:
                icon = pixmap.fullname
            else:
                icon = None

    result['nodisplay'] = nodisplay
    result['icon'] = icon
    return result

def find(search_dirs=None, pixmaps=None, max_depth=-1):
    """ *Public*. Find all `*.desktop` files in the directories passed in the
        seuquence *search_dirs*. If omitted, it defaults to the paths
        defined on module-level (:attr:`appfind.APPLICATION_PATHS`). One can
        define the maximum recursion-level via *max_depth* (`-1` indicates no
        limit). Usually, desktop-files do not need to be searched recursively,
        however..

        *pixmaps* must be a dictionary of :class:`PixmapRef` instances (as
        values) associated with the names they may be accessed with from the
        `*.desktop` files. If omitted, :func:`find_all_pixmaps` is called and
        the biggest pixmaps are extracted.

        This function is a recursive generator. """

    if pixmaps is None:
        pixmaps_ = find_all_pixmaps()
        pixmaps  = {}
        for k, v in pixmaps_.iteritems():
            pixmaps[k] = max(v, key=lambda x: x.size)

    if not search_dirs:
        search_dirs = APPLICATION_PATHS

    for folder in search_dirs:
        files, subdirs = _ff_split(os.listdir(folder), folder)
        subdirs = map(lambda x: os.path.join(folder, x), subdirs)

        for file_ in files:
            if file_.endswith('.desktop'):
                try:
                    yield parse_desktop_file(os.path.join(folder, file_),
                                             pixmaps)
                except TypeError as exc:
                    pass

        if max_depth != 0 and subdirs:
            for e in find(subdirs, pixmaps, max_depth - 1):
                yield e



