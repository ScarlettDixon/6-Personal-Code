#!/bin/bash
# Description: Script to setup the venv environment necessary to then run the given python script
# Author: Scarlett Dixon
# Bibliography: N/A

#---GLOBAL VARIABLES---
# Main Script Vars
production="Production"
venvName="venv"
requirementLocation="Configuration/requirements.txt"
scriptLocation="Scripts/launch.py"

# Testing Script Vars
testing="Testing"
testVenvName="test_venv"
testRequirementLocation="Configuration/test_requirements.txt"
testScriptLocation="Tests/UnitTesting/test_launch.py"

# Misc Vars
downloadsLocation="Downloads"
pythonCommand=python
pipCommand=pip


help(){
	cat <<EOF
Scad File Setup
Description: Used to setup, activate and deactivate the python script
Usage: remind [flag]
  -i Initialises the venv environment
  -s Starts the script with no link - useful for debugging
  -l starts the script but includes a youtube link as an argument
  -p starts the script but includes a playlist link as an argument
  -e starts the script but includes an error file location as an argument
  -t runs the test script, defaults to running the all tests
  -d Deletes the venv enironment
  -h Returns Help Screen
Examples:
	setup.sh -s
    setup.sh -l "https://www.youtube.com/kadfefjneman"
EOF
}

function init (){
    echo -e "---Setting Up Environment---" ;
    activate_check "$venvName" "$1"
    VenvPython=$(which python) ;
    echo "---Updating Virtual Environment Pip ---" ;
    $pythonCommand -m $pipCommand install --upgrade $pipCommand ;
    #At Location: $wh_py $wh_py -m $pipCommand install --upgrade $pipCommand ;
    #$pipCommand --disable-pip-version-check list --outdated --format=json | $pythonCommand -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 $pipCommand install -U ;
    echo "---Installing Required Libraries---" ;
    $pipCommand install -r $requirementLocation --upgrade ;
    echo "---Required Libraries Installed---" ;
    deactivate ;
}


function start (){
    activate_check "$venvName" "$production"
    script_check "$scriptLocation" "$production"
    
}

function link(){
    echo "---Running Python Script with given youtube Link---" ;
    activate_check "$venvName" "$production"
    echo -e "---Link URL: $1---" ;
    script_check "$scriptLocation" "$production" "-l $1 -f $downloadsLocation";
}

function playlist(){
    echo "---Running Python Script over given playlist---" ;
    activate_check "$venvName" "$production"
    echo -e "---Playlist URL: $1---" ;
    script_check "$scriptLocation" "$production" "-p $1 -f $downloadsLocation";
}

function errorfile(){
    echo "---Running Python Script over given error file---" ;
    activate_check "$venvName" "$production"
    echo -e "---Error File Location: $pwd/$1---" ;
    script_check "$scriptLocation" "$production" "-e $1 -f $downloadsLocation";
}

function test (){
    echo "---Running Test Script---" ;
    echo -e "---Test File Location: $pwd/$testScriptLocation---" ;
    activate_check "$testVenvName" "$testing"
    script_check "$testScriptLocation" "$testing"
}

function delete (){
    echo "---Deactivating Virtual Environment---" ;
    deactivate
    echo "---Virtual Environment Deactivated---" ;
    echo "---Deleting Virtual Environment---" ;
    rm -R $venvName ;
    echo "---Virtual Environment Deleted---" ;
}

function activate_check (){
    echo "---Activating Virtual Environment---" ;
    if [ ! -d "$1" ]; then #If Virtual Environment Directory Doesn't Exist
        if [ ${FUNCNAME[1]} == "init" || ${FUNCNAME[1]} == "test" ]; then
            $pythonCommand -m venv $1 ;
            echo "--- $2 Virtual Environment Created---" ;
        else
            echo "---$2 Virtual Environment Doesn't Exist---" ;
            echo "---Please Use the Initialise Argument---" ;
            exit ;
        fi
    else
        echo "---$2 Virtual Environment Exists---" ;
        source $1/bin/activate #- Starting Virtual Environment
        echo "---Virtual Environment Activated---" ;
    fi
}

function script_check () {
    if [ ! -f "$1" ]; then #If Script file doesn't exist
        echo "---$2 Script Doesn't Exist---" ;
        echo "---Please Generate the Script or Change the Script Location Variable---" ;
        exit ;
    else
        echo "---Running Python Script---" ;
        $pythonCommand $1 $3 ;
    fi
}

echo -e "---Youtube Downloader Setup---" ;
while getopts "dehilpst" options; do #Using getopts for options, no : if no argument
	case "${options}" in                        
	    i) init "$production";;
        s) start ;;
        l) link "$2" ;;
        p) playlist "$2" ;;
        e) errorfile "$2" ;;
        t) test ;;
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
