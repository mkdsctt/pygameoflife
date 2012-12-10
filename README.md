Description:
-------------
<pre>
This program uses python and pygame to implement Conway's Game of Life.
</pre>

Requirements:
-------------
<pre>
Python 2.7.3
Pygame 1.9.1
</pre>

Input File Format:
-------------
<pre>
# game of life simulation - seed description file format:
# the # symbol indicates a comment line
#'Width' refers to the canvas size (in pixels)  
#'Height' referse to the canvas width (in pixels)  
#'Size' is the size of a cell in the grid (in pixels)  
#'NUM' is the number of 'live' cells (coordinates to follow in the file)  
width,height,size,NUM
x[0],    y[0]
x[1],    y[1]
.        .
.        .
.        .
x[NUM-1],y[NUM-1]
</pre>

Keyboard Commands:
-------------
<pre>
ESC     exit
SPC     generation step
-       decrease the play speed
=       increase the play speed
p       toggle play/pause
c       clear game board
n       add noise
o       write game to std output
</pre>

Mouse Interaction:
-------------
<pre>
You can use the mouse to toggle cells on/off.
</pre>