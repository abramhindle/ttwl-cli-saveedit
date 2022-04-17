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
import ttwlsave
import argparse
from . import cli_common
from . import plot_missions
from ttwlsave.ttwlsave import TTWLSave

def main():

    # Set up args
    parser = argparse.ArgumentParser(
            description='Borderlands 3 CLI Savegame Editor v{} (PC Only)'.format(ttwlsave.__version__),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="""
                The default output type of "savegame" will output theoretically-valid
                savegames which can be loaded into BL3.  The output type "protobuf"
                will save out the extracted, decrypted protobufs.  The output
                type "json" will output a JSON-encoded version of the protobufs
                in question.  The output type "items" will output a text
                file containing base64-encoded representations of the user's
                inventory.  These can be read back in using the -i/--import-items
                option.  Note that these are NOT the same as the item strings used
                by the BL3 Memory Editor.
            """
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='BL3 CLI SaveEdit v{}'.format(ttwlsave.__version__),
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
            dest='save_game_id',
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
    # AH: Disabled for now
    # parser.add_argument('--zero-guardian-rank',
    #         dest='zero_guardian_rank',
    #         action='store_true',
    #         help='Zero out savegame Guardian Rank',
    #         )

    levelgroup = parser.add_mutually_exclusive_group()

    levelgroup.add_argument('--level',
            type=int,
            help='Set the character to this level (from 1 to {})'.format(ttwlsave.max_level),
            )

    levelgroup.add_argument('--level-max',
            dest='level_max',
            action='store_true',
            help='Set the character to max level ({})'.format(ttwlsave.max_level),
            )

    itemlevelgroup = parser.add_mutually_exclusive_group()

    itemlevelgroup.add_argument('--items-to-char',
            dest='items_to_char',
            action='store_true',
            help='Set all inventory items to the level of the character')

    itemlevelgroup.add_argument('--item-levels',
            dest='item_levels',
            type=int,
            help='Set all inventory items to the specified level')

    itemmayhemgroup = parser.add_mutually_exclusive_group()

    itemmayhemgroup.add_argument('--item-mayhem-max',
            dest='item_mayhem_max',
            action='store_true',
            help='Set all inventory items to the maximum Mayhem level ({})'.format(ttwlsave.mayhem_max))

    itemmayhemgroup.add_argument('--item-mayhem-levels',
            dest='item_mayhem_levels',
            type=int,
            choices=range(ttwlsave.mayhem_max+1),
            help='Set all inventory items to the specified Mayhem level (0 to remove)')

    parser.add_argument('--mayhem',
            type=int,
            choices=range(20),
            help='Set the mayhem mode for all playthroughs (mostly useful for Normal mode)',
            )

    parser.add_argument('--mayhem-seed',
            dest='mayhem_seed',
            type=int,
            help='Sets the mayhem random seed for all playthroughs',
            )

    parser.add_argument('--money',
            type=int,
            help='Set money value',
            )

    parser.add_argument('--eridium',
            type=int,
            help='Set Eridium value',
            )

    parser.add_argument('--clear-takedowns',
            dest='clear_takedowns',
            action='store_true',
            help='Clears out the Takedown Discovery missions so they don\'t clutter your UI',
            )

    unlock_choices = [
            'ammo', 'backpack',
            'analyzer', 'resonator',
            'gunslots', 'artifactslot', 'comslot', 'allslots',
            'tvhm',
            'vehicles', 'vehicleskins',
            'cubepuzzle',
            ]
    parser.add_argument('--unlock',
            action=cli_common.DictAction,
            choices=unlock_choices + ['all'],
            default={},
            help='Game features to unlock',
            )
    # AH: disabling NO TVHM
    # tvhmgroup = parser.add_mutually_exclusive_group()
    # 
    # tvhmgroup.add_argument('--copy-nvhm',
    #         action='store_true',
    #         help='Copies NVHM/Normal state to TVHM',
    #         )
    # 
    # tvhmgroup.add_argument('--copy-tvhm',
    #         action='store_true',
    #         help='Copies TVHM state to NVHM/Normal',
    #         )
    # 
    # tvhmgroup.add_argument('--unfinish-nvhm',
    #         dest='unfinish_nvhm',
    #         action='store_true',
    #         help='"Un-finishes" the game: remove all TVHM data and set Playthrough 1 to Not Completed',
    #         )
    parser.add_argument('--unfinish-missions',
            dest='unfinish_missions',
            action='store_true',
            help='"Un-finishes" the game: remove all Playthrough 0 to Not Completed',
            )

    parser.add_argument('--fake-tvhm',
            dest='fake_tvhm',
            action='store_true',
            help='"Un-finishes" the missions but finishes the game',
            )

    parser.add_argument('-i', '--import-items',
            dest='import_items',
            type=str,
            help='Import items from file',
            )

    parser.add_argument('--allow-fabricator',
            dest='allow_fabricator',
            action='store_true',
            help='Allow importing Fabricator when importing items from file',
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
    # AH: Disabled
    # parser.add_argument('--clear-bloody-harvest',
    #         action='store_true',
    #         help='Clear Bloody Harvest challenge state',
    #         )
    # 
    # parser.add_argument('--clear-broken-hearts',
    #         action='store_true',
    #         help='Clear Broken Hearts challenge state',
    #         )
    # 
    # parser.add_argument('--clear-cartels',
    #         action='store_true',
    #         help='Clear Revenge of the Cartels challenge state',
    #         )
    # 
    # parser.add_argument('--clear-all-events',
    #         action='store_true',
    #         help='Clear all seasonal event challenge states',
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
    elif 'allslots' in args.unlock:
        args.unlock['gunslots'] = True
        args.unlock['artifactslot'] = True
        args.unlock['comslot'] = True
    # AH: No TVHM
    # # Make sure we're not trying to clear and unlock THVM at the same time
    # if 'tvhm' in args.unlock and args.unfinish_nvhm:
    #     raise argparse.ArgumentTypeError('Cannot both unlock TVHM and un-finish NVHM')

    # Set max level arg
    if args.level_max:
        args.level = ttwlsave.max_level

    # Set max mayhem arg
    if args.item_mayhem_max:
        args.item_mayhem_levels = ttwlsave.mayhem_max

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
    # AH: More TVHM disable
    # # Some argument interactions we should check on
    # if args.copy_nvhm:
    #     if save.get_playthroughs_completed() < 1:
    #         if 'tvhm' not in args.unlock:
    #             args.unlock['tvhm'] = True
    # AH: NO TVHM
    # # If we've been told to copy TVHM state to NVHM, make sure we have TVHM data.
    # # TODO: need to check this out
    # if args.copy_tvhm:
    #     if save.get_playthroughs_completed() < 1:
    #         raise argparse.ArgumentTypeError('TVHM State not found to copy in {}'.format(args.input_filename))
    #  
    # Check to see if we have any changes to make
    have_changes = any([
        args.name,
        args.save_game_id is not None,
        args.randomize_guid,
        # args.zero_guardian_rank,
        args.level is not None,
        args.mayhem is not None,
        args.mayhem_seed is not None,
        args.money is not None,
        args.eridium is not None,
        args.clear_takedowns,
        len(args.unlock) > 0,
        # args.copy_nvhm,
        # args.copy_tvhm,
        args.import_items,
        args.items_to_char,
        args.item_levels,
        #args.unfinish_nvhm,
        args.unfinish_missions,
        args.fake_tvhm,
        args.item_mayhem_levels is not None,
        # args.delete_pt1_mission is not None,
        # args.delete_pt2_mission is not None,
        # args.clear_bloody_harvest,
        # args.clear_broken_hearts,
        # args.clear_cartels,
        # args.clear_all_events,
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
        # AH: No guardian rank
        # Zeroing Guardian Rank
        # if args.zero_guardian_rank:
        #     if not args.quiet:
        #         print(' - Zeroing Guardian Rank')
        #     save.zero_guardian_rank()

        # Mayhem Level
        if args.mayhem is not None:
            if not args.quiet:
                print(' - Setting Mayhem Level to: {}'.format(args.mayhem))
            save.set_all_mayhem_level(args.mayhem)
            if args.mayhem > 0:
                if not args.quiet:
                    print('   - Also ensuring that Mayhem Mode is unlocked')
                save.unlock_challenge(ttwlsave.MAYHEM)

        # Mayhem Seed
        if args.mayhem_seed is not None:
            if not args.quiet:
                print(' - Setting Mayhem Random Seed to: {}'.format(args.mayhem_seed))
            save.set_all_mayhem_seeds(args.mayhem_seed)

        # Level
        if args.level is not None:
            if not args.quiet:
                print(' - Setting Character Level to: {}'.format(args.level))
            save.set_level(args.level)

        # Money
        if args.money is not None:
            if not args.quiet:
                print(' - Setting Money to: {}'.format(args.money))
            save.set_money(args.money)

        # Eridium
        if args.eridium is not None:
            if not args.quiet:
                print(' - Setting Eridium to: {}'.format(args.eridium))
            save.set_eridium(args.eridium)
        # AH: No Takedowns
        # # Clearing Takedown Discovery
        # if args.clear_takedowns:
        #     if not args.quiet:
        #         print(' - Clearing Takedown Discovery missions')
        #     save.clear_takedown_discovery()
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

        # AH: No seasonal
        # # Clearing seasonal event status
        # if args.clear_bloody_harvest or args.clear_all_events:
        #     if not args.quiet:
        #         print(' - Clearing Bloody Harvest challenge state')
        #     save.clear_bloody_harvest()
        # 
        # if args.clear_broken_hearts or args.clear_all_events:
        #     if not args.quiet:
        #         print(' - Clearing Broken Hearts challenge state')
        #     save.clear_broken_hearts()
        # 
        # if args.clear_cartels or args.clear_all_events:
        #     if not args.quiet:
        #         print(' - Clearing Cartels challenge state')
        #     save.clear_cartels()

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
                save.set_max_sdus([ttwlsave.SDU_BACKPACK])
            # AH: No eridian
            # # Eridian Analyzer
            # if 'analyzer' in args.unlock:
            #     if not args.quiet:
            #         print('   - Eridian Analyzer')
            #     save.unlock_challenge(ttwlsave.ERIDIAN_ANALYZER)
            # 
            # # Eridian Resonator
            # if 'resonator' in args.unlock:
            #     if not args.quiet:
            #         print('   - Eridian Resonator')
            #     save.unlock_challenge(ttwlsave.ERIDIAN_RESONATOR)

            # Gun Slots
            if 'gunslots' in args.unlock:
                if not args.quiet:
                    print('   - Weapon Slots (3+4)')
                save.unlock_slots([ttwlsave.WEAPON3, ttwlsave.WEAPON4])

            # Artifact Slot
            if 'artifactslot' in args.unlock:
                if not args.quiet:
                    print('   - Artifact Inventory Slot')
                save.unlock_slots([ttwlsave.ARTIFACT])

            # COM Slot
            if 'comslot' in args.unlock:
                if not args.quiet:
                    print('   - COM Inventory Slot')
                save.unlock_slots([ttwlsave.COM])
            # AH: No vehicles 
            # # Vehicles
            # if 'vehicles' in args.unlock:
            #     if not args.quiet:
            #         print('   - Vehicles (and parts)')
            #     save.unlock_vehicle_chassis()
            #     save.unlock_vehicle_parts()
            #     if not args.quiet and not save.has_vehicle_chassis(ttwlsave.jetbeast_main_chassis):
            #         print('     - NOTE: The default Jetbeast chassis will be unlocked automatically by the game')
            # 
            # # Vehicle Skins
            # if 'vehicleskins' in args.unlock:
            #     if not args.quiet:
            #         print('   - Vehicle Skins')
            #     save.unlock_vehicle_skins()
            # 
            # # TVHM
            # if 'tvhm' in args.unlock:
            #     if not args.quiet:
            #         print('   - TVHM')
            #     save.set_playthroughs_completed(1)
            # 
            # # Eridian Cube puzzle
            # if 'cubepuzzle' in args.unlock:
            #     if not args.quiet:
            #         print('   - Eridian Cube Puzzle')
            #     save.unlock_cube_puzzle()

        # Import Items
        if args.import_items:
            cli_common.import_items(args.import_items,
                    save.create_new_item_encoded,
                    save.add_item,
                    file_csv=args.csv,
                    allow_fabricator=args.allow_fabricator,
                    quiet=args.quiet,
                    )

        # Setting item levels.  Keep in mind that we'll want to do this *after*
        # various of the actions above.  If we've been asked to up the level of
        # the character, we'll want items to follow suit, and if we've been asked
        # to change the level of items, we'll want to do it after the item import.
        if args.items_to_char or args.item_levels:
            if args.items_to_char:
                to_level = save.get_level()
            else:
                to_level = args.item_levels
            cli_common.update_item_levels(save.get_items(),
                    to_level,
                    quiet=args.quiet,
                    )

        # Item Mayhem level
        if args.item_mayhem_levels is not None:
            cli_common.update_item_mayhem_levels(save.get_items(),
                    args.item_mayhem_levels,
                    quiet=args.quiet,
                    )
        # AH: There is no NVHM
        # # Copying NVHM/TVHM state (or otherwise fiddle with playthroughs)
        # if args.copy_nvhm:
        #     if not args.quiet:
        #         print(' - Copying NVHM state to TVHM')
        #     save.copy_playthrough_data()
        # elif args.copy_tvhm:
        #     if not args.quiet:
        #         print(' - Copying TVHM state to NVHM')
        #     save.copy_playthrough_data(from_pt=1, to_pt=0)
        # elif args.unfinish_nvhm:
        #     if not args.quiet:
        #         print(' - Un-finishing NVHM state entirely')
        #     # ... or clearing TVHM state entirely.
        #     save.set_playthroughs_completed(0)
        #     save.clear_playthrough_data(1)

        if args.unfinish_missions:
            if not args.quiet:
                print(' - Un-finishing NVHM state entirely')
            # ... or clearing TVHM state entirely.
            save.set_playthroughs_completed(0)
            save.clear_playthrough_data(0)
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
                    save.delete_mission(0,mission,allow_plot=True)
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
