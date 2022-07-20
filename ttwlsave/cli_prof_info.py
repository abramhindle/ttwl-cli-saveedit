#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2020-2022 CJ Kucera (cj@apocalyptech.com)
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

import ttwlsave
import argparse
import itertools
from ttwlsave.ttwlprofile import TTWLProfile

def main():

    # Arguments
    parser = argparse.ArgumentParser(
            description='Wonderlands Profile Info Dumper v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='WL CLI SaveEdit v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='Show all available information',
            )

    parser.add_argument('-i', '--items',
            action='store_true',
            help='Show inventory items',
            )

    parser.add_argument('filename',
            help='Filename to process',
            )

    args = parser.parse_args()

    # Load the profile
    prof = TTWLProfile(args.filename)

    # Skeleton Keys
    print('Skeleton Keys: {}'.format(prof.get_skeleton_keys()))

    # SDUs
    sdus = prof.get_sdus_with_max(True)
    if len(sdus) == 0:
        print('No SDUs Purchased')
    else:
        print('SDUs:')
        for sdu, (count, max_sdus) in sdus.items():
            print(' - {}: {}/{}'.format(sdu, count, max_sdus))

    # Bank Items
    bank_items = prof.get_bank_items()
    print('Items in bank: {}'.format(len(bank_items)))
    if args.verbose or args.items:
        to_report = []
        for item in bank_items:
            if item.eng_name:
                to_report.append(' - {} ({}): {}'.format(item.eng_name, item.get_level_eng(), item.get_serial_base64()))
            else:
                to_report.append(' - unknown item: {}'.format(item.get_serial_base64()))
        for line in sorted(to_report):
            print(line)

    # Lost Loot Items
    lostloot_items = prof.get_lostloot_items()
    print('Items in Lost Loot machine: {}'.format(len(lostloot_items)))
    if args.verbose or args.items:
        to_report = []
        for item in lostloot_items:
            if item.eng_name:
                to_report.append(' - {} ({}): {}'.format(item.eng_name, item.get_level_eng(), item.get_serial_base64()))
            else:
                to_report.append(' - unknown item: {}'.format(item.get_serial_base64()))
        for line in sorted(to_report):
            print(line)

    # Customizations
    print('Customizations Unlocked: {}/{}'.format(
        len(prof.get_customizations()),
        prof.get_customizations_total(),
        ))

    # Myth Rank
    print('Myth Rank XP: {:,}'.format(prof.get_myth_xp()))
    total_myth = 0
    for stat, cur_value in prof.get_myth_rank_stats().items():
        if cur_value > 0:
            if total_myth == 0:
                print('Myth Rank Stats:')
            total_myth += cur_value
            if stat.num > 0:
                total = f'/{stat.num}'
            else:
                total = ''
            print(f' - {stat.label}: {cur_value}{total}')
    if total_myth == 0:
        print('No points allocated in Myth Rank')
    else:
        print(f'Total Myth Points Allocated: {total_myth}')

if __name__ == '__main__':
    main()
