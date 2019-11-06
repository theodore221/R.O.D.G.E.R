### GUI Interface

from tkinter import *
from tkinter import ttk
import os
import time
os.system ("sudo pigpiod")
time.sleep(1) # program needs to wait for a second before it can import the 'pi$
import pigpio
import inputs
import math

left = 5 # Declaring Pins
right = 21
middle = 13
idle = 1500 # above this is forwards, before this is backwards, range about 100$
low_front = 1600
low_back = 1400

pi = pigpio.pi()


### User Initizlization procedure to make sure motors are turned on safely
print ("Inititializing...")
print ("Switch OFF")
pi.set_servo_pulsewidth (left, idle)
pi.set_servo_pulsewidth (middle, idle)
pi.set_servo_pulsewidth (right, idle)
check = input ("Press Enter to continue")
print ("Switch ON and WAIT UNTIL COMPLETE")
check = input ("Press Enter to continue")



### Functions to call upon
def go_move (left_power, right_power):
    pi.set_servo_pulsewidth (left, idle) # Resets left and right motor before c$
    pi.set_servo_pulsewidth (right, idle)
    pi.set_servo_pulsewidth (left, left_power)
    pi.set_servo_pulsewidth (right, right_power)

def go_idle ():
    pi.set_servo_pulsewidth (left, 1500)
    pi.set_servo_pulsewidth (right, 1500)

def vertical_go (vertical_power):
    pi.set_servo_pulsewidth (middle, idle) # reset first
    pi.set_servo_pulsewidth (middle, vertical_power)

def vertical_idle ():
    pi.set_servo_pulsewidth (middle, idle)

def my_map (x, in_min, in_max, out_min, out_max): # Returns int not float!
    return int(((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min))

accl = 1500
back_accl = 1500
def update ():
    global accl
    accl = my_map (slider_value.get(), 0, 100, 1600, 2000)
    global back_accl
    back_accl = my_map (slider_value.get(), 0, 100, 1400, 1000)


def exitall ():
    pi.set_servo_pulsewidth (left, 0)
    pi.set_servo_pulsewidth (right, 0)
    pi.set_servo_pulsewidth (middle, 0)
    pi.stop()
    print("Motors off...")
    time.sleep(1)
    print ("Exiting...")
    time.sleep(1)
    exit()


controller = ""
# The motor idle point
CONST_IDLE = 1500

# ABS_RZ is right trigger with value range of 0 - 255
# ABS_Z is left trigger with value range of 0 - 255
# ABS_X is left thumbstick x axis with value range of aprox(-33000 - 33000)
# ABS_Y is left thumbstick y axis with value range of aprox(-33000 - 33000)
# ABS_HAT0Y is D pad 1 is down, -1 is up
# ABS_HAT0X id D pad 1 is right, -1 is left
for device in inputs.devices.gamepads:
    if device:
        controller = device
x = 0
y = 0
while 1:
    events = inputs.get_gamepad()
    for event in events:
        if event.code == "BTN_EAST":
            if event.state == 1:
                go_idle()
        if event.code == "ABS_X":
            if event.state > 6600 or event.state < -6600:
                x = event.state
            else:
                x = 0
        if event.code == "ABS_Y":
            if event.state > 6600 or event.state < -6600:
                y = event.state
            else:
                y = 0
    z = math.atan2(y, x)
    z = z * 180 / math.pi
    h = max(x, y)
    h = h/330
    h = abs(h)
    #print(h)
    xaccl = my_map(h,0,100,1600,2000)
    yaccl = my_map(h,0,100,1400,1000)
    if h < 4:
        h = 0
        go_idle()
    if h > 5:
        if z > -22.5 and z <= 22.5:
            go_move(yaccl,xaccl)
            print("E")
        elif z > 22.5 and z <= 67.5:
            print("NE")
            go_move(xaccl,low_front)
        elif z > 67.5 and z <= 112.5:
            print("N")
            go_move(xaccl,xaccl)
        elif z > 112.5 and z <= 157.5:
            print("NW")
            go_move(low_front,xaccl)
        elif z > 157.5 or z <= -157.5:
            print("West")
            go_move(xaccl,yaccl)
        elif z > -157.5 and z <= -112.5:
            print("SW")
            go_move(low_back,yaccl)
        elif z > -112.5 and z <= -67.5:
            print("S")
            go_move(yaccl, yaccl)
        elif z > -67.5 and z <= -22.5:
            print("SE")
            go_move(yaccl, low_back)

"""
### GUI BELOW HERE
root = Tk()
root.title ("GUI Interface 1")
user = ttk.Frame (root, relief=SOLID)
user.pack(side=LEFT)
Button (user, text="NW", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(low_front$
Button (user, text="N", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, accl$
Button (user, text="NE", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, low$
Button (user, text="W", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, back$
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: go_idle()).grid(row=2, column$
Button (user, text="E", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl,$
Button (user, text="SW", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(low_back,$
Button (user, text="S", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl,$
Button (user, text="SE", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl$

Button (user, text="UP", padx=my_padx, pady=my_pady, command=lambda: [(update()), (vertical_go(accl)$
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: vertical_idle()).grid(row=4, $
Button (user, text="DOWN", padx=my_padx, pady=my_pady, command=lambda: [(update()), (vertical_go(bac$

developer = ttk.Frame (root, relief=SOLID)
developer.pack (side=LEFT)

# USER FRAME
Label (user, text="User").grid(row=0, column=1)
my_padx = 30
my_pady = 30

Button (user, text="NW", padx=my_padx, pady=my_pady, command=lambda: [(update()$
Button (user, text="N", padx=my_padx, pady=my_pady, command=lambda: [(update())$
Button (user, text="NE", padx=my_padx, pady=my_pady, command=lambda: [(update()$
Button (user, text="W", padx=my_padx, pady=my_pady, command=lambda: [(update())$
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: go_idle($
Button (user, text="E", padx=my_padx, pady=my_pady, command=lambda: [(update())$
Button (user, text="SW", padx=my_padx, pady=my_pady, command=lambda: [(update()$
Button (user, text="S", padx=my_padx, pady=my_pady, command=lambda: [(update())$
Button (user, text="SE", padx=my_padx, pady=my_pady, command=lambda: [(update()$

Button (user, text="UP", padx=my_padx, pady=my_pady, command=lambda: [(update()$
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: vertical$
Button (user, text="DOWN", padx=my_padx, pady=my_pady, command=lambda: [(update$

slider_value = IntVar()
slider_value.set(50)
slider = ttk.Scale (user, from_=100, to=0, orient=VERTICAL, variable=slider_val$
#accl = my_map (slider_value.get(), 0, 100, 1600, 2000)
#back_accl = my_map (slider_value.get(), 0, 100, 1400, 1000)


# DEVELOPER FRAME
Label (developer, text="Developer").grid(row=0, column=1)
check_left = ttk.Checkbutton (developer, text="Left").grid(row=1, column=0)
check_right = ttk.Checkbutton (developer, text="Right").grid(row=1, column=1)
check_middle = ttk.Checkbutton (developer, text="Middle").grid(row=1, column=2)
Label (developer, text="Currently ").grid(row=3, column=0)
Label (developer, text="Currently ").grid(row=3, column=1)
Label (developer, text="Currently ").grid(row=3, column=2)
entry_left = Entry (developer)
entry_left.grid(row=4, column=0)
entry_right = Entry (developer)
entry_right.grid(row=4, column=1)
entry_middle = Entry (developer)
entry_middle.grid(row=4, column=2)
Button (developer, text="SET").grid(row=5, column=0)
Button (developer, text="SET").grid(row=5, column=1)
Button (developer, text="SET").grid(row=5, column=2)
Button (developer, text="ALL OFF").grid(row=6, column=1)
Button (developer, text="ALL ON").grid(row=7, column=1)
Button (developer, text="EXIT", command=lambda: exit()).grid(row=8, column=1)
"""
