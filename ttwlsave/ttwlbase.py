#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2022 CJ Kucera (cj@apocalyptech.com)
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

class TTWLBase(object):
    """
    Base object for TTWL savegame/profile info.  Meant to handle instances
    where there's literally identical structures between the two.  There's
    almost certainly a bunch of duplicated code between the two which should
    be merged in here -- I created this while working on Lucky Dice challenges,
    which needed to be handled identically on both sides, so that's mostly
    all that's in here.

    Note that the functionality in here will rely on the implementing class
    populating a `self.base_obj` data which points to the protobuf.  Currently
    saves use `self.save` and profiles use `self.prof`, so those are now also
    setting `base_obj` as well.

    A note about challenges: the way the protobufs get represented, we basically
    have to loop through a list of challenges until we find the one we want.
    It'd probably be a lot more sensible to load all that stuff into a dict when
    we load the protobuf in, so that we could just reference specific challenges
    more intelligently.  For now I'm not gonna bother with that, since so little
    uses it.
    """

    def __init__(self):
        """
        Make sure that implementing classes set `base_obj` when appropriate.
        """
        self.base_obj = None


    def get_all_challenges_raw(self):
        """
        Returns the savegame's list of all challenges, as the actual protobuf objects.
        """
        return sorted(self.base_obj.challenge_data, key=lambda chal: chal.challenge_class_path)


    def unlock_challenge_obj(self, challenge_obj,
            completed_count=1,
            progress_level=0,
            progress_counter=0,
            ):
        """
        Unlock the given challenge object.  Not sure what `progress_level`
        does, honestly.  Presumably `completed_count` would be useful for the
        more user-visible challenges on the map menu.  The ones that we're
        primarily concerned with here will just have 1 for it, though.
        """
        # First look for existing objects (should always be here, I think)
        for chal in self.base_obj.challenge_data:
            if chal.challenge_class_path == challenge_obj:
                chal.currently_completed = True
                chal.is_active = False
                chal.completed_count = completed_count
                chal.progress_counter = progress_counter
                chal.completed_progress_level = progress_level
                return

        # AFAIK we should never get here; rather than create a new one,
        # I'm just going to raise an Exception for now.
        raise Exception('Challenge not found: {}'.format(challenge_obj))


    def clear_challenge_prefix(self, prefix):
        """
        Removes all challenge data which matches the given `prefix`.  Completely
        removes the entries, as opposed to trying to intelligently clear their
        values.
        """
        prefix_lower = prefix.lower()
        indicies_to_del = []
        for idx, challenge in enumerate(self.base_obj.challenge_data):
            if challenge.challenge_class_path.lower().startswith(prefix_lower):
                indicies_to_del.append(idx)
        for idx in reversed(indicies_to_del):
            del self.base_obj.challenge_data[idx]


    def clear_dice_challenges(self):
        """
        Clears out Lucky Dice challenges.  This is done custom because there's
        260 of them (in addition to the "main" one), and there's no real point to
        hardcoding them.  The above methods would be pretty inefficient to use, too,
        since we loop through challenges until we find the correct name.

        Note that when clearing this on a savegame, the saves have an additional
        `tracked_interactions` structure which will need to be cleared out as well.
        """
        for chal in self.base_obj.challenge_data:
            if chal.challenge_class_path == '/Game/GameData/Challenges/GoldenDice/Challenge_Crew_GoldenDice_Meta.Challenge_Crew_GoldenDice_Meta_C':
                chal.completed_count = 0
                chal.currently_completed = False
                chal.progress_counter = 0
                chal.is_active = True
            elif chal.challenge_class_path.startswith('/Game/GameData/Challenges/GoldenDice/Challenge_TrackedInteraction_GoldenDice_'):
                chal.completed_count = 0
                chal.currently_completed = False
                chal.progress_counter = 0
                chal.is_active = False

    def finish_dice_challenges(self):
        """
        Mark all Lucky Dice challenges as complete.  This is done custom because
        there's 260 of them (in addition to the "main" one), and there's no real
        point to hardcoding them.  The above methods would be pretty inefficient to
        use, too, since we loop through challenges until we find the correct name.

        Note that if this is used on a savegame, the saves have an additional
        `tracked_interactions` structure to keep track of which dice have been found.
        If we wanted to be *completely* correct when running this on a save, we'd
        want to have a save-specific routine to also inject data in there.  The
        A/B/C/D GUID-type info in that structure corresponds perfectly to the hex
        values found in the challenge names, so it'd be easy enough.  Functionally,
        though, we don't have to care -- the game will auto-populate that structure
        based on the challenges set here, if it's not already present.
        """
        for chal in self.base_obj.challenge_data:
            if chal.challenge_class_path == '/Game/GameData/Challenges/GoldenDice/Challenge_Crew_GoldenDice_Meta.Challenge_Crew_GoldenDice_Meta_C':
                chal.completed_count = 1
                chal.currently_completed = True
                chal.progress_counter = 260
                chal.is_active = True
            elif chal.challenge_class_path.startswith('/Game/GameData/Challenges/GoldenDice/Challenge_TrackedInteraction_GoldenDice_'):
                chal.completed_count = 1
                chal.currently_completed = True
                chal.progress_counter = 0
                chal.is_active = False


