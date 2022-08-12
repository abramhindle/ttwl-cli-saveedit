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
from ttwlsave import InvSlot
from ttwlsave.ttwlsave import TTWLSave

def main():

    # Arguments
    parser = argparse.ArgumentParser(
            description='Wonderlands Savegame Info Dumper v{}'.format(ttwlsave.__version__),
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

    parser.add_argument('--rerolls',
            action='store_true',
            help='Also show enchantment reroll count on items',
            )

    parser.add_argument('--all-missions',
            action='store_true',
            help='Show all missions')

    parser.add_argument('--mission-paths',
            action='store_true',
            help='Display raw mission paths when reporting on missions')

    parser.add_argument('--all-challenges',
            action='store_true',
            help='Show all challenges')

    parser.add_argument('--fast-travel',
            action='store_true',
            help='Show all unlocked Fast Travel stations')

    parser.add_argument('--customizations',
            action='store_true',
            help='Show currently-selected customizations (as raw object paths)',
            )

    parser.add_argument('filename',
            help='Filename to process',
            )

    args = parser.parse_args()

    # Load the save
    save = TTWLSave(args.filename)

    # Character name
    print('Character: {}'.format(save.get_char_name()))

    # Savegame ID
    print('Savegame ID: {}'.format(save.get_savegame_id()))

    # Savegame GUID
    print('Savegame GUID: {}'.format(save.get_savegame_guid()))

    # Class
    print('Player Primary Class: {}'.format(save.get_primary_class(True)))
    print('Player Secondary Class: {}'.format(save.get_secondary_class(True)))

    # Companion Names
    companion_names = save.get_companion_names(True)
    if len(companion_names) > 0:
        print('Companion Names:')
        for (c_type, c_name) in companion_names.items():
            print(' - {} Name: {}'.format(c_type.label, c_name))

    # XP/Level
    print('XP: {}'.format(save.get_xp()))
    print('Level: {}'.format(save.get_level()))

    # Backstory
    print('Backstory: {}'.format(save.get_backstory(True)))

    # Hero Stats
    print('Raw Hero Stats (no Backstory or Myth Rank adjustments):')
    for stat, value in save.get_hero_stats().items():
        print(f' - {stat.label}: {value}')

    # Customizations
    if args.verbose or args.customizations:
        (cur_customizations, cur_emotes) = save.get_selected_customizations()
        if cur_customizations is None:
            print(f'WARNING: Unknown customization found: {cur_emotes}')
        else:
            print('Customizations:')
            (reports, emotes) = save.get_selected_customizations(eng=True)
            reports['Emotes'] = emotes
            reports.update(save.get_special_selected_customizations())
            for cust, value in reports.items():
                if type(value) == list:
                    print(f' - {cust}:')
                    for item in value:
                        print(f'     {item}')
                else:
                    print(f' - {cust}: {value}')

    # Currencies
    print('Currencies:')
    print(' - Money: {:,}'.format(save.get_money()))
    print(' - Moon Orbs: {:,}'.format(save.get_moon_orbs()))
    print(' - Lost Souls: {:,}'.format(save.get_souls()))

    # Chaos Level
    print('Chaos Level: {} (unlocked: {})'.format(*save.get_chaos_level_with_max()))

    ###
    ### Playthrough Info!
    ###
    print('Playthrough Info:')

    # Map
    mapname = save.get_last_maps(True)
    if mapname is not None:
        print(' - In Map: {}'.format(save.get_last_maps(True)))

    # FT Stations
    if args.verbose or args.fast_travel:
        stations = save.get_active_ft_station_lists()
        if stations is not None:
            if len(stations) == 0:
                print(' - No Active Fast Travel Stations')
            else:
                print(' - Active Fast Travel Stations:')
                for station in stations:
                    print('   - {}'.format(station))

    # Missions
    active_missions = save.get_active_mission_lists(True)
    active_missions_obj = save.get_active_mission_lists()
    if active_missions is not None:
        if len(active_missions) == 0:
            print(' - No Active Missions')
        else:
            print(' - Active Missions:')
            for mission, obj_name in sorted(zip(active_missions, active_missions_obj)):
                print('   - {}'.format(mission))
                if args.mission_paths:
                    print('     {}'.format(obj_name))

    # Completed mission count
    completed_missions = save.get_completed_mission_lists(True)
    completed_missions_obj = save.get_completed_mission_lists()
    if completed_missions is not None:
        print(' - Missions completed: {}'.format(len(completed_missions)))

        # Show all missions if need be
        if args.verbose or args.all_missions:
            for mission, obj_name in sorted(zip(completed_missions, completed_missions_obj)):
                print('   - {}'.format(mission))
                if args.mission_paths:
                    print('     {}'.format(obj_name))

        # "Important" missions - I'm torn as to whether or not this kind of thing
        # should be in ttwlsave.py itself, or at least some constants in __init__.py
        mission_set = set(completed_missions)
        importants = []
        if 'Epilogue' in mission_set:
            importants.append('Main Game')
        if 'Defeated Chums: Difficulty 4' in mission_set:
            importants.append('DLC1 - Coiled Captors')
        if 'Defeated Imelda: Difficulty 4' in mission_set:
            importants.append('DLC2 - Glutton\'s Gamble')
        if 'Defeated Fyodor: Difficulty 4' in mission_set:
            importants.append('DLC3 - Molten Mirrors')
        if 'Defeated Redmourne: Difficulty 4' in mission_set:
            importants.append('DLC4 - Shattering Spectreglass')
        if len(importants) > 0:
            print(' - Mission Milestones:')
            for important in importants:
                print('   - Finished: {}'.format(important))

    # Inventory Slots that we care about
    print('Unlockable Inventory Slots:')
    for slot in [
            # Not reporting on second spell slot since that's class-specific
            InvSlot.WEAPON3,
            InvSlot.WEAPON4,
            InvSlot.ARMOR,
            InvSlot.RING1,
            InvSlot.RING2,
            InvSlot.AMULET,
            ]:
        equip = save.get_equip_slot(slot)
        enabled = False
        if equip is not None:
            enabled = equip.enabled()
        print(' - {}: {}'.format(
            slot.label,
            enabled,
            ))

    # Inventory
    if args.verbose or args.items:
        items = save.get_items()
        if len(items) == 0:
            print('Nothing in Inventory')
        else:
            print('Inventory:')
            to_report = []
            for item in items:
                try:
                    reroll_extra = ''
                    if args.rerolls:
                        if item.rerolled:
                            reroll_extra = f' (rerolls: {item.rerolled})'
                    if item.eng_name:
                        to_report.append(' - {} ({}){}: {}'.format(
                            item.eng_name,
                            item.get_level_eng(),
                            reroll_extra,
                            item.get_serial_base64(),
                            ))
                    else:
                        to_report.append(' - unknown item: {}'.format(item.get_serial_base64()))
                except:
                    print(f"Parse error for {item.get_serial_base64()}")
                    to_report.append(' - unknown item: {}'.format(item.get_serial_base64()))

            for line in sorted(to_report):
                print(line)

    # Equipped Items
    if args.verbose or args.items:
        items = save.get_equipped_items(True)
        if any(items.values()):
            print('Equipped Items:')
            to_report = []
            for (slot, item) in items.items():
                if item:
                    try:
                        reroll_extra = ''
                        if args.rerolls:
                            if item.rerolled:
                                reroll_extra = f' (rerolls: {item.rerolled})'
                        if item.eng_name:
                            to_report.append(' - {}: {} ({}){}: {}'.format(
                                slot,
                                item.eng_name,
                                item.get_level_eng(),
                                reroll_extra,
                                item.get_serial_base64(),
                                ))
                        else:
                            to_report.append(' - {}: unknown item: {}'.format(slot, item.get_serial_base64()))
                    except:
                        print("Could not parse {}".format(item.get_serial_base64()))
                        to_report.append(' - {}: unknown item: {}'.format(slot, item.get_serial_base64()))
            for line in sorted(to_report):
                print(line)
        else:
            print('No Equipped Items')

    # SDUs
    sdus = save.get_sdus_with_max(True)
    if len(sdus) == 0:
        print('No SDUs Purchased')
    else:
        print('SDUs:')
        for sdu, (count, max_sdus) in sdus.items():
            print(' - {}: {}/{}'.format(sdu, count, max_sdus))

    # Ammo
    print('Ammo Pools:')
    for ammo, count in save.get_ammo_counts(True).items():
        print(' - {}: {}'.format(ammo, count))

    # "raw" Challenges
    if args.verbose or args.all_challenges:
        print('All Challenges:')
        for challenge in save.get_all_challenges_raw():
            print(' - {} (Completed: {}, Counter: {}, Progress: {})'.format(
                challenge.challenge_class_path,
                challenge.currently_completed,
                challenge.progress_counter,
                challenge.completed_progress_level,
                ))

if __name__ == '__main__':
    main()
