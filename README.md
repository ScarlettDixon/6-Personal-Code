# 6-Personal-Code
---

[![license](https://img.shields.io/github/license/ScarlettDixon/6-Personal-Code.svg)](LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![language](https://img.shields.io/badge/python-blue?logo=python)](https://www.python.org/)

Code used within my own systems or outside of the scope of work/schooling.
All information that would give away personal or security dependant details have been stripped from the code.

## Table of Contents

- [Security](#security)
- [Background](#background)
- [LinuxQOLI](#linuxqualityoflifeimprovements)
    - [Checksum](#checksum)
    - [TextEditorChoice](#texteditorchoice)
    - [Printstart](#printstart)
    - [ScreenSwap](#screenswap)
    - [FindLast](#findlast)
- [Projects](#projects)
    - [Mapper](#mapper)
    - [RPiNAT](#rpinat)
- [PTTools](#pentestingtools)
    - [Datagatherer](#datagatherer)
    - [Go-Bust](#go-bust)
    - [StartAirCrak](#startairCrak)
- [YoutubeDownloader](#youtubedownloader)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Security
I can take no responsibility for the security of these scripts as they were developed over multiple years and are numerous enough that I can not maintain them all. Use at your own risk.

## Background
Over the years I have completed many projects outside of work and schooling that have been useful for efficiency and in my personal development.
These repositories were mainly created before I had a full grasp of how Github worked so instead of repositories for each of these individually they are collected.

---
### LinuxQualityOfLifeImprovements
LinuxQOLI - Having started using arch linux to put myself into a position of learning, I found a few bits of code that were necessary to keep the system maintained could be reduced so as to not need to remember all of their intricate parts. This collection features only scripts and does not account for the number of simple commands added to bashrc.
They include:
##### Checksum
Used when downloading software with a checksum as security, takes checksum and file and compares them.
##### TextEditorChoice
Uses dmenu to allow a user to choose which text editor to use (nano, gedit, vscode) when editing.
##### Printstart
Starts and stops the printer service as that can be a good foothold into the system if left open.
##### ScreenSwap
For when switching between screens, software exists already to do this but greater control without unnecessary processes was deemed useful.
##### FindLast
This script is used to add a number of shortcuts for editing the latest changed file within a directory, including echoing details about that file, changing to that directory and adding the file or whole directory to be added to git.

---	
### Projects
Whether completed for myself or others,these projects contain multiple files and so deserved their own section, at this time some projects will be mentioned but not included due to them either not being completed or because of security concerns. 
They include:
##### Mapper
A piece of software designed for a client that takes in dimensions of a cube/cuboid and outputs a map that they can cut out and use, initially developed just to take in the three dimensions, it was later developed to include added features such as:
* A GUI for ease of use
* Centimetre and Inch options
* Tab options on the edge of the box for stability when glueing
* Being able to save the output image into multiple formats
* Having a circle on the back to be able to cut out (a feature the client asked for)
* Setting the DPI of the image to match up to whatever the client is using
* Defaults for all above options
##### RPiNAT
I have been interested in developing my networking skills in a more practical sense and wanted a server box I could test on the go. To do this normally I would need to take a screen every time as connecting to the new network means being able to discover the server's new IP which is impossible on some systems without tripping security defences. My idea was to create a service that would run when the device was powered on. This service would either connect to a known network with a pre-determined fixed address (which would generally be the home network or other trusted sources) or it would turn itself into a network, becoming an access point that I could then connect to. Work is unfortunately not finished but I am learning a lot about services in the process.

---
### PentestingTools
PTTools - These quick scripts were made to make pentesting easier during competitions or when otherwise training, use of common tools like gobuster or wireshark can be forgotten even after a small time has passed and so having a shorthand can be extremely useful. 
They Include:
##### Datagatherer
I was aware that this script might never be useful in actual pentesting but I created it to try to gain an understanding of the commands necessary to gather data on a system.
##### Go-Bust
Scrubbed of the pathways for security. A way of automating gobuster that takes common wordlists from the secclist package and runs them against a specified IP or website. Future improvements include more options for use and finding out a way to make pathways flexible rather than fixed.
##### StartAirCrak
Because the process of setting up Aircrack is so specific, this code was used to initialise or terminate the program.

---
### YoutubeDownloader
To keep audio copies of personal youtube videos, I developed a script to download them and convert them to the MP3 format. Attempts will be made in future to add more input protection and the option of keep the videos in their original mp4 format. Other features include:
* Metadata addition based on the video title and author
* Playlist or single video download
* A number of checks to ensure ease of use
Due to this becoming such a big project, I have given it its own folder, hopefully some future Devops content will involve testing of this script.


## Maintainers

[@ScarlettDixon](https://github.com/ScarlettDixon).

## Contributing

Issues and PRs accepted.

If editing the Readme, please conform to the [Standard README](https://github.com/RichardLitt/standard-readme) specification.

This Repository follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/ScarlettDixon/6-Personal-Code/graphs/contributors"></a>

## License

[GNU © Scarlett Dixon.](LICENSE)