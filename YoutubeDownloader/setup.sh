#!/bin/bash
# Description: Script to setup the venv environment necessary to then run the given python script
# Author: Scarlett Dixon
# Bibliography: N/A

venvName="venv"
requirementLocation="requirements.txt"
scriptLocation="__main__.py"
DownloadsLocation="Downloads"

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
  -d Deletes the venv enironment
  -h Returns Help Screen
Examples:
	setup.sh -s
    setup.sh -l "https://www.youtube.com/kadfefjneman"
EOF
}

init(){
    echo -e "---Setting Up Environment---" ;
    if [ ! -d "$venvName" ]; then
        python3 -m venv $venvName ;
    fi
    source $venvName/bin/activate ;
    python -m pip install --upgrade pip ;
    pip install -r $requirementLocation --upgrade ;
    deactivate ;
}


start(){
    echo "---Running Python Script with no Link---" ;
    source $venvName/bin/activate ; #- Starting venv
    python $scriptLocation ;
}

link(){
    echo "---Running Python Script with given youtube Link---" ;
    source $venvName/bin/activate ; #- Starting venv
    echo -e "---Link URL: $1---" ;
    python $scriptLocation "-l" $1 "-f" $DownloadsLocation;
}

playlist(){
    echo "---Running Python Script over given playlist---" ;
    source $venvName/bin/activate ; #- Starting venv
    python $scriptLocation "-p" "$1" "-f" $DownloadsLocation;
}

errorfile(){
    echo "---Running Python Script over given error file---" ;
    source $venvName/bin/activate ; #- Starting venv
    python $scriptLocation "-e" "$1" "-f" $DownloadsLocation;
}

delete(){
    deactivate ;
    rm -R $venvName ;
}

echo -e "---Youtube Downloader Setup---" ;
while getopts "islpedh" options; do #Using getopts for options, no : if no argument
	case "${options}" in                        
	    i) init ;;
        s) start ;;
        l) link "$2" ;;
        p) playlist "$2" ;;
        e) errorfile "$2" ;;
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
#