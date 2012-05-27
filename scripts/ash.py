#!/usr/bin/python

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>


""" ash
    ~~~

    Simple command-line tool for hashing based on arguments or stdin. """

import os
import sys
import argparse
import hashlib

HASHNAMES = {'md5': hashlib.md5, 'sha': hashlib.sha1, 'sha224': hashlib.sha224,
             'sha256': hashlib.sha256, 'sha384': hashlib.sha384,
             'sha512': hashlib.sha512}
HASHNAMES_str = ' | '.join(sorted(HASHNAMES.keys()))

def main():
    parser = argparse.ArgumentParser(description='Hashing app.')
    parser.add_argument('-p', '--piped', default=False, action='store_true',
        help='read hashes from stdin rather than from the command-line.')
    parser.add_argument('-a', '--algo', dest='algo', default='md5',
        help='the hashing-algorith. possible names are %s. default is md5.' %
             HASHNAMES_str)
    parser.add_argument('sources', nargs='*')
    args = parser.parse_args()

    hasher = HASHNAMES.get(args.algo, None)
    if not hasher:
        parser.error('unknow algorithm %r. possible names are %s.' %
                     (args.algo, HASHNAMES_str))

    sources = args.sources[:]

    if args.piped:
        sources.extend(map(lambda x: x.strip(), sys.stdin.readlines()))

    for source in sources:
        if source:
            print hasher(source).hexdigest()

    return 0


if __name__ == "__main__":
    main()


