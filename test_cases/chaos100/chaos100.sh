#!/bin/bash
mkdir output 
ttwl-save-edit -f --dont-randomize-guid --chaos 100 didfinish.sav output/didfinish.sav
if [[ $(ttwl-save-info output/didfinish.sav --mission-paths | fgrep 'Chaos Level: 100') ]]; then
	# nothing
    true
else
    echo "Not chaos 100!"
    exit 255
fi
exit 0
