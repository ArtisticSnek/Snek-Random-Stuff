from machine import Pin
import RTC
from neopixel import Neopixel
##RGB setup##
numpix = 12
strip = Neopixel(numpix, 0, 15, "GRBW")
strip.brightness(40)
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
h = 0
h1= 0

##RTC setup##
ds = RTC.DS1302(18,17,16)
def timerConv(secondsIn): #Bad solution, but works. It checks where in the minute/hour we are
    if secondsIn in range(0,6):
        return(1)
    if secondsIn in range(6,11):
        return(2)
    if secondsIn in range(11,16):
        return(3)
    if secondsIn in range(16,21):
        return(4)
    if secondsIn in range(21,26):
        return(5)
    if secondsIn in range(26,31):
        return(6)
    if secondsIn in range(31,36):
        return(7)
    if secondsIn in range(36,41):
        return(8)
    if secondsIn in range(41,46):
        return(9)
    if secondsIn in range(46,51):
        return(10)
    if secondsIn in range(51,56):
        return(11)
    if secondsIn in range(56,61):
        return(12)
    
print(ds.DateTime()) #Check time/date


pastsec = ds.Second() #Set up the checks for if something has changed
pastmin = ds.Minute()


##Main Loop##
while 1:
    if pastsec != ds.Second():#checks if something has changed
        print(ds.DateTime())
        pastsec = ds.Second() #If something has changed, update the variable it checks against
        strip.set_pixel(int(ds.Minute()/5)-1, (0, 0, 0, 0)) #Turn off previous leds
        strip.set_pixel(int(ds.Second()/5)-1, (0, 0, 0, 0))
        
        h+=72 #Changes RGB colour
        r, g, b = [int(255 * c) for c in hsv_to_rgb(h / 360.0, 1.0, 1.0)]
        
        
        strip.set_pixel(int(ds.Second()/5), (r, g, b, 0)) #Second Hand update
        if int(ds.Minute()/5) != int(ds.Second()/5): #Checks to see if I need to disable white minute LED
            h1+=2 #Changes RGB colour
            r, g, b = [int(255 * c) for c in hsv_to_rgb(h1 / 360.0, 1.0, 1.0)]
            strip.set_pixel(int(ds.Minute()/5), (r, g, b, 255))
                                                 
        strip.show() #Update RGB
