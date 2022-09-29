# Tiny Tina's Wonderlands Commandline Savegame/Profile Editor

This project is a commandline Python-based Wonderlands Savegame
and Profile Editor.  It's based on [apocalyptech's CLI editor for BL3](https://github.com/apocalyptech/bl3-cli-saveedit),
and provides some very similar functionality.  It can be used
to level up your characters, level up your gear, set character
stats (Hero Skills, Myth Rank), and unlock a variety of character
features early: feats/companions, second skill tree (including
re-selecting via Quick Change), Chaos Mode, SDUs, equipment slots,
and more.

This editor has only been tested on PC Savegames -- other platforms'
savegames are not supported at the moment.

Please keep the following in mind:

- The editor has been getting ported over from the BL3 version for a
  little while now, and it feels reasonably complete, but keep in mind
  that there are probably a few rough edges still, and there may be
  some BL3 references still hanging about -- this project hasn't yet
  reached v1.0.0.
- This app does not have any graphical interface.  You must be
  on a commandline in order to use it.  (A rudimentary web interface
  is available, though -- see below.)
- The app has only very limited item-editing capability at the
  moment, which is restricted to:
  - Item Levels can be changed
  - Chaos Level can be set on items
  - Enchantment Reroll count can be cleared
- Unlike in BL3, when creating new savegames for Wonderlands, the
  savegame GUID *must* be randomized, otherwise the game won't
  recognize the new save.  Therefore, rather than having a
  `--randomize-guid` option for the save editor, this Wonderlands
  version instead defaults to randomizing the GUID, and provides
  a `--dont-randomize-guid` argument.
- While I have not experienced any data loss with the app,
  **take backups of your savegames before using this**, and
  keep in mind that it could end up corrupting your saves.  If
  you do encounter any data loss problems, please contact me
  and I'll try to at least fix whatever bug caused it.

# Table of Contents

- [Web UI](#web-ui)
- [Installation](#installation)
  - [Upgrading](#upgrading)
  - [Notes for People Using Windows](#notes-for-people-using-windows)
  - [Running from Github](#running-from-github)
  - [Finding Savegames](#finding-savegames)
- [Editor Usage](#editor-usage)
- [TODO](#todo)
- [Credits](#credits)
- [License](#license)
- [Other Utilities](#other-utilities)
- [Changelog](#changelog)

# Web UI

Abram Hindle, who took an early lead in getting this ported over to
Wonderlands, is providing a simple web-based version of this utility,
so feel free to give that a try:

https://abramhindle.github.io/ttwl-cli-saveedit/

Yes, this will install python and ttwl-cli-saveedit in your browser and
give you a tiny UI to dupe your savefiles or import items.

# Installation

This editor requires [Python 3](https://www.python.org/), and has been
tested on 3.7, 3.8, 3.9, and 3.10.  It also requires the [protobuf package](https://pypi.org/project/protobuf/).

The easiest way to install this app is via `pip`/`pip3`.  Once Python 3 is
installed, you should be able to run this to install the app:

    pip3 install ttwl-cli-saveedit

Or, for Abram Hindle's development version:

    pip3 install --user git+https://github.com/abramhindle/ttwl-cli-saveedit

Once installed, there should be a few new commandline utilities available
to you.  The main editor is `ttwl-save-edit`, and you can see its possible
arguments with `-h`/`--help`:

    ttwl-save-edit -h

There's also a `ttwl-save-info` utility which just shows some information
about a specified savefile.  You can see its possible arguments with
`-h`/`--help` as well:

    ttwl-save-info -h

If you've got a raw savegame protobuf file that you've hand-edited (or
otherwise processed) that you'd like to import into an existing savegame,
you can do that with `ttwl-save-import-protobuf`:

    ttwl-save-import-protobuf -h

Alternatively, if you've got a savegame exported as JSON that you'd like
to import into an existing savegame, you can do that with
`ttwl-save-import-json`:

    ttwl-save-import-json -h

Finally, there's a utility which is intended to be used to generate
savegame archive saves (like the [BL3 ones found here](http://apocalyptech.com/games/bl-saves/bl3.php).
That archive doesn't yet exist for Wonderlands, but the utility should
be good to go.  It's unlikely to be useful to anyone but apocalyptech,
but you can try it out as well, if you like:

    ttwl-process-archive-saves -h

There are also profile-specific versions of most of those commands, which
can be used to edit the main BL3 `profile.sav`:

    ttwl-profile-edit -h
    ttwl-profile-info -h
    ttwl-profile-import-protobuf -h
    ttwl-profile-import-json -h

### Upgrading

When a new version is available, you can update using `pip3` like so:

    pip3 install --upgrade ttwl-cli-saveedit

You can check your current version by running any of the apps with the
`-V`/`--version` argument:

    ttwl-save-info --version

### Notes for People Using Windows

This is a command-line utility, which means there's no graphical interface,
and you'll have to run it from either a Windows `cmd.exe` prompt, or presumably
running through PowerShell should work, too.  The first step is to
install Python:

- The recommended way is to [install Python from python.org](https://www.python.org/downloads/windows/).
  Grab what's available in the 3.x series (at time of writing, that's 3.9.4),
  and when it's installing, make sure to check the checkbox which says something
  like "add to PATH", so that you can run Python from the commandline directly.
- If you're on Windows 10, you can apparently just type `python3` into a command
  prompt to be taken to the Windows store, where you can install Python with
  just one click.  I've heard reports that this method does *not* provide the
  ability to add Python to your system PATH, though, so it's possible that
  running it would be more complicated.

When it's installed, test that you can run it from the commandline.  Open up
either `cmd.exe` or PowerShell, and make sure that you see something like this
when you run `python -V`:

    C:\> python -V
    Python 3.9.4

If that works, you can then run the `pip3 install ttwl-cli-saveedit` command
as mentioned above, and use the commandline scripts to edit to your heart's
content.

### Notes for people on Steam Deck

Miniconda is a user space python distribution that works on Steam Deck.  
Once you've installed it open a new terminal session and it's executables 
will be in your path.

https://docs.conda.io/en/latest/miniconda.html

### Running from Github

Alternatively, if you want to download or run the Github version of
the app: clone the repository and then install `protobuf` (you can
use `pip3 install -r requirements.txt` to do so, though a `pip3 install protobuf`
will also work just fine).

You can then run the scripts directly from the Github checkout, though
you'll have to use a slightly different syntax.  For instance, rather than
running `ttwl-save-edit -h` to get help for the main savegame editor, you
would run:

    python -m ttwlsave.cli_edit -h

The equivalents for each of the commands are listed in their individual
README files, linked below.

### Finding Savegames

This app doesn't actually know *where* your savegames or profiles are located.
When you give it a filename, it'll expect that the file lives in your "current"
directory, unless the filename includes all its path information.  When launching
a `cmd.exe` on Windows, for instance, you'll probably start out in your home
directory (`C:\Users\username`), but your savegames will actually live in a
directory more like `C:\Users\username\My Documents\My Games\Tiny Tina's Wonderlands\Saved\SaveGames\<numbers>\`.
The easiest way to run the utilities is to just use `cd` to go into the dir
where your saves are (or otherwise launch your commandline in the directory you
want).  Otherwise, you could copy the save into your main user dir (and then
copy back after editing), or even specify the full paths with the filenames.

# Editor Usage

Full documentation for both savegames and profiles are linked immediately below,
but as a quick example, here's a command to list information about `2.sav`,
followed by an edit which saves out to a new `3.sav`

    ttwl-save-info -i 2.sav

    ttwl-save-edit --name 'CoolNewName' --save-game-id 3 --level 40 2.sav 3.sav

For instructions on using the Savegame portions of the editor, see
[README-saves.md](https://github.com/apocalyptech/ttwl-cli-saveedit/blob/master/README-saves.md).

For instructions on using the Profile portions of the editor, see
[README-profile.md](https://github.com/apocalyptech/ttwl-cli-saveedit/blob/master/README-profile.md).

# TODO

- Unlock overworld abilities early?
- Customization Randomization improvements:
  - Maybe would be nice to have a magic `all` value for `--randomize-customizations`
    to assume that all customizations are available, rather than having to read
    the list from a profile?
  - Allow only randomizing specific things?  (Char, Emotes, Banner, etc).  The
    backend functions already support that.
  - Option to copy customizations from one char to another?
  - For that matter, would it be worth having an explicit customization-export
    function which writes out *just* customizations to a file, which could then be
    imported via a different arg/util?  Probably not -- I think I'd probably just
    content myself with copy-from-another-char, but something to think about.
  - Expose symmetry chance to CLI arg
  - I'd kind of like to do custom weighting on facial accessory randomization.  I
    personally tend to prefer being able to see the character's face to having it
    covered up...
- Would be nice to have some enchantment-setting functions in here.
- Redo how we handle serial editing in `datalib.py`; it's super inefficient as-is
- Might be nice to pull some common item-handling argparse options into `cli_common.py`.
  The actual functionality is handled in there (levelling items, reroll counts, etc)
  but there's a fair bit of duplicated code in `cli_edit.py` and `cli_prof_edit.py`
  to handle argument parsing.
- Relatedly, there's a silly amount of code duplication inside `cli_common.py` related
  to properly pluralizing some of our item-editing user reporting.  Would be nice to
  roll that up a little more properly.
- PS4 Support (for already-unlocked saves, anyway)
- If we fail to read a savefile or profile, might be nice to *actually* check
  if it's the other of profile-or-savefile, and give a more helpful message in
  those cases.
- Unit tests?

# Credits

[Abram Hindle](https://github.com/abramhindle/) took an early lead in
porting the BL3 CLI editor over to Wonderlands, which is much
appreciated!  All the initial Wonderlands-support framework, and the
basic editor functionality is thanks to him.

The encryption/decryption stanzas in `BL3Save.__init__` and `BL3Save.save_to`
were [helpfully provided by Gibbed](https://twitter.com/gibbed/status/1246863435868049410?s=19)
(rick 'at' gibbed 'dot' us), so many thanks for that!  The protobuf definitions
are also provided by Gibbed, from his
[Borderlands3Protos](https://github.com/gibbed/Borderlands3Protos) repo,
and used with permission.  Gibbed also kindly provided the exact hashing
mechanism used to work with weapon skins and trinkets.

The rest of the savegame format was gleaned from 13xforever/Ilya's
`gvas-converter` project: https://github.com/13xforever/gvas-converter

Many thanks also to Baysix, who endured an awful lot of basic questions about
pulling apart item serial numbers.  Without their help, we wouldn't have
item level editing (or nice item names in the output)!

Many thanks to shroomz for figuring out the Myth Rank XP-to-Rank calculation.

Basically what I'm saying is that anything remotely "hard" in here is all thanks
to lots of other folks.  I'm just pasting together all their stuff.  Thanks, all!

# License

All code in this project is licensed under the
[zlib/libpng license](https://opensource.org/licenses/Zlib).  A copy is
provided in [COPYING.txt](COPYING.txt).

# Other Utilities

There aren't too many Wonderlands save editors in the wild yet.  One
fork of [FromDarkHell's BL3 Save/Profile Editor](https://github.com/FromDarkHell/BL3SaveEditor)
is currently being maintained by a third party, though:

- [somefunguy's WL fork of FDH's Editor](https://github.com/somefunguy/BL3SaveEditor/tree/ttwl-dlc3) -
  Written in C#, has EXE downloads for ease of use on Windows.

# Changelog
**v0.0.16**
  - New extraction and update to chaos level 100

**v0.0.15**
  - Mythrank Updates thanks to Shroomz

**v0.0.13**
  - Updated DLC4 definitions

**v0.0.12**
  - Apocalyptech contributions
      - Adding missing Fealty Oath ring from DLC3
      - Shuffling this custom exception around -- I did want that to live inside TTWLProfile, I suppose.
      - Option to see chosen customizations with ttwl-save-info
      - Slight bit of rearranging, and making some fuctions behave a bit more consistently
      - Turns out the DLCs have some Ear Shape customizations I missed
      - Missing EarShape and Exception in the wrong place?
      - Version update
      - Fixing link
      - Oh yeah, one more thing I'd wanted to add
      - A few more things for the TODO
      - A few more comments -- I suppose I probably should've waited another few tens of minutes before committing originally.  Ah, well.
      - Adding a bit of docs to this class
      - Add customization randomization
      - Updating this to take advantage of our simplified playthrough handling
      - Ah right, something else I'd wanted to look into
      - Rewording
      - May as well add that simple example back in to the main README; probably a good idea.
      - Get my savegame archive script up to theoretical snuff


**v0.0.10**
 - Mega patch from Apocalyptech

**v0.0.9**
 - Updated Inventory for Molten Mirrors (20220623)

**v0.0.8**
 - Added options to turn everything into chaotics, volatiles, or primordials

**v0.0.7**
 - Updated Inventory

**v0.0.6**
 - Updated Inventory
 - Added Primary and Secondary Class Reporting

**v0.0.5**
 - Changes to deploy it in the browser.

**v0.0.4**
 - Dealt with pet names. Missing profile.

**v0.0.3**
 - Updated from Gibbed's repo again for coiled captors. Made the profile info work.

**v0.0.2**
 - Updated the item defs from Gibbed from https://github.com/gibbed/WonderlandsDumps/blob/master/Inventory%20Serial%20Number%20Database.json

**v0.0.1**
 - Tried to port it to Tina Tiny's Wonderlands

**v1.16.1** - *(unreleased)*
 - Added `--copy-tvhm` option to copy TVHM state to NVHM.  **(untested still!)**

**v1.16.0** - November 18, 2021
 - Updated name of "Seventh Sense (unknown version)" to "Seventh Sense (purple
   version)", since realizing that it's now a valid drop from the Diamond
   Armory (presumably since DLC5's release).
 - Updated for Vault Card 3 patch:
   - Data Updates (to understand new gear)
   - Vault Card 3 Keys/Chests

**v1.15.1** - August 11, 2021
 - Updated with some Character Heads which were shipped with the Vault Card 2
   update but overlooked for 1.15.0.

**v1.15.0** - August 5, 2021
 - Updated for Vault Card 2 patch:
   - Data Updates (to understand new gear)
   - Vault Card 2 Keys/Chests
   - Updated Bank SDU count

**v1.14.0** - July 7, 2021
 - Added `--mission-paths` to `bl3-save-info`
 - Added `--delete-pt1-mission` and `--delete-pt2-mission` to `bl3-save-edit`
 - Added options to clear seasonal event challenge progress (Bloody Harvest,
   Broken Hearts, Revenge of the Cartels)

**v1.13.0** - June 24, 2021
 - Updated for today's patch
    - Updated level cap to 72
    - Updated protobufs
 - Added `--reverse` option for my Savegame Archive processing script, for some more
   flexibility on the CSS when outputting HTML

**v1.12.0** - April 11, 2021
 - Updated with DLC6 (Director's Cut) compatibility.
   - Support for updated item serial number format
   - Added `--guardian-keys`, `--vaultcard1-keys`, and `--vaultcard1-chests` arguments
     for profile editor
 - Fixed a few item names which weren't being mapped properly

**v1.11.1** - February 12, 2021
 - Fixed name of the Broken Hearts 2021 weapon trinket "Cosmic Romance" to be "Tentacle
   Ventricles" like in game -- it was updated with an OakTMS update on Feb 11 by GBX.

**v1.11.0** - February 1, 2021
 - Added Citizen Science editing functionality to profile editor, thanks
   to [@apple1417](https://github.com/apple1417/)

**v1.10.4** - January 21, 2021
 - Updated with the new cosmetics data from today's patch.  *(Totally forgot to do that
   in v1.10.3.)*

**v1.10.3** - January 21, 2021
 - Updated internal inventory DB with data from today's patch.  (No real functionality
   changes with this.)

**v1.10.2** - November 10, 2020
 - Updated internal inventory DB with a minor change which was in the previous GBX
   patch.  (Probably no actual functionality changes with this.)

**v1.10.1** - November 10, 2020
 - A second patch was released, about 12 hours after the Designer's Cut release, which
   updated the protobufs and was causing us to not read saves properly.  This has been
   fixed up now.
 - Also require at least protobuf v3.12, which appears to be required as of my
   latest protobuf generation.

**v1.10.0** - November 9, 2020
 - Updated with DLC5 (Designer's Cut) support

**v1.9.2** - October 8, 2020
 - Added in the missed weapon skin "Porphyrophobia," from Bloody Harvest 2020.

**v1.9.1** - September 30, 2020
 - Fixed unlocking FL4K's "Antisoci4l" head (though you should still get
   that one [all legit-like](https://gearboxloot.com/products/borderlands-3-mask-skins-head-pack))

**v1.9.0** - September 10, 2020
 - Updated with DLC4 (Psycho Krieg and the Fantastic Fustercluck) support

**v1.8.2** - July 27, 2020
 - Updated to allow unlocking the Battle Driver and Devil Tooth weapon trinkets, since
   the July 23 patch fixed those so that they properly stay in your profile.

**v1.8.1** - July 14, 2020
 - `--item-mayhem-max` and `--item-mayhem-levels` will now apply Mayhem parts to
   grenades as well as weapons.

**v1.8.0** - July 11, 2020
 - Added `--mayhem-seed` option to `bl3-save-edit`, to set the random seed used to
   determine active Mayhem modifiers.  The seed is now shown in the `bl3-save-info`
   output, as well.

**v1.7.2** - July 6, 2020
 - Allow characters to use skill trees properly if levelled higher directly from level 1.

**v1.7.1** - June 29, 2020
 - Added three more DLC3 room decorations that I'd missed orginally, for the profile
   editor's cosmetic-unlock ability
 - Added Jetbeast unlocks (both parts and skins)

**v1.7.0** - June 26, 2020
 - Updated for DLC3 (Bounty of Blood) content
   - Jetbeast vehicle unlocks are forthcoming, until I can actually test them out.
 - Added various Guardian Rank processing
   - For savegames and profiles, added `--zero-guardian-rank`
   - For only profiles, added `--min-guardian-rank`, `--guardian-rank-rewards`, and
     `--guardian-rank-tokens`
 - Added `--unlock cubepuzzle` to reset the Eridian Cube puzzle in Desolation's Edge
 - Added `--clear-takedowns` to get rid of the Takedown mission-pickup notifications
   for chars you never intend to do Takedowns with.
 - Item name processing will now recognize the specific legendary artifact balances
   added by the Maliwan Takedown update (they're functionally identical to the world-
   drop versions)
 - Updated `bl3-process-archive-saves` to wipe out Guardian Rank entirely

**v1.6.2** - June 18, 2020
 - Allow setting character/item levels higher than the currently-known max, in case
   users want to pre-level their saves ahead of level cap increases (and in case
   they don't want to wait for an official update of this app)

**v1.6.1** - June 13, 2020
 - Updated room decoration/trinket/weaponskin alphabetization to ignore case (so
   "Casino Banner" sorts before "COV Bat," for instance).
 - Counts of unlocked cosmetic items in `bl3-profile-info` will now include the
   "default" cosmetics which are always unlocked, so those counts match the numbers
   in-game.

**v1.6.0** - June 11, 2020
 - Updated for extra content introduced by Takedown at the Guardian Breach
 - Added `--golden-keys` option to `bl3-profile-edit`, to set available Golden Keys
 - Added `--randomize-guid` option to `bl3-save-edit`

**v1.5.2** - May 23, 2020
 - Updated item name mapping to include the COM Balances used by Trials bosses, for
   their dedicated COM drops.
 - Add in the `--csv` option to allow importing/exporting items into CSV files,
   instead of just text files (which is the default without `--csv`).  Has no effect
   except on item imports/exports.

**v1.5.1** - May 5, 2020
 - Fixed alphabetization of COV Buzzaxe room decoration.  In the game data it looks
   like it's called "Psycho Buzzaxe," but the actual in-game label is COV Buzzaxe.
 - Fixed name displays for "regular" (non-E-Tech, non-Legendary) Maliwan snipers and
   Tediore pistols.
 - Updated item name mapping to distinguish between the blue-rarity mission reward
   version of Redistributor from the legendary version from Maliwan Takedown.
 - Updated `bl3-process-archive-saves` to clear out some 3rd-playthrough data
   which earlier versions had accidentally introduced *(only really of interest
   to myself)*

**v1.5.0** - April 28, 2020
 - Added ability to alter Mayhem level for items, both in savegames and profile.
   `--item-mayhem-max` will set items to the max Mayhem level (`10`), or
   `--item-mayhem-levels <num>` will set a specific level (`0` to remove Mayhem
   from items entirely).
 - Item level reports when viewing contents or exporting items will include
   the Mayhem levels
 - Info views will show the total number of available SDUs along with the
   purchased count
 - Various internal code reorganization

**v1.4.0** - April 23, 2020
 - Updated for the Cartels + Mayhem 2.0 patch:
   - Update item/weapon handling to understand new serial number versions
   - Added in new cosmetic unlocks
   - Mayhem level can now be set as high as 10
   - Extra SDU levels added
   - Fixed a bug related to viewing vehicle unlocks, thanks to new game data
 - Introduction of profile editing utilities, via `bl3-profile-edit`,
   `bl3-profile-info`, `bl3-profile-import-json`, and `bl3-profile-import-protobuf`.
   The following functionality is supported:
   - Importing/Exporting to both JSON and Protobuf
   - Importing/Exporting items to/from the bank
   - Altering the level of gear stored in the bank
   - Unlocking all global customizations/cosmetics
   - Alphabetizing the list of room decorations, trinkets, and weapon skins
 - Display changes for `bl3-save-info` - introduced individual arguments to
   show more detailed information as-requested, instead of only having a
   global `-v`/`--verbose` option:
   - Added `-i`/`--items` argument, to show inventory information
   - Added `--fast-travel` argument, to show unlocked fast travel stations
   - Added `--all-challenges` argument, to list all challenges in the save file
     and their statuses (note: this will be over 1.5k items!)
   - Added `--all-missions` argument, to list all completed missions in addition
     to active ones
   - `-v`/`--verbose` now implies the four options above.
 - `bl3-save-info` will now also report on whether the savegame has finished the
   main game or any of the DLCs.
 - Added `--unfinish-nvhm` option to `bl3-save-edit`, to completely clear out
 any TVHM data and pretend that NVHM was never finished.

**v1.3.1** - April 14, 2020
 - Bah, forgot a few more README tweaks about the JSON export/import

**v1.3.0** - April 14, 2020
 - Added `json` output type, to export the protobuf as encoded into JSON
 - Added `bl3-save-import-json` utility, to load JSON into a savegame

**v1.2.2** - April 12, 2020
 - Updated README with some more specific Windows 10 installation advice.

**v1.2.1** - April 12, 2020
 - Updated Credits section of the README with one more credit that I'd
   wanted to put in but forgot. :)

**v1.2.0** - April 12, 2020
 - Added ability to change item/weapon levels, using `--items-to-char`
   or `--item-levels`
 - Item Imports will now *not* import Fabricators unless explicitly
   told to with the `--allow-fabricator` option.
 - Item names and levels are now shown where appropriate:
   - In verbose `bl3-save-info` output
   - In item export files
   - While importing items
 - Updated to Protobuf v3, which is what BL3 itself uses.  Now when we
   re-save without any edits, the save should be identical to the
   original savegame.
 - Item export will now be done without any encryption, so an item will
   have the exact same item code regardless of where it came from
   (previously, item codes would change every time the game was saved,
   so the same item could have very different-looking codes)
 - Added `-V`/`--version` flag to show version number

**v1.1.1** - April 7, 2020
 - Added in Citizen Science mission name.

**v1.1.0** - April 7, 2020
 - Added `bl3-save-import-protobuf` command, to load a raw protobuf file
   into an existing savegame.

**v1.0.1** - April 5, 2020
 - Some saves include Eridium as an ammo type, presumably related to the
   Fabricator.  Fixed a crash in `bl3-save-info` related to that.

**v1.0.0** - April 5, 2020
 - Initial version

