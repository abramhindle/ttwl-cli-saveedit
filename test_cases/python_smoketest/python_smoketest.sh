#!/bin/bash
echo Should print buffmeister twice
if ! python3 test.py; then
    echo "Python returned $?"
    exit 255
fi
