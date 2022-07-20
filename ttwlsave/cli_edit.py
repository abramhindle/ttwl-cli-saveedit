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
import ttwlsave
import argparse
from . import cli_common
from . import plot_missions
from ttwlsave import InvSlot, SDU, ChaosLevel
from ttwlsave.ttwlsave import TTWLSave

def main():

    # Set up args
    parser = argparse.ArgumentParser(
            description='Wonderlands CLI Savegame Editor v{} (PC Only)'.format(ttwlsave.__version__),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="""
                The default output type of "savegame" will output theoretically-valid
                savegames which can be loaded into WL.  The output type "protobuf"
                will save out the extracted, decrypted protobufs.  The output
                type "json" will output a JSON-encoded version of the protobufs
                in question.  The output type "items" will output a text
                file containing base64-encoded representations of the user's
                inventory.  These can be read back in using the -i/--import-items
                option.
            """
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='WL CLI SaveEdit v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-o', '--output',
            choices=['savegame', 'protobuf', 'json', 'items'],
            default='savegame',
            help='Output file format',
            )

    parser.add_argument('--csv',
            action='store_true',
            help='When importing or exporting items, use CSV files',
            )

    parser.add_argument('-f', '--force',
            action='store_true',
            help='Force output file to overwrite',
            )

    parser.add_argument('-q', '--quiet',
            action='store_true',
            help='Supress all non-essential output')

    # Actual changes the user can request
    parser.add_argument('--name',
            type=str,
            help='Set the name of the character',
            )

    parser.add_argument('--save-game-id',
            type=int,
            help='Set the save game slot ID (possibly not actually ever needed)',
            )
    # AH: By default if you don't change the GUID it doesn't work in TTWL
    parser.add_argument('--dont-randomize-guid',
            dest='randomize_guid',
            action='store_false',
            default=True,
            help='DON\'T Randomize the savegame GUID',
            )

    levelgroup = parser.add_mutually_exclusive_group()

    levelgroup.add_argument('--level',
            type=int,
            help='Set the character to this level (from 1 to {})'.format(ttwlsave.max_level),
            )

    levelgroup.add_argument('--level-max',
            action='store_true',
            help='Set the character to max level ({})'.format(ttwlsave.max_level),
            )

    parser.add_argument('--xp-max',
            action='store_true',
            help="""When using --level, instead of assigning the minimum amount of XP for
                the level, assign the maximum (so that 1 more XP will level to the next).
                Has no effect when setting a char to max level.""",
            )

    itemlevelgroup = parser.add_mutually_exclusive_group()

    itemlevelgroup.add_argument('--items-to-char',
            action='store_true',
            help='Set all inventory items to the level of the character')

    itemlevelgroup.add_argument('--item-levels',
            type=int,
            help='Set all inventory items to the specified level')

    chaos_level_group=parser.add_mutually_exclusive_group()

    for level in ChaosLevel:
        chaos_level_group.add_argument('--items-{}'.format(level.label.lower()),
                dest='items_chaos_level',
                action='store_const',
                const=level,
                help='Set all inventory item chaos levels to {}'.format(level.label),
                )

    parser.add_argument('--chaos',
            type=int,
            help='Set the Chaos Level',
            )

    parser.add_argument('--money',
            type=int,
            help='Set money value',
            )

    parser.add_argument('--moon-orbs',
            type=int,
            help='Set Moon Orbs value',
            )

    parser.add_argument('--souls',
            type=int,
            help='Set Lost Souls value',
            )


    unlock_choices = [
            'ammo', 'backpack',
            'equipslots',
            'feat', 'multiclass',
            ]
    parser.add_argument('--unlock',
            action=cli_common.DictAction,
            choices=unlock_choices + ['all'],
            default={},
            help='Game features to unlock',
            )

    parser.add_argument('--unfinish-missions',
            action='store_true',
            help='"Un-finishes" the game: remove all Playthrough 0 to Not Completed',
            )

    parser.add_argument('--fake-tvhm',
            action='store_true',
            help='"Un-finishes" the missions but finishes the game',
            )

    parser.add_argument('-i', '--import-items',
            type=str,
            help='Import items from file',
            )

    # parser.add_argument('--delete-pt1-mission',
    #         type=str,
    #         metavar='MISSIONPATH',
    #         action='append',
    #         help="""Deletes all stored info about the specified mission in
    #             Playthrough 1 (Normal).  Will only work on sidemissions.
    #             Use bl3-save-info's --mission-paths to see the correct
    #             mission path to use here.  This option can be specified
    #             more than once."""
    #         )
    # 
    # parser.add_argument('--delete-pt2-mission',
    #         type=str,
    #         metavar='MISSIONPATH',
    #         action='append',
    #         help="""Deletes all stored info about the specified mission in
    #             Playthrough 2 (TVHM).  Will only work on sidemissions.
    #             Use bl3-save-info's --mission-paths to see the correct
    #             mission path to use here.  This option can be specified
    #             more than once."""
    #         )

    # Positional args
    parser.add_argument('input_filename',
            help='Input filename',
            )

    parser.add_argument('output_filename',
            help='Output filename',
            )

    # Parse args
    args = parser.parse_args()
    if args.level is not None:
        if args.level < 1 or args.level > ttwlsave.max_supported_level:
            raise argparse.ArgumentTypeError('Valid level range is 1 through {} (currently known in-game max of {})'.format(
                ttwlsave.max_supported_level,
                ttwlsave.max_level,
                ))
        if args.level > ttwlsave.max_level:
            print('WARNING: Setting character level to {}, when {} is the currently-known max'.format(
                args.level,
                ttwlsave.max_level,
                ))

    # Expand any of our "all" unlock actions
    if 'all' in args.unlock:
        args.unlock = {k: True for k in unlock_choices}

    # Set max level arg
    if args.level_max:
        args.level = ttwlsave.max_level

    # Check item level.  The max storeable in the serial number is 127, but the
    # effective limit in-game is 100, thanks to MaxGameStage attributes.  We
    # could use `ttwlsave.max_level` here, too, of course, but in the event that
    # I don't get this updated in a timely fashion, having it higher would let
    # this util potentially continue to be able to level up gear.
    if args.item_levels:
        if args.item_levels < 1 or args.item_levels > 100:
            raise argparse.ArgumentTypeError('Valid item level range is 1 through 100')
        if args.item_levels > ttwlsave.max_level:
            print('WARNING: Setting item levels to {}, when {} is the currently-known max'.format(
                args.item_levels,
                ttwlsave.max_level,
                ))

    # Check Chaos level
    if args.chaos is not None:
        if args.chaos < 0 or args.chaos > ttwlsave.max_chaos_level:
            raise argparse.ArgumentTypeError(f'Valid Chaos Level range is 0 through {ttwlsave.max_chaos_level}')

    # AH: Only 1 playthrough
    # # Check to make sure that any deleted missions are not plot missions
    # for arg in [args.delete_pt1_mission, args.delete_pt2_mission]:
    #     if arg is not None:
    #         for mission in arg:
    #             if mission.lower() in plot_missions:
    #                 raise argparse.ArgumentTypeError('Plot mission cannot be deleted: {}'.format(mission))
    # 
    # Check for overwrite warnings
    if os.path.exists(args.output_filename) and not args.force:
        if args.output_filename == args.input_filename:
            confirm_msg = 'Really overwrite {} with specified changes (no backup will be made)'.format(args.output_filename)
        else:
            confirm_msg = '{} already exists.  Overwrite'.format(args.output_filename)
        sys.stdout.write('WARNING: {} [y/N]? '.format(confirm_msg))
        sys.stdout.flush()
        response = sys.stdin.readline().strip().lower()
        if len(response) == 0 or response[0] != 'y':
            print('Aborting!')
            sys.exit(1)
        print('')

    # Now load the savegame
    if not args.quiet:
        print('Loading {}'.format(args.input_filename))
    save = TTWLSave(args.input_filename)
    if not args.quiet:
        print('')

    # Check to see if we have any changes to make
    have_changes = any([
        args.name,
        args.save_game_id is not None,
        args.randomize_guid,
        args.level is not None,
        args.chaos is not None,
        args.money is not None,
        args.moon_orbs is not None,
        args.souls is not None,
        len(args.unlock) > 0,
        args.import_items,
        args.items_to_char,
        args.item_levels,
        args.items_chaos_level is not None,
        #args.unfinish_nvhm,
        args.unfinish_missions,
        args.fake_tvhm,
        # args.delete_pt1_mission is not None,
        # args.delete_pt2_mission is not None,
        ])

    # Make changes
    if have_changes:

        if not args.quiet:
            print('Making requested changes...')
            print('')

        # Char Name
        if args.name:
            if not args.quiet:
                print(' - Setting Character Name to: {}'.format(args.name))
            save.set_char_name(args.name)

        # Savegame ID
        if args.save_game_id is not None:
            if not args.quiet:
                print(' - Setting Savegame ID to: {}'.format(args.save_game_id))
            save.set_savegame_id(args.save_game_id)

        # Savegame GUID
        if args.randomize_guid:
            if not args.quiet:
                print(' - Randomizing savegame GUID')
            save.randomize_guid()

        # Chaos Level
        if args.chaos is not None:
            if not args.quiet:
                print(' - Setting Chaos Level to: {}'.format(args.chaos))
            save.set_chaos_level(args.chaos)
            # TODO: eh? --fake-tvhm unlocks this more properly...
            #if args.chaos > 0:
            #    if not args.quiet:
            #        print('   - Also ensuring that Chaos Mode is unlocked')
            #    save.unlock_challenge(ttwlsave.CHAOS)

        # Level
        if args.level is not None:
            if not args.quiet:
                if args.xp_max:
                    extra = ' (at max XP value)'
                else:
                    extra = ''
                print(' - Setting Character Level{} to: {}'.format(extra, args.level))
            points_added = save.set_level(args.level, top_val=args.xp_max)
            if points_added > 0:
                if points_added == 1:
                    plural = ''
                else:
                    plural = 's'
                print(f'   - Also added {points_added} skill point{plural}')

        # Money
        if args.money is not None:
            if not args.quiet:
                print(' - Setting Money to: {:,}'.format(args.money))
            save.set_money(args.money)

        # Moon Orbs
        if args.moon_orbs is not None:
            if not args.quiet:
                print(' - Setting Moon Orbs to: {:,}'.format(args.moon_orbs))
            save.set_moon_orbs(args.moon_orbs)

        # Lost Souls
        if args.souls is not None:
            if not args.quiet:
                print(' - Setting Lost Souls to: {:,}'.format(args.souls))
            save.set_souls(args.souls)

        # AH: Temporarily disabling this
        # # Deleting missions
        # for label, pt, arg in [
        #         ('Normal/NVHM', 0, args.delete_pt1_mission),
        #         ('TVHM', 1, args.delete_pt2_mission),
        #         ]:
        #     if arg is not None:
        #         for mission in arg:
        #             if not args.quiet:
        #                 print(' - Deleting {} mission: {}'.format(label, mission))
        #             if not save.delete_mission(pt, mission):
        #                 if not args.quiet:
        #                     print('   NOTE: Could not find {} mission to delete: {}'.format(
        #                         label,
        #                         mission,
        #                         ))

        # Unlocks
        if len(args.unlock) > 0:
            if not args.quiet:
                print(' - Processing Unlocks:')

            # Ammo
            if 'ammo' in args.unlock:
                if not args.quiet:
                    print('   - Ammo SDUs (and setting ammo to max)')
                save.set_max_sdus(ttwlsave.ammo_sdus)
                save.set_max_ammo()

            # Backpack
            if 'backpack' in args.unlock:
                if not args.quiet:
                    print('   - Backpack SDUs')
                save.set_max_sdus([SDU.BACKPACK])

            # Equipment Slots
            if 'equipslots' in args.unlock:
                if not args.quiet:
                    print('   - Equipment Slots')
                save.unlock_slots([
                    # Not unlocking the second spell slot since that's class-specific
                    InvSlot.WEAPON3,
                    InvSlot.WEAPON4,
                    InvSlot.ARMOR,
                    InvSlot.RING1,
                    InvSlot.RING2,
                    InvSlot.AMULET,
                    ])

            # Feats / Companions
            if 'feat' in args.unlock:
                if not args.quiet:
                    print('   - Feat / Companion')
                save.unlock_feat()

            # Multiclass
            if 'multiclass' in args.unlock:
                if not args.quiet:
                    print('   - Multiclass Capability')
                    if save.unlock_multiclass():
                        print('     - Also added +2 Skill Points')

        # Import Items (cli_common provides the console output)
        if args.import_items:
            cli_common.import_items(args.import_items,
                    save.create_new_item_encoded,
                    save.add_item,
                    file_csv=args.csv,
                    quiet=args.quiet,
                    )

        # Setting item levels.  Keep in mind that we'll want to do this *after*
        # various of the actions above.  If we've been asked to up the level of
        # the character, we'll want items to follow suit, and if we've been asked
        # to change the level of items, we'll want to do it after the item import.
        # (cli_common provides the console output)
        if args.items_to_char or args.item_levels:
            if args.items_to_char:
                to_level = save.get_level()
            else:
                to_level = args.item_levels
            cli_common.update_item_levels(save.get_items(),
                    to_level,
                    quiet=args.quiet,
                    )

        # Setting item Chaos Levels (Chaotic, Volatile, etc...)
        # (cli_common provides the console output)
        if args.items_chaos_level is not None:
            cli_common.update_chaos_level(save.get_items(),
                    args.items_chaos_level,
                    quiet=args.quiet,
                    )

        # Un-finish missions (TODO: test!)
        if args.unfinish_missions:
            if not args.quiet:
                print(' - Un-finishing NVHM state entirely')
            # ... or clearing TVHM state entirely.
            save.set_playthroughs_completed(0)
            save.clear_playthrough_data()

        # Fake "TVHM" (TODO: Test!)
        if args.fake_tvhm:
            if not args.quiet:
                print(' - Un-finishing missions and marking the playthrough complete state entirely -- enables chaos mode')
            # ... or clearing TVHM state entirely.
            # save.clear_playthrough_data(0)
            # save.clear_mission_pt(0)
            missions = save.get_pt_completed_mission_lists()[0]
            for mission in missions:
                # print(mission)
                if mission != "/Game/Missions/Plot/Mission_Plot11.Mission_Plot11_C":
                    save.delete_mission(mission, allow_plot=True)
            save.set_playthroughs_completed(1)
            save.finish_game()
        
        # Newline at the end of all this.
        if not args.quiet:
            print('')

    # Write out
    if args.output == 'savegame':
        save.save_to(args.output_filename)
        if not args.quiet:
            print('Wrote savegame to {}'.format(args.output_filename))
    elif args.output == 'protobuf':
        save.save_protobuf_to(args.output_filename)
        if not args.quiet:
            print('Wrote protobuf to {}'.format(args.output_filename))
    elif args.output == 'json':
        save.save_json_to(args.output_filename)
        if not args.quiet:
            print('Wrote JSON to {}'.format(args.output_filename))
    elif args.output == 'items':
        if args.csv:
            cli_common.export_items_csv(
                    save.get_items(),
                    args.output_filename,
                    quiet=args.quiet,
                    )
        else:
            cli_common.export_items(
                    save.get_items(),
                    args.output_filename,
                    quiet=args.quiet,
                    )
    else:
        # Not sure how we'd ever get here
        raise Exception('Invalid output format specified: {}'.format(args.output))


if __name__ == '__main__':
    main()
