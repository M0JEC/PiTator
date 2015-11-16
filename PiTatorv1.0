import os
import RPi.GPIO as GPIO
import time

import socket
import sys
from thread import *



try: #      Routine needed for keyboard input.
    from msvcrt import getch
except ImportError:
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
char = None

xseconds = 0 #  initialise time variables
yseconds = 0
ele = 0 #       Elevation
az = 0 #        Azimuth
xc = 6.666 #   X axis correction factor (degrees per second)
yc = 1.875 #    Y axis Correction Factor (degrees per second)
yt = 0 #        Y axis Target position
xt = 0 #        X axis Target position


class ActionHandler(object):
    def handle_p_set(self, azimuth, elevation):
        global xt
        global yt
        xt = float(azimuth)
        yt = float(elevation)
        print("set to {}:{}".format(azimuth, elevation))

    def handle_p_get(self):
        print("request postion")
        return [str(az), str(ele)]

    def handle_message(self, cmd, *params):
        action_map = {
            'P': self.handle_p_set,
            'p': self.handle_p_get
        }
        return "\n".join(action_map[cmd](*params) or []) or "\n"




def dt(): #     Direction test - Decides which routine to call for movemenr
    global ele
    global yc
    global yt
    global az
    global xc
    global xt
    oxt = xt #  Resets OLD xt and NEW xt variables used when over 85 Deg elevation
    nxt = xt
    if yt >= 85: #  subroutine to position the X axis 90 degrees off when at near vertical >85 Deg (saves time on overhead passes)
        print ('old x =') + str(xt)
        if xt >= 180: # Decides if the current position is above or below the mid position on the rotator.
            nxt = xt - 90
            oxt = xt
        else:
            nxt = xt + 90
            oxt = xt
        print ('new x =') + str(nxt)
        xt = nxt
    if xt >= az: #      RIGHT test
        if yt >= ele: # UP Test
            ur()
        else: #         If RIGHT and not UP must be DOWN and Right
            dr()
    elif xt <= az: #    LEFT test
        if yt >= ele: # UP test
            ul()
        else: #         If LEFT and not UP must be DOWN and Left
            dl()
    xt = oxt
    return()
def ul(): #     Move Up and/or Left
    global ele
    global yc
    global yt
    global az
    global xc
    global xt
    yseconds = (yt - ele) * (1 / yc)
    print ('target ') + str(yt) + (' degrees')
    print ('moving up for ') + str(yseconds) + (' seconds')
    
    xseconds = (az - xt) * (1 / xc)
    print ('target ') + str(xt) + (' degrees')
    print ('moving left for ') + str(xseconds) + (' Seconds')
    
    GPIO.output(17, True)
    GPIO.output(18, False)
    GPIO.output(27, True)
    GPIO.output(22, False)
    if xseconds > yseconds:
        time.sleep(yseconds)
        GPIO.output(18, True)
        time.sleep(xseconds - yseconds)
        GPIO.output(22, True)
    else:
        time.sleep(xseconds)
        GPIO.output(22, True)
        time.sleep(yseconds - xseconds)
        GPIO.output(18, True)
    
    ele = yt
    print ('elevation is ') + str(ele)
    
    az = xt
    print ('azimuth is ') + str(az)
    return()
def ur(): #     Move Up and/or Right
    global ele
    global yc
    global yt
    global az
    global xc
    global xt
    yseconds = (yt - ele) * (1 / yc)
    print ('target ') + str(yt) + (' degrees')
    print ('moving up for ') + str(yseconds) + (' seconds')
    
    xseconds = (xt - az) * (1 / xc)
    print ('target ') + str(xt) + (' degrees')
    print ('moving right for ') + str(xseconds) + (' Seconds')
    
    GPIO.output(17, True)
    GPIO.output(18, False)
    GPIO.output(22, True)
    GPIO.output(27, False)
    if xseconds > yseconds:
        time.sleep(yseconds)
        GPIO.output(18, True)
        time.sleep(xseconds - yseconds)
        GPIO.output(27, True)
    else:
        time.sleep(xseconds)
        GPIO.output(27, True)
        time.sleep(yseconds - xseconds)
        GPIO.output(18, True)
    
    ele = yt
    print ('elevation is ') + str(ele)
    
    az = xt
    print ('azimuth is ') + str(az)
    return()
def dl(): #     move down and/or left
    global ele
    global yc
    global yt
    global az
    global xc
    global xt
    yseconds = (ele - yt) * (1 / yc)
    print ('target ') + str(yt) + (' degrees')
    print ('moving Down for ') + str(yseconds) + (' seconds')
    
    xseconds = (az - xt) * (1 / xc)
    print ('target ') + str(xt) + (' degrees')
    print ('moving left for ') + str(xseconds) + (' Seconds')
    
    GPIO.output(18, True)
    GPIO.output(17, False)
    GPIO.output(27, True)
    GPIO.output(22, False)
    if xseconds > yseconds:
        time.sleep(yseconds)
        GPIO.output(17, True)
        time.sleep(xseconds - yseconds)
        GPIO.output(22, True)
    else:
        time.sleep(xseconds)
        GPIO.output(22, True)
        time.sleep(yseconds - xseconds)
        GPIO.output(17, True)
    
    ele = yt
    print ('elevation is ') + str(ele)
    
    az = xt
    print ('azimuth is ') + str(az)
    return()
def dr(): # move down and/or right
    global ele
    global yc
    global yt
    global az
    global xc
    global xt
    yseconds = (ele - yt) * (1 / yc)
    print ('target ') + str(yt) + (' degrees')
    print ('moving Down for ') + str(yseconds) + (' seconds')
    
    xseconds = (xt - az) * (1 / xc)
    print ('target ') + str(xt) + (' degrees')
    print ('moving Right for ') + str(xseconds) + (' Seconds')
    
    GPIO.output(18, True)
    GPIO.output(17, False)
    GPIO.output(22, True)
    GPIO.output(27, False)
    if xseconds > yseconds:
        time.sleep(yseconds)
        GPIO.output(17, True)
        time.sleep(xseconds - yseconds)
        GPIO.output(27, True)
    else:
        time.sleep(xseconds)
        GPIO.output(27, True)
        time.sleep(yseconds - xseconds)
        GPIO.output(17, True)
    
    ele = yt
    print ('elevation is ') + str(ele)
    
    az = xt
    print ('azimuth is ') + str(az)
    return()
def z(): #      Reset Rotator to ZERO end stop
    global az
    global ele
    print ('resetting zero')
    GPIO.output(18, True)
    GPIO.output(17, False)
    GPIO.output(27, True)
    GPIO.output(22, False)
    time.sleep(55)
    GPIO.output(17, True)
    GPIO.output(22, True)
    az = 0
    ele = 0
    print ('reset to zero')
    return()
def m(): #      Reset Rotator to MAXIMUM end stop
    global az
    global ele
    global xt
    global yt
    print ('resetting Max')
    GPIO.output(18, False)
    GPIO.output(17, True)
    GPIO.output(27, False)
    GPIO.output(22, True)
    time.sleep(55)
    GPIO.output(18, True)
    GPIO.output(27, True)
    yt = 90
    ele = 90
    xt = 360
    az = 360
    print ('reset to max')
    return()
def c(): #      Move rotator to centre position on both Axis
    global yt
    global xt
    yt = 45
    xt = 180
    dt()
    return()

    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #    Setup IO to Pi numbering
GPIO.setup(17, GPIO.OUT) #  Setup Relay pins as OUTPUTS
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

print ('resetting zero')
GPIO.output(18, True)
GPIO.output(17, False)
GPIO.output(27, True)
GPIO.output(22, False)
time.sleep(55)
GPIO.output(17, True)
GPIO.output(22, True)
az = 0
ele = 0
print ('reset to zero')




while 1: #      Routine to read keypress(es)

    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = 4500

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    s.listen(10)
    print 'Socket now listening'

    #Function for handling connections
    def clientthread(conn):
        #Sending message to connected client
        #conn.send('Welcome to the server. Receving Data...\n') #send only takes string

        #infinite loop so that function do not terminate and thread do not end.
        while True:

            #Receiving from client
            data = conn.recv(1024)
            #reply = 'Message Received at the server!\n'
            print data
            #if not data:
            #    break
            ret = ActionHandler().handle_message(*data.split())
            dt()
            conn.sendall(ret)

        conn.close()

    #now keep talking with the client
    while 1:
        #wait to accept a connection
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

        #start new thread
        start_new_thread(clientthread ,(conn,))

    s.close()

    inkey=getch()

    
    print ('key pressed was ') + str(inkey)
    if inkey=="u": #    go UP 1 degree
        yt = yt + 1
        if yt > 90: #   Upper limit of Y axis - loop to bottom of Y
            yt = yt - 90
        dt()
               
    elif inkey=="d": #  go DOWN 1 degree
        yt = yt - 1
        if yt < 0: #    Lower limit of Y axis - loot to top of Y
            yt = yt + 90
        dt()
       
    elif inkey=="r": #  go RIGHT 1 degree
        xt = xt + 1
        if xt > 360: #  Upper limit of X axis - loop to bottom 
            xt = xt - 360
        dt()
        
    elif inkey=="l": #  go LEFT 1 degree
        xt = xt - 1
        if xt < 0: #    Lower limit of X axis - loop to top
            xt =  xt + 360
        dt()

    elif inkey=="z": #  RESET to ZERO
        z()

    elif inkey=="m": #  RESET to MAXIMUM
        m()

    elif inkey=="M": #  MOVE to Maximum
        yt = 90
        xt = 360
        dt()

    elif inkey=="U": # MOVE up and right by 10 Degrees (for testing only)
        yt = yt + 10
        xt = xt + 10
        ur()

    elif inkey=="Z": #  MOVE to ZERO position
        yt = 0
        xt = 0
        dt()
        
    elif inkey=="c": #  MOVE to centre position
        c()
    elif inkey=="1": #  Memory 1
        xt = 90
        yt = 0
        dt()
    elif inkey=="2": #  Memory 2
        xt = 90
        yt = 84
        dt()
    elif inkey=="3": #  Memory 3
        xt = 90
        yt = 90
        dt()
    elif inkey=="4": #  Memory 4
        xt = 270
        yt = 89
        dt()
    elif inkey=="5": #  Memory 5
        xt = 270
        yt = 84
        dt()
    elif inkey=="6": #  Memory 6
        xt = 270
        yt = 0
        dt()
        
    elif inkey=="x": # eXit the programme
        quit()
    else:
        inkey = None # RESET inkey variable just incase.

