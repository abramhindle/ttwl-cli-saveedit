
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

# Editor Version
__version__ = '0.0.12'
# Forked from bl3-cli-saveedit
# __version__ = '1.16.1b1'

import enum
import random

class LabelEnum(enum.Enum):
    """
    An enum whose members have a label in addition to the value.  Optionally,
    can also include a number value, which might represent the maximum available
    or somesuch.  For our purposes, the value is going to be the object name.
    """

    def __new__(cls, label, value, num=None):
        obj = object.__new__(cls)
        obj.label = label
        obj._value_ = value
        obj.num = num
        return obj

    @classmethod
    def has_value(cls, value, default=None):
        """
        Check to see if this Enum contains the given `value`, returning a `default`
        value (`None` by default) if not found.
        """
        try:
            return cls(value)
        except:
            return default

    @classmethod
    def get_label(cls, value):
        """
        Returns our label for the specified `value`, if we can.  If `value` is
        not known to the Enum, return the `value` back, instead.
        """
        obj = cls.has_value(value)
        if obj:
            return obj.label
        else:
            return value

# CRC32 table used to compute various inventory hashes in the profile.  Many
# thanks to Gibbed, yet again, for supplying this!
_hash_cust_crc32_table = [
        0x00000000, 0x04C11DB7, 0x09823B6E, 0x0D4326D9, 0x130476DC, 0x17C56B6B, 0x1A864DB2, 0x1E475005,
        0x2608EDB8, 0x22C9F00F, 0x2F8AD6D6, 0x2B4BCB61, 0x350C9B64, 0x31CD86D3, 0x3C8EA00A, 0x384FBDBD,
        0x4C11DB70, 0x48D0C6C7, 0x4593E01E, 0x4152FDA9, 0x5F15ADAC, 0x5BD4B01B, 0x569796C2, 0x52568B75,
        0x6A1936C8, 0x6ED82B7F, 0x639B0DA6, 0x675A1011, 0x791D4014, 0x7DDC5DA3, 0x709F7B7A, 0x745E66CD,
        0x9823B6E0, 0x9CE2AB57, 0x91A18D8E, 0x95609039, 0x8B27C03C, 0x8FE6DD8B, 0x82A5FB52, 0x8664E6E5,
        0xBE2B5B58, 0xBAEA46EF, 0xB7A96036, 0xB3687D81, 0xAD2F2D84, 0xA9EE3033, 0xA4AD16EA, 0xA06C0B5D,
        0xD4326D90, 0xD0F37027, 0xDDB056FE, 0xD9714B49, 0xC7361B4C, 0xC3F706FB, 0xCEB42022, 0xCA753D95,
        0xF23A8028, 0xF6FB9D9F, 0xFBB8BB46, 0xFF79A6F1, 0xE13EF6F4, 0xE5FFEB43, 0xE8BCCD9A, 0xEC7DD02D,
        0x34867077, 0x30476DC0, 0x3D044B19, 0x39C556AE, 0x278206AB, 0x23431B1C, 0x2E003DC5, 0x2AC12072,
        0x128E9DCF, 0x164F8078, 0x1B0CA6A1, 0x1FCDBB16, 0x018AEB13, 0x054BF6A4, 0x0808D07D, 0x0CC9CDCA,
        0x7897AB07, 0x7C56B6B0, 0x71159069, 0x75D48DDE, 0x6B93DDDB, 0x6F52C06C, 0x6211E6B5, 0x66D0FB02,
        0x5E9F46BF, 0x5A5E5B08, 0x571D7DD1, 0x53DC6066, 0x4D9B3063, 0x495A2DD4, 0x44190B0D, 0x40D816BA,
        0xACA5C697, 0xA864DB20, 0xA527FDF9, 0xA1E6E04E, 0xBFA1B04B, 0xBB60ADFC, 0xB6238B25, 0xB2E29692,
        0x8AAD2B2F, 0x8E6C3698, 0x832F1041, 0x87EE0DF6, 0x99A95DF3, 0x9D684044, 0x902B669D, 0x94EA7B2A,
        0xE0B41DE7, 0xE4750050, 0xE9362689, 0xEDF73B3E, 0xF3B06B3B, 0xF771768C, 0xFA325055, 0xFEF34DE2,
        0xC6BCF05F, 0xC27DEDE8, 0xCF3ECB31, 0xCBFFD686, 0xD5B88683, 0xD1799B34, 0xDC3ABDED, 0xD8FBA05A,
        0x690CE0EE, 0x6DCDFD59, 0x608EDB80, 0x644FC637, 0x7A089632, 0x7EC98B85, 0x738AAD5C, 0x774BB0EB,
        0x4F040D56, 0x4BC510E1, 0x46863638, 0x42472B8F, 0x5C007B8A, 0x58C1663D, 0x558240E4, 0x51435D53,
        0x251D3B9E, 0x21DC2629, 0x2C9F00F0, 0x285E1D47, 0x36194D42, 0x32D850F5, 0x3F9B762C, 0x3B5A6B9B,
        0x0315D626, 0x07D4CB91, 0x0A97ED48, 0x0E56F0FF, 0x1011A0FA, 0x14D0BD4D, 0x19939B94, 0x1D528623,
        0xF12F560E, 0xF5EE4BB9, 0xF8AD6D60, 0xFC6C70D7, 0xE22B20D2, 0xE6EA3D65, 0xEBA91BBC, 0xEF68060B,
        0xD727BBB6, 0xD3E6A601, 0xDEA580D8, 0xDA649D6F, 0xC423CD6A, 0xC0E2D0DD, 0xCDA1F604, 0xC960EBB3,
        0xBD3E8D7E, 0xB9FF90C9, 0xB4BCB610, 0xB07DABA7, 0xAE3AFBA2, 0xAAFBE615, 0xA7B8C0CC, 0xA379DD7B,
        0x9B3660C6, 0x9FF77D71, 0x92B45BA8, 0x9675461F, 0x8832161A, 0x8CF30BAD, 0x81B02D74, 0x857130C3,
        0x5D8A9099, 0x594B8D2E, 0x5408ABF7, 0x50C9B640, 0x4E8EE645, 0x4A4FFBF2, 0x470CDD2B, 0x43CDC09C,
        0x7B827D21, 0x7F436096, 0x7200464F, 0x76C15BF8, 0x68860BFD, 0x6C47164A, 0x61043093, 0x65C52D24,
        0x119B4BE9, 0x155A565E, 0x18197087, 0x1CD86D30, 0x029F3D35, 0x065E2082, 0x0B1D065B, 0x0FDC1BEC,
        0x3793A651, 0x3352BBE6, 0x3E119D3F, 0x3AD08088, 0x2497D08D, 0x2056CD3A, 0x2D15EBE3, 0x29D4F654,
        0xC5A92679, 0xC1683BCE, 0xCC2B1D17, 0xC8EA00A0, 0xD6AD50A5, 0xD26C4D12, 0xDF2F6BCB, 0xDBEE767C,
        0xE3A1CBC1, 0xE760D676, 0xEA23F0AF, 0xEEE2ED18, 0xF0A5BD1D, 0xF464A0AA, 0xF9278673, 0xFDE69BC4,
        0x89B8FD09, 0x8D79E0BE, 0x803AC667, 0x84FBDBD0, 0x9ABC8BD5, 0x9E7D9662, 0x933EB0BB, 0x97FFAD0C,
        0xAFB010B1, 0xAB710D06, 0xA6322BDF, 0xA2F33668, 0xBCB4666D, 0xB8757BDA, 0xB5365D03, 0xB1F740B4,
        ]

def inventory_path_hash(object_path):
    """
    Computes the hashes used in the profile for weapon customizations and the skeleton key
    count.  Possibly used for other things, too.  Many thanks to Gibbed, yet again, for this!
    """
    global _hash_cust_crc32_table
    if '.' not in object_path:
        object_path = '{}.{}'.format(object_path, object_path.split('/')[-1])

    # TODO: Gibbed was under the impression that these were checksummed in
    # UTF-16, but the hashes all match for me when using latin1/utf-8.
    object_full = object_path.upper().encode('latin1')
    crc32 = 0
    for char in object_full:
        crc32 = (_hash_cust_crc32_table[(crc32 ^ (char >> 0)) & 0xFF] ^ (crc32 >> 8)) & 0xFFFFFFFF
        crc32 = (_hash_cust_crc32_table[(crc32 ^ (char >> 8)) & 0xFF] ^ (crc32 >> 8)) & 0xFFFFFFFF
    return crc32

class HashLabelEnum(LabelEnum):
    """
    A version of LabelEnum whose values should be the "hashed" inventory keys used
    by various things (money, some customizations) in savefiles.  Introduces an
    `obj_path` attribute which LabelEnum doesn't have, to store the "original"
    value.  Note that in these cases, the object path itself won't ever show up
    in saves/profiles directly, only the hashed value.
    """

    # Honestly not sure how I'd extend this "properly"; just reimplementing
    # it w/ our new functionality.
    def __new__(cls, label, obj_path, num=None):
        obj = object.__new__(cls)
        obj.label = label
        obj.obj_path = obj_path
        obj._value_ = inventory_path_hash(obj_path)
        obj.num = num
        return obj

# Classes
class CharClass(LabelEnum):
    BRRZERKER = ('Brr-Zerker', '/Game/PlayerCharacters/Barbarian/_Shared/_Design/SkillTree/AbilityTree_Branch_Barbarian.AbilityTree_Branch_Barbarian')
    CLAWBRINGER = ('Clawbringer', '/Game/PlayerCharacters/KnightOfTheClaw/_Shared/_Design/SkillTree/AbilityTree_Branch_DragonCleric.AbilityTree_Branch_DragonCleric')
    GRAVEBORN = ('Graveborn', '/Game/PlayerCharacters/Necromancer/_Shared/_Design/SkillTree/AbilityTree_Branch_Necromancer.AbilityTree_Branch_Necromancer')
    SPELLSHOT = ('Spellshot', '/Game/PlayerCharacters/GunMage/_Shared/_Design/SkillTree/AbilityTree_Branch_GunMage.AbilityTree_Branch_GunMage')
    SPOREWARDEN = ('Spore Warden', '/Game/PlayerCharacters/Ranger/_Shared/_Design/SkillTree/AbilityTree_Branch_Ranger.AbilityTree_Branch_Ranger')
    STABBOMANCER = ('Stabbomancer', '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/AbilityTree_Branch_Rogue.AbilityTree_Branch_Rogue')

# Companions
class Companion(LabelEnum):
    LICH = ('Demi-Lich', 'petnicknamelich')
    WYVERN = ('Wyvern', 'petnicknamewyvern')
    MUSHROOM = ('Mushroom', 'petnicknamemushroom')

# Currencies
class Currency(HashLabelEnum):
    MONEY = ('Money', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money', 2000000000)
    MOON_ORBS = ('Moon Orbs', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium', 16000)
    SOULS = ('Lost Souls', '/Game/PatchDLC/Indigo1/Common/Pickups/IndCurrency/InventoryCategory_IndCurrency.InventoryCategory_IndCurrency', None)

# Inventory Slots
class InvSlot(LabelEnum):
    MELEE = ('Melee', '/Game/Gear/Melee/_Shared/_Design/A_Data/BPInvSlot_Melee.BPInvSlot_Melee')
    WEAPON1 = ('Weapon 1', '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon1.BPInvSlot_Weapon1')
    WEAPON2 = ('Weapon 2', '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon2.BPInvSlot_Weapon2')
    WEAPON3 = ('Weapon 3', '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon3.BPInvSlot_Weapon3')
    WEAPON4 = ('Weapon 4', '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon4.BPInvSlot_Weapon4')
    WARD = ('Ward', '/Game/Gear/Shields/_Design/A_Data/BPInvSlot_Shield.BPInvSlot_Shield')
    SPELL1 = ('Spell', '/Game/Gear/SpellMods/_Shared/_Design/A_Data/BPInvSlot_SpellMod.BPInvSlot_SpellMod')
    SPELL2 = ('Spell 2', '/Game/Gear/SpellMods/_Shared/_Design/A_Data/BPInvSlot_SecondSpellMod.BPInvSlot_SecondSpellMod')
    ARMOR = ('Armor', '/Game/Gear/Pauldrons/_Shared/_Design/A_Data/InvSlot_Pauldron.InvSlot_Pauldron')
    RING1 = ('Ring 1', '/Game/Gear/Rings/_Shared/Design/A_Data/InvSlot_Ring_1.InvSlot_Ring_1')
    RING2 = ('Ring 2', '/Game/Gear/Rings/_Shared/Design/A_Data/InvSlot_Ring_2.InvSlot_Ring_2')
    AMULET = ('Amulet', '/Game/Gear/Amulets/_Shared/_Design/A_Data/InvSlot_Amulet.InvSlot_Amulet')

# SDUs
class SDU(LabelEnum):
    BACKPACK = ('Backpack', '/Game/Pickups/SDU/SDU_Backpack.SDU_Backpack', 13)
    AR = ('AR', '/Game/Pickups/SDU/SDU_AssaultRifle.SDU_AssaultRifle', 10)
    PISTOL = ('Pistol', '/Game/Pickups/SDU/SDU_Pistol.SDU_Pistol', 10)
    SNIPER = ('Sniper', '/Game/Pickups/SDU/SDU_SniperRifle.SDU_SniperRifle', 13)
    SHOTGUN = ('Shotgun', '/Game/Pickups/SDU/SDU_Shotgun.SDU_Shotgun', 10)
    GRENADE = ('Grenade', '/Game/Pickups/SDU/SDU_Grenade.SDU_Grenade', 10)
    SMG = ('SMG', '/Game/Pickups/SDU/SDU_SMG.SDU_SMG', 10)
    HEAVY = ('Heavy', '/Game/Pickups/SDU/SDU_Heavy.SDU_Heavy', 13)
ammo_sdus = [
        SDU.AR,
        SDU.PISTOL,
        SDU.SNIPER,
        SDU.SHOTGUN,
        SDU.GRENADE,
        SDU.SMG,
        SDU.HEAVY,
        ]

# Profile SDUs
class ProfileSDU(LabelEnum):
    LOSTLOOT = ('Lost Loot', '/Game/Pickups/SDU/SDU_LostLoot.SDU_LostLoot', 8)
    BANK = ('Bank', '/Game/Pickups/SDU/SDU_Bank.SDU_Bank', 23)

# Ammo
class Ammo(LabelEnum):
    AR = ('AR', '/Game/GameData/Weapons/Ammo/Resource_Ammo_AssaultRifle.Resource_Ammo_AssaultRifle', 1680)
    GRENADE = ('Grenade', '/Game/GameData/Weapons/Ammo/Resource_Ammo_Grenade.Resource_Ammo_Grenade', 13)
    HEAVY = ('Heavy', '/Game/GameData/Weapons/Ammo/Resource_Ammo_Heavy.Resource_Ammo_Heavy', 51)
    PISTOL = ('Pistol', '/Game/GameData/Weapons/Ammo/Resource_Ammo_Pistol.Resource_Ammo_Pistol', 1200)
    SMG = ('SMG', '/Game/GameData/Weapons/Ammo/Resource_Ammo_SMG.Resource_Ammo_SMG', 2160)
    SHOTGUN = ('Shotgun', '/Game/GameData/Weapons/Ammo/Resource_Ammo_Shotgun.Resource_Ammo_Shotgun', 280)
    SNIPER = ('Sniper', '/Game/GameData/Weapons/Ammo/Resource_Ammo_Sniper.Resource_Ammo_Sniper', 204)

# Item Chaos Levels
class ChaosLevel(LabelEnum):
    REGULAR = ('Regular', 0)
    CHAOTIC = ('Chaotic', 1)
    VOLATILE = ('Volatile', 2)
    PRIMORDIAL = ('Primordial', 3)
    ASCENDED = ('Ascended', 4)

# Keys (just Skeleton for now)
class Key(HashLabelEnum):
    SKELETON = ('Skeleton Keys', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey')

# Myth Rank -- value is just the index in the array; num is the max value
class MythRank(LabelEnum):
    # Archmage
    INTELLIGENCE = ('Intelligence', 0, 10)
    SPELL_CRIT_DAMAGE = ('Spell Crit Damage', 1, 20)
    SPELL_CRIT_CHANCE = ('Spell Crit Chance', 2, 20)
    FIRE_DAMAGE = ('Fire Damage', 3, 20)
    CRYO_DAMAGE = ('Cryo Damage', 4, 20)
    STATUS_CHANCE = ('Status Effect Chance', 5, 10)
    SPELL_DAMAGE = ('Spell Damage', 6, 0)
    # Blademaster
    STRENGTH = ('Strength', 7, 10)
    CONSTITUTION = ('Constitution', 8, 10)
    DARK_MAGIC_DAMAGE = ('Dark Magic Damage', 9, 20)
    MELEE_CRIT_CHANCE = ('Melee Crit Chance', 10, 20)
    MELEE_SPEED = ('Melee Swing Speed', 11, 20)
    MELEE_CRIT_DAMAGE = ('Melee Crit Damage', 12, 20)
    MELEE_DAMAGE = ('Melee Damage', 13, 0)
    # Deadeye
    DEXTERITY = ('Dexterity', 14, 10)
    GUN_HANDLING = ('Gun Handling', 15, 10)
    MOVE_SPEED = ('Move Speed', 16, 25)
    RELOAD_SPEED = ('Reload Speed', 17, 20)
    MAG_SIZE = ('Mag Size', 18, 15)
    FIRE_RATE = ('Fire Rate', 19, 20)
    GUN_DAMAGE = ('Gun Damage', 20, 0)
    # Druid
    WISDOM = ('Wisdom', 21, 10)
    COMPANION_DAMAGE = ('Companion Damage', 22, 20)
    ATTUNEMENT = ('Attunement', 23, 10)
    SHOCK_DAMAGE = ('Lightning Damage', 24, 20)
    LUCK = ('Loot Luck', 25, 20)
    POISON_DAMAGE = ('Poison Damage', 26, 20)
    ABILITY_DAMAGE = ('Ability Damage', 27, 0)

# Hero Stats
class HeroStats(LabelEnum):
    STR = ('Strength', 'strength')
    DEX = ('Dexterity', 'dexterity')
    INT = ('Intelligence', 'intelligence')
    WIS = ('Wisdom', 'wisdom')
    CON = ('Constitution', 'constitution')
    ATT = ('Attunement', 'luck')

# Backstories
class Backstory(LabelEnum):
    IDIOT = ('Village Idiot: STR+8, INT-3, WIS-3',
            '/Game/PlayerCharacters/_Shared/_Design/Aspects/Aspect_01.Aspect_01')
    ELVES = ('Raised By Elves: DEX+4, CON-4, ATT+2',
            '/Game/PlayerCharacters/_Shared/_Design/Aspects/Aspect_02.Aspect_02')
    MONK = ('Failed Monk: STR-4, DEX-2, INT+3, WIS+6',
            '/Game/PlayerCharacters/_Shared/_Design/Aspects/Aspect_03.Aspect_03')
    HOARDER = ('Recovering Inventory Hoarder: DEX-2, INT+2, CON-2, ATT+5',
            '/Game/PlayerCharacters/_Shared/_Design/Aspects/Aspect_04.Aspect_04')
    ALCHEMIST = ('Rogue Alchemist: DEX-2, WIS+8, CON-5, ATT+2',
            '/Game/PlayerCharacters/_Shared/_Design/Aspects/Aspect_05.Aspect_05')

# Char-level Stat (not sure if this is useful to set, but we'll do it anyway)
level_stat = '/Game/GameData/Stats/Progression/Stat_Character_Level.Stat_Character_Level'

# Level-based challenges (probably unimportant, but I've already started doing it,
# so here we go anyway)
level_challenges = [
        (10, '/Game/GameData/Challenges/System/BP_Challenge_Console_PlayerLevel_10.BP_Challenge_Console_PlayerLevel_10_C'),
        (20, '/Game/GameData/Challenges/System/BP_Challenge_Console_PlayerLevel_20.BP_Challenge_Console_PlayerLevel_20_C'),
        (30, '/Game/GameData/Challenges/System/BP_Challenge_Console_PlayerLevel_30.BP_Challenge_Console_PlayerLevel_30_C'),
        (40, '/Game/GameData/Challenges/System/BP_Challenge_Console_PlayerLevel_40.BP_Challenge_Console_PlayerLevel_40_C'),
        ]

# Most levels give +1 skill points, but there's a few exceptions.
skill_point_exceptions = {
        20: 2,
        40: 3,
        }

# XP - Multiplication value has changed to 65 (from 60, in all previous
# Borderlands games).  Exponent is still 2.8.  We're continuing to
# hardcode the list to avoid rounding/precision errors, though.
max_level = 40
required_xp_list = [
        # The first 40 here have been verified to be correct
        0,          # lvl 1
        388,        # lvl 2
        1344,       # lvl 3
        3087,       # lvl 4
        5824,       # lvl 5
        9746,       # lvl 6
        15042,      # lvl 7
        21892,      # lvl 8
        30470,      # lvl 9
        40947,      # lvl 10
        53492,      # lvl 11
        68266,      # lvl 12
        85433,      # lvl 13
        105149,     # lvl 14
        127570,     # lvl 15
        152850,     # lvl 16
        181140,     # lvl 17
        212590,     # lvl 18
        247348,     # lvl 19
        285561,     # lvl 20
        327372,     # lvl 21
        372925,     # lvl 22
        422362,     # lvl 23
        475823,     # lvl 24
        533448,     # lvl 25
        595376,     # lvl 26
        661743,     # lvl 27
        732685,     # lvl 28
        808338,     # lvl 29
        888835,     # lvl 30
        974310,     # lvl 31
        1064895,    # lvl 32
        1160721,    # lvl 33
        1261920,    # lvl 34
        1368621,    # lvl 35
        1480953,    # lvl 36
        1599044,    # lvl 37
        1723023,    # lvl 38
        1853015,    # lvl 39
        1989148,    # lvl 40

        # Theoretical values -- no real way to test these, but
        # I'll leave 'em here anyway in case the level cap ever
        # gets raised.  They're unlikely to be off by more than 1.
        2131546,    # lvl 41
        2280336,    # lvl 42
        2435641,    # lvl 43
        2597586,    # lvl 44
        2766293,    # lvl 45
        2941884,    # lvl 46
        3124484,    # lvl 47
        3314212,    # lvl 48
        3511190,    # lvl 49
        3715538,    # lvl 50
        3927377,    # lvl 51
        4146826,    # lvl 52
        4374005,    # lvl 53
        4609032,    # lvl 54
        4852025,    # lvl 55
        5103102,    # lvl 56
        5362381,    # lvl 57
        5629978,    # lvl 58
        5906010,    # lvl 59
        6190593,    # lvl 60
]
max_supported_level = len(required_xp_list)

# Maximum Chaos Level
max_chaos_level = 50

# InvData types which can accept Enchantment parts
# I'd be shocked if there weren't omissions of some sort in here.  These
# are, at least, the InventoryData values for Wards + Shields, plus all
# objects starting with `WT_`...
enchantment_invdata_types = {
        '/Game/Gear/Melee/Axes/_Shared/_Design/WT_Melee_Axe.WT_Melee_Axe',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Fish/WT_Melee_Fish.WT_Melee_Fish',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/LeChancesLastLeg/WT_Melee_LeChancesLastLeg.WT_Melee_LeChancesLastLeg',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/PegLeg/WT_Melee_PegLeg.WT_Melee_PegLeg',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/WT_Melee_Blunt.WT_Melee_Blunt',
        '/Game/Gear/Melee/Swords/_Shared/_Design/WT_Melee_Sword.WT_Melee_Sword',
        '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Dragonlord/Custom/WT_Sword2h_Fatebreaker.WT_Sword2h_Fatebreaker',
        '/Game/Gear/Melee/Swords_2H/_Shared/_Design/WT_Melee_Sword_2H.WT_Melee_Sword_2H',
        '/Game/Gear/Shields/_Design/A_Data/Shield_Default.Shield_Default',
        '/Game/Gear/SpellMods/_Shared/_Design/A_Data/ST_Spell.ST_Spell',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Custom/WT_AR_COV_RogueImp.WT_AR_COV_RogueImp',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/WT_AR_COV.WT_AR_COV',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/WT_AR_DAL.WT_AR_DAL',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/WT_AR_JAK.WT_AR_JAK',
        '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/WT_AR_TOR.WT_AR_TOR',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Custom/WT_AR_VLA_ManualTrans.WT_AR_VLA_ManualTrans',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/WT_AR_VLA.WT_AR_VLA',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/WT_HW_COV.WT_HW_COV',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/WT_HW_TOR.WT_HW_TOR',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/WT_HW_VLA.WT_HW_VLA',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/WT_PS_COV.WT_PS_COV',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/WT_PS_DAL.WT_PS_DAL',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/WT_PS_JAK.WT_PS_JAK',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/WT_PS_TED.WT_PS_TED',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/WT_PS_TOR.WT_PS_TOR',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/Custom/WT_PS_VLA_Automagic.WT_PS_VLA_Automagic',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/WT_PS_VLA.WT_PS_VLA',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/WT_SG_HYP.WT_SG_HYP',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/CustomWeapon/WT_SG_JAK_ReignOfArrows.WT_SG_JAK_ReignOfArrows',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/WT_SG_JAK.WT_SG_JAK',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/WT_SG_TED.WT_SG_TED',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/WT_SG_TOR.WT_SG_TOR',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/WT_SM_DAL.WT_SM_DAL',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/WT_SM_HYP.WT_SM_HYP',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/WT_SM_TED.WT_SM_TED',
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/WT_SR_DAL.WT_SR_DAL',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/WT_SR_HYP.WT_SR_HYP',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/WT_SR_JAK.WT_SR_JAK',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/WT_SR_VLA.WT_SR_VLA',
        '/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/WT_PS_Butterboom.WT_PS_Butterboom',
        }
enchantment_invdata_lower_types = set([t.lower() for t in enchantment_invdata_types])

# Profile Customization Types
class Customization(enum.Enum):
    BODY_SHAPE = 'Body Shape'
    HEAD_SHAPE = 'Head Shape'
    SKIN_COLOR = 'Skin Color'
    HAIR_HEADGEAR = 'Hair and Headgear'
    FACIAL_HAIR_MASKS = 'Facial Hair and Masks'
    HAIR_COLOR = 'Hair Color'
    EAR_SHAPE = 'Ear Shape'
    NOSE_SHAPE = 'Nose Shape'
    MOUTH_SHAPE = 'Mouth Shape'
    EYEBROW = 'Eyebrows'
    EYELASH = 'Eyelashes'
    EYE_SHAPE = 'Eye Shape'
    PUPIL = 'Pupils'
    EYE_COLOR = 'Eye Color'
    SCAR = 'Scar'
    SCAR_FLIP = 'Flip Scars'
    TATTOO = 'Tattoo'
    TATTOO_FLIP = 'Flip Tattoo'
    TATTOO_COLOR = 'Tattoo Color'
    EYELINER = 'Eyeliner'
    EYELINER_COLOR = 'Eyeliner Color'
    EYESHADOW = 'Eyeshadow'
    EYESHADOW_COLOR = 'Eyeshadow Color'
    BLUSH = 'Blush'
    BLUSH_COLOR = 'Blush Color'
    LIPSTICK = 'Lipstick'
    LIPSTICK_COLOR = 'Lipstick Color'
    ARMOR_PATTERN = 'Armor Pattern'
    UNDER_ARMOR_PATTERN = 'Under Armor Pattern'
    ARMOR_COLOR_PRIMARY = 'Armor Color (Primary)'
    ARMOR_COLOR_SECONDARY = 'Armor Color (Secondary)'
    ARMOR_COLOR_TERTIARY = 'Armor Color (Tertiary)'
    EMOTE = 'Emote'
    BANNER_SHAPE = 'Banner Shape'
    BANNER_SHAPE_COLOR = 'Banner Shape Color'
    BANNER_PATTERN = 'Banner Pattern'
    BANNER_PATTERN_COLOR = 'Banner Pattern Color'
    BANNER_ICON = 'Banner Icon'
    BANNER_ICON_COLOR = 'Banner Icon Color'
    STATUE_MATERIAL = 'Statue Material'
    STATUE_POSE = 'Statue Pose'

# Profile Customizations.  # Note that this dict doesn't include the ones which
# are available by default but don't ordinarily show up in the profile.  See
# `profile_customizations_defaults_by_cat` below for those.
profile_customizations_by_cat = {
        Customization.BODY_SHAPE: set(),
        Customization.HEAD_SHAPE: set(),
        Customization.SKIN_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_16.SkinToneColor_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_26.SkinToneColor_26',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_27.SkinToneColor_27',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_28.SkinToneColor_28',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_29.SkinToneColor_29',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_30.SkinToneColor_30',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/SkinTones/SkinToneColor_32.SkinToneColor_32',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Skintones/SkinToneColor_33.SkinToneColor_33',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/SkinTones/SkinToneColor_34.SkinToneColor_34',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_36.SkinToneColor_36',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_37.SkinToneColor_37',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_38.SkinToneColor_38',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_39.SkinToneColor_39',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_40.SkinToneColor_40',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_41.SkinToneColor_41',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_42.SkinToneColor_42',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_43.SkinToneColor_43',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_44.SkinToneColor_44',
                },
        Customization.HAIR_HEADGEAR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_01.HeadAccessory_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_02.HeadAccessory_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_03.HeadAccessory_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_04.HeadAccessory_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_05.HeadAccessory_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_06.HeadAccessory_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_07.HeadAccessory_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_08.HeadAccessory_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_09.HeadAccessory_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_10.HeadAccessory_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_15.HeadAccessory_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_20.HeadAccessory_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_25.HeadAccessory_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_31.HeadAccessory_31',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_32.HeadAccessory_32',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_33.HeadAccessory_33',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_34.HeadAccessory_34',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_35.HeadAccessory_35',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_36.HeadAccessory_36',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HeadAccessories/HeadAccessory_37.HeadAccessory_37',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_38.HeadAccessory_38',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_39.HeadAccessory_39',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_40.HeadAccessory_40',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_41.HeadAccessory_41',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_42.HeadAccessory_42',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_43.HeadAccessory_43',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HeadAccessories/HeadAccessory_44.HeadAccessory_44',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_45.HeadAccessory_45',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_46.HeadAccessory_46',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_47.HeadAccessory_47',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_48.HeadAccessory_48',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_49.HeadAccessory_49',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_50.HeadAccessory_50',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HeadAccessories/HeadAccessory_51.HeadAccessory_51',
                },
        Customization.FACIAL_HAIR_MASKS: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_10.FaceAccessory_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_12.FaceAccessory_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_13.FaceAccessory_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_14.FaceAccessory_14',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/FaceAccessories/FaceAccessory_15.FaceAccessory_15',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/FaceAccessories/FaceAccessory_16.FaceAccessory_16',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/FaceAccessories/FaceAccessory_17.FaceAccessory_17',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/FaceAccessories/FaceAccessory_18.FaceAccessory_18',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/FaceAccessories/FaceAccessory_19.FaceAccessory_19',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/FaceAccessories/FaceAccessory_20.FaceAccessory_20',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/FaceAccessories/FaceAccessory_21.FaceAccessory_21',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/FaceAccessories/FaceAccessory_22.FaceAccessory_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/FaceAccessories/FaceAccessory_23.FaceAccessory_23',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/FaceAccessories/FaceAccessory_24.FaceAccessory_24',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/FaceAccessories/FaceAccessory_25.FaceAccessory_25',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/FaceAccessories/FaceAccessory_26.FaceAccessory_26',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/FaceAccessories/FaceAccessory_27.FaceAccessory_27',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/FaceAccessories/FaceAccessory_28.FaceAccessory_28',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/FaceAccessories/FaceAccessory_29.FaceAccessory_29',
                },
        Customization.HAIR_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_12.HairColor_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_14.HairColor_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_15.HairColor_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_16.HairColor_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_17.HairColor_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_19.HairColor_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_20.HairColor_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_21.HairColor_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_22.HairColor_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_23.HairColor_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_24.HairColor_24',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_25.HairColor_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_26.HairColor_26',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_28.HairColor_28',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_29.HairColor_29',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_31.HairColor_31',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_32.HairColor_32',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HairColor/HairColor_34.HairColor_34',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/HairColor/HairColor_35.HairColor_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HairColor/HairColor_37.HairColor_37',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/HairColor/HairColor_38.HairColor_38',
                },
        Customization.EAR_SHAPE: {
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_13.EarShape_13',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_14.EarShape_14',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EarShapes/EarShape_15.EarShape_15',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EarShapes/EarShape_16.EarShape_16',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EarShape/EarShape_17.EarShape_17',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EarShape/EarShape_18.EarShape_18',
                },
        Customization.NOSE_SHAPE: set(),
        Customization.MOUTH_SHAPE: set(),
        Customization.EYEBROW: set(),
        Customization.EYELASH: set(),
        Customization.EYE_SHAPE: set(),
        Customization.PUPIL: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_04.Pupil_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_05.Pupil_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_07.Pupil_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_09.Pupil_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_10.Pupil_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_11.Pupil_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_12.Pupil_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_13.Pupil_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_15.Pupil_15',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Pupils/Pupil_16.Pupil_16',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Pupils/Pupil_17.Pupil_17',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Pupils/Pupil_18.Pupil_18',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Pupils/Pupil_19.Pupil_19',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Pupils/Pupil_20.Pupil_20',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Pupils/Pupil_21.Pupil_21',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_03.Pupil_03',
                },
        Customization.EYE_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_05.EyeColor_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_06.EyeColor_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_08.EyeColor_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_09.EyeColor_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_10.EyeColor_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_11.EyeColor_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_12.EyeColor_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_14.EyeColor_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_15.EyeColor_15',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_17.EyeColor_17',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_18.EyeColor_18',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeColor/EyeColor_20.EyeColor_20',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeColor/EyeColor_21.EyeColor_21',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeColor/EyeColor_23.EyeColor_23',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeColor/EyeColor_24.EyeColor_24',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_16.EyeColor_16',
                },
        Customization.SCAR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_02.Scars_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_03.Scars_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_07.Scars_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_12.Scars_12',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Scars/Scars_18.Scars_18',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Scars/Scars_19.Scars_19',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Scars/Scars_20.Scars_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Scars/Scars_21.Scars_21',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Scars/Scars_22.Scars_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Scars/Scars_23.Scars_23',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Scars/Scars_24.Scars_24',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Scars/Scars_25.Scars_25',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Scars/Scars_26.Scars_26',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Scars/Scars_27.Scars_27',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Scars/Scars_28.Scars_28',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Scars/Scars_29.Scars_29',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Scars/Scars_30.Scars_30',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Scars/Scars_31.Scars_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Scars/Scars_32.Scars_32',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_17.Scars_17',
                },
        Customization.SCAR_FLIP: set(),
        Customization.TATTOO: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_01.Tattoos_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_02.Tattoos_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_03.Tattoos_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_04.Tattoos_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_05.Tattoos_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_09.Tattoos_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_10.Tattoos_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_11.Tattoos_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_12.Tattoos_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_13.Tattoos_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_15.Tattoos_15',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooShapes/Tattoos_17.Tattoos_17',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooShapes/Tattoos_18.Tattoos_18',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooShapes/Tattoos_19.Tattoos_19',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooShapes/Tattoos_20.Tattoos_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooShapes/Tattoos_21.Tattoos_21',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooShapes/Tattoos_22.Tattoos_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooShapes/Tattoos_23.Tattoos_23',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooShapes/Tattoos_24.Tattoos_24',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooShapes/Tattoos_25.Tattoos_25',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooShapes/Tattoos_26.Tattoos_26',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Tattoos/Tattoos_27.Tattoos_27',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Tattoos/Tattoos_28.Tattoos_28',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Tattoos/Tattoos_29.Tattoos_29',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Tattoos/Tattoos_30.Tattoos_30',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Tattoos/Tattoos_31.Tattoos_31',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_16.Tattoos_16',
                },
        Customization.TATTOO_FLIP: set(),
        Customization.TATTOO_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_15.TattooColor_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_16.TattooColor_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_17.TattooColor_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_18.TattooColor_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_19.TattooColor_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_20.TattooColor_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_21.TattooColor_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_22.TattooColor_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_23.TattooColor_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_25.TattooColor_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_26.TattooColor_26',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_28.TattooColor_28',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooColors/TattooColor_31.TattooColor_31',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/TattooColors/TattooColor_32.TattooColor_32',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooColor/TattooColor_34.TattooColor_34',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/TattooColor/TattooColor_35.TattooColor_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/TattooColor/TattooColor_37.TattooColor_37',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/TattooColor/TattooColor_38.TattooColor_38',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_30.TattooColor_30',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_29.TattooColor_29',
                },
        Customization.EYELINER: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_04.EyelinerShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_08.EyelinerShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_09.EyelinerShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_11.EyelinerShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_12.EyelinerShape_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_13.EyelinerShape_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_14.EyelinerShape_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_15.EyelinerShape_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_16.EyelinerShape_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_17.EyelinerShape_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_18.EyelinerShape_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_20.EyelinerShape_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyelinerShape/EyelinerShape_22.EyelinerShape_22',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyelinerShape/EyelinerShape_23.EyelinerShape_23',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyelinerShape/EyelinerShape_24.EyelinerShape_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyelinerShape/EyelinerShape_25.EyelinerShape_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyelinerShape/EyelinerShape_26.EyelinerShape_26',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeLinerShape/EyelinerShape_27.EyelinerShape_27',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeLinerShape/EyelinerShape_28.EyelinerShape_28',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeLinerShape/EyelinerShape_29.EyelinerShape_29',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeLinerShape/EyelinerShape_30.EyelinerShape_30',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeLinerShape/EyelinerShape_31.EyelinerShape_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Eyeliner/EyelinerShape_32.EyelinerShape_32',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Eyeliner/EyelinerShape_33.EyelinerShape_33',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Eyeliner/EyelinerShape_34.EyelinerShape_34',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Eyeliner/EyelinerShape_35.EyelinerShape_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Eyeliner/EyelinerShape_36.EyelinerShape_36',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_21.EyelinerShape_21',
                },
        Customization.EYELINER_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_15_Eyeliner.MakeupColor_15_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_16_Eyeliner.MakeupColor_16_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_17_Eyeliner.MakeupColor_17_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_18_Eyeliner.MakeupColor_18_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_19_Eyeliner.MakeupColor_19_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_20_Eyeliner.MakeupColor_20_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_21_Eyeliner.MakeupColor_21_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_22_Eyeliner.MakeupColor_22_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_23_Eyeliner.MakeupColor_23_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_25_Eyeliner.MakeupColor_25_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_26_Eyeliner.MakeupColor_26_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_28_Eyeliner.MakeupColor_28_Eyeliner',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_31_Eyeliner.MakeupColor_31_Eyeliner',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_32_Eyeliner.MakeupColor_32_Eyeliner',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_34_Eyeliner.MakeupColor_34_Eyeliner',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_35_Eyeliner.MakeupColor_35_Eyeliner',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_37_Eyeliner.MakeupColor_37_Eyeliner',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_38_Eyeliner.MakeupColor_38_Eyeliner',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_30_Eyeliner.MakeupColor_30_Eyeliner',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_29_Eyeliner.MakeupColor_29_Eyeliner',
                },
        Customization.EYESHADOW: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_07.EyeShadow_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_09.EyeShadow_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_10.EyeShadow_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_12.EyeShadow_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_13.EyeShadow_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_14.EyeShadow_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_15.EyeShadow_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_16.EyeShadow_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_17.EyeShadow_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_18.EyeShadow_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_19.EyeShadow_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_20.EyeShadow_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeShadowShape/EyeShadow_22.EyeShadow_22',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeShadowShape/EyeShadow_23.EyeShadow_23',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeShadowShape/EyeShadow_24.EyeShadow_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeShadowShape/EyeShadow_25.EyeShadow_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/EyeShadowShape/EyeShadow_26.EyeShadow_26',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeShadowShapes/EyeShadow_27.EyeShadow_27',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeShadowShapes/EyeShadow_28.EyeShadow_28',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeShadowShapes/EyeShadow_29.EyeShadow_29',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeShadowShapes/EyeShadow_30.EyeShadow_30',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/EyeShadowShapes/EyeShadow_31.EyeShadow_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeShadow/EyeShadow_32.EyeShadow_32',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeShadow/EyeShadow_33.EyeShadow_33',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeShadow/EyeShadow_34.EyeShadow_34',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeShadow/EyeShadow_35.EyeShadow_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/EyeShadow/EyeShadow_36.EyeShadow_36',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_30_Eyeshadow.MakeupColor_30_Eyeshadow',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_21.EyeShadow_21',
                },
        Customization.EYESHADOW_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_15_Eyeshadow.MakeupColor_15_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_16_Eyeshadow.MakeupColor_16_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_17_Eyeshadow.MakeupColor_17_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_18_Eyeshadow.MakeupColor_18_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_19_Eyeshadow.MakeupColor_19_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_20_Eyeshadow.MakeupColor_20_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_21_Eyeshadow.MakeupColor_21_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_22_Eyeshadow.MakeupColor_22_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_23_Eyeshadow.MakeupColor_23_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_25_Eyeshadow.MakeupColor_25_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_26_Eyeshadow.MakeupColor_26_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_28_Eyeshadow.MakeupColor_28_Eyeshadow',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_31_Eyeshadow.MakeupColor_31_Eyeshadow',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_32_Eyeshadow.MakeupColor_32_Eyeshadow',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_34_Eyeshadow.MakeupColor_34_Eyeshadow',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_35_Eyeshadow.MakeupColor_35_Eyeshadow',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_37_Eyeshadow.MakeupColor_37_Eyeshadow',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_38_Eyeshadow.MakeupColor_38_Eyeshadow',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_29_Eyeshadow.MakeupColor_29_Eyeshadow',
                },
        Customization.BLUSH: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_02.BlushShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_10.BlushShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_11.BlushShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_12.BlushShape_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_13.BlushShape_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_14.BlushShape_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_15.BlushShape_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_16.BlushShape_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_17.BlushShape_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_18.BlushShape_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_19.BlushShape_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_20.BlushShape_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/BlushShapes/BlushShape_22.BlushShape_22',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/BlushShapes/BlushShape_23.BlushShape_23',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/BlushShapes/BlushShape_24.BlushShape_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/BlushShapes/BlushShape_25.BlushShape_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/BlushShapes/BlushShape_26.BlushShape_26',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/BlushShapes/BlushShape_27.BlushShape_27',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/BlushShapes/BlushShape_28.BlushShape_28',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/BlushShapes/BlushShape_29.BlushShape_29',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/BlushShapes/BlushShape_30.BlushShape_30',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/BlushShapes/BlushShape_31.BlushShape_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Blush/BlushShape_32.BlushShape_32',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Blush/BlushShape_33.BlushShape_33',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Blush/BlushShape_34.BlushShape_34',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Blush/BlushShape_35.BlushShape_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Blush/BlushShape_36.BlushShape_36',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_21.BlushShape_21',
                },
        Customization.BLUSH_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_15_Blush.MakeupColor_15_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_16_Blush.MakeupColor_16_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_17_Blush.MakeupColor_17_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_18_Blush.MakeupColor_18_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_19_Blush.MakeupColor_19_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_20_Blush.MakeupColor_20_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_21_Blush.MakeupColor_21_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_22_Blush.MakeupColor_22_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_23_Blush.MakeupColor_23_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_25_Blush.MakeupColor_25_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_26_Blush.MakeupColor_26_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_28_Blush.MakeupColor_28_Blush',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_31_Blush.MakeupColor_31_Blush',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_32_Blush.MakeupColor_32_Blush',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_34_Blush.MakeupColor_34_Blush',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_35_Blush.MakeupColor_35_Blush',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_37_Blush.MakeupColor_37_Blush',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_38_Blush.MakeupColor_38_Blush',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_30_Blush.MakeupColor_30_Blush',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_29_Blush.MakeupColor_29_Blush',
                },
        Customization.LIPSTICK: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_06.Lipstick_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_07.Lipstick_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_08.Lipstick_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_10.Lipstick_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_11.Lipstick_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_12.Lipstick_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_13.Lipstick_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_14.Lipstick_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_15.Lipstick_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_16.Lipstick_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_17.Lipstick_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_18.Lipstick_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_19.Lipstick_19',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/LipstickStyle/Lipstick_22.Lipstick_22',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/LipstickStyle/Lipstick_23.Lipstick_23',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/LipstickStyle/Lipstick_24.Lipstick_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/LipstickStyle/Lipstick_25.Lipstick_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/LipstickStyle/Lipstick_26.Lipstick_26',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/LipstickStyle/Lipstick_27.Lipstick_27',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/LipstickStyle/Lipstick_28.Lipstick_28',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/LipstickStyle/Lipstick_29.Lipstick_29',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/LipstickStyle/Lipstick_30.Lipstick_30',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/LipstickStyle/Lipstick_31.Lipstick_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Lipstick/Lipstick_32.Lipstick_32',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Lipstick/Lipstick_33.Lipstick_33',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Lipstick/Lipstick_34.Lipstick_34',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Lipstick/Lipstick_35.Lipstick_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Lipstick/Lipstick_36.Lipstick_36',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_21.Lipstick_21',
                },
        Customization.LIPSTICK_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_15_Lipstick.MakeupColor_15_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_16_Lipstick.MakeupColor_16_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_17_Lipstick.MakeupColor_17_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_18_Lipstick.MakeupColor_18_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_19_Lipstick.MakeupColor_19_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_20_Lipstick.MakeupColor_20_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_21_Lipstick.MakeupColor_21_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_22_Lipstick.MakeupColor_22_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_23_Lipstick.MakeupColor_23_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_25_Lipstick.MakeupColor_25_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_26_Lipstick.MakeupColor_26_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_28_Lipstick.MakeupColor_28_Lipstick',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_31_Lipstick.MakeupColor_31_Lipstick',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/MakeupColor/MakeupColor_32_Lipstick.MakeupColor_32_Lipstick',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_34_Lipstick.MakeupColor_34_Lipstick',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/MakeupColor/MakeupColor_35_Lipstick.MakeupColor_35_Lipstick',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_37_Lipstick.MakeupColor_37_Lipstick',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/MakeupColor/MakeupColor_38_Lipstick.MakeupColor_38_Lipstick',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_30_Lipstick.MakeupColor_30_Lipstick',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_29_Lipstick.MakeupColor_29_Lipstick',
                },
        Customization.ARMOR_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_03.ArmorPattern_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_04.ArmorPattern_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_05.ArmorPattern_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_06.ArmorPattern_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_07.ArmorPattern_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_09.ArmorPattern_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_10.ArmorPattern_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_11.ArmorPattern_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_12.ArmorPattern_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_13.ArmorPattern_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_15.ArmorPattern_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_16.ArmorPattern_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_18.ArmorPattern_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_19.ArmorPattern_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_21.ArmorPattern_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_22.ArmorPattern_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_23.ArmorPattern_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_25.ArmorPattern_25',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorPatterns/ArmorPattern_27.ArmorPattern_27',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorPatterns/ArmorPattern_28.ArmorPattern_28',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorPatterns/ArmorPattern_29.ArmorPattern_29',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorPatterns/ArmorPattern_30.ArmorPattern_30',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorPattern/ArmorPattern_31.ArmorPattern_31',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorPattern/ArmorPattern_32.ArmorPattern_32',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_24.ArmorPattern_24',
                },
        Customization.UNDER_ARMOR_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_03.UnderArmorPattern_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_05.UnderArmorPattern_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_08.UnderArmorPattern_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_10.UnderArmorPattern_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_11.UnderArmorPattern_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_12.UnderArmorPattern_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_17.UnderArmorPattern_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_18.UnderArmorPattern_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_19.UnderArmorPattern_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_20.UnderArmorPattern_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_21.UnderArmorPattern_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_22.UnderArmorPattern_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_23.UnderArmorPattern_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_24.UnderArmorPattern_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/UnderArmorPatterns/UnderArmorPattern_27.UnderArmorPattern_27',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/UnderArmorPatterns/UnderArmorPattern_28.UnderArmorPattern_28',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/UnderArmorPattern/UnderArmorPattern_29.UnderArmorPattern_29',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_14.UnderArmorPattern_14',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_13.UnderArmorPattern_13',
                },
        Customization.ARMOR_COLOR_PRIMARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_18_Primary.ArmorColor_18_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_19_Primary.ArmorColor_19_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_20_Primary.ArmorColor_20_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_21_Primary.ArmorColor_21_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_22_Primary.ArmorColor_22_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_23_Primary.ArmorColor_23_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_24_Primary.ArmorColor_24_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_25_Primary.ArmorColor_25_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_26_Primary.ArmorColor_26_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_27_Primary.ArmorColor_27_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_28_Primary.ArmorColor_28_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_29_Primary.ArmorColor_29_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_30_Primary.ArmorColor_30_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_31_Primary.ArmorColor_31_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_32_Primary.ArmorColor_32_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_33_Primary.ArmorColor_33_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_34_Primary.ArmorColor_34_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_35_Primary.ArmorColor_35_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_36_Primary.ArmorColor_36_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_37_Primary.ArmorColor_37_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_38_Primary.ArmorColor_38_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_39_Primary.ArmorColor_39_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_40_Primary.ArmorColor_40_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_41_Primary.ArmorColor_41_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_42_Primary.ArmorColor_42_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_43_Primary.ArmorColor_43_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_44_Primary.ArmorColor_44_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_45_Primary.ArmorColor_45_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_46_Primary.ArmorColor_46_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_47_Primary.ArmorColor_47_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_48_Primary.ArmorColor_48_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_49_Primary.ArmorColor_49_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_50_Primary.ArmorColor_50_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_51_Primary.ArmorColor_51_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_52_Primary.ArmorColor_52_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_53_Primary.ArmorColor_53_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_54_Primary.ArmorColor_54_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_55_Primary.ArmorColor_55_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_56_Primary.ArmorColor_56_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_57_Primary.ArmorColor_57_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_58_Primary.ArmorColor_58_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_59_Primary.ArmorColor_59_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_60_Primary.ArmorColor_60_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_61_Primary.ArmorColor_61_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_62_Primary.ArmorColor_62_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_71_Primary.ArmorColor_71_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_72_Primary.ArmorColor_72_Primary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_74_Primary.ArmorColor_74_Primary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_75_Primary.ArmorColor_75_Primary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_76_Primary.ArmorColor_76_Primary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_77_Primary.ArmorColor_77_Primary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_79_Primary.ArmorColor_79_Primary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_80_Primary.ArmorColor_80_Primary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_81_Primary.ArmorColor_81_Primary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_82_Primary.ArmorColor_82_Primary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_84_Primary.ArmorColor_84_Primary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_85_Primary.ArmorColor_85_Primary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_86_Primary.ArmorColor_86_Primary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_87_Primary.ArmorColor_87_Primary',
                # Assigned as part of the Butt Stallion Pack, but does *not* actually show up automatically!
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_63_Primary.ArmorColor_63_Primary',
                # Shows up automatically - Preorder Bonus (Gold armor)
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_69_Primary.ArmorColor_69_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_70_Primary.ArmorColor_70_Primary',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_66_Primary.ArmorColor_66_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_67_Primary.ArmorColor_67_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_68_Primary.ArmorColor_68_Primary',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_64_Primary.ArmorColor_64_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_65_Primary.ArmorColor_65_Primary',
                },
        Customization.ARMOR_COLOR_SECONDARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_18_Secondary.ArmorColor_18_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_19_Secondary.ArmorColor_19_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_20_Secondary.ArmorColor_20_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_21_Secondary.ArmorColor_21_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_22_Secondary.ArmorColor_22_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_23_Secondary.ArmorColor_23_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_24_Secondary.ArmorColor_24_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_25_Secondary.ArmorColor_25_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_26_Secondary.ArmorColor_26_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_27_Secondary.ArmorColor_27_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_28_Secondary.ArmorColor_28_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_29_Secondary.ArmorColor_29_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_30_Secondary.ArmorColor_30_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_31_Secondary.ArmorColor_31_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_32_Secondary.ArmorColor_32_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_33_Secondary.ArmorColor_33_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_34_Secondary.ArmorColor_34_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_35_Secondary.ArmorColor_35_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_36_Secondary.ArmorColor_36_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_37_Secondary.ArmorColor_37_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_38_Secondary.ArmorColor_38_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_39_Secondary.ArmorColor_39_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_40_Secondary.ArmorColor_40_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_41_Secondary.ArmorColor_41_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_42_Secondary.ArmorColor_42_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_43_Secondary.ArmorColor_43_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_44_Secondary.ArmorColor_44_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_45_Secondary.ArmorColor_45_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_46_Secondary.ArmorColor_46_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_47_Secondary.ArmorColor_47_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_48_Secondary.ArmorColor_48_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_49_Secondary.ArmorColor_49_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_50_Secondary.ArmorColor_50_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_51_Secondary.ArmorColor_51_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_52_Secondary.ArmorColor_52_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_53_Secondary.ArmorColor_53_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_54_Secondary.ArmorColor_54_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_55_Secondary.ArmorColor_55_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_56_Secondary.ArmorColor_56_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_57_Secondary.ArmorColor_57_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_58_Secondary.ArmorColor_58_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_59_Secondary.ArmorColor_59_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_60_Secondary.ArmorColor_60_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_61_Secondary.ArmorColor_61_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_62_Secondary.ArmorColor_62_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_71_Secondary.ArmorColor_71_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_72_Secondary.ArmorColor_72_Secondary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_74_Secondary.ArmorColor_74_Secondary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_75_Secondary.ArmorColor_75_Secondary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_76_Secondary.ArmorColor_76_Secondary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_77_Secondary.ArmorColor_77_Secondary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_79_Secondary.ArmorColor_79_Secondary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_80_Secondary.ArmorColor_80_Secondary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_81_Secondary.ArmorColor_81_Secondary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_82_Secondary.ArmorColor_82_Secondary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_84_Secondary.ArmorColor_84_Secondary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_85_Secondary.ArmorColor_85_Secondary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_86_Secondary.ArmorColor_86_Secondary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_87_Secondary.ArmorColor_87_Secondary',
                # Assigned as part of the Butt Stallion Pack, but does *not* actually show up automatically!
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_63_Secondary.ArmorColor_63_Secondary',
                # Shows up automatically - Preorder Bonus (Gold armor)
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_69_Secondary.ArmorColor_69_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_69_Tertiary.ArmorColor_69_Tertiary',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_66_Secondary.ArmorColor_66_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_67_Secondary.ArmorColor_67_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_68_Secondary.ArmorColor_68_Secondary',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_64_Secondary.ArmorColor_64_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_65_Secondary.ArmorColor_65_Secondary',
                },
        Customization.ARMOR_COLOR_TERTIARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_18_Tertiary.ArmorColor_18_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_19_Tertiary.ArmorColor_19_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_20_Tertiary.ArmorColor_20_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_21_Tertiary.ArmorColor_21_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_22_Tertiary.ArmorColor_22_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_23_Tertiary.ArmorColor_23_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_24_Tertiary.ArmorColor_24_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_25_Tertiary.ArmorColor_25_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_26_Tertiary.ArmorColor_26_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_27_Tertiary.ArmorColor_27_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_28_Tertiary.ArmorColor_28_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_29_Tertiary.ArmorColor_29_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_30_Tertiary.ArmorColor_30_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_31_Tertiary.ArmorColor_31_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_32_Tertiary.ArmorColor_32_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_33_Tertiary.ArmorColor_33_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_34_Tertiary.ArmorColor_34_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_35_Tertiary.ArmorColor_35_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_36_Tertiary.ArmorColor_36_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_37_Tertiary.ArmorColor_37_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_38_Tertiary.ArmorColor_38_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_39_Tertiary.ArmorColor_39_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_40_Tertiary.ArmorColor_40_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_41_Tertiary.ArmorColor_41_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_42_Tertiary.ArmorColor_42_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_43_Tertiary.ArmorColor_43_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_44_Tertiary.ArmorColor_44_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_45_Tertiary.ArmorColor_45_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_46_Tertiary.ArmorColor_46_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_47_Tertiary.ArmorColor_47_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_48_Tertiary.ArmorColor_48_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_49_Tertiary.ArmorColor_49_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_50_Tertiary.ArmorColor_50_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_51_Tertiary.ArmorColor_51_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_52_Tertiary.ArmorColor_52_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_53_Tertiary.ArmorColor_53_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_54_Tertiary.ArmorColor_54_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_55_Tertiary.ArmorColor_55_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_56_Tertiary.ArmorColor_56_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_57_Tertiary.ArmorColor_57_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_58_Tertiary.ArmorColor_58_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_59_Tertiary.ArmorColor_59_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_60_Tertiary.ArmorColor_60_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_61_Tertiary.ArmorColor_61_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_62_Tertiary.ArmorColor_62_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_71_Tertiary.ArmorColor_71_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_72_Tertiary.ArmorColor_72_Tertiary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_74_Tertiary.ArmorColor_74_Tertiary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_75_Tertiary.ArmorColor_75_Tertiary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_76_Tertiary.ArmorColor_76_Tertiary',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/ArmorColor/ArmorColor_77_Tertiary.ArmorColor_77_Tertiary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_79_Tertiary.ArmorColor_79_Tertiary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_80_Tertiary.ArmorColor_80_Tertiary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_81_Tertiary.ArmorColor_81_Tertiary',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/ArmorColor/ArmorColor_82_Tertiary.ArmorColor_82_Tertiary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_84_Tertiary.ArmorColor_84_Tertiary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_85_Tertiary.ArmorColor_85_Tertiary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_86_Tertiary.ArmorColor_86_Tertiary',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/ArmorColor/ArmorColor_87_Tertiary.ArmorColor_87_Tertiary',
                # Assigned as part of the Butt Stallion Pack, but does *not* actually show up automatically!
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_63_Tertiary.ArmorColor_63_Tertiary',
                # Shows up automatically - Preorder Bonus (Gold armor)
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_70_Secondary.ArmorColor_70_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_70_Tertiary.ArmorColor_70_Tertiary',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_66_Tertiary.ArmorColor_66_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_67_Tertiary.ArmorColor_67_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_68_Tertiary.ArmorColor_68_Tertiary',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_64_Tertiary.ArmorColor_64_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_65_Tertiary.ArmorColor_65_Tertiary',
                },
        Customization.EMOTE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_01.Emote_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_02.Emote_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_03.Emote_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_04.Emote_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_05.Emote_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_06.Emote_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_08.Emote_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_12.Emote_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_13.Emote_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_14.Emote_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_15.Emote_15',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_16.Emote_16',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_17.Emote_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_18.Emote_18',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Emotes/Emote_19.Emote_19',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Emotes/Emote_20.Emote_20',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Emote/Emote_21.Emote_21',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Emote/Emote_22.Emote_22',
                },
        Customization.BANNER_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_02.BannerShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_04.BannerShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_05.BannerShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_07.BannerShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_08.BannerShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_09.BannerShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_10.BannerShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_11.BannerShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_13.BannerShape_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_16.BannerShape_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_17.BannerShape_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_18.BannerShape_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_19.BannerShape_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_20.BannerShape_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Shape_21.Banner_Shape_21',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Shape_22.Banner_Shape_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Shape_23.Banner_Shape_23',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Shape_24.Banner_Shape_24',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Shape_25.Banner_Shape_25',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Shape_26.Banner_Shape_26',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_14.BannerShape_14',
                },
        Customization.BANNER_SHAPE_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_09_Shape.BannerColor_09_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_10_Shape.BannerColor_10_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_11_Shape.BannerColor_11_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_12_Shape.BannerColor_12_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_13_Shape.BannerColor_13_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_14_Shape.BannerColor_14_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_15_Shape.BannerColor_15_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_16_Shape.BannerColor_16_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_17_Shape.BannerColor_17_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_18_Shape.BannerColor_18_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_19_Shape.BannerColor_19_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_20_Shape.BannerColor_20_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_21_Shape.BannerColor_21_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_22_Shape.BannerColor_22_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_23_Shape.BannerColor_23_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_24_Shape.BannerColor_24_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_25_Shape.BannerColor_25_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_26_Shape.BannerColor_26_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_27_Shape.BannerColor_27_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_28_Shape.BannerColor_28_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_32_Shape.BannerColor_32_Shape',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Shape_33.BannerColor_Shape_33',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Shape_34.BannerColor_Shape_34',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Shape_35.BannerColor_Shape_35',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_36_Shape.BannerColor_36_Shape',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_37_Shape.BannerColor_37_Shape',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_38_Shape.BannerColor_38_Shape',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_39_Shape.BannerColor_39_Shape',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_40_Shape.BannerColor_40_Shape',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_41_Shape.BannerColor_41_Shape',
                # Shows up automatically, apparently - Vault-symbol related stuff
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_31_Shape.BannerColor_31_Shape',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_29_Shape.BannerColor_29_Shape',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_30_Shape.BannerColor_30_Shape',
                },
        Customization.BANNER_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_03.BannerPattern_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_04.BannerPattern_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_05.BannerPattern_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_06.BannerPattern_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_07.BannerPattern_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_08.BannerPattern_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_09.BannerPattern_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_10.BannerPattern_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_11.BannerPattern_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_12.BannerPattern_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_13.BannerPattern_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_14.BannerPattern_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_15.BannerPattern_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_18.BannerPattern_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_19.BannerPattern_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_20.BannerPattern_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_21.BannerPattern_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_22.BannerPattern_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_23.BannerPattern_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_24.BannerPattern_24',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Pattern_28.Banner_Pattern_28',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Pattern_29.Banner_Pattern_29',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Pattern_30.Banner_Pattern_30',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Pattern_31.Banner_Pattern_31',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Pattern_32.Banner_Pattern_32',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Pattern_33.Banner_Pattern_33',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Pattern_34.Banner_Pattern_34',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Pattern_35.Banner_Pattern_35',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Pattern_36.Banner_Pattern_36',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Pattern_37.Banner_Pattern_37',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Pattern_38.Banner_Pattern_38',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Pattern_39.Banner_Pattern_39',
                # Shows up automatically, apparently - Vault-symbol related stuff
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_26.BannerPattern_26',
                },
        Customization.BANNER_PATTERN_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_09_Pattern.BannerColor_09_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_10_Pattern.BannerColor_10_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_11_Pattern.BannerColor_11_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_12_Pattern.BannerColor_12_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_13_Pattern.BannerColor_13_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_14_Pattern.BannerColor_14_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_15_Pattern.BannerColor_15_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_16_Pattern.BannerColor_16_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_17_Pattern.BannerColor_17_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_18_Pattern.BannerColor_18_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_19_Pattern.BannerColor_19_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_20_Pattern.BannerColor_20_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_21_Pattern.BannerColor_21_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_22_Pattern.BannerColor_22_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_23_Pattern.BannerColor_23_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_24_Pattern.BannerColor_24_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_25_Pattern.BannerColor_25_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_26_Pattern.BannerColor_26_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_27_Pattern.BannerColor_27_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_28_Pattern.BannerColor_28_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_32_Pattern.BannerColor_32_Pattern',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Pattern_33.BannerColor_Pattern_33',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Pattern_34.BannerColor_Pattern_34',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Pattern_35.BannerColor_Pattern_35',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_36_Pattern.BannerColor_36_Pattern',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_37_Pattern.BannerColor_37_Pattern',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_38_Pattern.BannerColor_38_Pattern',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_39_Pattern.BannerColor_39_Pattern',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_40_Pattern.BannerColor_40_Pattern',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_41_Pattern.BannerColor_41_Pattern',
                # Shows up automatically, apparently - Vault-symbol related stuff
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_31_Pattern.BannerColor_31_Pattern',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_29_Pattern.BannerColor_29_Pattern',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_30_Pattern.BannerColor_30_Pattern',
                },
        Customization.BANNER_ICON: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_01.BannerIcon_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_03.BannerIcon_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_04.BannerIcon_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_06.BannerIcon_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_07.BannerIcon_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_08.BannerIcon_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_09.BannerIcon_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_10.BannerIcon_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_12.BannerIcon_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_13.BannerIcon_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_14.BannerIcon_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_15.BannerIcon_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_16.BannerIcon_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_25.BannerIcon_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_26.BannerIcon_26',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_27.BannerIcon_27',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_28.BannerIcon_28',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_31.BannerIcon_31',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_32.BannerIcon_32',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_33.BannerIcon_33',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_34.BannerIcon_34',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_35.BannerIcon_35',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_36.BannerIcon_36',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_37.BannerIcon_37',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_38.BannerIcon_38',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_39.BannerIcon_39',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_41.BannerIcon_41',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_43.Banner_Icon_43',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_44.Banner_Icon_44',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_45.Banner_Icon_45',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_46.Banner_Icon_46',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_47.Banner_Icon_47',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/Banner_Icon_48.Banner_Icon_48',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_49.Banner_Icon_49',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_50.Banner_Icon_50',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_51.Banner_Icon_51',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_52.Banner_Icon_52',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_53.Banner_Icon_53',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/Banner_Icon_54.Banner_Icon_54',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_55.Banner_Icon_55',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_56.Banner_Icon_56',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_57.Banner_Icon_57',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_58.Banner_Icon_58',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_59.Banner_Icon_59',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/Banner_Icon_60.Banner_Icon_60',
                # Shows up automatically, apparently - Vault-symbol related stuff
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_40.BannerIcon_40',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_30.BannerIcon_30',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_29.BannerIcon_29',
                },
        Customization.BANNER_ICON_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_09_Icon.BannerColor_09_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_10_Icon.BannerColor_10_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_11_Icon.BannerColor_11_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_12_Icon.BannerColor_12_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_13_Icon.BannerColor_13_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_14_Icon.BannerColor_14_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_15_Icon.BannerColor_15_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_16_Icon.BannerColor_16_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_17_Icon.BannerColor_17_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_18_Icon.BannerColor_18_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_19_Icon.BannerColor_19_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_20_Icon.BannerColor_20_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_21_Icon.BannerColor_21_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_22_Icon.BannerColor_22_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_23_Icon.BannerColor_23_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_24_Icon.BannerColor_24_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_25_Icon.BannerColor_25_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_26_Icon.BannerColor_26_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_27_Icon.BannerColor_27_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_28_Icon.BannerColor_28_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_32_Icon.BannerColor_32_Icon',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Icon_33.BannerColor_Icon_33',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Icon_34.BannerColor_Icon_34',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Banners/BannerColor_Icon_35.BannerColor_Icon_35',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_36_Icon.BannerColor_36_Icon',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_37_Icon.BannerColor_37_Icon',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Banners/BannerColor_38_Icon.BannerColor_38_Icon',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_39_Icon.BannerColor_39_Icon',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_40_Icon.BannerColor_40_Icon',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Banners/BannerColor_41_Icon.BannerColor_41_Icon',
                # Shows up automatically, apparently - Vault-symbol related stuff
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_31_Icon.BannerColor_31_Icon',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_29_Icon.BannerColor_29_Icon',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_30_Icon.BannerColor_30_Icon',
                },
        Customization.STATUE_MATERIAL: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_03.HeroStatueMaterial_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_05.HeroStatueMaterial_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_06.HeroStatueMaterial_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_07.HeroStatueMaterial_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_08.HeroStatueMaterial_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_09.HeroStatueMaterial_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_10.HeroStatueMaterial_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_11.HeroStatueMaterial_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_12.HeroStatueMaterial_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_14.HeroStatueMaterial_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_15.HeroStatueMaterial_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_16.HeroStatueMaterial_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_18.HeroStatueMaterial_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_19.HeroStatueMaterial_19',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Statues/Materials/HeroStatueMaterial_22.HeroStatueMaterial_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Statues/Materials/HeroStatueMaterial_23.HeroStatueMaterial_23',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Statues/Materials/HeroStatueMaterial_24.HeroStatueMaterial_24',
                # Shows up automatically - Dragon Lord Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_20.HeroStatueMaterial_20',
                # Shows up automatically - Butt Stallion Pack
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_21.HeroStatueMaterial_21',
                },
        Customization.STATUE_POSE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_01.HeroStatuePose_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_02.HeroStatuePose_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_04.HeroStatuePose_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_05.HeroStatuePose_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_06.HeroStatuePose_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_08.HeroStatuePose_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_10.HeroStatuePose_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_11.HeroStatuePose_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_12.HeroStatuePose_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_13.HeroStatuePose_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_14.HeroStatuePose_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_15.HeroStatuePose_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_17.HeroStatuePose_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_18.HeroStatuePose_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_19.HeroStatuePose_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_20.HeroStatuePose_20',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Statues/Poses/HeroStatuePose_21.HeroStatuePose_21',
                '/Game/PatchDLC/Indigo1/PlayerCharacters/_Shared/_Design/Customization/Statues/Poses/HeroStatuePose_22.HeroStatuePose_22',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Statues/Poses/HeroStatuePose_23.HeroStatuePose_23',
                '/Game/PatchDLC/Indigo2/PlayerCharacters/_Shared/_Design/Statues/Poses/HeroStatuePose_24.HeroStatuePose_24',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Statues/Poses/HeroStatuePose_25.HeroStatuePose_25',
                '/Game/PatchDLC/Indigo3/PlayerCharacters/_Shared/Design/Customization/Statues/Poses/HeroStatuePose_26.HeroStatuePose_26',
                },
        }

# For ease of use, a few transformations on the above dict
profile_customizations_to_type = {}
profile_customizations = set()
for cust_type, cust_set in profile_customizations_by_cat.items():
    profile_customizations |= cust_set
    for cust in cust_set:
        profile_customizations_to_type[cust] = cust_type

# "Default" customizations which are available via the GUI but which don't
# actually show up in the customiztaion unlock list.  We want to include
# these as part of the unlocked-cosmetic count, but don't want to inject
# them into that list.
profile_customizations_defaults_by_cat = {
        Customization.BODY_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Body/BodyShape_01.BodyShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Body/BodyShape_02.BodyShape_02',
                },
        Customization.HEAD_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_01.HeadType_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_02.HeadType_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_03.HeadType_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_04.HeadType_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_05.HeadType_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_06.HeadType_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_07.HeadType_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_08.HeadType_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_09.HeadType_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_10.HeadType_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Head/HeadType_11.HeadType_11',
                },
        Customization.SKIN_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_01.SkinToneColor_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_02.SkinToneColor_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_03.SkinToneColor_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_04.SkinToneColor_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_05.SkinToneColor_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_06.SkinToneColor_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_07.SkinToneColor_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_08.SkinToneColor_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_09.SkinToneColor_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_10.SkinToneColor_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_11.SkinToneColor_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_12.SkinToneColor_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_13.SkinToneColor_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_14.SkinToneColor_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_15.SkinToneColor_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_17.SkinToneColor_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_18.SkinToneColor_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_19.SkinToneColor_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_20.SkinToneColor_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_21.SkinToneColor_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_22.SkinToneColor_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_23.SkinToneColor_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_24.SkinToneColor_24',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_25.SkinToneColor_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/SkinTone/SkinToneColor_31.SkinToneColor_31',
                },
        Customization.HAIR_HEADGEAR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_00.HeadAccessory_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_11.HeadAccessory_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_12.HeadAccessory_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_13.HeadAccessory_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_14.HeadAccessory_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_16.HeadAccessory_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_17.HeadAccessory_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_18.HeadAccessory_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_19.HeadAccessory_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_21.HeadAccessory_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_22.HeadAccessory_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_23.HeadAccessory_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_24.HeadAccessory_24',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeadAcc/HeadAccessory_30.HeadAccessory_30',
                },
        Customization.FACIAL_HAIR_MASKS: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_00.FaceAccessory_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_01.FaceAccessory_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_02.FaceAccessory_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_03.FaceAccessory_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_04.FaceAccessory_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_05.FaceAccessory_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_06.FaceAccessory_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_07.FaceAccessory_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_08.FaceAccessory_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_09.FaceAccessory_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/FaceAcc/FaceAccessory_11.FaceAccessory_11',
                },
        Customization.HAIR_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_01.HairColor_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_02.HairColor_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_03.HairColor_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_04.HairColor_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_05.HairColor_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_06.HairColor_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_07.HairColor_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_08.HairColor_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_09.HairColor_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_10.HairColor_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_11.HairColor_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_13.HairColor_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_18.HairColor_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_27.HairColor_27',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HairColor/HairColor_30.HairColor_30',
                },
        Customization.EAR_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_01.EarShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_02.EarShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_03.EarShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_04.EarShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_05.EarShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_06.EarShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_07.EarShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_08.EarShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_09.EarShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_10.EarShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_11.EarShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EarShape/EarShape_12.EarShape_12',
                },
        Customization.NOSE_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_01.NoseShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_02.NoseShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_03.NoseShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_04.NoseShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_05.NoseShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_06.NoseShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_07.NoseShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_08.NoseShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_09.NoseShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_10.NoseShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_11.NoseShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_12.NoseShape_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_13.NoseShape_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_14.NoseShape_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_15.NoseShape_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_16.NoseShape_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/NoseShape/NoseShape_17.NoseShape_17',
                },
        Customization.MOUTH_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_01.MouthShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_02.MouthShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_03.MouthShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_04.MouthShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_05.MouthShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_06.MouthShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_07.MouthShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_08.MouthShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_09.MouthShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_10.MouthShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_11.MouthShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/MouthShape/MouthShape_12.MouthShape_12',
                },
        Customization.EYEBROW: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_00.Eyebrows_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_01.Eyebrows_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_02.Eyebrows_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_03.Eyebrows_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_04.Eyebrows_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_05.Eyebrows_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_06.Eyebrows_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_07.Eyebrows_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_08.Eyebrows_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_09.Eyebrows_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyebrows/Eyebrows_10.Eyebrows_10',
                },
        Customization.EYELASH: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyelashes/Eyelashes_00.Eyelashes_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyelashes/Eyelashes_01.Eyelashes_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Eyelashes/Eyelashes_02.Eyelashes_02',
                },
        Customization.EYE_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_01.EyeShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_02.EyeShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_03.EyeShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_04.EyeShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_05.EyeShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_06.EyeShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_07.EyeShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_08.EyeShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_09.EyeShape_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_10.EyeShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_11.EyeShape_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_12.EyeShape_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_13.EyeShape_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_14.EyeShape_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_15.EyeShape_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_16.EyeShape_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeShape/EyeShape_17.EyeShape_17',
                },
        Customization.PUPIL: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_00.Pupil_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_01.Pupil_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_02.Pupil_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_06.Pupil_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_08.Pupil_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/PupilShape/Pupil_14.Pupil_14',
                },
        Customization.EYE_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_01.EyeColor_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_02.EyeColor_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_03.EyeColor_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_04.EyeColor_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_07.EyeColor_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/EyeColor/EyeColor_13.EyeColor_13',
                },
        Customization.SCAR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_00.Scars_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_01.Scars_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_04.Scars_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_05.Scars_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_06.Scars_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_08.Scars_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_09.Scars_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_10.Scars_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_13.Scars_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_14.Scars_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_15.Scars_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/Scars_16.Scars_16',
                },
        Customization.SCAR_FLIP: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/ScarFlip_00.ScarFlip_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Scar/ScarFlip_01.ScarFlip_01',
                },
        Customization.TATTOO: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_00.Tattoos_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_06.Tattoos_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_07.Tattoos_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_08.Tattoos_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/Tattoos_14.Tattoos_14',
                },
        Customization.TATTOO_FLIP: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/TattooFlip_00.TattooFlip_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Tattoo/TattooFlip_01.TattooFlip_01',
                },
        Customization.TATTOO_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_01.TattooColor_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_02.TattooColor_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_03.TattooColor_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_04.TattooColor_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_05.TattooColor_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_06.TattooColor_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_07.TattooColor_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_08.TattooColor_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_09.TattooColor_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_10.TattooColor_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_11.TattooColor_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_12.TattooColor_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_13.TattooColor_13',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_14.TattooColor_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_24.TattooColor_24',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/TattooColor/TattooColor_27.TattooColor_27',
                },
        Customization.EYELINER: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_00.EyelinerShape_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_01.EyelinerShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_02.EyelinerShape_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_03.EyelinerShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_05.EyelinerShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_06.EyelinerShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_07.EyelinerShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_10.EyelinerShape_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLiner/EyelinerShape_19.EyelinerShape_19',
                },
        Customization.EYELINER_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_01_Eyeliner.MakeupColor_01_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_02_Eyeliner.MakeupColor_02_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_03_Eyeliner.MakeupColor_03_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_04_Eyeliner.MakeupColor_04_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_05_Eyeliner.MakeupColor_05_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_06_Eyeliner.MakeupColor_06_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_07_Eyeliner.MakeupColor_07_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_08_Eyeliner.MakeupColor_08_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_09_Eyeliner.MakeupColor_09_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_10_Eyeliner.MakeupColor_10_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_11_Eyeliner.MakeupColor_11_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_12_Eyeliner.MakeupColor_12_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_13_Eyeliner.MakeupColor_13_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_14_Eyeliner.MakeupColor_14_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_24_Eyeliner.MakeupColor_24_Eyeliner',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeLinerColor/MakeupColor_27_Eyeliner.MakeupColor_27_Eyeliner',
                },
        Customization.EYESHADOW: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_00.EyeShadow_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_01.EyeShadow_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_02.EyeShadow_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_03.EyeShadow_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_04.EyeShadow_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_05.EyeShadow_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_06.EyeShadow_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_08.EyeShadow_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadow/EyeShadow_11.EyeShadow_11',
                },
        Customization.EYESHADOW_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_01_Eyeshadow.MakeupColor_01_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_02_Eyeshadow.MakeupColor_02_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_03_Eyeshadow.MakeupColor_03_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_04_Eyeshadow.MakeupColor_04_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_05_Eyeshadow.MakeupColor_05_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_06_Eyeshadow.MakeupColor_06_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_07_Eyeshadow.MakeupColor_07_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_08_Eyeshadow.MakeupColor_08_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_09_Eyeshadow.MakeupColor_09_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_10_Eyeshadow.MakeupColor_10_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_11_Eyeshadow.MakeupColor_11_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_12_Eyeshadow.MakeupColor_12_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_13_Eyeshadow.MakeupColor_13_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_14_Eyeshadow.MakeupColor_14_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_24_Eyeshadow.MakeupColor_24_Eyeshadow',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/EyeShadowColor/MakeupColor_27_Eyeshadow.MakeupColor_27_Eyeshadow',
                },
        Customization.BLUSH: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_00.BlushShape_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_01.BlushShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_03.BlushShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_04.BlushShape_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_05.BlushShape_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_06.BlushShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_07.BlushShape_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_08.BlushShape_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Blush/BlushShape_09.BlushShape_09',
                },
        Customization.BLUSH_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_01_Blush.MakeupColor_01_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_02_Blush.MakeupColor_02_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_03_Blush.MakeupColor_03_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_04_Blush.MakeupColor_04_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_05_Blush.MakeupColor_05_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_06_Blush.MakeupColor_06_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_07_Blush.MakeupColor_07_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_08_Blush.MakeupColor_08_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_09_Blush.MakeupColor_09_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_10_Blush.MakeupColor_10_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_11_Blush.MakeupColor_11_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_12_Blush.MakeupColor_12_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_13_Blush.MakeupColor_13_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_14_Blush.MakeupColor_14_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_24_Blush.MakeupColor_24_Blush',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/BlushColor/MakeupColor_27_Blush.MakeupColor_27_Blush',
                },
        Customization.LIPSTICK: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_00.Lipstick_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_01.Lipstick_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_02.Lipstick_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_03.Lipstick_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_04.Lipstick_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_05.Lipstick_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_09.Lipstick_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/Lipstick/Lipstick_20.Lipstick_20',
                },
        Customization.LIPSTICK_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_01_Lipstick.MakeupColor_01_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_02_Lipstick.MakeupColor_02_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_03_Lipstick.MakeupColor_03_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_04_Lipstick.MakeupColor_04_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_05_Lipstick.MakeupColor_05_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_06_Lipstick.MakeupColor_06_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_07_Lipstick.MakeupColor_07_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_08_Lipstick.MakeupColor_08_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_09_Lipstick.MakeupColor_09_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_10_Lipstick.MakeupColor_10_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_11_Lipstick.MakeupColor_11_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_12_Lipstick.MakeupColor_12_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_13_Lipstick.MakeupColor_13_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_14_Lipstick.MakeupColor_14_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_24_Lipstick.MakeupColor_24_Lipstick',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Makeup/LipstickColor/MakeupColor_27_Lipstick.MakeupColor_27_Lipstick',
                },
        Customization.ARMOR_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_00.ArmorPattern_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_01.ArmorPattern_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_02.ArmorPattern_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_08.ArmorPattern_08',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_14.ArmorPattern_14',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_17.ArmorPattern_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_20.ArmorPattern_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/Pattern/ArmorPattern_26.ArmorPattern_26',
                },
        Customization.UNDER_ARMOR_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_00.UnderArmorPattern_00',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_01.UnderArmorPattern_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_02.UnderArmorPattern_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_06.UnderArmorPattern_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_07.UnderArmorPattern_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_09.UnderArmorPattern_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_15.UnderArmorPattern_15',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_16.UnderArmorPattern_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_25.UnderArmorPattern_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/UnderPattern/UnderArmorPattern_26.UnderArmorPattern_26',
                },
        Customization.ARMOR_COLOR_PRIMARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_01_Primary.ArmorColor_01_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_02_Primary.ArmorColor_02_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_03_Primary.ArmorColor_03_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_04_Primary.ArmorColor_04_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_05_Primary.ArmorColor_05_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_06_Primary.ArmorColor_06_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_07_Primary.ArmorColor_07_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_08_Primary.ArmorColor_08_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_09_Primary.ArmorColor_09_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_10_Primary.ArmorColor_10_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_11_Primary.ArmorColor_11_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_12_Primary.ArmorColor_12_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_13_Primary.ArmorColor_13_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_14_Primary.ArmorColor_14_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_15_Primary.ArmorColor_15_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_16_Primary.ArmorColor_16_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_17_Primary.ArmorColor_17_Primary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorPrimary/ArmorColor_73_Primary.ArmorColor_73_Primary',
                },
        Customization.ARMOR_COLOR_SECONDARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_01_Secondary.ArmorColor_01_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_02_Secondary.ArmorColor_02_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_03_Secondary.ArmorColor_03_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_04_Secondary.ArmorColor_04_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_05_Secondary.ArmorColor_05_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_06_Secondary.ArmorColor_06_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_07_Secondary.ArmorColor_07_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_08_Secondary.ArmorColor_08_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_09_Secondary.ArmorColor_09_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_10_Secondary.ArmorColor_10_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_11_Secondary.ArmorColor_11_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_12_Secondary.ArmorColor_12_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_13_Secondary.ArmorColor_13_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_14_Secondary.ArmorColor_14_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_15_Secondary.ArmorColor_15_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_16_Secondary.ArmorColor_16_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_17_Secondary.ArmorColor_17_Secondary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorSecondary/ArmorColor_73_Secondary.ArmorColor_73_Secondary',
                },
        Customization.ARMOR_COLOR_TERTIARY: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_01_Tertiary.ArmorColor_01_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_02_Tertiary.ArmorColor_02_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_03_Tertiary.ArmorColor_03_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_04_Tertiary.ArmorColor_04_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_05_Tertiary.ArmorColor_05_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_06_Tertiary.ArmorColor_06_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_07_Tertiary.ArmorColor_07_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_08_Tertiary.ArmorColor_08_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_09_Tertiary.ArmorColor_09_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_10_Tertiary.ArmorColor_10_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_11_Tertiary.ArmorColor_11_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_12_Tertiary.ArmorColor_12_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_13_Tertiary.ArmorColor_13_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_14_Tertiary.ArmorColor_14_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_15_Tertiary.ArmorColor_15_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_16_Tertiary.ArmorColor_16_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_17_Tertiary.ArmorColor_17_Tertiary',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Armor/ColorTertiary/ArmorColor_73_Tertiary.ArmorColor_73_Tertiary',
                },
        Customization.EMOTE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_07.Emote_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_09.Emote_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_10.Emote_10',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Emotes/Emote_11.Emote_11',
                },
        Customization.BANNER_SHAPE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_01.BannerShape_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_03.BannerShape_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_06.BannerShape_06',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_12.BannerShape_12',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Background/BannerShape_15.BannerShape_15',
                },
        Customization.BANNER_SHAPE_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_01_Shape.BannerColor_01_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_02_Shape.BannerColor_02_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_03_Shape.BannerColor_03_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_04_Shape.BannerColor_04_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_05_Shape.BannerColor_05_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_06_Shape.BannerColor_06_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_07_Shape.BannerColor_07_Shape',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/BackgroundColor/BannerColor_08_Shape.BannerColor_08_Shape',
                },
        Customization.BANNER_PATTERN: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_01.BannerPattern_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_02.BannerPattern_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_16.BannerPattern_16',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_17.BannerPattern_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_25.BannerPattern_25',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Pattern/BannerPattern_27.BannerPattern_27',
                },
        Customization.BANNER_PATTERN_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_01_Pattern.BannerColor_01_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_02_Pattern.BannerColor_02_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_03_Pattern.BannerColor_03_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_04_Pattern.BannerColor_04_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_05_Pattern.BannerColor_05_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_06_Pattern.BannerColor_06_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_07_Pattern.BannerColor_07_Pattern',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/PatternColor/BannerColor_08_Pattern.BannerColor_08_Pattern',
                },
        Customization.BANNER_ICON: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_02.BannerIcon_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_05.BannerIcon_05',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_11.BannerIcon_11',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_17.BannerIcon_17',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_18.BannerIcon_18',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_19.BannerIcon_19',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_20.BannerIcon_20',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_21.BannerIcon_21',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_22.BannerIcon_22',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_23.BannerIcon_23',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_24.BannerIcon_24',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/Icon/BannerIcon_42.BannerIcon_42',
                },
        Customization.BANNER_ICON_COLOR: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_01_Icon.BannerColor_01_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_02_Icon.BannerColor_02_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_03_Icon.BannerColor_03_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_04_Icon.BannerColor_04_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_05_Icon.BannerColor_05_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_06_Icon.BannerColor_06_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_07_Icon.BannerColor_07_Icon',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/Banner/IconColor/BannerColor_08_Icon.BannerColor_08_Icon',
                },
        Customization.STATUE_MATERIAL: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_01.HeroStatueMaterial_01',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_02.HeroStatueMaterial_02',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_04.HeroStatueMaterial_04',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Material/HeroStatueMaterial_13.HeroStatueMaterial_13',
                },
        Customization.STATUE_POSE: {
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_03.HeroStatuePose_03',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_07.HeroStatuePose_07',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_09.HeroStatuePose_09',
                '/Game/PlayerCharacters/_Shared/_Design/Customization/HeroStatue/Pose/HeroStatuePose_16.HeroStatuePose_16',
                },
        }

# For ease of use, a few transformations on the above dict
profile_customizations_defaults = set()
for cust_type, cust_set in profile_customizations_defaults_by_cat.items():
    profile_customizations_defaults |= cust_set
    for cust in cust_set:
        profile_customizations_to_type[cust] = cust_type

# Customization slider config -- We don't actually care about the label, but
# using LabelEnum lets us take advantage of some other functionality in there.
class CustomizationLink(LabelEnum):
    EAR = ('Ear', 'EarLink')
    MOUTH = ('Mouth', 'MouthLink')
    EYE = ('Eye', 'EyeLink')

class CustomizationSlider:
    """
    Custom class to support customization slider randomization.  This is quite
    a bit more code than I'd ideally like in this class (which I'd prefer
    stay pretty data-focused), but I also sort of don't want it anywhere
    else.  Eh, so it goes.
    """

    def __init__(self, var, range_regular, range_overdrive,
            link=None, link_var=None,
            link_is_inverse=False,
            ):
        self.var = var
        self.range_regular = range_regular
        self.range_overdrive = range_overdrive
        self.link = link
        self.link_var = link_var
        self.link_is_inverse = link_is_inverse

    def values(self, link_state, overdrive=False, just_first=False):
        """
        Returns a dict whose keys are the attribute names to change, and
        whose values are the values to set.  We're doing it this way
        on account of "linked" attributes (symmetry, basically).  `link_state`
        should be a dict whose keys are CustomizationLink enums, and
        whose values are booleans -- `True` if the values are linked,
        `False` otherwise.  If linked, the two returned entries in
        the dict will have the same value (adjusted for `link_is_inverse`,
        if necessary).  Otherwise, both will have random values in
        the same range.

        If `just_first` is `True`, instead of returning a dict, *only*
        return the value of the "main" variable.  We're just using that
        for voice pitch scaling, since that's handled pretty differently
        in the save file.
        """
        if overdrive:
            range_to_use = self.range_overdrive
        else:
            range_to_use = self.range_regular
        to_ret = {}
        to_ret[self.var] = random.uniform(*range_to_use)
        if just_first:
            return to_ret[self.var]
        if self.link is not None and self.link_var is not None:
            if link_state[self.link]:
                if self.link_is_inverse:
                    to_ret[self.link_var] = range_to_use[0]+range_to_use[1]-to_ret[self.var]
                else:
                    to_ret[self.link_var] = to_ret[self.var]
            else:
                to_ret[self.link_var] = random.uniform(*range_to_use)
        return to_ret

# Main Customization Sliders
customization_main_sliders = [
        CustomizationSlider('LeftEyePosX',
            (-0.5, 0.5),
            (-1.4, 1.2),
            link=CustomizationLink.EYE,
            link_var='RightEyePosX',
            link_is_inverse=True,
            ),
        CustomizationSlider('LeftEyePosY',
            (-0.4, 0.5),
            (-0.9, 1.0),
            link=CustomizationLink.EYE,
            link_var='RightEyePosY',
            ),
        CustomizationSlider('LeftEyeRot',
            (-15, 15),
            (-45, 45),
            link=CustomizationLink.EYE,
            link_var='RightEyeRot',
            link_is_inverse=True,
            ),
        CustomizationSlider('LeftEyeScale',
            (0.9, 1.1),
            (0.4, 1.8),
            link=CustomizationLink.EYE,
            link_var='RightEyeScale',
            ),
        CustomizationSlider('LeftEarScale',
            (0.9, 1.2),
            (0.3, 2.5),
            link=CustomizationLink.EAR,
            link_var='RightEarScale',
            ),
        CustomizationSlider('NosePosY',
            (-0.5, 0.3),
            (-2.0, 2.0),
            ),
        CustomizationSlider('NoseScale',
            (0.6, 1.2),
            (0.2, 1.8),
            ),
        CustomizationSlider('MouthPosY',
            (-0.5, 0.5),
            (-1.2, 1.4),
            ),
        CustomizationSlider('MouthUpperLipScale',
            (0.8, 1.2),
            (0.6, 1.8),
            link=CustomizationLink.MOUTH,
            link_var='MouthLowerLipScale',
            ),
        CustomizationSlider('BodyScale',
            (0.92, 1.02),
            (0.89, 1.08),
            ),
        CustomizationSlider('HeadAndNeck_Scale',
            (0.98, 1.02),
            (0.94, 1.1),
            ),
        ]

# Vocal pitch slider
customization_pitch_slider = CustomizationSlider('pitch',
        (0.2, 0.8),
        (0.0, 1.0),
        )

# Ordinarily nowadays I'd use sets for these, but the `random` functions prefer
# lists, so lists it is.
customization_pronouns = [
        '/Game/PlayerCharacters/_Shared/_Design/PlayerPronouns/PlayerPronouns_Feminine.PlayerPronouns_Feminine',
        '/Game/PlayerCharacters/_Shared/_Design/PlayerPronouns/PlayerPronouns_Masculine.PlayerPronouns_Masculine',
        '/Game/PlayerCharacters/_Shared/_Design/PlayerPronouns/PlayerPronouns_Neutral.PlayerPronouns_Neutral',
        ]

# Ditto
customization_voices = [
        '/Game/Dialog/Nametags/DNT_PlBraveF.DNT_PlBraveF',
        '/Game/Dialog/Nametags/DNT_PlBraveM.DNT_PlBraveM',
        '/Game/Dialog/Nametags/DNT_PlCleverF.DNT_PlCleverF',
        '/Game/Dialog/Nametags/DNT_PlCleverM.DNT_PlCleverM',
        '/Game/Dialog/Nametags/DNT_PlGruffF.DNT_PlGruffF',
        '/Game/Dialog/Nametags/DNT_PlGruffM.DNT_PlGruffM',
        '/Game/Dialog/Nametags/DNT_PlWeirdF.DNT_PlWeirdF',
        '/Game/Dialog/Nametags/DNT_PlWeirdM.DNT_PlWeirdM',
        ]

# Mission names
#
# For most missions, the following find statement will generate this list:
#
#    for file in $(find Game/Missions Game/PatchDLC/Indigo1/Common/Missions Game/PatchDLC/Indigo*/Missions \( -iname "Mission_*.uexp" \) -print); do echo -n "'/$(dirname $file)/$(basename $file .uexp)': \""; echo $(strings $file | head -n 2 | tail -n 1)\",; done | sort -i
#
mission_to_name = {
        '/Game/Missions/Major/Beanstalk/Mission_Skybound': "Walk the Stalk",
        '/Game/Missions/Major/Goblin/Mission_GTFO': "Goblins Tired of Forced Oppression",
        '/Game/Missions/Major/Goblin/Mission_GTFOP2': "The Slayer of Vorcanar",
        '/Game/Missions/Major/Oasis/Mission_Doomed': "The Ditcher",
        '/Game/Missions/Major/Pirate/Mission_CrookedEyePhil': "The Trial of Crooked-Eye Phil",
        '/Game/Missions/Plot/Mission_Plot00': "Bunkers & Badasses",
        '/Game/Missions/Plot/Mission_Plot01': "Hero of Brighthoof",
        '/Game/Missions/Plot/Mission_Plot02': "A Hard Day's Knight",
        '/Game/Missions/Plot/Mission_Plot04': "Thy Bard, with a Vengeance",
        '/Game/Missions/Plot/Mission_Plot05': "Emotion of the Ocean",
        '/Game/Missions/Plot/Mission_Plot06': "Ballad of Bones",
        '/Game/Missions/Plot/Mission_Plot07': "Mortal Coil",
        '/Game/Missions/Plot/Mission_Plot08': "The Son of a Witch",
        '/Game/Missions/Plot/Mission_Plot09': "Soul Purpose",
        '/Game/Missions/Plot/Mission_Plot10': "Fatebreaker",
        '/Game/Missions/Plot/Mission_Plot11': "Epilogue",
        '/Game/Missions/Side/Overworld/Overworld/AB1_MinersProblem/Mission_OW_AB1_MinersProblem': "Alchemy: Precious Metals",
        '/Game/Missions/Side/Overworld/Overworld/AB2_MiracleGrow/Mission_OW_AB2_MiracleGrow': "Alchemy: Miracle Growth",
        '/Game/Missions/Side/Overworld/Overworld/AB3_SolarCream/Mission_OW_AB3_SolarCream': "Alchemy: To Block the Sun",
        '/Game/Missions/Side/Overworld/Overworld/AKnifeAtTheirBacks/Mission_OW_AKnifeAtTheirBacks': "Knife to Meet You",
        '/Game/Missions/Side/Overworld/Overworld/BlessedBeThySword/Mission_OW_BlessedBeThySword': "A Realm in Peril",
        '/Game/Missions/Side/Overworld/Overworld/ClericallyLost/Mission_OW_ClericallyLost': "Clerical Error",
        '/Game/Missions/Side/Overworld/Overworld/CrabyThePet/Mission_OW_CrabyThePet': "A Pet's Rest",
        '/Game/Missions/Side/Overworld/Overworld/DestructionRainsFromTheHeaven/Mission_OW_DestructionRainsFromTheHeaven': "Destruction Rains from the Heavens",
        '/Game/Missions/Side/Overworld/Overworld/EyeLostIt/Mission_OW_EyeLostIt': "Eye Lost It",
        '/Game/Missions/Side/Overworld/Overworld/FumblingAround/Mission_OW_FumblingAround': "Working Blueprint",
        '/Game/Missions/Side/Overworld/Overworld/IBelieveIcanTouchTheSky/Mission_OW_IBelieveIcanTouchTheSky': "On Wings and Dreams",
        '/Game/Missions/Side/Overworld/Overworld/InMyImage/Mission_OW_InMyImage': "In My Image",
        '/Game/Missions/Side/Overworld/Overworld/ItFellFromTheSkies/Mission_OW_ItFellFromTheSkies': "Cheesy Pick-Up",
        '/Game/Missions/Side/Overworld/Overworld/PocketSandstorm/Mission_OW_PocketSandstorm': "Pocket Sandstorm",
        '/Game/Missions/Side/Overworld/Overworld/TheLegendaryBow/Mission_OW_TheLegendaryBow': "Legendary Bow",
        '/Game/Missions/Side/Overworld/Overworld/VisionOfDeception/Mission_OW_VisionOfDeception': "Lens of the Deceiver",
        '/Game/Missions/Side/Zone_1/Goblin/Mission_MurderHobos': "Non-Violent Offender",
        '/Game/Missions/Side/Zone_1/Goblin/Mission_SmithsCharade': "Forgery",
        '/Game/Missions/Side/Zone_1/Hubtown/Mission_InnerDemons': "Inner Daemons",
        '/Game/Missions/Side/Zone_1/Intro/Mission_RatQuestPt1': "Goblins in the Garden",
        '/Game/Missions/Side/Zone_1/Intro/Mission_RatQuestPt2': "A Farmer's Ardor",
        '/Game/Missions/Side/Zone_1/Mushroom/Mission_BlueOnes': "Little Boys Blue",
        '/Game/Missions/Side/Zone_1/Mushroom/Mission_ClaptrapGrenade': "A Knight's Toil",
        '/Game/Missions/Side/Zone_1/Mushroom/Mission_MinstrelMetal': "Lyre and Brimstone",
        '/Game/Missions/Side/Zone_1/Mushroom/Mission_ToothFairy': "Cash 4 Teeth",
        '/Game/Missions/Side/Zone_1/Sewers/Mission_CloggageOfTheDammed': "On the Wink of Destruction",
        '/Game/Missions/Side/Zone_2/Abyss/Mission_CurseOfTheTwistedSisters': "Of Curse and Claw",
        '/Game/Missions/Side/Zone_2/Abyss/Mission_Diplomacy': "Diplomatic Relations",
        '/Game/Missions/Side/Zone_2/Beanstalk/Mission_DeRat': "A Small Favor",
        '/Game/Missions/Side/Zone_2/Beanstalk/Mission_ElderWyvern': "Burning Hunger",
        '/Game/Missions/Side/Zone_2/Beanstalk/Mission_RonRivote': "Ron Rivote",
        '/Game/Missions/Side/Zone_2/Pirate/Mission_JaggedToothCrew': "All Swashed Up",
        '/Game/Missions/Side/Zone_2/Pirate/Mission_LittlePookie': "A Walk to Dismember",
        '/Game/Missions/Side/Zone_2/Pirate/MIssion_PirateLife': "A Wandering Aye",
        '/Game/Missions/Side/Zone_2/Pirate/Mission_WhaleTale': "In the Belly Is a Beast",
        '/Game/Missions/Side/Zone_2/SeaBed/Mission_DyingWish': "Twenty Thousand Years Under the Sea",
        '/Game/Missions/Side/Zone_2/SeaBed/Mission_SharkPearls': "Raiders of the Lost Shark",
        '/Game/Missions/Side/Zone_3/Climb/Mission_AncientPowers': "Ancient Powers",
        '/Game/Missions/Side/Zone_3/Climb/Mission_AncientPowersCombat1': "Ancient Powers (Part 2)",
        '/Game/Missions/Side/Zone_3/Climb/Mission_AncientPowersCombat2': "Ancient Powers (Part 3)",
        '/Game/Missions/Side/Zone_3/Climb/Mission_AncientPowersDreadLord': "Ancient Powers (Part 4)",
        '/Game/Missions/Side/Zone_3/Climb/Mission_AncientPowersDreadLordRepeatable': "Ancient Powers (Part 5)",
        '/Game/Missions/Side/Zone_3/Climb/Mission_LavaGoodTime': "Spell to Pay",
        '/Game/Missions/Side/Zone_3/Climb/Mission_MonsterLover': "Necromance Her",
        '/Game/Missions/Side/Zone_3/Oasis/Mission_LowTideBoil': "Gumbo No. 5",
        '/Game/Missions/Side/Zone_3/Sands/Mission_BlueHatCult': "Armageddon Distracted",
        '/Game/Missions/Side/Zone_3/Sands/Mission_ElementalBeer': "Hot Fizz",
        '/Game/PatchDLC/Indigo1/Common/Missions/Mission_Indigo_Epilogue': "Vesper's Epilogue",
        '/Game/PatchDLC/Indigo1/Common/Missions/Mission_Indigo_FirstWheelUse': "Meet the Wheel of Fate",
        '/Game/PatchDLC/Indigo1/Common/Missions/Mission_PLC_Completion': "Nightmare in Dreamveil",
        '/Game/PatchDLC/Indigo1/Missions/CompletionMission/Mission_PLC1_CompletionV1': "Defeated Chums: Difficulty 1",
        '/Game/PatchDLC/Indigo1/Missions/CompletionMission/Mission_PLC1_CompletionV2': "Defeated Chums: Difficulty 2",
        '/Game/PatchDLC/Indigo1/Missions/CompletionMission/Mission_PLC1_CompletionV3': "Defeated Chums: Difficulty 3",
        '/Game/PatchDLC/Indigo1/Missions/CompletionMission/Mission_PLC1_CompletionV4': "Defeated Chums: Difficulty 4",
        '/Game/PatchDLC/Indigo1/Missions/Mission_PLC1': "Best Chums",
        '/Game/PatchDLC/Indigo2/Missions/Mission_PLC2': "Pesto Chango",
        '/Game/PatchDLC/Indigo2/Missions/NonRepeatableMissions/Mission_PLC2_CompletionV1': "Defeated Imelda: Difficulty 1",
        '/Game/PatchDLC/Indigo2/Missions/NonRepeatableMissions/Mission_PLC2_CompletionV2': "Defeated Imelda: Difficulty 2",
        '/Game/PatchDLC/Indigo2/Missions/NonRepeatableMissions/Mission_PLC2_CompletionV3': "Defeated Imelda: Difficulty 3",
        '/Game/PatchDLC/Indigo2/Missions/NonRepeatableMissions/Mission_PLC2_CompletionV4': "Defeated Imelda: Difficulty 4",
        '/Game/PatchDLC/Indigo3/Missions/CompletionMissions/Mission_PLC3_CompletionV1': "Defeated Fyodor: Difficulty 1",
        '/Game/PatchDLC/Indigo3/Missions/CompletionMissions/Mission_PLC3_CompletionV2': "Defeated Fyodor: Difficulty 2",
        '/Game/PatchDLC/Indigo3/Missions/CompletionMissions/Mission_PLC3_CompletionV3': "Defeated Fyodor: Difficulty 3",
        '/Game/PatchDLC/Indigo3/Missions/CompletionMissions/Mission_PLC3_CompletionV4': "Defeated Fyodor: Difficulty 4",
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3_3_1': "Puns and Crimeishment: Misery's Mine",
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3_3_2': "Puns and Crimeishment: Crystal Chasm",
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3_3_3': "Puns and Crimeishment: Slammer Central",
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3_3_4': "Puns and Crimeishment: Firedeep Forge",
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3': "Puns and Crimeishment",
        }
for k, v in list(mission_to_name.items()):
    lower = k.lower()
    last_bit = lower.split('/')[-1]
    new_k = '{}.{}_c'.format(lower, last_bit)
    mission_to_name[new_k] = v

# Plot missions (of the sort that we don't want to allow removing, since you'd
# probably be locked out of the plot missions).  These were just copy+pasted
# from the mission_to_name structure above and pruned manually.
plot_missions = set()
for mission_name in [
        '/Game/Missions/Plot/Mission_Plot00',
        '/Game/Missions/Plot/Mission_Plot01',
        '/Game/Missions/Plot/Mission_Plot02',
        '/Game/Missions/Plot/Mission_Plot04',
        '/Game/Missions/Plot/Mission_Plot05',
        '/Game/Missions/Plot/Mission_Plot06',
        '/Game/Missions/Plot/Mission_Plot07',
        '/Game/Missions/Plot/Mission_Plot08',
        '/Game/Missions/Plot/Mission_Plot09',
        '/Game/Missions/Plot/Mission_Plot10',
        '/Game/Missions/Plot/Mission_Plot11',
        ]:
    lower = mission_name.lower()
    last_bit = lower.split('/')[-1]
    plot_missions.add('{}.{}_c'.format(lower, last_bit))

# Map-to-eng
map_to_eng = {
        'Abyss_P': "Drowned Abyss",
        'AbyssBoss_P': "The Godswell",
        'Beanstalk_P': "Tangledrift",
        'Climb_P': "Karnok's Wall",
        'D_LootRoom_P': "Loot of Chaos",
        'EndlessDungeon_P': "The Chaos Chamber",
        'Goblin_P': "Mount Craw",
        'Graveyard_P': "Shattergrave Barrow",
        'Hubtown_P': "Brighthoof",
        'Ind_CaravanHub_01_P': "Dreamveil Overlook",
        'Intro_P': "Queen's Gate",
        'Mushroom_P': "Weepwild Dankness",
        'Oasis_P': "Sunfang Oasis",
        'Overworld_P': "Overworld",
        'Pirate_P': "Crackmast Cove",
        'Pyramid_P': "The Fearamid",
        'PyramidBoss_P': "Crest of Fate",
        'Sands_P': "Ossu-Gol Necropolis",
        'SeaBed_P': "Wargtooth Shallows",
        'Tutorial_P': "Snoring Valley",
        }

# Autogenerated by gen_fts_mappings.py, in Apocalyptech's dir in the BLCM wlmods project (in dataprocessing)
fts_to_map = {
        '/game/gamedata/fasttravel/fts_abyss_01.fts_abyss_01': 'Abyss_P',
        '/game/gamedata/fasttravel/fts_abyss_02.fts_abyss_02': 'Abyss_P',
        '/game/gamedata/fasttravel/fts_abyss_03.fts_abyss_03': 'Abyss_P',
        '/game/gamedata/fasttravel/fts_abyssboss_01.fts_abyssboss_01': 'AbyssBoss_P',
        '/game/gamedata/fasttravel/fts_abyssboss_02.fts_abyssboss_02': 'AbyssBoss_P',
        '/game/gamedata/fasttravel/fts_beanstalk-sendonly.fts_beanstalk-sendonly': 'Beanstalk_P',
        '/game/gamedata/fasttravel/fts_beanstalk_01.fts_beanstalk_01': 'Beanstalk_P',
        '/game/gamedata/fasttravel/fts_beanstalk_02.fts_beanstalk_02': 'Beanstalk_P',
        '/game/gamedata/fasttravel/fts_beanstalk_03.fts_beanstalk_03': 'Beanstalk_P',
        '/game/gamedata/fasttravel/fts_climb_01.fts_climb_01': 'Climb_P',
        '/game/gamedata/fasttravel/fts_climb_02.fts_climb_02': 'Climb_P',
        '/game/gamedata/fasttravel/fts_climb_03.fts_climb_03': 'Climb_P',
        '/game/gamedata/fasttravel/fts_dungeon.fts_dungeon': 'Overworld_P',
        '/game/gamedata/fasttravel/fts_endlessdungeon.fts_endlessdungeon': 'EndlessDungeon_P',
        '/game/gamedata/fasttravel/fts_goblin_01.fts_goblin_01': 'Goblin_P',
        '/game/gamedata/fasttravel/fts_goblin_02.fts_goblin_02': 'Goblin_P',
        '/game/gamedata/fasttravel/fts_goblin_03.fts_goblin_03': 'Goblin_P',
        '/game/gamedata/fasttravel/fts_graveyard_01.fts_graveyard_01': 'Graveyard_P',
        '/game/gamedata/fasttravel/fts_graveyard_02.fts_graveyard_02': 'Graveyard_P',
        '/game/gamedata/fasttravel/fts_hubtown_01.fts_hubtown_01': 'Hubtown_P',
        '/game/gamedata/fasttravel/fts_hubtown_02.fts_hubtown_02': 'Hubtown_P',
        '/game/gamedata/fasttravel/fts_hubtown_03.fts_hubtown_03': 'Hubtown_P',
        '/game/gamedata/fasttravel/fts_hubtown_04.fts_hubtown_04': 'Hubtown_P',
        '/game/gamedata/fasttravel/fts_hubtown_05.fts_hubtown_05': 'Hubtown_P',
        '/game/gamedata/fasttravel/fts_intro_01.fts_intro_01': 'Intro_P',
        '/game/gamedata/fasttravel/fts_intro_02.fts_intro_02': 'Intro_P',
        '/game/gamedata/fasttravel/fts_intro_03.fts_intro_03': 'Intro_P',
        '/game/gamedata/fasttravel/fts_mushroom_01.fts_mushroom_01': 'Mushroom_P',
        '/game/gamedata/fasttravel/fts_mushroom_02.fts_mushroom_02': 'Mushroom_P',
        '/game/gamedata/fasttravel/fts_mushroom_03.fts_mushroom_03': 'Mushroom_P',
        '/game/gamedata/fasttravel/fts_oasis_01.fts_oasis_01': 'Oasis_P',
        '/game/gamedata/fasttravel/fts_oasis_02.fts_oasis_02': 'Oasis_P',
        '/game/gamedata/fasttravel/fts_oasis_03.fts_oasis_03': 'Oasis_P',
        '/game/gamedata/fasttravel/fts_overworld1.fts_overworld1': 'Overworld_P',
        '/game/gamedata/fasttravel/fts_overworld2.fts_overworld2': 'Overworld_P',
        '/game/gamedata/fasttravel/fts_overworld2a.fts_overworld2a': 'Overworld_P',
        '/game/gamedata/fasttravel/fts_overworld3.fts_overworld3': 'Overworld_P',
        '/game/gamedata/fasttravel/fts_pirate-sendonly.fts_pirate-sendonly': 'Pirate_P',
        '/game/gamedata/fasttravel/fts_pirate_01.fts_pirate_01': 'Pirate_P',
        '/game/gamedata/fasttravel/fts_pirate_02.fts_pirate_02': 'Pirate_P',
        '/game/gamedata/fasttravel/fts_pirate_03.fts_pirate_03': 'Pirate_P',
        '/game/gamedata/fasttravel/fts_pyramid_01.fts_pyramid_01': 'Pyramid_P',
        '/game/gamedata/fasttravel/fts_pyramid_02.fts_pyramid_02': 'Pyramid_P',
        '/game/gamedata/fasttravel/fts_pyramid_03.fts_pyramid_03': 'Pyramid_P',
        '/game/gamedata/fasttravel/fts_pyramidboss-sendonly.fts_pyramidboss-sendonly': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/fts_pyramidboss.fts_pyramidboss': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/fts_sands_01.fts_sands_01': 'Sands_P',
        '/game/gamedata/fasttravel/fts_sands_02.fts_sands_02': 'Sands_P',
        '/game/gamedata/fasttravel/fts_sands_03.fts_sands_03': 'Sands_P',
        '/game/gamedata/fasttravel/fts_seabed_01.fts_seabed_01': 'SeaBed_P',
        '/game/gamedata/fasttravel/fts_seabed_02.fts_seabed_02': 'SeaBed_P',
        '/game/gamedata/fasttravel/fts_seabed_03.fts_seabed_03': 'SeaBed_P',
        '/game/gamedata/fasttravel/fts_tutorial_01.fts_tutorial_01': 'Tutorial_P',
        '/game/gamedata/fasttravel/fts_tutorial_02.fts_tutorial_02': 'Tutorial_P',
        '/game/gamedata/fasttravel/fts_tutorial_03.fts_tutorial_03': 'Tutorial_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_abyss_abyssboss.lts_abyss_abyssboss': 'Abyss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_abyss_overworld.lts_abyss_overworld': 'Abyss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_abyssboss_abyss.lts_abyssboss_abyss': 'AbyssBoss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_abyssboss_overworld.lts_abyssboss_overworld': 'AbyssBoss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_beanstalk_overworld.lts_beanstalk_overworld': 'Beanstalk_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_climb_overworld.lts_climb_overworld': 'Climb_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_climb_overworld2.lts_climb_overworld2': 'Climb_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_endlessdungeon_hubtown.lts_endlessdungeon_hubtown': 'EndlessDungeon_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_endlessdungeon_lootroom.lts_endlessdungeon_lootroom': 'EndlessDungeon_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_goblin_overworld.lts_goblin_overworld': 'Goblin_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_graveyard_overworld.lts_graveyard_overworld': 'Graveyard_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtown_endlessdungeon.lts_hubtown_endlessdungeon': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtown_intro.lts_hubtown_intro': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtown_overworld.lts_hubtown_overworld': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtown_overworld2.lts_hubtown_overworld2': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtown_pyrboss.lts_hubtown_pyrboss': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_hubtownportal.lts_hubtownportal': 'Hubtown_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_intro_hubtown.lts_intro_hubtown': 'Intro_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_intro_overworld.lts_intro_overworld': 'Intro_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_lootroom_endlessdungeon.lts_lootroom_endlessdungeon': 'D_LootRoom_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_mushroom_overworld.lts_mushroom_overworld': 'Mushroom_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_mushroom_seabed.lts_mushroom_seabed': 'Mushroom_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_oasis_overworld.lts_oasis_overworld': 'Oasis_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld2_climb.lts_overworld2_climb': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_abyss.lts_overworld_abyss': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_abyssboss.lts_overworld_abyssboss': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_beanstalk.lts_overworld_beanstalk': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_climb.lts_overworld_climb': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_goblin.lts_overworld_goblin': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_graveyard.lts_overworld_graveyard': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_hubtown.lts_overworld_hubtown': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_hubtown2.lts_overworld_hubtown2': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_intro.lts_overworld_intro': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_mushroom.lts_overworld_mushroom': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_oasis.lts_overworld_oasis': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_pirate.lts_overworld_pirate': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_pyramid.lts_overworld_pyramid': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_sands.lts_overworld_sands': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_sands2.lts_overworld_sands2': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_seabed.lts_overworld_seabed': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_seabed2.lts_overworld_seabed2': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_overworld_tutorial.lts_overworld_tutorial': 'Overworld_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_pirate_overworld.lts_pirate_overworld': 'Pirate_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_pyramid_overworld.lts_pyramid_overworld': 'Pyramid_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_pyramid_pyramidboss.lts_pyramid_pyramidboss': 'Pyramid_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_pyramidboss_pyramid.lts_pyramidboss_pyramid': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_pyrboss_hubtown.lts_pyrboss_hubtown': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_sands2_overworld.lts_sands2_overworld': 'Sands_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_sands_overworld.lts_sands_overworld': 'Sands_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_seabed2_overworld.lts_seabed2_overworld': 'SeaBed_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_seabed_mushroom.lts_seabed_mushroom': 'SeaBed_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_seabed_overworld.lts_seabed_overworld': 'SeaBed_P',
        '/game/gamedata/fasttravel/leveltravelstations/lts_tutorial_overworld.lts_tutorial_overworld': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_13.rts_abyss_p_resurrecttravelstation_daffodil_13': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_2.rts_abyss_p_resurrecttravelstation_daffodil_2': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_3.rts_abyss_p_resurrecttravelstation_daffodil_3': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_4.rts_abyss_p_resurrecttravelstation_daffodil_4': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_5.rts_abyss_p_resurrecttravelstation_daffodil_5': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_6.rts_abyss_p_resurrecttravelstation_daffodil_6': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_7.rts_abyss_p_resurrecttravelstation_daffodil_7': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyss/rts_abyss_p_resurrecttravelstation_daffodil_9.rts_abyss_p_resurrecttravelstation_daffodil_9': 'Abyss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/abyssboss/rts_abyssboss_combat_7.rts_abyssboss_combat_7': 'AbyssBoss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_castle_resurrecttravelstation_daffodil_finalslide.rts_beanstalk_castle_resurrecttravelstation_daffodil_finalslide': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_castlefinale.rts_beanstalk_combat_resurrecttravelstation_daffodil_castlefinale': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_castlemid.rts_beanstalk_combat_resurrecttravelstation_daffodil_castlemid': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_castlestart.rts_beanstalk_combat_resurrecttravelstation_daffodil_castlestart': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_cathedral.rts_beanstalk_combat_resurrecttravelstation_daffodil_cathedral': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_cathedralreveal.rts_beanstalk_combat_resurrecttravelstation_daffodil_cathedralreveal': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_derattop.rts_beanstalk_combat_resurrecttravelstation_daffodil_derattop': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_farm.rts_beanstalk_combat_resurrecttravelstation_daffodil_farm': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_firstslideending.rts_beanstalk_combat_resurrecttravelstation_daffodil_firstslideending': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthouse.rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthouse': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthousereveal.rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthousereveal': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthousereveal_0.rts_beanstalk_combat_resurrecttravelstation_daffodil_lighthousereveal_0': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_obeliskstart.rts_beanstalk_combat_resurrecttravelstation_daffodil_obeliskstart': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_ronrivote.rts_beanstalk_combat_resurrecttravelstation_daffodil_ronrivote': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_combat_resurrecttravelstation_daffodil_townentrance.rts_beanstalk_combat_resurrecttravelstation_daffodil_townentrance': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_geo_elderwyvern_resurrecttravelstation_daffodil_elderwyvernentrance.rts_beanstalk_geo_elderwyvern_resurrecttravelstation_daffodil_elderwyvernentrance': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_geo_ronrivote_resurrecttravelstation_daffodil_ronrivote.rts_beanstalk_geo_ronrivote_resurrecttravelstation_daffodil_ronrivote': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_geo_ronrivote_resurrecttravelstation_rr_insidecastle.rts_beanstalk_geo_ronrivote_resurrecttravelstation_rr_insidecastle': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_m_derat_resurrecttravelstation_daffodil_ronrivote.rts_beanstalk_m_derat_resurrecttravelstation_daffodil_ronrivote': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/beanstalk/rts_beanstalk_m_elderwyvern_resurrecttravelstation_daffodil_3.rts_beanstalk_m_elderwyvern_resurrecttravelstation_daffodil_3': 'Beanstalk_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_m_ancientpowers_resurrecttravelstation_daffodil_5.rts_climb_m_ancientpowers_resurrecttravelstation_daffodil_5': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil.rts_climb_p_resurrecttravelstation_daffodil': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_0.rts_climb_p_resurrecttravelstation_daffodil_0': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_1.rts_climb_p_resurrecttravelstation_daffodil_1': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_10.rts_climb_p_resurrecttravelstation_daffodil_10': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_11.rts_climb_p_resurrecttravelstation_daffodil_11': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_14.rts_climb_p_resurrecttravelstation_daffodil_14': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_15.rts_climb_p_resurrecttravelstation_daffodil_15': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_2.rts_climb_p_resurrecttravelstation_daffodil_2': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_3.rts_climb_p_resurrecttravelstation_daffodil_3': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_4.rts_climb_p_resurrecttravelstation_daffodil_4': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_5.rts_climb_p_resurrecttravelstation_daffodil_5': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_6.rts_climb_p_resurrecttravelstation_daffodil_6': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_7.rts_climb_p_resurrecttravelstation_daffodil_7': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_8.rts_climb_p_resurrecttravelstation_daffodil_8': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/climb/rts_climb_p_resurrecttravelstation_daffodil_9.rts_climb_p_resurrecttravelstation_daffodil_9': 'Climb_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_10.rts_goblin_dynamic_10': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_11.rts_goblin_dynamic_11': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_12.rts_goblin_dynamic_12': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_13.rts_goblin_dynamic_13': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_14.rts_goblin_dynamic_14': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_15.rts_goblin_dynamic_15': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_16.rts_goblin_dynamic_16': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_17.rts_goblin_dynamic_17': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_18.rts_goblin_dynamic_18': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_19.rts_goblin_dynamic_19': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_20.rts_goblin_dynamic_20': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_dynamic_3.rts_goblin_dynamic_3': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_0.rts_goblin_p_0': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_1.rts_goblin_p_1': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_2.rts_goblin_p_2': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_3.rts_goblin_p_3': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_4.rts_goblin_p_4': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_5.rts_goblin_p_5': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_6.rts_goblin_p_6': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_7.rts_goblin_p_7': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_8.rts_goblin_p_8': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/goblin/rts_goblin_p_9.rts_goblin_p_9': 'Goblin_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_blockout_crypt_resurrecttravelstation_daffodil_11.rts_graveyard_blockout_crypt_resurrecttravelstation_daffodil_11': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_blockout_resurrecttravelstation_daffodil_2.rts_graveyard_blockout_resurrecttravelstation_daffodil_2': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_blockout_resurrecttravelstation_daffodil_3.rts_graveyard_blockout_resurrecttravelstation_daffodil_3': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_bossarena_resurrecttravelstation_daffodil_5.rts_graveyard_bossarena_resurrecttravelstation_daffodil_5': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_dynamic_resurrecttravelstation_daffodil_11.rts_graveyard_dynamic_resurrecttravelstation_daffodil_11': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_dynamic_resurrecttravelstation_daffodil_2.rts_graveyard_dynamic_resurrecttravelstation_daffodil_2': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_dynamic_resurrecttravelstation_daffodil_3.rts_graveyard_dynamic_resurrecttravelstation_daffodil_3': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_dynamic_resurrecttravelstation_daffodil_4.rts_graveyard_dynamic_resurrecttravelstation_daffodil_4': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/graveyard/rts_graveyard_p_resurrecttravelstation_daffodil_2.rts_graveyard_p_resurrecttravelstation_daffodil_2': 'Graveyard_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_combat_resurrecttravelstation_daffodil_2.rts_hubtown_combat_resurrecttravelstation_daffodil_2': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_dynamic_resurrecttravelstation_daffodil_0.rts_hubtown_dynamic_resurrecttravelstation_daffodil_0': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_dynamic_resurrecttravelstation_daffodil_2.rts_hubtown_dynamic_resurrecttravelstation_daffodil_2': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_dynamic_resurrecttravelstation_daffodil_3.rts_hubtown_dynamic_resurrecttravelstation_daffodil_3': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_dynamic_resurrecttravelstation_daffodil_4.rts_hubtown_dynamic_resurrecttravelstation_daffodil_4': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_m_dockblocked_resurrecttravelstation_daffodil_4.rts_hubtown_m_dockblocked_resurrecttravelstation_daffodil_4': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_m_plot04_resurrecttravelstation_daffodil_4.rts_hubtown_m_plot04_resurrecttravelstation_daffodil_4': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_p_resurrecttravelstation_daffodil_0.rts_hubtown_p_resurrecttravelstation_daffodil_0': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_p_resurrecttravelstation_daffodil_1.rts_hubtown_p_resurrecttravelstation_daffodil_1': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/hubtown/rts_hubtown_p_resurrecttravelstation_daffodil_2.rts_hubtown_p_resurrecttravelstation_daffodil_2': 'Hubtown_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_0.rts_intro_dynamic_resurrecttravelstation_daffodil_0': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_1.rts_intro_dynamic_resurrecttravelstation_daffodil_1': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_2.rts_intro_dynamic_resurrecttravelstation_daffodil_2': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_3.rts_intro_dynamic_resurrecttravelstation_daffodil_3': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_4.rts_intro_dynamic_resurrecttravelstation_daffodil_4': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_5.rts_intro_dynamic_resurrecttravelstation_daffodil_5': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_6.rts_intro_dynamic_resurrecttravelstation_daffodil_6': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_7.rts_intro_dynamic_resurrecttravelstation_daffodil_7': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_8.rts_intro_dynamic_resurrecttravelstation_daffodil_8': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/intro/rts_intro_dynamic_resurrecttravelstation_daffodil_9.rts_intro_dynamic_resurrecttravelstation_daffodil_9': 'Intro_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_0.rts_mushroom_dynamic_0': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_1.rts_mushroom_dynamic_1': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_2.rts_mushroom_dynamic_2': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_4.rts_mushroom_dynamic_4': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_6.rts_mushroom_dynamic_6': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_dynamic_7.rts_mushroom_dynamic_7': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_0.rts_mushroom_p_0': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_1.rts_mushroom_p_1': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_2.rts_mushroom_p_2': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_3.rts_mushroom_p_3': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_4.rts_mushroom_p_4': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_5.rts_mushroom_p_5': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_6.rts_mushroom_p_6': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/mushroom/rts_mushroom_p_7.rts_mushroom_p_7': 'Mushroom_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_0.rts_oasis_dynamic_resurrecttravelstation_daffodil_0': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_1.rts_oasis_dynamic_resurrecttravelstation_daffodil_1': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_10.rts_oasis_dynamic_resurrecttravelstation_daffodil_10': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_2.rts_oasis_dynamic_resurrecttravelstation_daffodil_2': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_3.rts_oasis_dynamic_resurrecttravelstation_daffodil_3': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_4.rts_oasis_dynamic_resurrecttravelstation_daffodil_4': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_5.rts_oasis_dynamic_resurrecttravelstation_daffodil_5': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_6.rts_oasis_dynamic_resurrecttravelstation_daffodil_6': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_7.rts_oasis_dynamic_resurrecttravelstation_daffodil_7': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_8.rts_oasis_dynamic_resurrecttravelstation_daffodil_8': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/oasis/rts_oasis_dynamic_resurrecttravelstation_daffodil_9.rts_oasis_dynamic_resurrecttravelstation_daffodil_9': 'Oasis_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_1.rts_pirate_dynamic_resurrecttravelstation_daffodil_1': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_2.rts_pirate_dynamic_resurrecttravelstation_daffodil_2': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_3.rts_pirate_dynamic_resurrecttravelstation_daffodil_3': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_4.rts_pirate_dynamic_resurrecttravelstation_daffodil_4': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_5.rts_pirate_dynamic_resurrecttravelstation_daffodil_5': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_6.rts_pirate_dynamic_resurrecttravelstation_daffodil_6': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_dynamic_resurrecttravelstation_daffodil_7.rts_pirate_dynamic_resurrecttravelstation_daffodil_7': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_0.rts_pirate_p_resurrecttravelstation_daffodil_0': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_1.rts_pirate_p_resurrecttravelstation_daffodil_1': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_2.rts_pirate_p_resurrecttravelstation_daffodil_2': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_3.rts_pirate_p_resurrecttravelstation_daffodil_3': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_4.rts_pirate_p_resurrecttravelstation_daffodil_4': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_5.rts_pirate_p_resurrecttravelstation_daffodil_5': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_6.rts_pirate_p_resurrecttravelstation_daffodil_6': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pirate/rts_pirate_p_resurrecttravelstation_daffodil_7.rts_pirate_p_resurrecttravelstation_daffodil_7': 'Pirate_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramid/rts_pyramid_p_resurrecttravelstation_daffodil.rts_pyramid_p_resurrecttravelstation_daffodil': 'Pyramid_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramid/rts_pyramid_p_resurrecttravelstation_daffodil_0.rts_pyramid_p_resurrecttravelstation_daffodil_0': 'Pyramid_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramid/rts_pyramid_p_resurrecttravelstation_daffodil_1.rts_pyramid_p_resurrecttravelstation_daffodil_1': 'Pyramid_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramid/rts_pyramid_p_resurrecttravelstation_daffodil_3.rts_pyramid_p_resurrecttravelstation_daffodil_3': 'Pyramid_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramid/rts_pyramid_p_resurrecttravelstation_daffodil_4.rts_pyramid_p_resurrecttravelstation_daffodil_4': 'Pyramid_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramidboss/rts_pyramidboss_dynamic_p_resurrecttravelstation_daffodil_0.rts_pyramidboss_dynamic_p_resurrecttravelstation_daffodil_0': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/pyramidboss/rts_pyramidboss_p_resurrecttravelstation_daffodil_0.rts_pyramidboss_p_resurrecttravelstation_daffodil_0': 'PyramidBoss_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_outpost_approach.rts_sands_dynamic_resurrecttravelstation_outpost_approach': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-basement.rts_sands_dynamic_resurrecttravelstation_slums-basement': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-blueh.rts_sands_dynamic_resurrecttravelstation_slums-blueh': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-blueh_0.rts_sands_dynamic_resurrecttravelstation_slums-blueh_0': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-fire.rts_sands_dynamic_resurrecttravelstation_slums-fire': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-gate.rts_sands_dynamic_resurrecttravelstation_slums-gate': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-ice.rts_sands_dynamic_resurrecttravelstation_slums-ice': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-ice_1.rts_sands_dynamic_resurrecttravelstation_slums-ice_1': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums-tunnel.rts_sands_dynamic_resurrecttravelstation_slums-tunnel': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums_bluehat.rts_sands_dynamic_resurrecttravelstation_slums_bluehat': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_slums_wall.rts_sands_dynamic_resurrecttravelstation_slums_wall': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_under-downbeat.rts_sands_dynamic_resurrecttravelstation_under-downbeat': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_under-downbeat_2.rts_sands_dynamic_resurrecttravelstation_under-downbeat_2': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_under-obelisk.rts_sands_dynamic_resurrecttravelstation_under-obelisk': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_dynamic_resurrecttravelstation_under-temple.rts_sands_dynamic_resurrecttravelstation_under-temple': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_m_plot09_travelstation_onetimeforcedteleport_2.rts_sands_m_plot09_travelstation_onetimeforcedteleport_2': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/sands/rts_sands_m_plot09_travelstation_onetimeforcedteleport_5.rts_sands_m_plot09_travelstation_onetimeforcedteleport_5': 'Sands_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_boss_resurrecttravelstation_daffodil_2.rts_seabed_boss_resurrecttravelstation_daffodil_2': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_4.rts_seabed_combat_4': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_generouslyhighhalfheight.rts_seabed_combat_generouslyhighhalfheight': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstation_daffodil_11.rts_seabed_combat_resurrecttravelstation_daffodil_11': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstation_daffodil_15.rts_seabed_combat_resurrecttravelstation_daffodil_15': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstation_daffodil_19.rts_seabed_combat_resurrecttravelstation_daffodil_19': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstation_daffodil_3.rts_seabed_combat_resurrecttravelstation_daffodil_3': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstation_daffodil_5.rts_seabed_combat_resurrecttravelstation_daffodil_5': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstationobjectdaff.rts_seabed_combat_resurrecttravelstationobjectdaff': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_combat_resurrecttravelstationobjectdaff_0.rts_seabed_combat_resurrecttravelstationobjectdaff_0': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_geo_intro_4.rts_seabed_geo_intro_4': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_0.rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_0': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_1.rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_1': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/seabed/rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_3.rts_seabed_geo_sharkpearls_resurrecttravelstation_daffodil_3': 'SeaBed_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_geo_resurrecttravelstation_daffodil_0.rts_tutorial_geo_resurrecttravelstation_daffodil_0': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_geo_resurrecttravelstation_daffodil_1.rts_tutorial_geo_resurrecttravelstation_daffodil_1': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_geo_resurrecttravelstation_daffodil_2.rts_tutorial_geo_resurrecttravelstation_daffodil_2': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_geo_resurrecttravelstation_daffodil_3.rts_tutorial_geo_resurrecttravelstation_daffodil_3': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_0.rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_0': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_2.rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_2': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_3.rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_3': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_4.rts_tutorial_m_plot0tutorial_resurrecttravelstation_daffodil_4': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_0.rts_tutorial_p_resurrecttravelstation_daffodil_0': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_1.rts_tutorial_p_resurrecttravelstation_daffodil_1': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_2.rts_tutorial_p_resurrecttravelstation_daffodil_2': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_3.rts_tutorial_p_resurrecttravelstation_daffodil_3': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_4.rts_tutorial_p_resurrecttravelstation_daffodil_4': 'Tutorial_P',
        '/game/gamedata/fasttravel/resurrecttravelstations/autogen/tutorial/rts_tutorial_p_resurrecttravelstation_daffodil_5.rts_tutorial_p_resurrecttravelstation_daffodil_5': 'Tutorial_P',
        '/game/patchdlc/indigo1/gamedata/fasttravel/fts_caravanhub.fts_caravanhub': 'Ind_CaravanHub_01_P',
        '/game/patchdlc/indigo1/gamedata/fasttravel/leveltravelstations/lts_caravanhub_overworld_overworld.lts_caravanhub_overworld_overworld': 'Ind_CaravanHub_01_P',
        '/game/patchdlc/indigo1/gamedata/fasttravel/leveltravelstations/lts_overworld_caravanhub.lts_overworld_caravanhub': 'Overworld_P',
        }

