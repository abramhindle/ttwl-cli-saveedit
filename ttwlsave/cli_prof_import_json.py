#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2020-2021 CJ Kucera (cj@apocalyptech.com)
# 
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the authors be held liable for any damages arising from
# the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software in a
#    product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
# 3. This notice may not be removed or altered from any source distribution.

import os
import sys
import argparse
import ttwlsave
from ttwlsave.bl3profile import BL3Profile

def main():

    # Set up args
    parser = argparse.ArgumentParser(
            description='Import BL3 Profile JSON v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='BL3 CLI SaveEdit v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-j', '--json',
            type=str,
            required=True,
            help='Filename containing JSON to import')

    parser.add_argument('-t', '--to-filename',
            dest='filename_to',
            type=str,
            required=True,
            help='Filename to import JSON into')

    parser.add_argument('-c', '--clobber',
            action='store_true',
            help='Clobber (overwrite) files without asking')

    # Parse args
    args = parser.parse_args()

    # Make sure that files exist
    if not os.path.exists(args.filename_to):
        raise Exception('Filename {} does not exist'.format(args.filename_to))
    if not os.path.exists(args.json):
        raise Exception('Filename {} does not exist'.format(args.json))

    # Load the profile file
    prof_file = BL3Profile(args.filename_to)

    # Load the JSON file and import (so we know it's valid before
    # we ask for confirmation)
    with open(args.json, 'rt') as df:
        prof_file.import_json(df.read())

    # Ask for confirmation
    if not args.clobber:
        sys.stdout.write('Really import JSON from {} into {} [y/N]? '.format(
            args.json,
            args.filename_to,
            ))
        sys.stdout.flush()
        response = sys.stdin.readline().strip().lower()
        if response == 'y':
            pass
        else:
            print('')
            print('Aborting!')
            print('')
            sys.exit(1)

    # ... and save.
    prof_file.save_to(args.filename_to)

    # Report!
    print('')
    print('Done!')
    print('')

if __name__ == '__main__':
    main()

