#!/usr/bin/bash

# Check if folder res exists, if not then create it
if [ ! -d res ]; then
    mkdir res
fi

# Download file and put it in res
wget https://raw.githubusercontent.com/city-knowledge-graphs/phd-course/main/python/lab-session3/data/confOf.owl -O res/confOf.owl
wget https://raw.githubusercontent.com/city-knowledge-graphs/phd-course/main/python/lab-session3/data/ekaw.owl -O res/ekaw.owl
wget https://raw.githubusercontent.com/city-knowledge-graphs/phd-course/main/python/lab-session3/data/confOf-ekaw-reference-mappings.ttl -O res/confOf-ekaw-reference-mappings.ttl