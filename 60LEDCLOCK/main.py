from machine import Pin
import RTC
from neopixel import Neopixel
from time import sleep


##RGB setup##
numpix = 60
strip = Neopixel(numpix, 0, 28, "GRB")
strip.brightness(20)

#HSV to RGB
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
    


##RTC setup##
ds = RTC.DS1302(18,17,16)
print(ds.DateTime()) #Check time/date
pastsec = ds.Second() #Set up the checks for if something has changed
pastmin = ds.Minute()

#For the H value in HSV
hPoints = 0
hHour = 0
hMin = 0
hSecond = 0

##Main Loop##

while 1:
    Hour = int(ds.Hour()%12) #24 hour to 12 hour
    Min = int(ds.Minute()) #Easier to call min
    Sec = int(ds.Second()) #Easier to call second
    if pastsec != ds.Second(): # Checks to see if the second has changed
        print(ds.DateTime()) #Prints the time
        pastsec = ds.Second() #Updates the time to check against
        strip.set_pixel(int(ds.Minute())-1, (0, 0, 0)) #Turn off previous leds
        strip.set_pixel(int(ds.Second())-1, (0, 0, 0))
        strip.set_pixel(Hour*5 + int((ds.Minute()/60)*5)-1, (0, 0, 0))
        r, g, b = [int(255 * c) for c in hsv_to_rgb(Sec*6 / 360.0, 1.0, 1.0)] #RGB changing for second hand
        strip.set_pixel(int(ds.Second()), (r, g, b)) #Sets the second hand to correct position and RGB
        strip.set_pixel(int(ds.Minute()), (255, 0, 0)) #Updates the minute hand
        strip.set_pixel(Hour*5 + int((ds.Minute()/60)*5), (0, 255, 0)) #Updates hour hand
        
        
    hPoints += 1 #Changes the H value in HSV for the points on the clock
    
    ##This code following is dumb, but it works. Looks to see if a hand is over a point of the clock and stops the point overwriting it
    if Sec == 0 or Min == 0 or (Hour*5 + int((ds.Minute()/60)*5)) == 0:
        pass
    else:
        r, g, b = [int(255 * c) for c in hsv_to_rgb(hPoints / 360.0, 1.0, 1.0)]
        strip.set_pixel(0, (r, g, b))
    if Sec == 15 or Min == 15 or (Hour*5 + int((ds.Minute()/60)*5)) == 15:
        pass
    else:
        r, g, b = [int(255 * c) for c in hsv_to_rgb(hPoints / 360.0, 1.0, 0.125)]
        strip.set_pixel(15, (r, g, b))
    if Sec == 30 or Min == 30 or (Hour*5 + int((ds.Minute()/60)*5)) == 30:
        pass
    else:
        r, g, b = [int(255 * c) for c in hsv_to_rgb(hPoints / 360.0, 1.0, 0.125)]
        strip.set_pixel(30, (r, g, b))
    if Sec == 45 or Min == 45 or (Hour*5 + int((ds.Minute()/60)*5)) == 45:
        pass
    else:
        r, g, b = [int(255 * c) for c in hsv_to_rgb(hPoints / 360.0, 1.0, 0.125)]
        strip.set_pixel(45, (r, g, b))
        
    strip.show() #Updates the ring