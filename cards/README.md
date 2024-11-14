# Cards

## Main idea

stability ai back output:1248×1872
double width to add a card same size: 2496×1872
If we halve:1248×936
halve again: 624×468

First we generate the card fronts: 

python exportPNG.py Vert2_CAD_001/svgs/sprite.svg Vert2_CAD_001/ -w 624

This will generarte cards into Vert2_CAD_001/pngs. Eeach card is 624×936 and weight about 30-40 kb. 

Then we run the program to 




## exportPNG.py

Export SVG cards files from sprite sheet to PNG files, or make a PNG sprite sheet.

usage
-----

    exportPNG.py source folder [options]

arguments
---------

**positional arguments:**  

    source    source sprite file path  
    folder    parent directory for png folder 
    
    The folder argument is the name folder that will contain a "pngs" subfolder into 
    which the PNG files will be written.  It will be created if it doesn't exist.

**optional arguments:**

    -h, --help                       show this help message and exit  
    -s, --sprite                     create sprite sheet also   
    -o, --sprite_only                create sprite sheet only  
    -w WIDTH, --width WIDTH          image width (default 75 pixels)  
    -i INKSCAPE, --inkscape INKSCAPE path to inkscape  
    
    The --width argument controls the width of the cards, both for individual files and 
    for sprite sheets.  
    The --sprite parameter indicates that a sprite sheet should be produced in addition 
    to the individual cards.  
    If the --sprite_only parameter is given, only the sprite sheet will be produced.

requirements
------------

This program requires python and Inkscape.  It has been tested with python 3.8, and with Inkscape 1.1.  All testing has been on Xubuntu 20.





