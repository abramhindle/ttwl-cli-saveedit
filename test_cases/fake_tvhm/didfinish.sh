#!/bin/bash
mkdir -q output 
ttwl-save-edit -f --dont-randomize-guid --fake-tvhm didfinish.sav output/didfinish.sav
if [[ $(ttwl-save-info output/didfinish.sav -v --mission-paths | fgrep Mission_Plot00_C) ]]; then
    echo "There are missions and there shouldn't be"
    exit 255
fi
if [[ $(ttwl-save-info output/didfinish.sav --mission-paths | fgrep 'Chaos Level: 50') ]]; then
	# nothing
    true
else
    echo "Not chaos 50!"
    exit 255
fi
exit 0
