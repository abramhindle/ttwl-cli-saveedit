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

import os
import sys
import html
import argparse
import ttwlsave
from ttwlsave.ttwlsave import TTWLSave

def main():

    # Set up args
    parser = argparse.ArgumentParser(
            description='Process Mod-Testing Wonderlands Archive Savegames v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='WL CLI SaveEdit v{}'.format(ttwlsave.__version__),
            )

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-f', '--filename',
            type=str,
            help='Specific filename to process')

    group.add_argument('-d', '--directory',
            type=str,
            help='Directory to process (defaults to "step")')

    parser.add_argument('-i', '--info',
            type=str,
            help='HTML File to write output summary to')

    parser.add_argument('-r', '--reverse',
            action='store_true',
            help='Reverse the order of CSS in HTML rows')

    parser.add_argument('-o', '--output',
            type=str,
            required=True,
            help='Output filename/directory to use')

    parser.add_argument('-c', '--clobber',
            action='store_true',
            help='Clobber (overwrite) files without asking')

    # Parse args
    args = parser.parse_args()
    if not args.filename and not args.directory:
        args.directory = 'step'

    # Construct a list of filenames
    targets = []
    if args.directory:
        for filename in sorted(os.listdir(args.directory)):
            if '.sav' in filename:
                targets.append(os.path.join(args.directory, filename))
    else:
        targets.append(args.filename)

    # If we're a directory, make sure it exists
    if args.directory and not os.path.exists(args.output):
        os.mkdir(args.output)

    # If we've been given an info file, check to see if it exists
    if args.info and not args.clobber and os.path.exists(args.info):
        sys.stdout.write('WARNING: {} already exists.  Overwrite [y/N/a/q]? '.format(args.info))
        sys.stdout.flush()
        response = sys.stdin.readline().strip().lower()
        if response == 'y':
            pass
        elif response == 'n':
            args.info = None
        elif response == 'a':
            args.clobber = True
        elif response == 'q':
            sys.exit(1)
        else:
            # Default to No
            args.info = None

    # Open the info file, if we have one.
    if args.info:
        idf = open(args.info, 'w')

    # Now loop through and process
    files_written = 0
    if args.reverse:
        row_offset = 1
    else:
        row_offset = 0
    for filename in targets:

        # Figure out an output filename
        if args.filename:
            base_filename  = args.filename
            output_filename = args.output
        else:
            base_filename = filename.split('/')[-1]
            output_filename = os.path.join(args.output, base_filename)

        # See if the path already exists
        if os.path.exists(output_filename) and not args.clobber:
            sys.stdout.write('WARNING: {} already exists.  Overwrite [y/N/a/q]? '.format(output_filename))
            sys.stdout.flush()
            response = sys.stdin.readline().strip().lower()
            if response == 'y':
                pass
            elif response == 'n':
                continue
            elif response == 'a':
                args.clobber = True
            elif response == 'q':
                break
            else:
                # Default to No
                response = 'n'

        # Load!
        print('Processing: {}'.format(filename))
        save = TTWLSave(filename)
        char_level = save.get_level()

        # Write to our info file, if we have it
        if args.info:

            # Write out the row
            print('<tr class="row{}">'.format((files_written + row_offset) % 2), file=idf)
            print(f'<td class="level">{char_level}</td>', file=idf)
            print(f'<td class="filename"><a href="wl/{base_filename}">{base_filename}</a></td>', file=idf)
            print('<td class="in_map">{}</td>'.format(save.get_pt_last_map(0, True)), file=idf)
            missions = save.get_pt_active_mission_list(0, True)
            if len(missions) == 0:
                print('<td class="empty_missions">&nbsp;</td>', file=idf)
            else:
                print('<td class="active_missions">', file=idf)
                print('<ul>', file=idf)
                for mission in sorted(missions):
                    print('<li>{}</li>'.format(html.escape(mission, quote=False)), file=idf)
                print('</ul>', file=idf)
                print('</td>', file=idf)
            print('</tr>', file=idf)

        # May as well force the name, while we're at it
        save.set_char_name("WL Savegame Archive")

        # Randomize GUID
        save.randomize_guid()

        # Max XP
        # (Actually, not bothering with this -- Wonderlands enemies scale with
        # your char so there's no real advantage to forcing us to max, and this
        # way we'd have an opportunity to test out some level-change-based
        # behavior.)
        #save.set_level(ttwlsave.max_level)

        # Max Hero Stats
        # (eh, actually don't bother -- would probably just gunk up the UI
        # with "points available" warnings, and it's not like we're not
        # cheating like hell with our gear anyway.)
        #save.set_hero_stats(ttwlsave.HeroStats, 30)

        # Currency
        save.set_money(50000000) # Fifty million
        save.set_moon_orbs(10000)
        save.set_souls(200)

        # Max SDUs
        save.set_max_sdus()

        # Max Ammo
        save.set_max_ammo()

        # Unlock all inventory slots
        save.unlock_slots()

        # Unlock Feats/Companions
        # (Not gonna do this after all, I don't think.)
        #save.unlock_feat()

        # Unlock Multiclass
        # (Not gonna do this after all, I don't think.)
        #save.unlock_multiclass()

        # Unlock Chaos Mode (though don't actually set a value)
        save.set_chaos_level(ttwlsave.max_chaos_level, unlock_only=True)

        # Inventory - force our testing gear
        # Gear data just taken from my modtest char - Level 40 + Ascended
        # If the max level or Chaos Level ever updates, they'll get upgraded below
        manual_transmission = 'WL(BQAAAABXNIA7ORppgmool0p50WCcRx0zrBU6hAAAAAAAAGdAACAA)'
        transistor = 'WL(BQAAAACnEIC79mEggTIGugpRfCgjCAAABA==)'
        goblin_pickaxe = 'WL(BQAAAAA0SIA7LQmBgzJG6DEwMSwAAEAA)'
        save.overwrite_item_in_slot_encoded(ttwlsave.InvSlot.WEAPON1, manual_transmission)
        save.overwrite_item_in_slot_encoded(ttwlsave.InvSlot.WARD, transistor)
        save.overwrite_item_in_slot_encoded(ttwlsave.InvSlot.MELEE, goblin_pickaxe)

        # Bring testing gear up to our max level, while we're at it.
        for item in save.get_items():
            if item.level != char_level:
                item.level = char_level
            if item.chaos_level != ttwlsave.ChaosLevel.ASCENDED.value:
                item.chaos_level = ttwlsave.ChaosLevel.ASCENDED.value
            # The serials above don't have any rerolls logged, but we may as well
            # be sure about that anyway
            item.rerolled = 0

        # Write out
        save.save_to(output_filename)
        files_written += 1

    if args.filename:
        if files_written == 1:
            print('Done!  Wrote to {}'.format(args.output))
    else:
        if files_written == 1:
            plural = ''
        else:
            plural = 's'
        print('Done!  Wrote {} file{} to {}'.format(files_written, plural, args.output))

    if args.info:
        print('Wrote HTML summary to {}'.format(args.info))
        idf.close()

if __name__ == '__main__':
    main()

