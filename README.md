# 6-Personal-Code
Code used within my own systems or outside of the scope of work/schooling
All information that would give away personal or security dependant details have been stripped from the code

---
### Linux quality of life improvements - 
Having started using arch linux to put myself into a position of learning, I found a few bits of code that were necessary to keep the system maintained could be reduced so as to not need to remember all of their intricate parts. This collection features only scripts and does not account for the number of simple commands added to bashrc.
They include:
##### Checksum - 
Used when downloading software with a checksum as security, takes checksum and file and compares them.
##### NaorGa - 
Uses dmenu to allow a user to choose whether to use Nano or gedit when editing.
##### Printstart - 
Starts and stops the printer service as that can be a good foothold into the system if left open.
##### ScreenSwap - 
For when switching between screens, software exists already to do this but greater control without unnecessary processes was deemed useful.

---	
### Projects - 
Whether completed for myself or others,these projects contain multiple files and so deserved their own section, at this time some projects will be mentioned but not included due to them either not being completed or because of security concerns.
They include:
##### Mapper - 
A piece of software designed for a client that takes in dimensions of a cube/cuboid and outputs a map that they can cut out and use, initially developed just to take in the three dimensions, it was later developed to include added features such as:
* A GUI for ease of use
* Centimetre and Inch options
* Tab options on the edge of the box for stability when glueing
* Being able to save the output image into multiple formats
* Having a circle on the back to be able to cut out (a feature the client asked for)
* Setting the DPI of the image to match up to whatever the client is using
* Defaults for all above options

##### RPiNAT - 
I have been interested in developing my networking skills in a more practical sense and wanted a server box I could test on the go. To do this normally I would need to take a screen every time as connecting to the new network means being able to discover the server's new IP which is impossible on some systems without tripping security defences. My idea was to create a service that would run when the device was powered on. This service would either connect to a known network with a pre-determined fixed address (which would generally be the home network or other trusted sources) or it would turn itself into a network, becoming an access point that I could then connect to. Work is unfortunately not finished but I am learning a lot about services in the process.

---
### Pentesting tools - 
These quick scripts were made to make pentesting easier during competitions or when otherwise training, use of common tools like gobuster or wireshark can be forgotten even after a small time has passed and so having a shorthand can be extremely useful. They Include:
##### Datagatherer - 
I was aware that this script might never be useful in actual pentesting but I created it to try to gain an understanding of the commands necessary to gather data on a system.
##### Go-Bust - 
Scrubbed of the pathways for security. A way of automating gobuster that takes common wordlists from the secclist package and runs them against a specified IP or website. Future improvements include more options for use and finding out a way to make pathways flexible rather than fixed.
##### StartAirCrak - 
Because the process of setting up Aircrack is so specific, this code was used to initialise or terminate the program.


