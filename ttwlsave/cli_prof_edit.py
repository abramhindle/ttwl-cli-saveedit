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
from . import cli_common, myth_xp_for_rank, myth_rank_for_xp
from ttwlsave import ProfileSDU, ChaosLevel
from ttwlsave.ttwlprofile import TTWLProfile

def main():

    # Set up args
    parser = argparse.ArgumentParser(
            description='Wonderlands CLI Profile Editor v{} (PC Only)'.format(ttwlsave.__version__),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog="""
                The default output type of "profile" will output theoretically-valid
                profile which can be loaded into WL.  The output type "protobuf"
                will save out the extracted, decrypted protobufs.  The output
                type "json" will output a JSON-encoded version of the protobufs
                in question.  The output type "items" will output a text file
                containing base64-encoded representations of items in the user's
                bank.  These can be read back in using the -i/--import-items
                option.  Note that these are NOT the same as the item strings used
                by the WL Memory Editor.
            """
            )

    parser.add_argument('-V', '--version',
            action='version',
            version='WL CLI SaveEdit v{}'.format(ttwlsave.__version__),
            )

    parser.add_argument('-o', '--output',
            choices=['profile', 'protobuf', 'json', 'items'],
            default='profile',
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

    # Now the actual arguments

    parser.add_argument('--skeleton-keys',
            type=int,
            help='Number of Skeleton Keys in the profile',
            )

    myth_group = parser.add_mutually_exclusive_group()

    myth_group.add_argument('--zero-myth-rank',
            action='store_true',
            help='Zero out Myth Rank entirely',
            )

    myth_group.add_argument('--myth-stats-max',
            action='store_true',
            help='Max out Myth Rank Stats where possible',
            )

    myth_group.add_argument('--myth-stats-points',
            type=int,
            help="""Set all Myth Rank Stats to the specified value (will not
                go over the maximums for each category though)."""
            )

    rank_group = parser.add_mutually_exclusive_group()

    rank_group.add_argument('--myth-xp',
            type=int,
            help='Sets the raw Myth Rank XP value',
            )

    rank_group.add_argument('--myth-rank',
            type=int,
            help='Sets the Myth Rank to the specified level',
            )

    itemlevelgroup = parser.add_mutually_exclusive_group()

    itemlevelgroup.add_argument('--item-levels-max',
            action='store_true',
            help='Set all bank items to max level')

    itemlevelgroup.add_argument('--item-levels',
            type=int,
            help='Set all bank items to the specified level')

    chaos_level_group=parser.add_mutually_exclusive_group()

    for level in ChaosLevel:
        chaos_level_group.add_argument('--items-{}'.format(level.label.lower()),
                dest='items_chaos_level',
                action='store_const',
                const=level,
                help='Set all bank item chaos levels to {}'.format(level.label),
                )

    parser.add_argument('--clear-rerolls',
            action='store_true',
            help='Clears the reroll counter for all items in the bank',
            )

    parser.add_argument('-i', '--import-items',
            type=str,
            help='Import items from file',
            )

    parser.add_argument('--clear-customizations',
            action='store_true',
            help='Remove all unlocked customizations',
            )

    unlock_choices = [
            'lostloot', 'bank',
            'customizations',
            ]
    parser.add_argument('--unlock',
            action=cli_common.SetAction,
            choices=unlock_choices + ['all'],
            default={},
            help='Game features to unlock',
            )

    # Positional args
    parser.add_argument('input_filename',
            help='Input filename',
            )

    parser.add_argument('output_filename',
            help='Output filename',
            )

    # Parse args
    args = parser.parse_args()

    # Expand any of our "all" unlock actions
    if 'all' in args.unlock:
        args.unlock = {k: True for k in unlock_choices}

    # Set max item level arg
    if args.item_levels_max:
        args.item_levels = ttwlsave.max_level

    # Check key counts; don't let them be below zero
    if args.skeleton_keys is not None and args.skeleton_keys < 0:
        raise argparse.ArgumentTypeError('Skeleton keys cannot be negative')

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

    # Check Myth Rank Numbers
    if args.myth_stats_points is not None:
        if args.myth_stats_points < 0:
            raise argparse.ArgumentTypeError('Myth Rank Point value cannot be negative')

    # Check Myth XP Numbers
    if args.myth_xp is not None:
        if args.myth_xp < 0:
            raise argparse.ArgumentTypeError('Myth Rank XP value cannot be negative')

    # Check Myth Rank Numbers
    if args.myth_rank is not None:
        if args.myth_rank < 1:
            raise argparse.ArgumentTypeError('Myth Rank value must be at least 1')

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

    # Now load the profile
    if not args.quiet:
        print('Loading {}'.format(args.input_filename))
    profile = TTWLProfile(args.input_filename)
    if not args.quiet:
        print('')

    # Check to see if we have any changes to make
    have_changes = any([
        args.skeleton_keys is not None,
        args.zero_myth_rank,
        args.myth_stats_max,
        args.myth_stats_points is not None,
        args.myth_xp is not None,
        args.myth_rank is not None,
        len(args.unlock) > 0,
        args.import_items,
        args.item_levels,
        args.items_chaos_level is not None,
        args.clear_rerolls,
        args.clear_customizations,
        ])

    # Make changes
    if have_changes:

        if not args.quiet:
            print('Making requested changes...')
            print('')

        # Skeleton Keys
        if args.skeleton_keys is not None:
            if not args.quiet:
                print(' - Setting Skeleton Key count to {}'.format(args.skeleton_keys))
            profile.set_skeleton_keys(args.skeleton_keys)

        # Zeroing Myth Rank Entirely
        if args.zero_myth_rank:
            if not args.quiet:
                print(' - Clearing Myth Rank Entirely')
            profile.zero_myth_rank()

        # See if we need to doublecheck Myth XP
        check_myth_xp = False

        # Maxing out Myth Rank Stats (where appropriate)
        if args.myth_stats_max:
            if not args.quiet:
                print(' - Setting Myth Rank stats to the maximum, where possible')
            profile.myth_stats_max()
            check_myth_xp = True

        # Setting Myth Rank Stats to a specific value
        if args.myth_stats_points is not None:
            if not args.quiet:
                print(f' - Setting all Myth Rank points to: {args.myth_stats_points}')
            profile.set_myth_stats_points(args.myth_stats_points)
            check_myth_xp = True

        # Setting Myth Rank/XP
        # Make sure this happens *after* the other Myth Rank options, in case the user's
        # specified multiple options.  Our general operating procedure is as follows:
        #   1. We check for the minimum required rank/XP, given the Rank Stats which have
        #      been chosen.  Under no circumstances allow the XP value to drop below that.
        #   2. If the user's explicitly setting a rank or XP value, we *will* allow the
        #      values to drop below what the user currently has set (though not below
        #      that minimum amount).
        #   3. If The user hasn't explicitly set rank or XP (and we're just checking due
        #      to setting stats, above), the only thing we'll do is bring the XP up to
        #      the minimum required.
        if check_myth_xp or args.myth_xp is not None or args.myth_rank is not None:
            disclaimer = False
            required_rank = profile.get_myth_points_allocated()
            required_xp = myth_xp_for_rank(required_rank)
            if args.myth_xp is not None:
                if args.myth_xp < required_xp:
                    args.myth_xp = required_xp
                    new_rank = required_rank
                    if not args.quiet:
                        print(f' - Overriding requested Myth XP to minimum for profile: {args.myth_xp:,}')
                else:
                    new_rank = myth_rank_for_xp(args.myth_xp)
                    if new_rank == -1:
                        new_rank = 'unknown'
                if not args.quiet:
                    print(f' - Setting Myth XP to: {args.myth_xp:,} (rank {new_rank})')
                    disclaimer = True
                profile.set_myth_xp(args.myth_xp)
            elif args.myth_rank is not None:
                if args.myth_rank < required_rank:
                    args.myth_rank = required_rank
                    if not args.quiet:
                        print(f' - Overriding requested Myth Rank to minimum for profile: {args.myth_rank}')
                if profile.get_myth_rank() == args.myth_rank:
                    if not args.quiet:
                        print(f' - Not setting Myth Rank (already at Myth Rank {args.myth_rank})')
                        disclaimer = True
                else:
                    # We're not using required_xp because we might be setting higher than
                    # is actually required
                    rank_xp = myth_xp_for_rank(args.myth_rank)
                    if not args.quiet:
                        print(f' - Setting Myth Rank to: {args.myth_rank} (XP {rank_xp:,})')
                        disclaimer = True
                    profile.set_myth_xp(rank_xp)
            else:
                if profile.get_myth_xp() < required_xp:
                    if not args.quiet:
                        print(f' - Setting Myth Rank to: {required_rank} (XP {required_xp:,})')
                        disclaimer = True
                    profile.set_myth_xp(required_xp)

            if disclaimer:
                print('   (note: Myth Rank calculation might not be 100% accurate)')

        # Clear Customizations (do this *before* explicit customization unlocks)
        if args.clear_customizations:
            if not args.quiet:
                print(' - Clearing all customizations')
            profile.clear_all_customizations()

        # Unlocks
        if len(args.unlock) > 0:
            if not args.quiet:
                print(' - Processing Unlocks:')

            # Lost Loot
            if 'lostloot' in args.unlock:
                if not args.quiet:
                    print('   - Lost Loot SDUs')
                profile.set_max_sdus([ProfileSDU.LOSTLOOT])

            # Bank
            if 'bank' in args.unlock:
                if not args.quiet:
                    print('   - Bank SDUs')
                profile.set_max_sdus([ProfileSDU.BANK])

            # Customizations
            if 'customizations' in args.unlock:
                if not args.quiet:
                    print('   - Customizations')
                profile.unlock_customizations()

        # Import Items (cli_common provides the console output)
        if args.import_items:
            cli_common.import_items(args.import_items,
                    profile.create_new_bank_item_encoded,
                    profile.add_bank_item,
                    file_csv=args.csv,
                    quiet=args.quiet,
                    )

        # Setting item levels.  Keep in mind that we'll want to do this *after*
        # various of the actions above.  If we've been asked to change the level
        # of items, we'll want to do it after the item import.
        # (cli_common provides the console output)
        if args.item_levels:
            cli_common.update_item_levels(profile.get_bank_items(),
                    args.item_levels,
                    quiet=args.quiet,
                    )

        # Setting item Chaos Levels (Chaotic, Volatile, etc...)
        # (cli_common provides the console output)
        if args.items_chaos_level is not None:
            cli_common.update_chaos_level(profile.get_bank_items(),
                    args.items_chaos_level,
                    quiet=args.quiet,
                    )

        # Clearing reroll counts (cli_common provides the console output)
        if args.clear_rerolls:
            cli_common.clear_rerolls(profile.get_bank_items(),
                    quiet=args.quiet,
                    )

        # Newline at the end of all this.
        if not args.quiet:
            print('')

    # Write out
    if args.output == 'profile':
        profile.save_to(args.output_filename)
        if not args.quiet:
            print('Wrote profile to {}'.format(args.output_filename))
    elif args.output == 'protobuf':
        profile.save_protobuf_to(args.output_filename)
        if not args.quiet:
            print('Wrote protobuf to {}'.format(args.output_filename))
    elif args.output == 'json':
        profile.save_json_to(args.output_filename)
        if not args.quiet:
            print('Wrote JSON to {}'.format(args.output_filename))
    elif args.output == 'items':
        if args.csv:
            cli_common.export_items_csv(
                    profile.get_bank_items(),
                    args.output_filename,
                    quiet=args.quiet,
                    )
        else:
            cli_common.export_items(
                    profile.get_bank_items(),
                    args.output_filename,
                    quiet=args.quiet,
                    )
    else:
        # Not sure how we'd ever get here
        raise Exception('Invalid output format specified: {}'.format(args.output))

if __name__ == '__main__':
    main()
