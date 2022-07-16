
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
__version__ = '0.0.9'
# Forked from bl3-cli-saveedit
# __version__ = '1.16.1b1'

import enum

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
(BRRZERKER, CLAWBRINGER, GRAVEBORN, SPELLSHOT, SPOREWARDEN, STABBOMANCER) = range(6)
class_to_eng = {
        BRRZERKER: 'Brr-Zerker',
        CLAWBRINGER: 'Clawbringer',
        GRAVEBORN: 'Graveborn',
        SPELLSHOT: 'Spellshot',
        SPOREWARDEN: 'Spore Warden',
        STABBOMANCER: 'Stabbomancer',
        }
classobj_to_class = {
        '/Game/PlayerCharacters/Barbarian/_Shared/_Design/SkillTree/AbilityTree_Branch_Barbarian.AbilityTree_Branch_Barbarian': BRRZERKER,
        '/Game/PlayerCharacters/GunMage/_Shared/_Design/SkillTree/AbilityTree_Branch_GunMage.AbilityTree_Branch_GunMage': SPELLSHOT,
        '/Game/PlayerCharacters/KnightOfTheClaw/_Shared/_Design/SkillTree/AbilityTree_Branch_DragonCleric.AbilityTree_Branch_DragonCleric': CLAWBRINGER,
        '/Game/PlayerCharacters/Necromancer/_Shared/_Design/SkillTree/AbilityTree_Branch_Necromancer.AbilityTree_Branch_Necromancer': GRAVEBORN,
        '/Game/PlayerCharacters/Ranger/_Shared/_Design/SkillTree/AbilityTree_Branch_Ranger.AbilityTree_Branch_Ranger': SPOREWARDEN,
        '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/AbilityTree_Branch_Rogue.AbilityTree_Branch_Rogue': STABBOMANCER,
        #'/Game/PlayerCharacters/Beastmaster/PlayerClassId_Beastmaster.PlayerClassId_Beastmaster': BEASTMASTER,
        #'/Game/PlayerCharacters/Gunner/PlayerClassId_Gunner.PlayerClassId_Gunner': GUNNER,
        #'/Game/PlayerCharacters/Operative/PlayerClassId_Operative.PlayerClassId_Operative': OPERATIVE,
        #'/Game/PlayerCharacters/SirenBrawler/PlayerClassId_Siren.PlayerClassId_Siren': SIREN,
        }

# Pets
(LICH, WYVERN, MUSHROOM) = range(3)
pet_to_eng = {
        LICH: 'Demi-Lich',
        WYVERN: 'Wyvern',
        MUSHROOM: 'Mushroom',
        }
petkey_to_pet = {
        'petnicknamelich': LICH,
        # TODO: just guessing at these two
        'petnicknamewyvern': WYVERN,
        'petnicknamemushroom': MUSHROOM,
        }
pet_to_petkey = {v: k for k, v in petkey_to_pet.items()}

# Currencies
class Currency(HashLabelEnum):
    MONEY = ('Money', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Money.InventoryCategory_Money', 2000000000)
    MOON_ORBS = ('Moon Orbs', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_Eridium.InventoryCategory_Eridium', 16000)
    SOULS = ('Souls', '/Game/PatchDLC/Indigo1/Common/Pickups/IndCurrency/InventoryCategory_IndCurrency.InventoryCategory_IndCurrency', None)

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

# Challenges
(MAYHEM,
        CHAL_ARTIFACT,
        COM_BEASTMASTER,
        COM_GUNNER,
        COM_OPERATIVE,
        COM_SIREN,
        ) = range(6)
challenge_to_eng = {
        MAYHEM: 'Mayhem Mode',
        CHAL_ARTIFACT: 'Artifact Slot',
        COM_BEASTMASTER: 'Beastmaster COM Slot',
        COM_GUNNER: 'Gunner COM Slot',
        COM_OPERATIVE: 'Operative COM Slot',
        COM_SIREN: 'Siren COM Slot',
        }
challenge_char_lock = {
        #COM_BEASTMASTER: BEASTMASTER,
        #COM_GUNNER: GUNNER,
        #COM_OPERATIVE: OPERATIVE,
        #COM_SIREN: SIREN,
        }
challengeobj_to_challenge = {
        '/Game/GameData/Challenges/Account/Challenge_VaultReward_Mayhem.Challenge_VaultReward_Mayhem_C': MAYHEM,
        '/Game/GameData/Challenges/Account/Challenge_VaultReward_ArtifactSlot.Challenge_VaultReward_ArtifactSlot_C': CHAL_ARTIFACT,
        '/Game/GameData/Challenges/Character/Beastmaster/BP_Challenge_Beastmaster_ClassMod.BP_Challenge_Beastmaster_ClassMod_C': COM_BEASTMASTER,
        '/Game/GameData/Challenges/Character/Gunner/BP_Challenge_Gunner_ClassMod.BP_Challenge_Gunner_ClassMod_C': COM_GUNNER,
        '/Game/GameData/Challenges/Character/Operative/BP_Challenge_Operative_ClassMod.BP_Challenge_Operative_ClassMod_C': COM_OPERATIVE,
        '/Game/GameData/Challenges/Character/Siren/BP_Challenge_Siren_ClassMod.BP_Challenge_Siren_ClassMod_C': COM_SIREN,

        # This alone is not sufficient to unlock Sanctuary early
        #'/Game/GameData/Challenges/FastTravel/Challenge_FastTravel_Sanctuary3_2.Challenge_FastTravel_Sanctuary3_2_C': FOO,

        # Unlocking Fabricator really doesn't interest me; I think you'd need the item drop to go along with it, too.
        #'/Game/GameData/Challenges/Account/Challenge_VaultReward_Fabricator.Challenge_VaultReward_Fabricator_C': FOO,

        # Also, where are the other two gun slots?
        }
challenge_to_challengeobj = {v: k for k, v in challengeobj_to_challenge.items()}

# Level-based challenges (probably unimportant, but I've already started doing it,
# so here we go anyway)
level_stat = '/Game/PlayerCharacters/_Shared/_Design/Stats/Character/Stat_Character_Level.Stat_Character_Level'
level_challenges = [
        (2, '/Game/GameData/Challenges/System/BP_Challenge_Console_1.BP_Challenge_Console_1_C'),
        (10, '/Game/GameData/Challenges/System/BP_Challenge_Console_2.BP_Challenge_Console_2_C'),
        (25, '/Game/GameData/Challenges/System/BP_Challenge_Console_3.BP_Challenge_Console_3_C'),
        (50, '/Game/GameData/Challenges/System/BP_Challenge_Console_4.BP_Challenge_Console_4_C'),
        ]

# Profile customizations - Skins
# (all these customization sections omit the ones unlocked by default,
# which don't seem to show up in the profile usually)
profile_skins = set([
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomSkin_Beastmaster_DLC4_01.CustomSkin_Beastmaster_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomSkin_Gunner_DLC4_01.CustomSkin_Gunner_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomSkin_Operative__DLC4_01.CustomSkin_Operative__DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomSkin_Siren__DLC4_01.CustomSkin_Siren__DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_63.CustomSkin_Beastmaster_63',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_63.CustomSkin_Gunner_63',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_63.CustomSkin_Operative_63',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_63.CustomSkin_Siren_63',
    '/Game/PatchDLC/BloodyHarvest/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_40.CustomSkin_Beastmaster_40',
    '/Game/PatchDLC/BloodyHarvest/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_40.CustomSkin_Gunner_40',
    '/Game/PatchDLC/BloodyHarvest/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_40.CustomSkin_Operative_40',
    '/Game/PatchDLC/BloodyHarvest/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_40.CustomSkin_Siren_40',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_CS.CustomSkin_Beastmaster_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_CS.CustomSkin_Gunner_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_CS.CustomSkin_Operative_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_CS.CustomSkin_Siren_CS',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Beastmaster_44.CustomSkin_Beastmaster_44',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Beastmaster_46.CustomSkin_Beastmaster_46',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Gunner_44.CustomSkin_Gunner_44',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Gunner_46.CustomSkin_Gunner_46',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Operative_44.CustomSkin_Operative_44',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Operative_46.CustomSkin_Operative_46',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Siren_44.CustomSkin_Siren_44',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomSkin_Siren_46.CustomSkin_Siren_46',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_47.CustomSkin_Beastmaster_47',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_48.CustomSkin_Beastmaster_48',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_47.CustomSkin_Gunner_47',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_48.CustomSkin_Gunner_48',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_47.CustomSkin_Operative_47',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_48.CustomSkin_Operative_48',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_47.CustomSkin_Siren_47',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_48.CustomSkin_Siren_48',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Beastmaster_50.CustomSkin_Beastmaster_50',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Beastmaster_65.CustomSkin_Beastmaster_65',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Gunner_50.CustomSkin_Gunner_50',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Gunner_65.CustomSkin_Gunner_65',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Operative_50.CustomSkin_Operative_50',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Operative_65.CustomSkin_Operative_65',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Siren_50.CustomSkin_Siren_50',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomSkin_Siren_65.CustomSkin_Siren_65',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_61.CustomSkin_Beastmaster_61',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_61.CustomSkin_Gunner_61',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_61.CustomSkin_Operative_61',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Siren/Skins/CustomSkin_Siren_61.CustomSkin_Siren_61',
    '/Game/PatchDLC/Geranium/Customizations/PlayerSkin/CustomSkin_Beastmaster_DLC3_1.CustomSkin_Beastmaster_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerSkin/CustomSkin_Gunner_DLC3_1.CustomSkin_Gunner_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerSkin/CustomSkin_Operative_DLC3_1.CustomSkin_Operative_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerSkin/CustomSkin_Siren_DLC3_1.CustomSkin_Siren_DLC3_1',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomSkin_Beastmaster_DLC2_01.CustomSkin_Beastmaster_DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomSkin_Gunner_DLC2_01.CustomSkin_Gunner_DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomSkin_Operative__DLC2_01.CustomSkin_Operative__DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomSkin_Siren__DLC2_01.CustomSkin_Siren__DLC2_01',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin51/CustomSkin_Beastmaster_51.CustomSkin_Beastmaster_51',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin51/CustomSkin_Gunner_51.CustomSkin_Gunner_51',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin51/CustomSkin_Operative_51.CustomSkin_Operative_51',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin51/CustomSkin_Siren_51.CustomSkin_Siren_51',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin62/CustomSkin_Beastmaster_62.CustomSkin_Beastmaster_62',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin62/CustomSkin_Gunner_62.CustomSkin_Gunner_62',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin62/CustomSkin_Operative_62.CustomSkin_Operative_62',
    '/Game/PatchDLC/Ixora/PlayerCharacters/_Customizations/PlayerSkins/Skin62/CustomSkin_Siren_62.CustomSkin_Siren_62',
    '/Game/PatchDLC/Ixora2/PlayerCharacters/_Shared/Skins/CustomSkin_Beastmaster_66.CustomSkin_Beastmaster_66',
    '/Game/PatchDLC/Ixora2/PlayerCharacters/_Shared/Skins/CustomSkin_Gunner_66.CustomSkin_Gunner_66',
    '/Game/PatchDLC/Ixora2/PlayerCharacters/_Shared/Skins/CustomSkin_Operative_66.CustomSkin_Operative_66',
    '/Game/PatchDLC/Ixora2/PlayerCharacters/_Shared/Skins/CustomSkin_Siren_66.CustomSkin_Siren_66',
    '/Game/PatchDLC/Raid1/PlayerCharacters/_Customizations/Beastmaster/CustomSkin_Beastmaster_45.CustomSkin_Beastmaster_45',
    '/Game/PatchDLC/Raid1/PlayerCharacters/_Customizations/Gunner/CustomSkin_Gunner_45.CustomSkin_Gunner_45',
    '/Game/PatchDLC/Raid1/PlayerCharacters/_Customizations/Operative/CustomSkin_Operative_45.CustomSkin_Operative_45',
    '/Game/PatchDLC/Raid1/PlayerCharacters/_Customizations/Siren/CustomSkin_Siren_45.CustomSkin_Siren_45',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/PlayerSkins/CustomSkin_Beastmaster_52.CustomSkin_Beastmaster_52',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/PlayerSkins/CustomSkin_Gunner_52.CustomSkin_Gunner_52',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/PlayerSkins/CustomSkin_Operative_52.CustomSkin_Operative_52',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/PlayerSkins/CustomSkin_Siren_52.CustomSkin_Siren_52',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Beastmaster_67.CustomSkin_Beastmaster_67',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Beastmaster_68.CustomSkin_Beastmaster_68',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Beastmaster_69.CustomSkin_Beastmaster_69',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Beastmaster_70.CustomSkin_Beastmaster_70',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Gunner_67.CustomSkin_Gunner_67',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Gunner_68.CustomSkin_Gunner_68',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Gunner_69.CustomSkin_Gunner_69',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Gunner_70.CustomSkin_Gunner_70',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Operative_67.CustomSkin_Operative_67',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Operative_68.CustomSkin_Operative_68',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Operative_69.CustomSkin_Operative_69',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Operative_70.CustomSkin_Operative_70',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Siren_67.CustomSkin_Siren_67',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Siren_68.CustomSkin_Siren_68',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Siren_69.CustomSkin_Siren_69',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomSkin_Siren_70.CustomSkin_Siren_70',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Beastmaster_75.CustomSkin_Beastmaster_75',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Beastmaster_76.CustomSkin_Beastmaster_76',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Beastmaster_77.CustomSkin_Beastmaster_77',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Beastmaster_78.CustomSkin_Beastmaster_78',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Gunner_75.CustomSkin_Gunner_75',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Gunner_76.CustomSkin_Gunner_76',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Gunner_77.CustomSkin_Gunner_77',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Gunner_78.CustomSkin_Gunner_78',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Operative_75.CustomSkin_Operative_75',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Operative_76.CustomSkin_Operative_76',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Operative_77.CustomSkin_Operative_77',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Operative_78.CustomSkin_Operative_78',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Siren_75.CustomSkin_Siren_75',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Siren_76.CustomSkin_Siren_76',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Siren_77.CustomSkin_Siren_77',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomSkin_Siren_78.CustomSkin_Siren_78',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Beastmaster_71.CustomSkin_Beastmaster_71',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Beastmaster_72.CustomSkin_Beastmaster_72',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Beastmaster_73.CustomSkin_Beastmaster_73',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Beastmaster_74.CustomSkin_Beastmaster_74',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Gunner_71.CustomSkin_Gunner_71',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Gunner_72.CustomSkin_Gunner_72',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Gunner_73.CustomSkin_Gunner_73',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Gunner_74.CustomSkin_Gunner_74',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Operative_71.CustomSkin_Operative_71',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Operative_72.CustomSkin_Operative_72',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Operative_73.CustomSkin_Operative_73',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Operative_74.CustomSkin_Operative_74',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Siren_71.CustomSkin_Siren_71',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Siren_72.CustomSkin_Siren_72',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Siren_73.CustomSkin_Siren_73',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomSkin_Siren_74.CustomSkin_Siren_74',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Beastmaster/_Shared/Skins/CustomSkin_Beastmaster_38.CustomSkin_Beastmaster_38',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Gunner/_Shared/Skins/CustomSkin_Gunner_38.CustomSkin_Gunner_38',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Operative/_Shared/Skins/CustomSkin_Operative_38.CustomSkin_Operative_38',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/SirenBrawler/_Shared/Skins/CustomSkin_Siren_38.CustomSkin_Siren_38',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_1.CustomSkin_Beastmaster_1',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_10.CustomSkin_Beastmaster_10',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_11.CustomSkin_Beastmaster_11',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_12.CustomSkin_Beastmaster_12',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_13.CustomSkin_Beastmaster_13',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_14.CustomSkin_Beastmaster_14',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_15.CustomSkin_Beastmaster_15',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_16.CustomSkin_Beastmaster_16',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_17.CustomSkin_Beastmaster_17',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_18.CustomSkin_Beastmaster_18',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_19.CustomSkin_Beastmaster_19',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_2.CustomSkin_Beastmaster_2',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_20.CustomSkin_Beastmaster_20',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_21.CustomSkin_Beastmaster_21',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_22.CustomSkin_Beastmaster_22',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_23.CustomSkin_Beastmaster_23',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_24.CustomSkin_Beastmaster_24',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_25.CustomSkin_Beastmaster_25',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_26.CustomSkin_Beastmaster_26',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_27.CustomSkin_Beastmaster_27',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_28.CustomSkin_Beastmaster_28',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_29.CustomSkin_Beastmaster_29',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_3.CustomSkin_Beastmaster_3',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_30.CustomSkin_Beastmaster_30',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_31.CustomSkin_Beastmaster_31',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_32.CustomSkin_Beastmaster_32',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_34.CustomSkin_Beastmaster_34',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_35.CustomSkin_Beastmaster_35',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_36.CustomSkin_Beastmaster_36',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_37.CustomSkin_Beastmaster_37',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_39.CustomSkin_Beastmaster_39',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_4.CustomSkin_Beastmaster_4',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_41.CustomSkin_Beastmaster_41',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_42.CustomSkin_Beastmaster_42',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_43.CustomSkin_Beastmaster_43',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_5.CustomSkin_Beastmaster_5',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_6.CustomSkin_Beastmaster_6',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_7.CustomSkin_Beastmaster_7',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_8.CustomSkin_Beastmaster_8',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_9.CustomSkin_Beastmaster_9',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_1.CustomSkin_Gunner_1',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_10.CustomSkin_Gunner_10',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_11.CustomSkin_Gunner_11',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_12.CustomSkin_Gunner_12',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_13.CustomSkin_Gunner_13',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_14.CustomSkin_Gunner_14',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_15.CustomSkin_Gunner_15',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_16.CustomSkin_Gunner_16',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_17.CustomSkin_Gunner_17',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_18.CustomSkin_Gunner_18',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_19.CustomSkin_Gunner_19',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_2.CustomSkin_Gunner_2',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_20.CustomSkin_Gunner_20',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_21.CustomSkin_Gunner_21',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_22.CustomSkin_Gunner_22',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_23.CustomSkin_Gunner_23',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_24.CustomSkin_Gunner_24',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_25.CustomSkin_Gunner_25',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_26.CustomSkin_Gunner_26',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_27.CustomSkin_Gunner_27',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_28.CustomSkin_Gunner_28',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_29.CustomSkin_Gunner_29',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_3.CustomSkin_Gunner_3',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_30.CustomSkin_Gunner_30',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_31.CustomSkin_Gunner_31',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_32.CustomSkin_Gunner_32',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_34.CustomSkin_Gunner_34',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_35.CustomSkin_Gunner_35',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_36.CustomSkin_Gunner_36',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_37.CustomSkin_Gunner_37',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_39.CustomSkin_Gunner_39',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_4.CustomSkin_Gunner_4',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_41.CustomSkin_Gunner_41',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_42.CustomSkin_Gunner_42',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_43.CustomSkin_Gunner_43',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_5.CustomSkin_Gunner_5',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_6.CustomSkin_Gunner_6',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_7.CustomSkin_Gunner_7',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_8.CustomSkin_Gunner_8',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_9.CustomSkin_Gunner_9',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_1.CustomSkin_Operative_1',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_10.CustomSkin_Operative_10',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_11.CustomSkin_Operative_11',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_12.CustomSkin_Operative_12',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_13.CustomSkin_Operative_13',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_14.CustomSkin_Operative_14',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_15.CustomSkin_Operative_15',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_16.CustomSkin_Operative_16',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_17.CustomSkin_Operative_17',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_18.CustomSkin_Operative_18',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_19.CustomSkin_Operative_19',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_2.CustomSkin_Operative_2',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_20.CustomSkin_Operative_20',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_21.CustomSkin_Operative_21',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_22.CustomSkin_Operative_22',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_23.CustomSkin_Operative_23',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_24.CustomSkin_Operative_24',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_25.CustomSkin_Operative_25',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_26.CustomSkin_Operative_26',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_27.CustomSkin_Operative_27',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_28.CustomSkin_Operative_28',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_29.CustomSkin_Operative_29',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_3.CustomSkin_Operative_3',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_30.CustomSkin_Operative_30',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_31.CustomSkin_Operative_31',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_32.CustomSkin_Operative_32',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_34.CustomSkin_Operative_34',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_35.CustomSkin_Operative_35',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_36.CustomSkin_Operative_36',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_37.CustomSkin_Operative_37',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_39.CustomSkin_Operative_39',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_4.CustomSkin_Operative_4',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_41.CustomSkin_Operative_41',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_42.CustomSkin_Operative_42',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_43.CustomSkin_Operative_43',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_5.CustomSkin_Operative_5',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_6.CustomSkin_Operative_6',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_7.CustomSkin_Operative_7',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_8.CustomSkin_Operative_8',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_9.CustomSkin_Operative_9',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_1.CustomSkin_Siren_1',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_10.CustomSkin_Siren_10',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_11.CustomSkin_Siren_11',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_12.CustomSkin_Siren_12',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_13.CustomSkin_Siren_13',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_14.CustomSkin_Siren_14',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_15.CustomSkin_Siren_15',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_16.CustomSkin_Siren_16',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_17.CustomSkin_Siren_17',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_18.CustomSkin_Siren_18',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_19.CustomSkin_Siren_19',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_2.CustomSkin_Siren_2',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_20.CustomSkin_Siren_20',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_21.CustomSkin_Siren_21',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_22.CustomSkin_Siren_22',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_23.CustomSkin_Siren_23',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_24.CustomSkin_Siren_24',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_25.CustomSkin_Siren_25',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_26.CustomSkin_Siren_26',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_27.CustomSkin_Siren_27',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_28.CustomSkin_Siren_28',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_29.CustomSkin_Siren_29',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_3.CustomSkin_Siren_3',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_30.CustomSkin_Siren_30',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_31.CustomSkin_Siren_31',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_32.CustomSkin_Siren_32',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_34.CustomSkin_Siren_34',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_35.CustomSkin_Siren_35',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_36.CustomSkin_Siren_36',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_37.CustomSkin_Siren_37',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_39.CustomSkin_Siren_39',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_4.CustomSkin_Siren_4',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_41.CustomSkin_Siren_41',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_42.CustomSkin_Siren_42',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_43.CustomSkin_Siren_43',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_5.CustomSkin_Siren_5',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_6.CustomSkin_Siren_6',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_7.CustomSkin_Siren_7',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_8.CustomSkin_Siren_8',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_9.CustomSkin_Siren_9',
    ])
profile_skins_defaults = set([
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Skins/CustomSkin_Beastmaster_Default.CustomSkin_Beastmaster_Default',
    '/Game/PlayerCharacters/_Customizations/Gunner/Skins/CustomSkin_Gunner_Default.CustomSkin_Gunner_Default',
    '/Game/PlayerCharacters/_Customizations/Operative/Skins/CustomSkin_Operative_Default.CustomSkin_Operative_Default',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Skins/CustomSkin_Siren_Default.CustomSkin_Siren_Default',
    ])

# Profile customizations - Heads
profile_heads = set([
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomHead_Beastmaster_DLC4_01.CustomHead_Beastmaster_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomHead_Gunner_DLC4_01.CustomHead_Gunner_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomHead_Operative_DLC4_01.CustomHead_Operative_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/_Shared/CustomHead_Siren_DLC4_01.CustomHead_Siren_DLC4_01',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_CS.CustomHead_Beastmaster_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_CS.CustomHead_Gunner_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_CS.CustomHead_Operative_CS',
    '/Game/PatchDLC/CitizenScience/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_CS.CustomHead_Siren_CS',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_25.CustomHead_Beastmaster_25',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_27.CustomHead_Beastmaster_27',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_28.CustomHead_Beastmaster_28',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_29.CustomHead_Beastmaster_29',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_25.CustomHead_Gunner_25',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_27.CustomHead_Gunner_27',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_28.CustomHead_Gunner_28',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_29.CustomHead_Gunner_29',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_25.CustomHead_Operative_25',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_27.CustomHead_Operative_27',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_28.CustomHead_Operative_28',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_29.CustomHead_Operative_29',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_25.CustomHead_Siren_25',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_27.CustomHead_Siren_27',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_28.CustomHead_Siren_28',
    '/Game/PatchDLC/Customizations/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_29.CustomHead_Siren_29',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomHead_Beastmaster_30.CustomHead_Beastmaster_30',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomHead_Gunner_30.CustomHead_Gunner_30',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomHead_Operative_30.CustomHead_Operative_30',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/_Shared/CustomHead_Siren_30.CustomHead_Siren_30',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_34.CustomHead_Beastmaster_34',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_34.CustomHead_Gunner_34',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_34.CustomHead_Operative_34',
    '/Game/PatchDLC/Event2/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_34.CustomHead_Siren_34',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomHead_BeastMaster_Twitch.CustomHead_BeastMaster_Twitch',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomHead_Gunner_Twitch.CustomHead_Gunner_Twitch',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomHead_Operative_Twitch.CustomHead_Operative_Twitch',
    '/Game/PatchDLC/EventVDay/PlayerCharacters/_Shared/CustomHead_Siren_Twitch.CustomHead_Siren_Twitch',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Beastmaster/Heads/DA_BMHead33.DA_BMHead33',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Beastmaster/Heads/DA_BMHead35.DA_BMHead35',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Beastmaster/Heads/DA_BMHead36.DA_BMHead36',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Beastmaster/Heads/DA_BMHead37.DA_BMHead37',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Gunner/Heads/DA_GNRHead33.DA_GNRHead33',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Gunner/Heads/DA_GNRHead35.DA_GNRHead35',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Gunner/Heads/DA_GNRHead36.DA_GNRHead36',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Gunner/Heads/DA_GNRHead37.DA_GNRHead37',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Operative/Heads/DA_OPHead33.DA_OPHead33',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Operative/Heads/DA_OPHead35.DA_OPHead35',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Operative/Heads/DA_OPHead36.DA_OPHead36',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Operative/Heads/DA_OPHead37.DA_OPHead37',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Siren/Heads/DA_SRNHead33.DA_SRNHead33',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Siren/Heads/DA_SRNHead35.DA_SRNHead35',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Siren/Heads/DA_SRNHead36.DA_SRNHead36',
    '/Game/PatchDLC/EventVDay/TwitchDrops/PlayerCharacters/_Customizations/Siren/Heads/DA_SRNHead37.DA_SRNHead37',
    '/Game/PatchDLC/Geranium/Customizations/PlayerHead/CustomHead38/CustomHead_Beastmaster_38.CustomHead_Beastmaster_38',
    '/Game/PatchDLC/Geranium/Customizations/PlayerHead/CustomHead38/CustomHead_Gunner_38.CustomHead_Gunner_38',
    '/Game/PatchDLC/Geranium/Customizations/PlayerHead/CustomHead38/CustomHead_Operative_38.CustomHead_Operative_38',
    '/Game/PatchDLC/Geranium/Customizations/PlayerHead/CustomHead38/CustomHead_Siren_38.CustomHead_Siren_38',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomHead_Beastmaster_DLC2_01.CustomHead_Beastmaster_DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomHead_Gunner_DLC2_01.CustomHead_Gunner_DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomHead_Operative_DLC2_01.CustomHead_Operative_DLC2_01',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/_Shared/CustomHead_Siren_DLC2_01.CustomHead_Siren_DLC2_01',
    '/Game/PatchDLC/Ixora/PlayerCharacters/Beastmaster/Heads/DA_BMHead39.DA_BMHead39',
    '/Game/PatchDLC/Ixora/PlayerCharacters/Gunner/Heads/DA_GNRHead39.DA_GNRHead39',
    '/Game/PatchDLC/Ixora/PlayerCharacters/Operative/Heads/DA_OPHead39.DA_OPHead39',
    '/Game/PatchDLC/Ixora/PlayerCharacters/SirenBrawler/Heads/DA_SRNHead39.DA_SRNHead39',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/CustomHeads/CustomHead46/CustomHead_Beastmaster_46.CustomHead_Beastmaster_46',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/CustomHeads/CustomHead46/CustomHead_Gunner_46.CustomHead_Gunner_46',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/CustomHeads/CustomHead46/CustomHead_Operative_46.CustomHead_Operative_46',
    '/Game/PatchDLC/Takedown2/PlayerCharacters/_Customizations/CustomHeads/CustomHead46/CustomHead_Siren_46.CustomHead_Siren_46',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomHeads/CustomHead47/CustomHead_Beastmaster_47.CustomHead_Beastmaster_47',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomHeads/CustomHead47/CustomHead_Gunner_47.CustomHead_Gunner_47',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomHeads/CustomHead47/CustomHead_Operative_47.CustomHead_Operative_47',
    '/Game/PatchDLC/VaultCard/PlayerCharacters/_Shared/CustomHeads/CustomHead47/CustomHead_Siren_47.CustomHead_Siren_47',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomHeads/CustomHead_Beastmaster_49.CustomHead_Beastmaster_49',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomHeads/CustomHead_Gunner_49.CustomHead_Gunner_49',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomHeads/CustomHead_Operative_49.CustomHead_Operative_49',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/_Shared/CustomHeads/CustomHead_Siren_49.CustomHead_Siren_49',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/Beastmaster/Heads/DA_BMHead03.DA_BMHead03',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/Gunner/Heads/DA_GNRHead03.DA_GNRHead03',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/Operative/Heads/DA_OPHead03.DA_OPHead03',
    '/Game/PatchDLC/VaultCard2/PlayerCharacters/SirenBrawler/Heads/DA_SRNHead03.DA_SRNHead03',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Beastmaster_32.CustomHead_Beastmaster_32',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Beastmaster_48.CustomHead_Beastmaster_48',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Gunner_32.CustomHead_Gunner_32',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Gunner_48.CustomHead_Gunner_48',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Operative_32.CustomHead_Operative_32',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Operative_48.CustomHead_Operative_48',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Siren_32.CustomHead_Siren_32',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/_Shared/CustomHeads/CustomHead_Siren_48.CustomHead_Siren_48',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Beastmaster/Heads/DA_BMHead40.DA_BMHead40',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Beastmaster/Heads/DA_BMHead41.DA_BMHead41',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Beastmaster/Heads/DA_BMHead42.DA_BMHead42',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Beastmaster/Heads/DA_BMHead44.DA_BMHead44',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Gunner/Heads/DA_GNRHead40.DA_GNRHead40',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Gunner/Heads/DA_GNRHead41.DA_GNRHead41',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Gunner/Heads/DA_GNRHead42.DA_GNRHead42',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Gunner/Heads/DA_GNRHead44.DA_GNRHead44',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Operative/Heads/DA_OPHead40.DA_OPHead40',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Operative/Heads/DA_OPHead41.DA_OPHead41',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Operative/Heads/DA_OPHead42.DA_OPHead42',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/Operative/Heads/DA_OPHead44.DA_OPHead44',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/SirenBrawler/Heads/DA_SRNHead40.DA_SRNHead40',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/SirenBrawler/Heads/DA_SRNHead41.DA_SRNHead41',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/SirenBrawler/Heads/DA_SRNHead42.DA_SRNHead42',
    '/Game/PatchDLC/VaultCard3/PlayerCharacters/SirenBrawler/Heads/SRNHead44/DA_SRNHead44.DA_SRNHead44',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_1.CustomHead_Beastmaster_1',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_10.CustomHead_Beastmaster_10',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_11.CustomHead_Beastmaster_11',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_12.CustomHead_Beastmaster_12',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_13.CustomHead_Beastmaster_13',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_14.CustomHead_Beastmaster_14',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_15.CustomHead_Beastmaster_15',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_16.CustomHead_Beastmaster_16',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_17.CustomHead_Beastmaster_17',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_18.CustomHead_Beastmaster_18',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_19.CustomHead_Beastmaster_19',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_20.CustomHead_Beastmaster_20',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_21.CustomHead_Beastmaster_21',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_22.CustomHead_Beastmaster_22',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_23.CustomHead_Beastmaster_23',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_24.CustomHead_Beastmaster_24',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_26.CustomHead_Beastmaster_26',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_4.CustomHead_Beastmaster_4',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_5.CustomHead_Beastmaster_5',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_6.CustomHead_Beastmaster_6',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_7.CustomHead_Beastmaster_7',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_8.CustomHead_Beastmaster_8',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_9.CustomHead_Beastmaster_9',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_1.CustomHead_Gunner_1',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_10.CustomHead_Gunner_10',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_11.CustomHead_Gunner_11',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_12.CustomHead_Gunner_12',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_13.CustomHead_Gunner_13',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_14.CustomHead_Gunner_14',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_15.CustomHead_Gunner_15',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_16.CustomHead_Gunner_16',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_17.CustomHead_Gunner_17',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_18.CustomHead_Gunner_18',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_19.CustomHead_Gunner_19',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_20.CustomHead_Gunner_20',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_21.CustomHead_Gunner_21',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_22.CustomHead_Gunner_22',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_23.CustomHead_Gunner_23',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_24.CustomHead_Gunner_24',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_26.CustomHead_Gunner_26',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_4.CustomHead_Gunner_4',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_5.CustomHead_Gunner_5',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_6.CustomHead_Gunner_6',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_7.CustomHead_Gunner_7',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_8.CustomHead_Gunner_8',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_9.CustomHead_Gunner_9',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_1.CustomHead_Operative_1',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_10.CustomHead_Operative_10',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_11.CustomHead_Operative_11',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_12.CustomHead_Operative_12',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_13.CustomHead_Operative_13',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_14.CustomHead_Operative_14',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_15.CustomHead_Operative_15',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_16.CustomHead_Operative_16',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_17.CustomHead_Operative_17',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_18.CustomHead_Operative_18',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_19.CustomHead_Operative_19',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_20.CustomHead_Operative_20',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_21.CustomHead_Operative_21',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_22.CustomHead_Operative_22',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_23.CustomHead_Operative_23',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_24.CustomHead_Operative_24',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_26.CustomHead_Operative_26',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_4.CustomHead_Operative_4',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_5.CustomHead_Operative_5',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_6.CustomHead_Operative_6',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_7.CustomHead_Operative_7',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_8.CustomHead_Operative_8',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_9.CustomHead_Operative_9',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_1.CustomHead_Siren_1',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_10.CustomHead_Siren_10',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_11.CustomHead_Siren_11',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_12.CustomHead_Siren_12',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_13.CustomHead_Siren_13',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_14.CustomHead_Siren_14',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_15.CustomHead_Siren_15',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_16.CustomHead_Siren_16',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_17.CustomHead_Siren_17',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_18.CustomHead_Siren_18',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_19.CustomHead_Siren_19',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_20.CustomHead_Siren_20',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_21.CustomHead_Siren_21',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_22.CustomHead_Siren_22',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_23.CustomHead_Siren_23',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_24.CustomHead_Siren_24',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_26.CustomHead_Siren_26',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_4.CustomHead_Siren_4',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_5.CustomHead_Siren_5',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_6.CustomHead_Siren_6',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_7.CustomHead_Siren_7',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_8.CustomHead_Siren_8',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_9.CustomHead_Siren_9',
    ])
profile_heads_defaults = set([
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Heads/CustomHead_Beastmaster_Default.CustomHead_Beastmaster_Default',
    '/Game/PlayerCharacters/_Customizations/Gunner/Heads/CustomHead_Gunner_Default.CustomHead_Gunner_Default',
    '/Game/PlayerCharacters/_Customizations/Operative/Heads/CustomHead_Operative_Default.CustomHead_Operative_Default',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Heads/CustomHead_Siren_Default.CustomHead_Siren_Default',
    ])

# Profile customizations - Emotes
profile_emotes = set([
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_DLC4_01.CustomEmote_Beastmaster_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_DLC4_02.CustomEmote_Beastmaster_DLC4_02',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_DLC4_01.CustomEmote_Gunner_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_DLC4_02.CustomEmote_Gunner_DLC4_02',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_DLC4_01.CustomEmote_Operative_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_DLC4_02.CustomEmote_Operative_DLC4_02',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_DLC4_01.CustomEmote_Siren_DLC4_01',
    '/Game/PatchDLC/Alisma/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_DLC4_02.CustomEmote_Siren_DLC4_02',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_13_HandsomeJack.CustomEmote_Beastmaster_13_HandsomeJack',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_14_MakeItRain.CustomEmote_Beastmaster_14_MakeItRain',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_13_Handsome_Jack.CustomEmote_Gunner_13_Handsome_Jack',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_14_MakeItRain.CustomEmote_Gunner_14_MakeItRain',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_13_HandsomeJack.CustomEmote_Operative_13_HandsomeJack',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_14_MakeItRain.CustomEmote_Operative_14_MakeItRain',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_13_HandsomeJack.CustomEmote_Siren_13_HandsomeJack',
    '/Game/PatchDLC/Dandelion/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_14_MakeItRain.CustomEmote_Siren_14_MakeItRain',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Beastmaster_DLC3_1.CustomEmote_Beastmaster_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Beastmaster_DLC3_2.CustomEmote_Beastmaster_DLC3_2',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Gunner_DLC3_1.CustomEmote_Gunner_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Gunner_DLC3_2.CustomEmote_Gunner_DLC3_2',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Operative_DLC3_1.CustomEmote_Operative_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Operative_DLC3_2.CustomEmote_Operative_DLC3_2',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Siren_DLC3_1.CustomEmote_Siren_DLC3_1',
    '/Game/PatchDLC/Geranium/Customizations/PlayerEmote/CustomEmote_Siren_DLC3_2.CustomEmote_Siren_DLC3_2',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_15.CustomEmote_Beastmaster_15',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_16.CustomEmote_Beastmaster_16',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_15.CustomEmote_Gunner_15',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Gunner/CustomEmote_Gunner_16.CustomEmote_Gunner_16',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_15.CustomEmote_Operative_15',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/Operative/CustomEmote_Operative_16.CustomEmote_Operative_16',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_15.CustomEmote_Siren_15',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Customizations/Emotes/SirenBrawler/CustomEmote_Siren_16.CustomEmote_Siren_16',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC1_1.CustomEmote_Beastmaster_VC1_1',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC1_2.CustomEmote_Beastmaster_VC1_2',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC1_1.CustomEmote_Gunner_VC1_1',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC1_2.CustomEmote_Gunner_VC1_2',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Operative/CustomEmote_Operative_VC1_1.CustomEmote_Operative_VC1_1',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/Operative/CustomEmote_Operative_VC1_2.CustomEmote_Operative_VC1_2',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/SirenBrawler/CustomEmote_Siren_VC1_1.CustomEmote_Siren_VC1_1',
    '/Game/PatchDLC/VaultCard/Customizations/Emotes/SirenBrawler/CustomEmote_Siren_VC1_2.CustomEmote_Siren_VC1_2',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC2_1.CustomEmote_Beastmaster_VC2_1',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC2_2.CustomEmote_Beastmaster_VC2_2',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC2_1.CustomEmote_Gunner_VC2_1',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC2_2.CustomEmote_Gunner_VC2_2',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Operative/CustomEmote_Operative_VC2_1.CustomEmote_Operative_VC2_1',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Operative/CustomEmote_Operative_VC2_2.CustomEmote_Operative_VC2_2',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Siren/CustomEmote_Siren_VC2_1.CustomEmote_Siren_VC2_1',
    '/Game/PatchDLC/VaultCard2/Customizations/Emotes/Siren/CustomEmote_Siren_VC2_2.CustomEmote_Siren_VC2_2',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC3_1.CustomEmote_Beastmaster_VC3_1',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC3_2.CustomEmote_Beastmaster_VC3_2',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Beastmaster/CustomEmote_Beastmaster_VC3_3.CustomEmote_Beastmaster_VC3_3',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC3_1.CustomEmote_Gunner_VC3_1',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC3_2.CustomEmote_Gunner_VC3_2',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Gunner/CustomEmote_Gunner_VC3_3.CustomEmote_Gunner_VC3_3',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Operative/CustomEmote_Operative_VC3_1.CustomEmote_Operative_VC3_1',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Operative/CustomEmote_Operative_VC3_2.CustomEmote_Operative_VC3_2',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Operative/CustomEmote_Operative_VC3_3.CustomEmote_Operative_VC3_3',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Siren/CustomEmote_Siren_VC3_1.CustomEmote_Siren_VC3_1',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Siren/CustomEmote_Siren_VC3_2.CustomEmote_Siren_VC3_2',
    '/Game/PatchDLC/VaultCard3/Customizations/Emotes/Siren/CustomEmote_Siren_VC3_3.CustomEmote_Siren_VC3_3',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_05_Heart.CustomEmote_Beastmaster_05_Heart',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_06_FingerGuns.CustomEmote_Beastmaster_06_FingerGuns',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_09_RobotDance.CustomEmote_Beastmaster_09_RobotDance',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_10_KickDance.CustomEmote_Beastmaster_10_KickDance',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_11_Chicken_Dance.CustomEmote_Beastmaster_11_Chicken_Dance',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_12_Death.CustomEmote_Beastmaster_12_Death',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_05_Heart.CustomEmote_Gunner_05_Heart',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_06_FingerGuns.CustomEmote_Gunner_06_FingerGuns',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_09_RobotDance.CustomEmote_Gunner_09_RobotDance',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_10_KickDance.CustomEmote_Gunner_10_KickDance',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_11_ChickenDance.CustomEmote_Gunner_11_ChickenDance',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_12_Death.CustomEmote_Gunner_12_Death',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_05_Heart.CustomEmote_Operative_05_Heart',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_06_FingerGuns.CustomEmote_Operative_06_FingerGuns',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_09_RobotDance.CustomEmote_Operative_09_RobotDance',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_10_KickDance.CustomEmote_Operative_10_KickDance',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_11_ChickenDance.CustomEmote_Operative_11_ChickenDance',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_12_Death.CustomEmote_Operative_12_Death',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_05_Heart.CustomEmote_Siren_05_Heart',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_06_FingerGuns.CustomEmote_Siren_06_FingerGuns',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_09_RobotDance.CustomEmote_Siren_09_RobotDance',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_10_KickDance.CustomEmote_Siren_10_KickDance',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_11_ChickenDance.CustomEmote_Siren_11_ChickenDance',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_12_Death.CustomEmote_Siren_12_Death',
    ])
profile_emotes_defaults = set([
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_01_Wave.CustomEmote_Beastmaster_01_Wave',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_02_Cheer.CustomEmote_Beastmaster_02_Cheer',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_03_Point.CustomEmote_Beastmaster_03_Point',
    '/Game/PlayerCharacters/_Customizations/Beastmaster/Emotes/CustomEmote_Beastmaster_04_Laugh.CustomEmote_Beastmaster_04_Laugh',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_01_Wave.CustomEmote_Gunner_01_Wave',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_02_Cheer.CustomEmote_Gunner_02_Cheer',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_03_Point.CustomEmote_Gunner_03_Point',
    '/Game/PlayerCharacters/_Customizations/Gunner/Emotes/CustomEmote_Gunner_04_Laugh.CustomEmote_Gunner_04_Laugh',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_01_Wave.CustomEmote_Operative_01_Wave',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_02_Cheer.CustomEmote_Operative_02_Cheer',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_03_Point.CustomEmote_Operative_03_Point',
    '/Game/PlayerCharacters/_Customizations/Operative/Emotes/CustomEmote_Operative_04_Laugh.CustomEmote_Operative_04_Laugh',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_01_Wave.CustomEmote_Siren_01_Wave',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_02_Cheer.CustomEmote_Siren_02_Cheer',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_03_Point.CustomEmote_Siren_03_Point',
    '/Game/PlayerCharacters/_Customizations/SirenBrawler/Emotes/CustomEmote_Siren_04_Laugh.CustomEmote_Siren_04_Laugh',
    ])

# Skeleton Keys
class Key(HashLabelEnum):
    SKELETON = ('Skeleton Keys', '/Game/Gear/_Shared/_Design/InventoryCategories/InventoryCategory_GoldenKey')

# XP
max_level = 40
required_xp_list = [
    0,          # lvl 1
    358,        # lvl 2
    1241,       # lvl 3
    2850,       # lvl 4
    5376,       # lvl 5
    8997,       # lvl 6
    13886,      # lvl 7
    20208,      # lvl 8
    28126,      # lvl 9
    37798,      # lvl 10
    49377,      # lvl 11
    63016,      # lvl 12
    78861,      # lvl 13
    97061,      # lvl 14
    117757,     # lvl 15
    141092,     # lvl 16
    167206,     # lvl 17
    196238,     # lvl 18
    228322,     # lvl 19
    263595,     # lvl 20
    302190,     # lvl 21
    344238,     # lvl 22
    389873,     # lvl 23
    439222,     # lvl 24
    492414,     # lvl 25
    549578,     # lvl 26
    610840,     # lvl 27
    676325,     # lvl 28
    746158,     # lvl 29
    820463,     # lvl 30
    899363,     # lvl 31
    982980,     # lvl 32
    1071435,    # lvl 33
    1164850,    # lvl 34
    1263343,    # lvl 35
    1367034,    # lvl 36
    1476041,    # lvl 37
    1590483,    # lvl 38
    1710476,    # lvl 39
    1836137,    # lvl 40
    1967582,    # lvl 41
    2104926,    # lvl 42
    2248285,    # lvl 43
    2397772,    # lvl 44
    2553501,    # lvl 45
    2715586,    # lvl 46
    2884139,    # lvl 47
    3059273,    # lvl 48
    3241098,    # lvl 49
    3429728,    # lvl 50
    3625271,    # lvl 51
    3827840,    # lvl 52
    4037543,    # lvl 53
    4254491,    # lvl 54
    4478792,    # lvl 55
    4710556,    # lvl 56
    4949890,    # lvl 57
    5196902,    # lvl 58
    5451701,    # lvl 59
    5714393,    # lvl 60
    5985086,    # lvl 61
    6263885,    # lvl 62
    6550897,    # lvl 63
    6846227,    # lvl 64
    7149982,    # lvl 65
    7462266,    # lvl 66
    7783184,    # lvl 67
    8112840,    # lvl 68
    8451340,    # lvl 69
    8798786,    # lvl 70
    9155282,    # lvl 71
    9520932,    # lvl 72
    9895837,    # lvl 73
    10280103,    # lvl 74
    10673830,    # lvl 75
    11077120,    # lvl 76
    11490077,    # lvl 77
    11912801,    # lvl 78
    12345393,    # lvl 79
    12787955,    # lvl 80
]
max_supported_level = len(required_xp_list)

# Mayhem parts
mayhem_part_to_lvl = {
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_01.Part_WeaponMayhemLevel_01': 1,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_02.Part_WeaponMayhemLevel_02': 2,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_03.Part_WeaponMayhemLevel_03': 3,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_04.Part_WeaponMayhemLevel_04': 4,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_05.Part_WeaponMayhemLevel_05': 5,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_06.Part_WeaponMayhemLevel_06': 6,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_07.Part_WeaponMayhemLevel_07': 7,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_08.Part_WeaponMayhemLevel_08': 8,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_09.Part_WeaponMayhemLevel_09': 9,
        '/Game/PatchDLC/Mayhem2/Gear/Weapon/_Shared/_Design/MayhemParts/Part_WeaponMayhemLevel_10.Part_WeaponMayhemLevel_10': 10,
        }
mayhem_part_lower_to_lvl = {k.lower(): v for k, v in mayhem_part_to_lvl.items()}
mayhem_lvl_to_part = {v: k for k, v in mayhem_part_to_lvl.items()}
mayhem_max = max(mayhem_part_to_lvl.values())

# InvData types which can accept Mayhem parts
# (may have to be more clever about this if non-guns start accepting *different* Mayhem parts)
mayhem_invdata_types = set([
    '/Game/Gear/Weapons/AssaultRifles/Atlas/_Shared/_Design/WT_AR_ATL.WT_AR_ATL',
    '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/WT_AR_COV.WT_AR_COV',
    '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/WT_AR_DAL.WT_AR_DAL',
    '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/WT_AR_JAK.WT_AR_JAK',
    '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/WT_AR_TOR.WT_AR_TOR',
    '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/WT_AR_VLA.WT_AR_VLA',
    '/Game/Gear/Weapons/HeavyWeapons/ATL/_Shared/_Design/WT_HW_ATL.WT_HW_ATL',
    '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/WT_HW_COV.WT_HW_COV',
    '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/WT_HW_TOR.WT_HW_TOR',
    '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/WT_HW_VLA.WT_HW_VLA',
    '/Game/Gear/Weapons/Pistols/Atlas/_Shared/_Design/WT_PS_ATL.WT_PS_ATL',
    '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/WT_PS_COV.WT_PS_COV',
    '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/WT_PS_DAL.WT_PS_DAL',
    '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/WT_PS_JAK.WT_PS_JAK',
    '/Game/Gear/Weapons/Pistols/Maliwan/_Shared/_Design/WT_PS_MAL.WT_PS_MAL',
    '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/WT_PS_TED.WT_PS_TED',
    '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/WT_PS_TOR.WT_PS_TOR',
    '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/WT_PS_VLA.WT_PS_VLA',
    '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/WT_SM_DAL.WT_SM_DAL',
    '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/WT_SM_HYP.WT_SM_HYP',
    '/Game/Gear/Weapons/SMGs/Maliwan/_Shared/_Design/WT_SM_MAL.WT_SM_MAL',
    '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/WT_SM_TED.WT_SM_TED',
    '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/WT_SG_HYP.WT_SG_HYP',
    '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/WT_SG_JAK.WT_SG_JAK',
    '/Game/Gear/Weapons/Shotguns/Maliwan/_Shared/_Design/WT_SG_MAL.WT_SG_MAL',
    '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/WT_SG_TED.WT_SG_TED',
    '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/WT_SG_TOR.WT_SG_TOR',
    '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/WT_SR_DAL.WT_SR_DAL',
    '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/WT_SR_HYP.WT_SR_HYP',
    '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/WT_SR_JAK.WT_SR_JAK',
    '/Game/Gear/Weapons/SniperRifles/Maliwan/Shared/_Design/WT_SR_MAL.WT_SR_MAL',
    '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/WT_SR_VLA.WT_SR_VLA',
    '/Game/Gear/GrenadeMods/_Design/A_Data/GM_Default.GM_Default',
    ])
mayhem_invdata_lower_types = set([t.lower() for t in mayhem_invdata_types])

# Anointable InvData types - will be identical to Mayhemable list, plus shields
anointable_invdata_types = mayhem_invdata_types | set(['/Game/Gear/Shields/_Design/A_Data/Shield_Default.Shield_Default'])
anointable_invdata_lower_types = set([t.lower() for t in anointable_invdata_types])

# Guardian Rank Rewards
guardian_rank_rewards = set([
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_Accuracy.GuardianReward_Accuracy',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ActionSkillCooldown.GuardianReward_ActionSkillCooldown',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_CriticalDamage.GuardianReward_CriticalDamage',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_FFYLDuration.GuardianReward_FFYLDuration',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_FFYLMovementSpeed.GuardianReward_FFYLMovementSpeed',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_GrenadeDamage.GuardianReward_GrenadeDamage',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_GunDamage.GuardianReward_GunDamage',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_GunFireRate.GuardianReward_GunFireRate',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_MaxHealth.GuardianReward_MaxHealth',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_MeleeDamage.GuardianReward_MeleeDamage',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_RarityRate.GuardianReward_RarityRate',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_RecoilReduction.GuardianReward_RecoilReduction',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ReloadSpeed.GuardianReward_ReloadSpeed',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ShieldCapacity.GuardianReward_ShieldCapacity',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ShieldRechargeDelay.GuardianReward_ShieldRechargeDelay',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ShieldRechargeRate.GuardianReward_ShieldRechargeRate',
    '/Game/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_VehicleDamage.GuardianReward_VehicleDamage',
    '/Game/PatchDLC/Hibiscus/PlayerCharacters/_Shared/_Design/GuardianRank/GuardianReward_ElementalDamage.GuardianReward_ElementalDamage',
    ])

# Mission names
#
# For most missions, the following find statement will generate this list:
#
#    for file in $(find Game/Missions Game/PatchDLC/Indigo*/Missions \( -iname "Mission_*.uexp" \) -print); do echo -n "'/$(dirname $file)/$(basename $file .uexp)': \""; echo $(strings $file | head -n 2 | tail -n 1)\",; done | sort -i
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
        'Anger_P': "Castle Crimson",
        'Archive_P': "Dustbound Archives",
        'AtlasHQ_P': "Atlas HQ",
        'Bar_P': "Lodge",
        'Beach_P': "Tazendeer Ruins",
        'BloodyHarvest_P': "Heck Hole",
        'COVSlaughter_P': "Slaughter Shaft",
        'Cabin_P': "Enoch's Grove",
        'Camp_P': "Negul Neshai",
        'Cartels_P': "Villa Ultraviolet",
        'CasinoIntro_P': "Grand Opening",
        'Chase_P': "Sapphire's Run",
        'CityBoss_P': "Forgotten Basilica",
        'CityVault_P': "Neon Arterial",
        'City_P': "Meridian Metroplex",
        'Convoy_P': "Sandblast Scar",
        'Core_P': "Jack's Secret",
        'CraterBoss_P': "Crater's Edge",
        'CreatureSlaughter_P': "Cistern of Slaughter",
        'Crypt_P': "Pyre of Stars",
        'DesertBoss_P': "Great Vault",
        'Desert_P': "Devil's Razor",
        'Desertvault_P': "Cathedral of the Twin Gods",
        'Desolate_P': "Desolation's Edge",
        'Eldorado_P': "Vaulthalla",
        'Experiment_P': "Benediction of Pain",
        'Facility_P': "Bloodsun Canyon",
        'FinalBoss_P': "Destroyer's Rift",
        'Forest_P': "Obsidian Forest",
        'Frontier_P': "The Blastplains",
        'FrostSite_P': "Stormblind Complex",
        'GuardianTakedown_P': "Minos Prime / The Shattered Tribunal",
        'Impound_P': "Impound Deluxe",
        'Lake_P': "Skittermaw Basin",
        'Lodge_P': "Ashfall Peaks",
        'Mansion_P': "Jakobs Estate",
        'MarshFields_P': "Ambermire",
        'Mine_P': "Konrad's Hold",
        'Monastery_P': "Athenas",
        'MotorcadeFestival_P': "Carnivora",
        'MotorcadeInterior_P': "Guts of Carnivora",
        'Motorcade_P': "Splinterlands",
        'NekroMystery_p': "Scryer's Crypt",
        'Noir_P': "Eschaton Row",
        'OrbitalPlatform_P': "Skywell-27",
        'Outskirts_P': "Meridian Outskirts",
        'PandoraMystery_p': "Karass Canyon",
        'Prison_P': "Anvil",
        'Prologue_P': "Droughts",
        'ProvingGrounds_Trial1_P': "Gradient of Dawn (Survival)",
        'ProvingGrounds_Trial4_P': "Skydrowned Pulpit (Fervor)",
        'ProvingGrounds_Trial5_P': "Ghostlight Beacon (Cunning)",
        'ProvingGrounds_Trial6_P': "Hall Obsidian (Supremacy)",
        'ProvingGrounds_Trial7_P': "Precipice Anchor (Discipline)",
        'ProvingGrounds_Trial8_P': "Wayward Tether (Instinct)",
        'Raid_P': "Midnight's Cairn (Maliwan Takedown)",
        'Recruitment_P': "Covenant Pass",
        'Sacrifice_P': "Ascension Bluff",
        'SacrificeBoss_p': "Darkthirst Dominion",
        'Sanctuary3_P': "Sanctuary",
        'Sanctum_P': "The Psychoscape",
        'Strip_P': "Spendopticon",
        'TechSlaughter_P': "Slaughterstar 3000",
        'TowerLair_P': "VIP Tower",
        'Towers_P': "Lectra City",
        'Town_P': "Vestige",
        'Trashtown_P': "Compactor",
        'Venue_P': "Heart's Desire",
        'Village_P': "Cursehaven",
        'Watership_P': "Voracious Canopy",
        'WetlandsBoss_P': "Floating Tomb",
        'WetlandsVault_P': "Blackbarrel Cellars",
        'Wetlands_P': "Floodmoor Basin",
        'Woods_P': "Cankerwood",
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


# item type to english
item_type_eng = {
    0: "",
    1: "Chaotic",
    2: "Volatile",
    3: "Primordial",
#    4: "Ascended",
}
