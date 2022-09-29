# Wonderlands Commandline Savegame Editor - Savegame Editing Reference

This is the documentation for the save editing portions of the
TTWL CLI Savegame Editor.  For general app information, installation,
upgrade procedures, and other information, please see the main
[README file](README.md).

These docs will assume that you've installed via `pip3` - if you're using
a Github checkout, substitute the commands as appropriate.  The equivalent
commands will be:

    python -m ttwlsave.cli_edit -h
    python -m ttwlsave.cli_info -h
    python -m ttwlsave.cli_import_protobuf -h
    python -m ttwlsave.cli_import_json -h
    python -m ttwlsave.cli_archive -h

# Table of Contents

- [Basic Operation](#basic-operation)
- [Output Formats](#output-formats)
- [Modifying the Savegame](#modifying-the-savegame)
  - [Character Name](#character-name)
  - [Save Game ID](#save-game-id)
  - [Save Game GUID](#save-game-guid)
  - [Character Level](#character-level)
  - [Hero Stats](#hero-stats)
  - [Chaos Level](#chaos-level)
  - [Currency (Money, Moon Orbs, and Lost Souls)](#currency-money-moon-orbs-and-lost-souls)
  - [Mission Deletion](#mission-deletion)
  - [Item Levels](#item-levels)
  - [Item Chaos Levels](#item-chaos-levels)
  - [Item Reroll Counts](#item-reroll-counts)
  - [Wipe Inventory](#wipe-inventory)
  - [Clear Lucky Dice](#clear-lucky-dice)
  - [Unlocks](#unlocks)
    - [Ammo/Backpack Unlocks](#ammobackpack-unlocks)
    - [Equipment Slots](#equipment-slots)
    - [Feat/Companion](#featcompanion)
    - [Multiclass](#multiclass)
    - [Chaos Mode](#chaos-mode)
    - [All Unlocks at Once](#all-unlocks-at-once)
  - ["Un-Finish" Missions](#un-finish-missions)
  - [Fake TVHM](#fake-tvhm)
  - [Delete Missions](#delete-missions)
  - [Randomize Customizations](#randomize-customizations)
  - [Import Items](#import-items)
- [Importing Raw Protobufs](#importing-raw-protobufs)
- [Importing JSON](#importing-json)
- [Savegame Info Usage](#savegame-info-usage)
  - [Items/Inventory](#itemsinventory)
  - [Fast Travel Stations](#fast-travel-stations)
  - [Challenges](#challenges)
  - [Missions](#missions)
  - [Customizations](#customizations)

# Basic Operation

At its most basic, you can run the editor with only an input and output
file, and it will simply load and then re-encode the savegame.  For
instance, in this example, `old.sav` and `new.sav` will be identical as
far as WL is concerned:

    ttwl-save-edit old.sav new.sav

If `new.sav` exists, the utility will prompt you if you want to overwrite
it.  If you want to force the utility to overwrite without asking,
use the `-f`/`--force` option:

    ttwl-save-edit old.sav new.sav -f

As the app processes files, it will output exactly what it's doing.  If
you prefer to have silent output (unless there's an error), such as if
you're using this to process a group of files in a loop, you can use
the `-q`/`--quiet` option:

    ttwl-save-edit old.sav new.sav -q

Note that currently, the app will refuse to overwrite the same file that
you're editing.  You'll need to move/rename the `new.sav` over the
original, if you want it to replace your current save.  Be sure to keep
backups!

# Output Formats

The editor can output files in a few different formats, and you can
specify the format using the `-o`/`--output` option, like so:

    ttwl-save-edit old.sav new.sav -o savegame
    ttwl-save-edit old.sav new.pbraw -o protobuf
    ttwl-save-edit old.sav new.json -o json
    ttwl-save-edit old.sav new.txt -o items

- **savegame** - This is the default, if you don't specify an output
  format.  It will save the game like a valid WL savegame.  This
  will likely be your most commonly-used option.
- **protobuf** - This will write out the raw, unencrypted Protobuf
  entries contained in the savegame, which might be useful if you
  want to look at them with a Protobuf viewer of some sort (such
  as [this one](https://protogen.marcgravell.com/decode)), or to
  make hand edits of your own.  Raw protobuf files can be imported
  back into savegames using the separate `ttwl-save-import-protobuf`
  command, whose docs you can find near the bottom of this README.
- **json** - Alternatively, this will write out the raw protobufs
  as encoded into JSON.  Like the protobuf output, you should be
  able to edit this by hand and then re-import using the
  `ttwl-save-import-json` utility.  **NOTE:** JSON import is not
  super well-tested yet, so keep backups!
- **items** - This will output a text file containing item codes
  which can be read back in to other savegames.  It uses a format
  similar to the item codes used by Gibbed's BL2/TPS editors.
  (It will probably be identical to the codes used by Gibbed's WL
  editor, once that is released, but time will tell on that front.)
  - You can optionally specify the `--csv` flag to output a CSV file
    instead of "regular" text file.  The first column will be the
    item names, the second will be the item codes.

Keep in mind that when saving in `items` format, basically all of
the other CLI arguments are pointless, since the app will only save
out the items textfile.

# Modifying the Savegame

Here's a list of all the edits you can make to the savegame.  You
can specify as many of these as you want on the commandline, to
process multiple changes at once.

## Character Name

This can be done with the `--name` option:

    ttwl-save-edit old.sav new.sav --name "Gregor Samsa"

## Save Game ID

Like with BL2/TPS, I suspect that this ID isn't at all important, but
the editor can set it anyway with the `--save-game-id` option.  WL
itself sets the savegame ID to match the filename of the savegame, if
interpreted as a hex value (so `10.sav` would have an ID of `16`).

    ttwl-save-edit old.sav new.sav --save-game-id 2

## Save Game GUID

Each savegame in Wonderlands has an internal GUID, which is essentially
a random bunch of data which uniquely identifies the savegame.  In
previous Borderlands games, this value wasn't super important, but in
Wonderlands, new savegames *must* have their GUIDs randomized, or the
game won't recognize the new save.  So, in this editor, randomizing the
GUID is the default behavior when doing any operation on savegames.
To *prevent* GUID randomization (for instance, if you're planning on
overwriting an existing savegame, rather than creating a new one),
you can use the `--dont-randomize-guid` option instead:

    ttwl-save-edit old.sav new.sav --dont-randomize-guid --other-options

## Character Level

You can set your character to a specific level using `--level <num>`,
or to the max level allowed by the game using `--level-max`

    ttwl-save-edit old.sav new.sav --level 20
    ttwl-save-edit old.sav new.sav --level-max

By default, this will set your XP level to the minimum for the specified
level.  To set to the *maximum* XP for the level (so that a +1XP will
level you up), add `--xp-max`

    ttwl-save-edit old.sav new.sav --level 25 --xp-max

The `--xp-max` argument has no effect when setting the user to the
maximum level.

These arguments will also add in any appropriate skill points which
would have happened as a result of levelling.

## Backstory

Character backstory can be set with the `--backstory` argument.  The
following values are valid to specify which backstory to set:

 - `idiot`: Village Idiot
 - `elves`: Raised by Elves
 - `monk`: Failed Monk
 - `hoarder`: Recovering Inventory Hoarder
 - `alchemist`: Rogue Alchemist

For example:

    ttwl-save-edit old.sav new.sav --backstory elves

## Hero Stats

There are a few options available to set your character's Hero Stats.
Note that all of these options operate on the "raw" stat values, which
range from 1 to 30 (and default to 10 on freshly-created characters).
The values you see and set with these options do *not* take into account
the character's backstory, or any Myth Rank buffs.  The valid range
for these values will always be 1 through 30.

First, `--hero-stats` can be used to set all stats to an arbitrary
value:

    ttwl-save-edit old.sav new.sav --hero-stats 15

Alternatively, `--hero-stats-max` will set them all to their maximum
values (30):


    ttwl-save-edit old.sav new.sav --hero-stats-max

Finally, there are individual arguments for each stat:

    ttwl-save-edit old.sav new.sav --str 15
    ttwl-save-edit old.sav new.sav --dex 15
    ttwl-save-edit old.sav new.sav --int 15
    ttwl-save-edit old.sav new.sav --wis 15
    ttwl-save-edit old.sav new.sav --con 15
    ttwl-save-edit old.sav new.sav --att 15

The individual-stat options get processed after the "global"
options, so if for instance you wanted to set all values to
15 but raise Strength and Dexterity to 20, you could specify:

    ttwl-save-edit old.sav new.sav --hero-stats 15 --str 20 --dex 20

## Chaos Level

The `--chaos` argument can be used to activate Chaos Mode at any point,
and/or unlock Chaos Levels you haven't yet unlocked legitimately.  This
will also unlock the Chaos Mode menu regardless of your plot progress,
though there'll be no in-game way to unlock more Chaos Levels until you
finish the game properly.

    ttwl-save-edit old.sav new.sav --chaos 50

To unlock Chaos Mode without setting the active Chaos Level, use the
`--unlock chaos` option.

## Currency (Money, Moon Orbs, and Lost Souls)

Money, Moon Orbs, and Lost Souls can be set with the `--money`, `--moon-orbs`,
and `--souls` arguments, respectively:

    ttwl-save-edit old.sav new.sav --money 20000000
    ttwl-save-edit old.sav new.sav --moon-orbs 10000
    ttwl-save-edit old.sav new.sav --souls 200

Note that the game's maximum money is 2 billion, and the maximum Moon
Orbs is 16,000.  This utility will let you set values higher than that,
but doing so isn't recommended.  There doesn't seem to be a defined
maximum for Lost Souls.

## Mission Deletion

If you ever have a sidemission lock up, or just want to repeat a side
mission, the `--delete--mission` argument can be used to delete the
mission from your savegame so it can be picked up again.  Note that this
will *only* work for side missions.  Plot missions aren't picked up at
will like side missions are, and deleting plot missions will basically
lock your character out of the rest of the game.

To use this argument, you'll need to know the full object path to the
mission you want to delete.  This can be found using
`ttwl-save-info --mission-paths`.  Docs for that function
[can be found here](#missions).

    ttwl-save-edit old.sav new.sav --delete-mission /Game/Missions/Side/Zone_3/Climb/Mission_LavaGoodTime.Mission_LavaGoodTime_C

The `--delete-mission` argument can be specified more than once if you'd
like to delete more than one mission at a time.

## Item Levels

There are two arguments to set item levels.  The first is to set
all items/weapons in your inventory to match your character's level.
If you're also changing your character's level at the same time,
items/weapons will get that new level.  This can be done with
`--items-to-char`

    ttwl-save-edit old.sav new.sav --items-to-char

Alternatively, you can set an explicit level using `--item-levels`

    ttwl-save-edit old.sav new.sav --item-levels 57

## Item Chaos Levels

Gear in Wonderlands can be set to one of a few "special" Chaos Levels,
namely (in ascending level of power): Chaotic, Volatile, Primordial,
and Ascended.  Ordinarily these levels can only be set while playing in Chaos
Mode.  There are some arguments available to set all items in your inventory to
the given Chaos Level, though, including removing the Chaos Level entirely:

    ttwl-save-edit old.sav new.sav --items-regular
    ttwl-save-edit old.sav new.sav --items-chaotic
    ttwl-save-edit old.sav new.sav --items-volatile
    ttwl-save-edit old.sav new.sav --items-primordial
    ttwl-save-edit old.sav new.sav --items-ascended

## Item Reroll Counts

Rerolling enchantments on an item gets progressively more expensive until
it becomes literally impossible given the Moon Orb currency cap.  The
`--clear-rerolls` option will reset the counter to zero for all items in
your inventory, so the reroll costs reset as well.

    ttwl-save-edit old.sav new.sav --clear-rerolls

## Wipe Inventory

Inventory can be wiped entirely using the `--wipe-inventory` argument:

    ttwl-save-edit old.sav new.sav --wipe-inventory

This will happen prior to any item imports (see below), so you can wipe
the inventory and import in the same command (and then use the above
levelling commands to alter the gear after import).

## Clear Lucky Dice

If you feel like hunting for Lucky Dice after unlocking them all, the
`--clear-lucky-dice` argument can be used to mark them all as no longer
found:

    ttwl-save-edit old.sav new.sav --clear-lucky-dice

Note that Lucky Dice information is *also* stored in the profile, and
Lucky Dice completions are propagated between the two.  You will need
to clear out Lucky Dice completion from your profile as well, if you
want to start from scratch.

There is no argument to *finish* Lucky Dice discoveries on the savegame
side -- to do that, edit the profile instead.

## Unlocks

There are a number of things you can unlock with the utility, all
specified using the `--unlock` argument.  You can specify this
multiple times on the commandline, to unlock more than one thing
at once, like so:

    ttwl-save-edit old.sav new.sav --unlock ammo --unlock backpack

### Ammo/Backpack Unlocks

The `ammo` and `backpack` unlocks will give you the maximum number
of SDUs for all ammo types, and your backpack space, respectively.
The `ammo` SDU unlock will also fill your ammo reserves.

    ttwl-save-edit old.sav new.sav --unlock ammo
    ttwl-save-edit old.sav new.sav --unlock backpack

### Equipment Slots

You can use the `equipslots` unlock to activate all equipment
slots (namely: the 3rd and 4th weapon slots, armor, both rings,
and amulet).  This will *not* unlock the second spell slot,
since that's skill/class-based.

    ttwl-save-edit old.sav new.sav --unlock equipslots

### Feat/Companion

You can use the `feat` unlock to activate your character's
Feat/Companion.

    ttwl-save-edit old.sav new.sav --unlock feat

### Multiclass

The `multiclass` unlock will allow you to spec into a second
class, allow changing your secondary class (instead of having
to wait for the end of the game), and give you the extra +2
skill points which the game ordinarily gives you when the
second class slot is unlocked (the skill points will not be
given if the savegame's secondary class is already unlocked).

    ttwl-save-edit old.sav new.sav --unlock multiclass

### Chaos Mode

The `chaos` unlock will unlock Chaos Mode all the way through
the maximum available Chaos Level, without making any changes
to the active Chaos Level.  To set the active level, or to only
unlock Chaos Levels up to a certain point, use the `--chaos`
option.

    ttwl-save-edit old.sav new.sav --unlock chaos

### All Unlocks at Once

You can also use `all` to unlock all the various `--unlock`
options at once, without having to specify each one individually:

    ttwl-save-edit old.sav new.sav --unlock all

## "Un-Finish" Missions

**TODO:** Docs!

## Fake TVHM

**TODO:** Docs!  (also test to see if we need this)

## Delete Missions

**TODO:** Docs!

## Randomize Customizations

The `--randomize-customizations` argument will randomize all available
customization options, given a profile file (so that we know which
customizations have been unlocked).  Specify the profile filename
like so:

    ttwl-save-edit old.sav new.sav --randomize-customizations profile.sav

This will randomize chosen customizations (including Emotes, Banner, and
Statue), all the sliders, and other options which the in-game randomization
doesn't seem to touch (like body type and voice selection, etc).  When
doing the randomizations, there is a 10% chance for Eyes/Mouth/Ears to be
asymmetric (calculated independently for each).  By default, the sliders
will use the "regular" bounds, but if you specify the `--overdrive`
argument, it will use the "overdrive" presets instead, which allow for
much wilder extremes:

    ttwl-save-edit old.sav new.sav --randomize-customizations profile.sav --overdrive

## Import Items

The `-i`/`--import-items` option will let you import items into
a savegame, of the sort you can export using `-o items`.  Simply
specify a text file as the argument to `-i` and it will load in
any line starting with `TTWL(` as an item into the savegame:

    ttwl-save-edit old.sav new.sav -i items.txt

Note that by default, the app will not allow Fabricators to be
imported into a save, since the player doesn't have a good way to
get rid of them.  You can tell the app to allow importing
Fabricators anyway with the `--allow-fabricator` option (which has
no use when not used along with `-i`/`--import-items`)

    ttwl-save-edit old.sav new.sav -i items.txt --allow-fabricator

If the utility can't tell what an item is during import (which may
happen if WL has been updated but this editor hasn't been updated
yet), it will refuse to import the unknown items, unless
`--allow-fabricator` is specified, since the unknown item could be
a Fabricator.  Other edits and imports can still happen, however.

If you have items saved in a CSV file (such as one exported using
`-o items --csv`), you can add the `--csv` argument to import items
from the CSV:

    ttwl-save-edit old.sav new.sav -i items.csv --csv

When reading CSV files, any valid WL item code found by itself in
a field in the CSV will be imported, so the CSV doesn't have to
be in the exact same format as the ones generated by `-o items --csv`.

# Importing Raw Protobufs

If you've saved a savegame in raw protobuf format (using the
`-o protobuf` option, or otherwise), you may want to re-import it
into a savegame, perhaps after having edited it by hand.  This can
be done with the separate utility `ttwl-save-import-protobuf`.  This
requires a `-p`/`--protobuf` argument to specify the file where
the raw protobuf is stored, and a `-t`/`--to-filename` argument,
which specifies the filename to import the protobufs into:

    ttwl-save-import-protobuf -p edited.pbraw -t old.sav

By default this will prompt for confirmation before actually
overwriting the file, but you can use the `-c`/`--clobber` option
to force it to overwrite without asking:

    ttwl-save-import-protobuf -p edited.pbraw -t old.sav -c

**NOTE:** This (and the JSON import) is the one place where these
utilities *expect* to overwrite the file you're giving it.  In the
above examples, it requires an existing `old.sav` file, and the
savefile contents will be written directly into that file.  This
option does *not* currently create a brand-new valid savegame for
you.

# Importing JSON

If you saved a savegame in JSON format (using the `-o json` option),
you may want to re-import it into a savegame, perhaps after having
edited it by hand.  This can be done with the separate utility
`ttwl-save-import-json`.  This requires a `-j`/`--json` argument to
specify the file where the JSON is stored, and a `-t`/`--to-filename`
argument, which specifies the filename to import the JSON into:

    ttwl-save-import-json -j edited.json -t old.sav

By default this will prompt for confirmation before actually
overwriting the file, but you can use the `-c`/`--clobber` option
to force it to overwrite without asking:

    ttwl-save-import-json -j edited.json -t old.sav -c

**NOTE:** This (and the protobuf import) is the one place where these
utilities *expect* to overwrite the file you're giving it.  In the
above examples, it requires an existing `old.sav` file, and the
savefile contents will be written directly into that file.  This
option does *not* currently create a brand-new valid savegame for
you.

# Savegame Info Usage

The `ttwl-save-info` script is extremely simple, and just dumps a bunch
of information about the specified savegame to the console.  If you
specify the `-v`/`--verbose` option, it'll output a bunch more info
than it ordinarily would, such as inventory contents and discovered
Fast Travel stations:

    ttwl-save-info -v old.sav

Instead of doing a global "verbose" option, you can instead choose
to output just some of the extra information:

## Items/Inventory

The `-i`/`--items` argument will output your inventory, including item
codes which could be put in a text file for later import:

    ttwl-save-info -i old.sav

You can also add in the `--rerolls` argument to also show the number of
enchantment rerolls that each item has logged.  This will only change
the output when there's been at least one reroll.

    ttwl-save-info -i --reroll old.sav

## Fast Travel Stations

The `--fast-travel` argument will output a list of all unlocked
Fast Travel stations, per playthrough.  These are reported as the raw
object name in the game, so you may have to use a
[level name reference](https://github.com/BLCM/BLCMods/wiki/Level-Name-Reference#borderlands-3)
to get a feel for what is what.

    ttwl-save-info --fast-travel old.sav

## Challenges

The `--all-challenges` argument will output the state of all challenges
in your savegame.  Note that WL uses challenges to keep track of a
lot of info in the savegames, and this list will be over 1.5k items
long!  As with the fast travel stations, these will be reported as the
raw object names.

    ttwl-save-info --all-challenges old.sav

## Missions

The `--all-missions` argument will output all of the missions that the
character has completed, in addition to the active missions which are
always shown.

    ttwl-save-info --all-missions old.sav

If you want to see the actual object paths to any reported missions
(for instance, when looking to clear out sidemission progress to deal
with locked missions), use the `--mission-paths` option:

    ttwl-save-info --mission-paths old.sav
    ttwl-save-info --all-missions --mission-paths old.sav

## Customizations

The `--customizations` argument will output all the raw chosen-customization
data for the given save file.  This information isn't super useful on its
own, but it's available anyway, if you're curious.

    ttwl-save-info --customizations old.sav

