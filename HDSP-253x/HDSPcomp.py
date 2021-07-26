from HDSPlib import *

def MultiWriteln(line, ds1, ds2):
    if len(line) > 16:
            pass
    else:
        for i in range (0, len(line)):
            if i < 8:
                ds1.write(line[i], i+1)
                ds1.apply()
            else:
                ds2.write(line[i], (i+1)-8)
                ds2.apply()