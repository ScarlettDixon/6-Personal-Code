#!/bin/bash

pythonCommand=python3
pipCommand=pip

echo "---Updating Main Pip---" ;
which python ;
$pythonCommand -m $pipCommand install --upgrade $pipCommand ;
echo "---Setting Up Environment---" ;
$pythonCommand -m venv venv ;
echo "---Virtual Environment Created, Activating---" ;
source venv/bin/activate ;
echo "---Virtual Environment Activated---" ;
echo "---Updating Virtual Environment---" ;
wh_py=$(which python) ;
echo "Updating the Pip found here: $wh_py" ;
$wh_py -m $pipCommand install --upgrade $pipCommand ;
$pipCommand --disable-pip-version-check list --outdated --format=json | $pythonCommand -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 $pipCommand install -U ;
echo "---Installing Required Libraries---" ;
$pipCommand install -q -r Configuration/requirements.txt ;
echo "---Required Libraries Installed---" ;
echo "---Running Script---" ;
python Scripts/__main__.py ;