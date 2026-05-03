#!/bin/bash
# Description: Script to setup the venv environment necessary to then run the given python script
# Author: Scarlett Dixon
# Bibliography: N/A

venvName="venv"
requirementLocation="requirements.txt"
scriptLocation="Scripts/CyberdeckPython.py"
pythonCommand=python
pipCommand=pip

help(){
	cat <<EOF
Scad File Setup
Description: Used to setup, activate and deactivate the python script
Usage: remind [flag]
  -i Initialises the venv environment
  -s Starts the script
  -d Deletes the venv enironment
  -h Returns Help Screen
Examples:
	setup.sh -s
EOF
}

init(){
    echo -e "---Setting Up Environment---" ;
    if [ ! -d "$venvName" ]; then #If Virtual Environment doesn't exist
        $pythonCommand -m venv $venvName ;
        echo "---Virtual Environment Created---" ;
    fi
    echo "---Activating Virtual Environment---" ;
    source $venvName/bin/activate
    echo "---Virtual Environment Activated---" ;
    VenvPython=$(which python) ;
    echo "---Updating Virtual Environment Pip ---" ;
    $pythonCommand -m $pipCommand install --upgrade $pipCommand
    #At Location: $wh_py $wh_py -m $pipCommand install --upgrade $pipCommand ;
    #$pipCommand --disable-pip-version-check list --outdated --format=json | $pythonCommand -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 $pipCommand install -U ;
    echo "---Installing Required Libraries---" ;
    $pipCommand install -r $requirementLocation --upgrade
    echo "---Required Libraries Installed---" ;
    deactivate
}


start(){
    echo "---Activating Virtual Environment---" ;
    source $venvName/bin/activate #- Starting venv
    echo "---Virtual Environment Activated---" ;
    echo "---Running Python Script---" ;
    $pythonCommand $scriptLocation
}

delete(){
    echo "---Deactivating Virtual Environment---" ;
    deactivate
    echo "---Virtual Environment Deactivated---" ;
    echo "---Deleting Virtual Environment---" ;
    rm -R $venvName ;
    echo "---Virtual Environment Deleted---" ;
}

echo -e "---Scad File Setup---"
while getopts "isdh" options; do #Using getopts for options, no : if no argument
	case "${options}" in                        
	    i) init ;;
        s) start ;;
		d) delete ;;
		h) help ;;
	    \?) start;;
  	esac
done



#Using the code:
#pyenv install 3.7.0 - install older version of python
#pyenv local 3.7.0 - switch to it
#pip install <PackageName>
#pip install -r requirements.txt
#Issues can be caused by none up to date packages, stop this by doing the following:
#python -m pip install --upgrade pytube & 
#python3 -m pip list --format=freeze > requirements.txt
#python -m pip cache remove <Pattern>
# echo "---Updating Main Pip---" ;
# which python ;
# $pythonCommand -m $pipCommand install --upgrade $pipCommand ;