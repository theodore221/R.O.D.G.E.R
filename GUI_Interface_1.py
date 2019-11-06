### GUI Interface

### Questions
# Why you can't go from forwards to backwards but you can go from backwards to forwards
# Why you can go forwards to backwards if you put it in 'idle' first but I DO execute that command in the 'go_move' function
# Is there variables I can draw on from the chip such as 'motor spinning' or something

import cProfile
from tkinter import *
from tkinter import ttk
#import cv2
#from PIL import Image
#from PIL import ImageTk
import os
import time
os.system ("sudo pigpiod")
time.sleep(1) # program needs to wait for a second before it can import the 'pigpio library'
import pigpio

left = 5 # Declaring Pins
right = 21
middle = 13
idle = 1500 # above this is forwards, before this is backwards, range about 1000-2000
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
    pi.set_servo_pulsewidth (left, idle) # Resets left and right motor before changing speed
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


accl = idle
back_accl = idle
def update ():
    global accl
    accl = my_map (slider_value.get(), 0, 100, 1600, 2000)
    global back_accl
    back_accl = my_map (slider_value.get(), 0, 100, 1400, 1000)

def motor_set (motor, option):
    try:
        speed = int(option.get())
    except ValueError:
        print ("Text field is not in integer format")
        option.insert (0, "Not a number, try again")
        time.sleep(2)
        option.delete (0, END)
        speed = 1500
    pi.set_servo_pulsewidth (motor, idle)
    pi.set_servo_pulsewidth (motor, speed)

def all_idle ():
    pi.set_servo_pulsewidth (left, idle)
    pi.set_servo_pulsewidth (right, idle)
    pi.set_servo_pulsewidth (middle, idle)

def all_on ():
    pi.set_servo_pulsewidth (left, accl)
    pi.set_servo_pulsewidth (right, accl)
    pi.set_servo_pulsewidth (middle, accl)

def exitall ():
    pi.set_servo_pulsewidth (left, 0)
    pi.set_servo_pulsewidth (right, 0)
    pi.set_servo_pulsewidth (middle, 0)
    pi.stop()
    vid.release()
    cv2.destroyAllWindows()
    print("Motors off...")
    print ("Camera Off...")
    time.sleep(1)
    print ("Exiting...")
    time.sleep(1)
    exit()

### GUI BELOW HERE
root = Tk()
root.title ("GUI Interface 1")
user = ttk.Frame (root, relief=SOLID)
user.pack(side=LEFT)
developer = ttk.Frame (root, relief=SOLID)
developer.pack (side=LEFT)
video_screen = ttk.Frame (root, relief=SOLID, width=600, height=500)
video_screen.pack (side=LEFT)

# USER FRAME
Label (user, text="User").grid(row=0, column=1)
my_padx = 30
my_pady = 30

Button (user, text="NW", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(low_front, accl))]).grid(row=1, column=0)
Button (user, text="N", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, accl))]).grid(row=1, column=1)
Button (user, text="NE", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, low_front))]).grid(row=1, column=2)
Button (user, text="W", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(accl, back_accl))]).grid(row=2, column=0)
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: go_idle()).grid(row=2, column=1)
Button (user, text="E", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl, accl))]).grid(row=2, column=2)
Button (user, text="SW", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(low_back, back_accl))]).grid(row=3, column=0)
Button (user, text="S", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl, back_accl))]).grid(row=3, column=1)
Button (user, text="SE", padx=my_padx, pady=my_pady, command=lambda: [(update()), (go_move(back_accl, low_back))]).grid(row=3, column=2)

Button (user, text="UP", padx=my_padx, pady=my_pady, command=lambda: [(update()), (vertical_go(accl))]).grid(row=4, column=0)
Button (user, text="IDLE", padx=my_padx, pady=my_pady, command=lambda: vertical_idle()).grid(row=4, column=1)
Button (user, text="DOWN", padx=my_padx, pady=my_pady, command=lambda: [(update()), (vertical_go(back_accl))]).grid(row=4, column=2)

slider_value = IntVar()
slider_value.set(50)
slider = ttk.Scale (user, from_=100, to=0, orient=VERTICAL, variable=slider_value).grid(row=2, column=3)
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
Button (developer, text="SET", command = lambda: motor_set(left, entry_left)).grid(row=5, column=0)
Button (developer, text="SET", command = lambda: motor_set(right, entry_right)).grid(row=5, column=1)
Button (developer, text="SET", command = lambda: motor_set(middle, entry_middle)).grid(row=5, column=2)
Button (developer, text="ALL OFF", command = lambda: all_idle()).grid(row=6, column=1)
Button (developer, text="ALL ON", command = lambda: all_on ()).grid(row=7, column=1)
Button (developer, text="EXIT", command=lambda: exit()).grid(row=8, column=1)

# Video_screen
Label (video_screen, text="LIVE STREAM").pack()
my_video = Label(video_screen)
my_video.pack()
on_off = IntVar()
check_video = ttk.Checkbutton (video_screen, text="Video", variable=on_off, command=lambda: video_update())
check_video.pack()



#vid = cv2.VideoCapture ("http://172.19.183.103:9000/?action=stream")
vid = cv2.VideoCapture (0)
def show_frame():
    _, frame = vid.read()
    temp_img = Image.fromarray (frame)
    temp_imgtk = ImageTk.PhotoImage(image=temp_img)
    my_video.imgtk = (temp_imgtk)
    my_video.configure (image=temp_imgtk)
    my_video.after (10, show_frame)

def video_update():
    if on_off.get() == 1:
        show_frame()

#show_frame()
root.mainloop()



### Open CV Displaying by itself
#vid = cv2.VideoCapture ("http://172.19.11.242:9000/?action=stream")
#vid = cv2.VideoCapture (0)
#while vid.isOpened():
#    ret, frame = vid.read()
#    if ret:
#        cv2.imshow("original", frame)
#        if cv2.waitKey (1) & 0xFF == ord("q"):
#            break
#vid.release()
#cv2.destroyAllWindows()
