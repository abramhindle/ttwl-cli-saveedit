# Wonderlands Commandline Profile Editor - Profile Editing Reference

This is the documentation for the profile editing portions of the
TTWL CLI Savegame Editor.  For general app information, installation,
upgrade procedures, and other information, please see the main
[README file](README.md).

These docs will assume that you've installed via `pip3` - if you're using
a Github checkout, substitute the commands as appropriate.  The equivalent
commands will be:

    python -m ttwlsave.cli_prof_edit -h
    python -m ttwlsave.cli_prof_info -h
    python -m ttwlsave.cli_prof_import_protobuf -h
    python -m ttwlsave.cli_prof_import_json -h

# Table of Contents

- [Basic Operation](#basic-operation)
- [Output Formats](#output-formats)
- [Modifying the Profile](#modifying-the-profile)
  - [Skeleton Keys](#skeleton-keys)
  - [Myth Rank](#myth-rank)
    - [Zeroing Myth Rank](#zeroing-myth-rank)
    - [Set Myth Rank Stats to Max](#set-myth-rank-stats-to-max)
    - [Set Arbitrary Myth Rank Stats Points](#set-arbitrary-myth-rank-stats-points)
    - [Set Myth Rank XP](#set-myth-rank-xp)
  - [Bank Item Levels](#bank-item-levels)
  - [Bank Item Chaos Levels](#bank-item-chaos-levels)
  - [Clear Customizations](#clear-customizations)
  - [Unlocks](#unlocks)
    - [Lost Loot and Bank Capacity](#lost-loot-and-bank-capacity)
    - [Customizations](#customizations)
    - [All Unlocks at Once](#all-unlocks-at-once)
  - [Import Bank Items](#import-bank-items)
- [Importing Raw Protobufs](#importing-raw-protobufs)
- [Importing JSON](#importing-json)
- [Profile Info Usage](#profile-info-usage)
  - [Items/Inventory](#itemsinventory)

# Basic Operation

At its most basic, you can run the editor with only an input and output
file, and it will simply load and then re-encode the profile.  For
instance, in this example, `profile.sav` and `newprofile.sav` will be
identical as far as WL is concerned:

    ttwl-profile-edit profile.sav newprofile.sav

If `newprofile.sav` exists, the utility will prompt you if you want to
overwrite it.  If you want to force the utility to overwrite without asking,
use the `-f`/`--force` option:

    ttwl-profile-edit profile.sav newprofile.sav -f

As the app processes files, it will output exactly what it's doing.  If
you prefer to have silent output (unless there's an error), such as if
you're using this to process a group of files in a loop, you can use
the `-q`/`--quiet` option:

    ttwl-profile-edit profile.sav newprofile.sav -q

Note that currently, the app will refuse to overwrite the same file that
you're editing.  You'll need to move/rename the `newprofile.sav` over the
original, if you want it to replace your current profile.  Be sure to keep
backups!

# Output Formats

The editor can output files in a few different formats, and you can
specify the format using the `-o`/`--output` option, like so:

    ttwl-profile-edit profile.sav newprofile.sav -o profile
    ttwl-profile-edit profile.sav newprofile.pbraw -o protobuf
    ttwl-profile-edit profile.sav newprofile.json -o json
    ttwl-profile-edit profile.sav newprofile.txt -o items

- **profile** - This is the default, if you don't specify an output
  format.  It will save the game like a valid WL profile.  This
  will likely be your most commonly-used option.
- **protobuf** - This will write out the raw, unencrypted Protobuf
  entries contained in the profile, which might be useful if you
  want to look at them with a Protobuf viewer of some sort (such
  as [this one](https://protogen.marcgravell.com/decode)), or to
  make hand edits of your own.  Raw protobuf files can be imported
  back into the profile using the separate `ttwl-profile-import-protobuf`
  command, whose docs you can find near the bottom of this README.
- **json** - Alternatively, this will write out the raw protobufs
  as encoded into JSON.  Like the protobuf output, you should be
  able to edit this by hand and then re-import using the
  `ttwl-profile-import-json` utility.  **NOTE:** JSON import is not
  super well-tested yet, so keep backups!
- **items** - This will output a text file containing item codes
  for all items in your bank, which can be read back in to other
  savegames or profiles.  It uses a format similar to the item codes
  used by Gibbed's BL2/TPS editors.  (It will probably be identical
  to the codes used by Gibbed's WL editor, once that is released,
  but time will tell on that front.)
  - You can optionally specify the `--csv` flag to output a CSV file
    instead of "regular" text file.  The first column will be the
    item names, the second will be the item codes.

Keep in mind that when saving in `items` format, basically all of
the other CLI arguments are pointless, since the app will only save
out the items textfile.

# Modifying the Profile

Here's a list of all the edits you can make to the profile.  You
can specify as many of these as you want on the commandline, to
process multiple changes at once.

## Skeleton Keys

The number of Skeleton Keys stored in the profile can be set using
the `--skeleton-keys` argument:

    ttwl-profile-edit profile.sav newprofile.sav --skeleton-keys 150

## Myth Rank

There are a number of functions available for managing Myth Rank
in profiles.  Note that we don't currently know the equation used to
convert Myth Rank XP into Myth Points, so allocating points into
the Myth Rank stats can lead to the game's UI showing negative
points available, etc.  That doesn't seem to hurt the game at all,
though.

### Zeroing Myth Rank

Myth Rank can be completely cleared from a profile using the
`--zero-myth-rank` argument.  This will wipe both stat allocations
and the "raw" Myth Rank XP, so you'd be starting completely fresh.

    ttwl-profile-edit profile.sav newprofile.sav --zero-myth-rank

### Set Myth Rank Stats to Max

Many of the Myth Rank stats have a maximum point allocation.  To set
those stats to the maximum values, use `--myth-stats-max`.  This will
also ensure that the stats *without* maximum values have at least
1 point allocated.

    ttwl-profile-edit profile.sav newprofile.sav --myth-stats-max

### Set Arbitrary Myth Rank Stats Points

You can also globally set a specific value to be allocated into all
Myth Rank stats.  This won't allocate more than the maximum, for
stats which have a maximum value established.  For example, to put
7 points into all stats:

    ttwl-profile-edit profile.sav newprofile.sav --myth-stats-points 7

### Set Myth Rank XP

As mentioned above, we don't currently know the equation used to convert
Myth Rank XP into Myth Rank Points.  If you use one of the arguments
above to allocate more points than your current XP would allow, the game's
UI will report a negative number of points available.  This doesn't
actually hurt anything, but might be annoying to look at, so you can
use `--myth-xp` to try and get rid of that.  Alternatively, this could
just be used to provide you with some more points to allocate in-game.

    ttwl-profile-edit profile.sav newprofile.sav --myth-xp 2000000

## Bank Item Levels

There are two arguments to set item levels for gear that's stored in
your bank.  The first is to set all items/weapons in the bank to the
max level in the game.  This can be done with `--item-levels-max`

    ttwl-profile-edit profile.sav newprofile.sav --item-levels-max

Alternatively, you can set an explicit level using `--item-levels`

    ttwl-profile-edit profile.sav newprofile.sav --item-levels 57

## Bank Item Chaos Levels

Gear in Wonderlands can be set to one of a few "special" Chaos Levels,
namely (in ascending level of power): Chaotic, Volatile, Primordial,
and Ascended.  Ordinarily these levels can only be set while playing in Chaos
Mode.  There are some arguments available to set all items in your bank to
the given Chaos Level, though, including removing the Chaos Level entirely:

    ttwl-profile-edit profile.sav newprofile.sav --items-regular
    ttwl-profile-edit profile.sav newprofile.sav --items-chaotic
    ttwl-profile-edit profile.sav newprofile.sav --items-volatile
    ttwl-profile-edit profile.sav newprofile.sav --items-primordial
    ttwl-profile-edit profile.sav newprofile.sav --items-ascended

## Clear Customizations

If for some reason you'd like to clear your profile of all found
customizations, you can do so with `--clear-customizations`.  (This was
honestly mostly just useful to myself when testing the app.)

    ttwl-profile-edit profile.sav newprofile.sav --clear-customizations

## Unlocks

There are a number of things you can unlock with the utility, all
specified using the `--unlock` argument.  You can specify this
multiple times on the commandline, to unlock more than one thing
at once, like so:

    ttwl-profile-edit profile.sav newprofile.sav --unlock lostloot --unlock bank

### Lost Loot and Bank Capacity

The `lostloot` and `bank` unlocks will give you the maximum number
of SDUs for the Lost Loot machine and Bank, respectively:

    ttwl-profile-edit profile.sav newprofile.sav --unlock lostloot
    ttwl-profile-edit profile.sav newprofile.sav --unlock bank

### Customizations

You can use the `--unlock customizations` option to unlock all
available customizations/cosmetics.  Note that as new content is released,
this editor will have to be updated to include the new customizations.

    ttwl-profile-edit profile.sav newprofile.sav --unlock customizations

**Note:** DLC-locked customizations, such as the Golden Hero Armor,
will remain unavailable even if unlocked via this utility.  If you later
purchase the DLC in question, though, the relevant cosmetics should show
up as available immediately.

### All Unlocks at Once

You can also use `all` to unlock all the various `--unlock`
options at once, without having to specify each one individually:

    ttwl-profile-edit profile.sav newprofile.sav --unlock all

## Import Bank Items

The `-i`/`--import-items` option will let you import items into
your bank, of the sort you can export using `-o items`.  Simply
specify a text file as the argument to `-i` and it will load in
any line starting with `TTWL(` as an item into the savegame:

    ttwl-profile-edit profile.sav newprofile.sav -i items.txt

Note that by default, the app will not allow Fabricators to be
imported into the bank, since the player doesn't have a good way to
get rid of them.  You can tell the app to allow importing
Fabricators anyway with the `--allow-fabricator` option (which has
no use when not used along with `-i`/`--import-items`)

    ttwl-profile-edit profile.sav newprofile.sav -i items.txt --allow-fabricator

If the utility can't tell what an item is during import (which may
happen if WL has been updated but this editor hasn't been updated
yet), it will refuse to import the unknown items, unless
`--allow-fabricator` is specified, since the unknown item could be
a Fabricator.  Other edits and imports can still happen, however.

If you have items saved in a CSV file (such as one exported using
`-o items --csv`), you can add the `--csv` argument to import items
from the CSV:

    ttwl-profile-edit profile.sav newprofile.sav -i items.csv --csv

When reading CSV files, any valid WL item code found by itself in
a field in the CSV will be imported, so the CSV doesn't have to
be in the exact same format as the ones generated by `-o items --csv`.

# Importing Raw Protobufs

If you've saved a profile in raw protobuf format (using the
`-o protobuf` option, or otherwise), you may want to re-import it
into the profile, perhaps after having edited it by hand.  This can
be done with the separate utility `ttwl-profile-import-protobuf`.  This
requires a `-p`/`--protobuf` argument to specify the file where
the raw protobuf is stored, and a `-t`/`--to-filename` argument,
which specifies the filename to import the protobufs into:

    ttwl-profile-import-protobuf -p edited.pbraw -t profile.sav

By default this will prompt for confirmation before actually
overwriting the file, but you can use the `-c`/`--clobber` option
to force it to overwrite without asking:

    ttwl-profile-import-protobuf -p edited.pbraw -t profile.sav -c

**NOTE:** This (and the JSON import) is the one place where these
utilities *expect* to overwrite the file you're giving it.  In the
above examples, it requires an existing `old.sav` file, and the
savefile contents will be written directly into that file.  This
option does *not* currently create a brand-new valid savegame for
you.

# Importing JSON

If you saved a profile in JSON format (using the `-o json` option),
you may want to re-import it into the profile, perhaps after having
edited it by hand.  This can be done with the separate utility
`ttwl-profile-import-json`.  This requires a `-j`/`--json` argument to
specify the file where the JSON is stored, and a `-t`/`--to-filename`
argument, which specifies the filename to import the JSON into:

    ttwl-profile-import-json -j edited.json -t profile.sav

By default this will prompt for confirmation before actually
overwriting the file, but you can use the `-c`/`--clobber` option
to force it to overwrite without asking:

    ttwl-profile-import-json -j edited.json -t profile.sav -c

**NOTE:** This (and the protobuf import) is the one place where these
utilities *expect* to overwrite the file you're giving it.  In the
above examples, it requires an existing `old.sav` file, and the
savefile contents will be written directly into that file.  This
option does *not* currently create a brand-new valid savegame for
you.

# Profile Info Usage

The `ttwl-profile-info` script is extremely simple, and just dumps a bunch
of information about the specified savegame to the console.  If you
specify the `-v`/`--verbose` option, it'll output a bunch more info
than it ordinarily would, such as bank and lost loot contents:

    ttwl-profile-info -v profile.sav

Instead of doing a global "verbose" option, you can instead choose
to output just some of the extra information, though at the moment there's
only one extra option, so the two are identical:

## Items/Inventory

The `-i`/`--items` argument will output your bank and Lost Loot machine
contents, including item codes which could be put in a text file for
later import:

    ttwl-profile-info -i profile.sav
