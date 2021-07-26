from HDSPlib import * # import the library
from time import sleep

disp = HDSP253x([16,17,18,19,20,21,22,10], [14,13,12], 15, 11) #Assign pins to the display HDSP253x([D0-D8], [A3-A0], WR, RST)

disp.reset() #Clears the display
character = "A"
position = 2
disp.write(character, position) #Writes a character to a specific position on the display
disp.apply() #Makes the character visible. This should be called after every character
sleep(5)
disp.reset()
disp.writeln("Test") # takes a string and outputs it to one display
sleep(5)

from HDSPcomp import * #imports the HDSP multi display library

disp1 = HDSP253x([16,17,18,19,20,21,22,10], [14,13,12], 8, 9) #All pins are the sime besides WR and RST

MultiWriteln("Hello world!", disp, disp1) #The string to write and the two displays. Automatically applys changes