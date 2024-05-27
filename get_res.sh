#!/usr/bin/bash

# Check if folder res exists, if not then create it
if [ ! -d res ]; then
    mkdir res
fi

# Download file and put it in res
wget http://oaei.webdatacommons.org/tdrs/testdata/persistent/knowledgegraph/v3/suite/starwars-swtor/component/target/ -O res/oldRepubl.xml
wget http://oaei.webdatacommons.org/tdrs/testdata/persistent/knowledgegraph/v3/suite/starwars-swg/component/target/ -O res/starWarGalax.xml

