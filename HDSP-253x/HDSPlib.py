from machine import Pin
from time import sleep
from HDSPchars import *
#####setup for the display######
#FL = high
#A0,A1,A2 = Pico - character pins
#A3,A4 = High
#Cls = high
#Clk = disconnected
#WR = Pico - Clock
#CE = low
#RD = high
#Dx = Pico - Data Pins
#RST - Pico - Reset
################################


rows = { #binary for each row
    0 : [0,0,0,0],
    1 : [0,0,0,1],
    2 : [0,0,1,0],
    3 : [0,0,1,1],
    4 : [0,1,0,0],
    5 : [0,1,0,1],
    6 : [0,1,1,0],
    7 : [0,1,1,1],
    8 : [1,0,0,0],
    9 : [1,0,0,1],
    10 : [1,0,1,0],
    11 : [1,0,1,1],
    12 : [1,1,0,0],
    13 : [1,1,0,1],
    14 : [1,1,1,0],
    15 : [1,1,1,1]
    }
columns = { #binary for each column
    0 : [0,0,0,0],
    1 : [0,0,0,1],
    2 : [0,0,1,0],
    3 : [0,0,1,1],
    4 : [0,1,0,0],
    5 : [0,1,0,1],
    6 : [0,1,1,0],
    7 : [0,1,1,1]
    }
posi = { #Character position binary
    1 : [0,0,0],
    2 : [0,0,1],
    3 : [0,1,0],
    4 : [0,1,1],
    5 : [1,0,0],
    6 : [1,0,1],
    7 : [1,1,0],
    8 : [1,1,1]
    }
class HDSP253x: #create class
    def __init__(self, dataPin, charaPin, clk, rst): #bind pins. data pin should be 8 long tuple from lowest data pin to highest data pin. character pin should be 3 long tuple the same as data.
        self.dataPin = tuple(dataPin)
        self.charaPin = tuple(charaPin)
        self.clk = clk
        self.rst = rst
        #setting neccesary pins high
        Pin(self.clk, Pin.OUT).high()
        Pin(self.rst, Pin.OUT).high()
    def reset(self): #reset function
        Pin(self.rst, Pin.OUT).high()
        sleep(0.0001)
        Pin(self.rst, Pin.OUT).low()
        sleep(0.0001)
        Pin(self.rst, Pin.OUT).high()
    def apply(self): #update function
        Pin(self.clk, Pin.OUT).high()
        sleep(0.0001)
        Pin(self.clk, Pin.OUT).low()
        sleep(0.0001)
        Pin(self.clk, Pin.OUT).high()
    def write(self, character, position): #Writes single character to display
        row = []
        col = []
        r = []
        c = []
        #Pin(self.rst,Pin.OUT).high()
        if character in chars: #checks if character exists
            r, c = chars[str(character)] #variables for row and column
            row = rows[r] #converts row to binary
            #row.reverse()
            col = columns[c] #converts column to binary
            #col.reverse()
            data = col + row
            data.reverse()
            for i in range (0,8): #for each data pin, decide whether high or low
                if data[i] == 1:
                    Pin(self.dataPin[i], Pin.OUT).high()
                else:
                    Pin(self.dataPin[i], Pin.OUT).low()
            posBin = posi[position] #converts position to binary
            for i in range (0,3): #for each position pin, decide if high or low
                if posBin[i] == 1:
                    Pin(self.charaPin[i], Pin.OUT).high()
                else:
                    Pin(self.charaPin[i], Pin.OUT).low()
    def writeln(self, line):
        if len(line) > 8:
            pass
        else:
            for i in range (0, len(line)):
                self.write(line[i], i+1)
                self.apply()

