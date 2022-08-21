#!/bin/bash
ttwl-save-edit -f --dont-randomize-guid --fake-tvhm didnotfinish.sav output/didnotfinish.sav
ttwl-save-info output/didnotfinish.sav --mission-paths | fgrep /Game/Missions/Plot/Mission_Plot00.Mission_Plot00_C
if [[ $(ttwl-save-info output/didnotfinish.sav --mission-paths | fgrep /Game/Missions/Plot/Mission_Plot00.Mission_Plot00_C) ]]; then
    echo "There are missions and there shouldn't be"
    exit 255
fi
exit 0
