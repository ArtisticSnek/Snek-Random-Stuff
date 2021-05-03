import usb_hid
import time
import pwmio
import busio
import adafruit_nunchuk
from time import sleep
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import board
from digitalio import DigitalInOut
import digitalio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import neopixel

DEVICE_ADDRESS = 0x52  # device address of DS3231 board
# The follow is for I2C communications

I2C = busio.I2C(scl=board.GP1, sda=board.GP0)

nc = adafruit_nunchuk.Nunchuk(I2C)

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
#For rgb led
pixel_pin = board.GP13
num_pixels = 30
ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
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
#Analog setup
#Analog conversion
#Mute led
led1 = digitalio.DigitalInOut(board.GP14)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP15)
led2.direction = digitalio.Direction.OUTPUT
#buttons
b1 = digitalio.DigitalInOut(board.GP8)
b1.pull = digitalio.Pull.DOWN

b2 = digitalio.DigitalInOut(board.GP7)
b2.pull = digitalio.Pull.DOWN

b3 = digitalio.DigitalInOut(board.GP3)
b3.pull = digitalio.Pull.DOWN

b4 = digitalio.DigitalInOut(board.GP2)
b4.pull = digitalio.Pull.DOWN
#indicators
ind1 = digitalio.DigitalInOut(board.GP11)
ind1.direction = digitalio.Direction.OUTPUT

ind2 = digitalio.DigitalInOut(board.GP10)
ind2.direction = digitalio.Direction.OUTPUT

ind3 = digitalio.DigitalInOut(board.GP9)
ind3.direction = digitalio.Direction.OUTPUT
#rotary encoder defining
in1 = digitalio.DigitalInOut(board.GP6)
in1.pull = digitalio.Pull.DOWN
in2 = digitalio.DigitalInOut(board.GP5)
in1.pull = digitalio.Pull.DOWN
in3 = digitalio.DigitalInOut(board.GP4)
in3.pull = digitalio.Pull.DOWN
led1.value = True

laststate1 = in1.value #volume in1
pastb1 = b1.value #mute button
pastb2 = b2.value #deafen button
pastb3 = b3.value #KB1
pastb4 = b4.value #KB2
def mouseanalog():
    ax, ay, az = nc.acceleration
    jx, jy = nc.joystick
    jx -= 130
    jy -= 130
    if jx > 10:
        if ax > 700:
            mouse.move(20)
        else:
            mouse.move(x=+int(jx/10))
    if jx < -10:
        if ax > 700:
            mouse.move(-20)
        else:
            mouse.move(x=-int(abs(jx/10)))
    if jy > 10:
        if ay > 700:
            mouse.move(y=-20)
        else:
            mouse.move(y=-int(jy/10))
    if jy < -10:
        
        if ay > 700:
            mouse.move(y=20)
        else:
            mouse.move(y=+int(abs(jy/10)))
    if nc.buttons.C:
        mouse.press(Mouse.LEFT_BUTTON)
    else:
        mouse.release_all()
    if nc.buttons.Z:
        mouse.click(Mouse.RIGHT_BUTTON)
        
    '''
    if get_voltage(analog_in1) > 2:
        mouse.move(x=-5)
    if sw.value != swp:
        swp = sw.value
        if sw.value == 0:
            mouse.press(Mouse.LEFT_BUTTON)
        else:
            mouse.release_all()
    '''
def mute():
    global pastb1
    if b1.value != pastb1:
        pastb1 = b1.value
        if b1.value:
            if led1.value == True:
                led1.value = False
                led2.value = True
                kbd.send(Keycode.SHIFT, Keycode.ALT, Keycode.F6)
            else:
                led2.value = False
                led1.value = True
                kbd.send(Keycode.SHIFT, Keycode.ALT, Keycode.F6)
def deafen():
    global pastb2
    if b2.value != pastb2:
        pastb2 = b2.value
        if b2.value:
            if ind1.value == True:
                ind1.value = False
                ind2.value = True
                kbd.send(Keycode.SHIFT, Keycode.CONTROL, Keycode.F7)
            else:
                ind1.value = True
                ind2.value = False
                kbd.send(Keycode.SHIFT, Keycode.CONTROL, Keycode.F7)
def KB1():
    global pastb3
    if b3.value != pastb3:
        pastb3 = b3.value
        if b3.value:
            if ind3.value == True:
                ind3.value = False
                kbd.send(Keycode.SHIFT, Keycode.CONTROL, Keycode.F2)
            else:
                ind3.value = True
                kbd.send(Keycode.SHIFT, Keycode.CONTROL, Keycode.F2)
def KB2():
    global pastb4
    state = 0
    if b4.value != pastb4:
        pastb4 = b4.value
        if b4.value:
            if state == 0:
                kbd.send(Keycode.SHIFT, Keycode.ALT, Keycode.F9)
            else:
                kbd.send(Keycode.SHIFT, Keycode.ALT, Keycode.F9)

def volume():
    global laststate1
    state1 = in1.value
    if state1 != laststate1:
        if in2.value != state1:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        else:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    laststate1 = state1
    pastb2 = b2.value
    
h = 0
ind1.value = True
while 1:
    mouseanalog()
    mute()
    deafen()
    volume()
    KB1()
    KB2()
    red, green, blue = [int(255 * c) for c in hsv_to_rgb(h / 360.0, 1.0, 1.0)]
    h += 1
    pixels.fill((red, green, blue, 0))
    pixels.show()
    
        
        
    
