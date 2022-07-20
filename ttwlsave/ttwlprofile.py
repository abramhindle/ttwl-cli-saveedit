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

# The encryption/decryption stanzas in TTWLProfile.__init__
# were helpfully provided by Gibbed (rick 'at' gibbed 'dot' us), so many
# thanks for that!  https://gist.github.com/gibbed/b6a93f74c575ce99b42c3b629ac1856a
#
# The rest of the savegame format was gleaned from 13xforever/Ilya's
# "gvas-converter" project: https://github.com/13xforever/gvas-converter

import base64
import struct
import google.protobuf
import google.protobuf.json_format
from . import *
from . import datalib
from . import OakProfile_pb2, OakShared_pb2

class LostLootItem(datalib.WLSerial):
    """
    Pretty thin wrapper around the serial number for an item found in the
    Lost Loot machine.  Mostly just so we can keep track of what index it
    is in the profile.

    NOTE: This is technically relatively untested in Wonderlands -- the
    Bank used to make use of this structure in BL3, but in WL it was
    updated to use the same structure as player inventory, so that now
    lives in `datalib.WLItem`.  We don't have any functions which alter
    Lost Loot data, so really only reads have been tested.  This worked
    fine for Bank data in BL3, though, so it *should* be all right, one
    hopes.
    """

    def __init__(self, serial_number, container, index, datawrapper):
        self.container = container
        self.index = index
        # print(f'Prof:{serial_number}')
        super().__init__(serial_number, datawrapper)

    @staticmethod
    def create(serial_number, container, datawrapper):
        """
        Creates a new item with the specified serial number, in the specified
        `container`
        """
        return LostLootItem(serial_number, container, -1, datawrapper)

    def _update_superclass_serial(self):
        """
        Action to take when our serial number gets updated.  In this case,
        overwriting our position in the containing list.
        """
        if self.index >= 0:
            self.container[self.index] = self.serial

class TTWLProfile(object):
    """
    Wrapper around the protobuf object for a WL profile file.

    Only tested on PC versions.  Thanks to Gibbed for the encryption method and
    the Protobuf definitions!

    https://gist.github.com/gibbed/b6a93f74c575ce99b42c3b629ac1856a

    All these getters/setters are rather un-Pythonic; should be using
    some decorations for that instead.  Alas!
    """

    _prefix_magic = bytearray([
        0xD8, 0x04, 0xB9, 0x08, 0x5C, 0x4E, 0x2B, 0xC0,
        0x61, 0x9F, 0x7C, 0x8D, 0x5D, 0x34, 0x00, 0x56,
        0xE7, 0x7B, 0x4E, 0xC0, 0xA4, 0xD6, 0xA7, 0x01,
        0x14, 0x15, 0xA9, 0x93, 0x1F, 0x27, 0x2C, 0x8F,
        ])

    _xor_magic = bytearray([
        0xE8, 0xDC, 0x3A, 0x66, 0xF7, 0xEF, 0x85, 0xE0,
        0xBD, 0x4A, 0xA9, 0x73, 0x57, 0x99, 0x30, 0x8C,
        0x94, 0x63, 0x59, 0xA8, 0xC9, 0xAE, 0xD9, 0x58,
        0x7D, 0x51, 0xB0, 0x1E, 0xBE, 0xD0, 0x77, 0x43,
        ])

    def __init__(self, filename, debug=False):
        self.filename = filename
        self.datawrapper = datalib.DataWrapper()
        with open(filename, 'rb') as df:

            header = df.read(4)
            assert(header == b'GVAS')

            self.sg_version = self._read_int(df)
            if debug:
                print('Profile version: {}'.format(self.sg_version))
            self.pkg_version = self._read_int(df)
            if debug:
                print('Package version: {}'.format(self.pkg_version))
            self.engine_major = self._read_short(df)
            self.engine_minor = self._read_short(df)
            self.engine_patch = self._read_short(df)
            self.engine_build = self._read_int(df)
            if debug:
                print('Engine version: {}.{}.{}.{}'.format(
                    self.engine_major,
                    self.engine_minor,
                    self.engine_patch,
                    self.engine_build,
                    ))
            self.build_id = self._read_str(df)
            if debug:
                print('Build ID: {}'.format(self.build_id))
            self.fmt_version = self._read_int(df)
            if debug:
                print('Custom Format Version: {}'.format(self.fmt_version))
            fmt_count = self._read_int(df)
            if debug:
                print('Custom Format Data Count: {}'.format(fmt_count))
            self.custom_format_data = []
            for _ in range(fmt_count):
                guid = self._read_guid(df)
                entry = self._read_int(df)
                if debug:
                    print(' - GUID {}: {}'.format(guid, entry))
                self.custom_format_data.append((guid, entry))
            self.sg_type = self._read_str(df)
            if debug:
                print('Profile type: {}'.format(sg_type))

            # Read in the actual data
            remaining_data_len = self._read_int(df)
            data = bytearray(df.read(remaining_data_len))

            # Decrypt
            for i in range(len(data)-1, -1, -1):
                if i < 32:
                    b = TTWLProfile._prefix_magic[i]
                else:
                    b = data[i - 32]
                b ^= TTWLProfile._xor_magic[i % 32]
                data[i] ^= b

            # Make sure that was all there was
            last = df.read()
            assert(len(last) == 0)

            # Parse protobufs
            self.import_protobuf(data)

    def import_protobuf(self, data):
        """
        Given raw protobuf data, load it into ourselves so
        that we can work with it.  This also sets up a few
        convenience vars for our later use
        """

        # Now parse the protobufs
        self.prof = OakProfile_pb2.Profile()
        try:
            self.prof.ParseFromString(data)
        except google.protobuf.message.DecodeError as e:
            raise Exception('Unable to parse profile (did you pass a savegame, instead?): {}'.format(e)) from None

        # Do some data processing so that we can wrap things APIwise
        # First: Bank
        self.bank = [datalib.WLItem(i, self.datawrapper) for i in self.prof.bank_inventory_list]

        # Next: Lost Loot
        self.lost_loot = [LostLootItem(s, self.prof.lost_loot_inventory_list, idx, self.datawrapper) for idx, s in enumerate(self.prof.lost_loot_inventory_list)]

    def import_json(self, json_str):
        """
        Given JSON data, convert to protobuf and load it into ourselves so
        that we can work with it.  This also sets up a few convenience vars
        for our later use
        """
        message = google.protobuf.json_format.Parse(json_str, OakProfile_pb2.Profile())
        self.import_protobuf(message.SerializeToString())

    def save_to(self, filename):
        """
        Saves ourselves to a new filename
        """
        with open(filename, 'wb') as df:

            # Header info
            df.write(b'GVAS')
            self._write_int(df, self.sg_version)
            self._write_int(df, self.pkg_version)
            self._write_short(df, self.engine_major)
            self._write_short(df, self.engine_minor)
            self._write_short(df, self.engine_patch)
            self._write_int(df, self.engine_build)
            self._write_str(df, self.build_id)
            self._write_int(df, self.fmt_version)
            self._write_int(df, len(self.custom_format_data))
            for guid, entry in self.custom_format_data:
                self._write_guid(df, guid)
                self._write_int(df, entry)
            self._write_str(df, self.sg_type)

            # Turn our parsed protobuf back into data
            data = bytearray(self.prof.SerializeToString())

            # Encrypt
            for i in range(len(data)):
                if i < 32:
                    b = self._prefix_magic[i]
                else:
                    b = data[i - 32]
                b ^= self._xor_magic[i % 32]
                data[i] ^= b

            # Write out to the file
            self._write_int(df, len(data))
            df.write(data)

    def save_protobuf_to(self, filename):
        """
        Saves the raw protobufs to the specified filename
        """
        with open(filename, 'wb') as df:
            df.write(self.prof.SerializeToString())

    def save_json_to(self, filename):
        """
        Saves a JSON version of our protobuf to the specfied filename
        """
        with open(filename, 'w') as df:
            df.write(google.protobuf.json_format.MessageToJson(self.prof,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                ))

    def _read_int(self, df):
        return struct.unpack('<I', df.read(4))[0]

    def _write_int(self, df, value):
        df.write(struct.pack('<I', value))

    def _read_short(self, df):
        return struct.unpack('<H', df.read(2))[0]

    def _write_short(self, df, value):
        df.write(struct.pack('<H', value))

    def _read_str(self, df):
        datalen = self._read_int(df)
        if datalen == 0:
            return None
        elif datalen == 1:
            return ''
        else:
            value = df.read(datalen)
            return value[:-1].decode('utf-8')

    def _write_str(self, df, value):
        if value is None:
            self._write_int(df, 0)
        elif value == '':
            self._write_int(df, 1)
        else:
            data = value.encode('utf-8') + b'\0'
            self._write_int(df, len(data))
            df.write(data)

    def _read_guid(self, df):
        data = df.read(16)
        return data
        # A bit silly to bother formatting it, since we don't care.
        #arr = ''.join(['{:02x}'.format(d) for d in data])
        #return '{}-{}-{}-{}-{}'.format(
        #        arr[0:8],
        #        arr[8:12],
        #        arr[12:16],
        #        arr[16:20],
        #        arr[20:32],
        #        )

    def _write_guid(self, df, value):
        df.write(value)

    def get_sdus(self, eng=False):
        """
        Returns a dict containing the SDU type and the number purchased.  The SDU
        type key will be a constant by default, or an English label if `eng` is `True`
        """
        to_ret = {}
        for psdu in self.prof.profile_sdu_list:
            if eng:
                key = ProfileSDU.get_label(psdu.sdu_data_path)
            else:
                key = ProfileSDU(psdu.sdu_data_path)
            to_ret[key] = psdu.sdu_level
        return to_ret

    def get_sdus_with_max(self, eng=False):
        """
        Returns a dict whose keys are the SDU type, and the values are tuples with
        two values:
            1. The number of that SDU type purchased
            2. The maximum number of SDUs available for that type
        The SDU type key will be a constant by default, or an English label if
        `eng` is `True`.  This is just a convenience function suitable for
        giving more information to users.
        """
        to_ret = {}
        for psdu_proto in self.prof.profile_sdu_list:
            psdu = ProfileSDU(psdu_proto.sdu_data_path)
            if eng:
                key = ProfileSDU.get_label(psdu_proto.sdu_data_path)
            else:
                key = psdu.value
            to_ret[key] = (psdu_proto.sdu_level, psdu.num)
        return to_ret

    def get_sdu(self, sdu):
        """
        Returns the number of SDUs purchased for the specified type
        """
        sdus = self.get_sdus()
        if sdu in sdus:
            return sdus[sdu]
        return 0

    def set_max_sdus(self, sdulist=None):
        """
        Sets the specified SDUs (or all SDUs that we know about) to be at the max level
        """
        if sdulist is None:
            all_sdus = set(ProfileSDU)
        else:
            all_sdus = set(sdulist)

        # Set all existing SDUs to max
        for psdu_proto in self.prof.profile_sdu_list:
            psdu = ProfileSDU(psdu_proto.sdu_data_path)
            if psdu in all_sdus:
                all_sdus.remote(psdu)
                psdu_proto.sdu_level = psdu.num

        # If we're missing any, add them.
        for psdu in all_sdus:
            self.prof.profile_sdu_list.append(OakShared_pb2.OakSDUSaveGameData(
                sdu_data_path=psdu.value,
                sdu_level=psdu.num,
                ))

    def create_new_bank_item(self, item_serial):
        """
        Creates a new item (as a WLItem object) from the given binary `item_serial`,
        which can later be added to our item bank list.
        """

        # Okay, I have no idea what this pickup_order_index attribute is about, but let's
        # make sure it's unique anyway.  It might be related to ordering when picking
        # up multiple items at once, which would probably make it more useful for auto-pick-up
        # items like money and ammo...
        max_pickup_order = 0
        for item in self.bank:
            if item.get_pickup_order_idx() > max_pickup_order:
                max_pickup_order = item.get_pickup_order_idx()

        # Create the item and return it
        return datalib.WLItem.create(self.datawrapper,
                serial_number=item_serial,
                pickup_order_idx=max_pickup_order+1,
                is_favorite=True,
                )

    def create_new_bank_item_encoded(self, item_serial_b64):
        """
        Creates a new item (as a WLItem object) from the base64-encoded (and
        "WL()"-wrapped) `item_serial_b64`, which can later be added to our bank.
        """
        return self.create_new_bank_item(datalib.WLSerial.decode_serial_base64(item_serial_b64))

    def get_lostloot_items(self):
        """
        Returns a list of this profile's Lost Loot items, as LostLootItem objects.
        """
        return self.lost_loot

    def get_bank_items(self):
        """
        Returns a list of this profile's bank items, as WLItem objects.
        """
        return self.bank

    def add_new_bank_item(self, item_serial):
        """
        Adds a new item to our bank using the binary `item_serial`.
        Returns a tuple containing the new WLItem object itself, and its
        new index in our bank list.
        """
        new_item = self.create_new_bank_item(item_serial)
        return (new_item, self.add_bank_item(new_item))

    def add_bank_item(self, new_item):
        """
        Adds a new `new_item` (WLItem object) to our bank.  Returns the item's
        new index in the bank.
        """

        # Add the item to the protobuf
        self.prof.bank_inventory_list.append(new_item.protobuf)

        # The protobuf reference that we append to the protobuf list
        # ends up *not* being the one that's actually used when we
        # save, so if we want to be able to alter it later (say, below
        # when levelling up items), we have to grab a fresh reference
        # to it.
        new_item.protobuf = self.prof.bank_inventory_list[-1]

        # Now update our internal items list and return
        self.bank.append(new_item)
        return len(self.bank)-1

    def get_cur_customizations(self, cust_set):
        """
        Returns a set of the currently-unlocked customizations which live in the
        given `cust_set`.  (A variety of customization types all live in the same
        data structure in the savegame, which is why we have this layer.)
        """
        to_ret = set()
        for cust in self.prof.unlocked_customizations:
            if cust.customization_asset_path in cust_set:
                to_ret.add(cust.customization_asset_path)
        return to_ret

    def unlock_customization_set(self, cust_set):
        """
        Unlocks the given set of customizations in the main customization
        area.
        """
        current_custs = self.get_cur_customizations(cust_set)
        missing = cust_set - current_custs
        for cust in missing:
            self.prof.unlocked_customizations.append(OakShared_pb2.OakCustomizationSaveGameData(
                is_new=True,
                customization_asset_path=cust,
                ))

    def get_customizations_total(self):
        """
        Returns the total number of customizations that are possible to unlock.  Includes
        the customizations which are unlocked by default
        """
        return len(profile_customizations) + len(profile_customizations_defaults)

    def get_customizations(self):
        """
        Returns a set of the current customizations which are unlocked.  Includes the
        customizations which are unlocked by default
        """
        return self.get_cur_customizations(profile_customizations) | profile_customizations_defaults

    def unlock_customizations(self):
        """
        Unlocks all customizations
        """
        self.unlock_customization_set(profile_customizations)

    def clear_all_customizations(self):
        """
        Removes all unlocked customizations.
        """
        del self.prof.unlocked_customizations[:]

    def _get_generic_keys(self, key):
        """
        The profile holds info for a few different key types now.  This
        will return the count for the specified `key`.
        """
        for cat in self.prof.bank_inventory_category_list:
            if cat.base_category_definition_hash == key.value:
                return cat.quantity
        return 0

    def _set_generic_keys(self, key, num_keys):
        """
        The profile holds info for a few different key types now.  This
        will set the number of keys for the specified `key` to
        `num_keys.
        """
        for cat in self.prof.bank_inventory_category_list:
            if cat.base_category_definition_hash == key.value:
                cat.quantity = num_keys
                return

        # If we got here, apparently this profile hasn't seen this key type at all
        self.prof.bank_inventory_category_list.append(OakShared_pb2.InventoryCategorySaveData(
            base_category_definition_hash=key.value,
            quantity=num_keys
            ))

    def get_skeleton_keys(self):
        """
        Returns the number of skeleton keys stored on this profile
        """
        return self._get_generic_keys(Key.SKELETON)

    def set_skeleton_keys(self, num_keys):
        """
        Sets the number of skeleton keys to `num_keys`
        """
        self._set_generic_keys(Key.SKELETON, num_keys)

    def set_myth_stats_points(self, points):
        """
        Sets all Myth Rank points to the specified value, making sure to not go
        over the maximums for each category.
        """
        for idx, rank in enumerate(MythRank):
            if rank.num > 0 and points > rank.num:
                to_set = rank.num
            else:
                to_set = points
            self.prof.player_prestige.points_spent_by_index_order[idx] = to_set

    def zero_myth_rank(self):
        """
        Resets this profile's Myth Rank entirely
        """
        self.set_myth_stats_points(0)
        self.prof.player_prestige.prestige_experience = 0

    def myth_stats_max(self):
        """
        Sets Myth Rank Stats to their maximum values, for the categories which
        have maximums.  Other categories will just make sure there's at least
        one point in them.
        """
        for idx, rank in enumerate(MythRank):
            if rank.num > 0:
                self.prof.player_prestige.points_spent_by_index_order[idx] = rank.num
            else:
                self.prof.player_prestige.points_spent_by_index_order[idx] = max(
                        1,
                        self.prof.player_prestige.points_spent_by_index_order[idx],
                        )

    def set_myth_xp(self, value):
        """
        Sets our raw Myth Rank XP to the specified `value`.  This is what the game
        uses to determin how many Myth Rank points "should" be available.  We
        don't yet know the equation used to calculate the XP->points value, so
        this'll have to do for now.
        """
        self.prof.player_prestige.prestige_experience = value

    def get_myth_xp(self):
        """
        Returns the raw Myth Rank XP for the profile
        """
        return self.prof.player_prestige.prestige_experience

    def get_myth_rank_stats(self):
        """
        Returns a dict containing information about how Myth Rank is allocated
        in the profile.  Keys will be a MythRank enum member, and the values
        will be the currently-set points.
        """
        to_ret = {}
        for stat, cur_value in zip(MythRank, self.prof.player_prestige.points_spent_by_index_order):
            to_ret[stat] = cur_value
        return to_ret

