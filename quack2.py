#!/usr/bin/env python2
#Python script for controling motors via motor controler controled by wii remote
# Author : Ethan Brierley

print("  ____            _             _   ____           _                          ____  _   ____       _           _           _        __        ___ _   ____                      _ ")
print(" / ___|___  _ __ | |_ _ __ ___ | | |  _ \ __ _ ___| |__   ___ _ __ _ __ _   _|  _ \(_) |  _ \ ___ | |__   ___ | |_  __   _(_) __ _  \ \      / (_|_) |  _ \ ___ _ __ ___   ___ | |_ ___ ")
print("| |   / _ \| '_ \| __| '__/ _ \| | | |_) / _` / __| '_ \ / _ \ '__| '__| | | | |_) | | | |_) / _ \| '_ \ / _ \| __| \ \ / / |/ _` |  \ \ /\ / /| | | | |_) / _ \ '_ ` _ \ / _ \| __/ _ \ ")
print("| |__| (_) | | | | |_| | | (_) | | |  _ < (_| \__ \ |_) |  __/ |  | |  | |_| |  __/| | |  _ < (_) | |_) | (_) | |_   \ V /| | (_| |   \ V  V / | | | |  _ <  __/ | | | | | (_) | ||  __/")
print(" \____\___/|_| |_|\__|_|  \___/|_| |_| \_\__,_|___/_.__/ \___|_|  |_|   \__, |_|   |_| |_| \_\___/|_.__/ \___/ \__|   \_/ |_|\__,_|    \_/\_/  |_|_| |_| \_\___|_| |_| |_|\___/ \__\___(_)")
print("                                                                        |___/")

print ("Importing.")

import wiringpi #For PWM
import time #For Sleep.
import cwiid #For wiimote
import sys #For Powering off
import pygame #For the playing of mp3 files
import subprocess
#import sys, os
import sys

#Setting up veriables for pins
print ("Setting Pins.")

pinLeft = 4 #Wiringpi pin number for connection from pi to motor controler that controls left wheel going forward.
pinRight = 3 #Wiringpi pin number for connection from pi to motor controler that controls Right wheel going forward.
pinBackwardsLeft = 2 #Wiringpi pin number for connection from pi to motor controler that controls left wheel going backwards.
pinBackwardsRight = 0 #Wiringpi pin number for connection from pi to motor controler that controls right wheel going backwards.
pinError = 7
pinOn = 5
sonicTriger = 21
frontSonicInput = 23
backSonicInput = 25
leftSonicInput = 27
rightSonicInput = 26
moveLeft = 0
moveRight = 0
moveBackByRight = 0
moveBackByLeft = 0
breakLoop = 0
timeFront = 0
timeBack = 0
timeLeft = 0
timeRight = 0
speed = 1
ai = 1
temperature = 20
speedSound = 33100 + (0.6*temperature)
retrySend = 1
testTime = 0.005
sensitivity = 5
tempConnected = False

#Setting up pin modes

wiringpi.wiringPiSetup()
wiringpi.pinMode(pinLeft,1)
wiringpi.pinMode(pinRight,1)
wiringpi.pinMode(pinBackwardsLeft,1)
wiringpi.pinMode(pinBackwardsRight,1)
wiringpi.pinMode(pinOn,1)
wiringpi.pinMode(sonicTriger,1)
wiringpi.pinMode(frontSonicInput,0)
wiringpi.pinMode(backSonicInput,0)
wiringpi.pinMode(leftSonicInput,0)
wiringpi.pinMode(rightSonicInput,0)
# Seting up PWM using Pin, Initial Value and Range parameters

wiringpi.softPwmCreate(pinLeft,0,100)
wiringpi.softPwmCreate(pinRight,0,100)
wiringpi.softPwmCreate(pinBackwardsLeft,0,100)
wiringpi.softPwmCreate(pinBackwardsRight,0,100)
wiringpi.softPwmCreate(pinError,0,100)
wiringpi.softPwmCreate(pinOn,0,100)

#Setting up functions that control movement

def Forward ():
    wiringpi.softPwmWrite(pinLeft,int(100*speed))
    wiringpi.softPwmWrite(pinRight,int(100*speed))
def Left ():
    wiringpi.softPwmWrite(pinRight,0)
    wiringpi.softPwmWrite(pinLeft,int(100*speed))
def Right ():
    wiringpi.softPwmWrite(pinLeft,0)
    wiringpi.softPwmWrite(pinRight,int(100*speed))
def LessRight ():
    wiringpi.softPwmWrite(pinLeft,int(50*speed))
    wiringpi.softPwmWrite(pinRight,int(100*speed))
def LessLeft ():
    wiringpi.softPwmWrite(pinLeft,int(100*speed))
    wiringpi.softPwmWrite(pinRight,int(50*speed))
def MoreLeft ():
    wiringpi.softPwmWrite(pinLeft,int(100*speed))
    wiringpi.softPwmWrite(pinBackwardsRight,int(100*speed))
def MoreRight ():
    wiringpi.softPwmWrite(pinBackwardsLeft,int(100*speed))
    wiringpi.softPwmWrite(pinRight,int(100*speed))
def Backwards ():
    wiringpi.softPwmWrite(pinBackwardsLeft,int(100*speed))
    wiringpi.softPwmWrite(pinBackwardsRight,int(100*speed))
def PWMMove():
    wiringpi.softPwmWrite(pinBackwardsLeft,int(moveLeft*speed))
    wiringpi.softPwmWrite(pinBackwardsRight,int(moveRight*speed))
    wiringpi.softPwmWrite(pinLeft,int(moveBackByLeft*speed))
    wiringpi.softPwmWrite(pinRight,int(moveBackByRight*speed))
def Clean ():
    wiringpi.softPwmWrite(pinLeft,0)
    wiringpi.softPwmWrite(pinRight,0)
    wiringpi.softPwmWrite(pinBackwardsLeft,0)
    wiringpi.softPwmWrite(pinBackwardsRight,0)
    wiringpi.softPwmWrite(pinError,0)
    wiringpi.digitalWrite(sonicTriger,0)
    print ("Cleaning")

#Setting up functions that play sounds

def Startingup():
    print ("Playing winxp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("winxp.mp3")
    pygame.mixer.music.play()
def LogOff():
    print ("Playing logoff.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("logoff.mp3")
    pygame.mixer.music.play()
def ErrorSound():
    print ("Playing errorsound.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("errorsound.mp3")
    pygame.mixer.music.play()
def Horn():
    print ("Playing horn.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("horn.mp3")
    pygame.mixer.music.play()
def Door():
    print ("Playing door.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("door.mp3")
    pygame.mixer.music.play()



def Poweroff():
    wiringpi.softPwmWrite(pinOn,0)
    Clean()
    os.system('sh autolaunchlog.sh')
    LogOff()
    time.sleep(10)
    command = "/usr/bin/sudo /sbin/shutdown now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #os.system('sh autolaunchlog.sh')
    output = process.communicate()[0]
    print (str(output))
    print ("end")
    #os.system('sh autolaunchlog.sh')

def checkSpeedChange():
    global speed
    if (wm.state['buttons'] & cwiid.BTN_PLUS):
        if speed < 1:
            speed = speed + 0.2
            print ("Because button plus was pressed there has been a 20% incress in speed. The new speed is "+str(speed*100)+"% times the set speeds")
            while (wm.state['buttons'] & cwiid.BTN_PLUS):
                pass
        else:
            print ("Speed is already at its highest")
            while (wm.state['buttons'] & cwiid.BTN_PLUS):
                pass
    elif (wm.state['buttons'] & cwiid.BTN_MINUS):
        if speed > 0.3:
            speed = speed - 0.2
            print ("Because button minus was pressed there has been a 20% decress in speed. The new speed is "+str(speed*100)+"% times the set speeds")
            while (wm.state['buttons'] & cwiid.BTN_MINUS):
                pass
        else:
            print ("Speed is already at its lowest")
            while (wm.state['buttons'] & cwiid.BTN_MINUS):
                pass
    else:
        pass

def checkHornPress():
    if (wm.state['buttons'] & cwiid.BTN_2):
        print ("Due to the button 2 being pressed.")
        Horn()
        while (wm.state['buttons'] & cwiid.BTN_2):
            pass
    else:
        pass

def checkTemp():
    if tempConnected:
        tfile = open("/sys/bus/w1/devices/10-000802824e58/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature
    else:
        pass

def sendSonicSig():
    wiringpi.digitalWrite(sonicTriger,1)
    time.sleep(0.00001)
    wiringpi.digitalWrite(sonicTriger,0)

def waitForResponceFront():
    global startingTime
    global retrySend
    responce = wiringpi.digitalRead(frontSonicInput)
    while responce == False:
        responce = wiringpi.digitalRead(frontSonicInput)
        if (time.time()-startingTime) > 1:
            print ("This is taking too long retrying.")
            retrySend = 1
            responce = True
        else:
            retrySend = 0

def waitForResponceAll():
    global startingTime
    global retrySend
    global timeFront
    global timeBack
    global timeLeft
    global timeRight
    responcefront = wiringpi.digitalRead(frontSonicInput)
    responceBack = wiringpi.digitalRead(backSonicInput)
    responceLeft = wiringpi.digitalRead(leftSonicInput)
    responceRight = wiringpi.digitalRead(rightSonicInput)
    while responcefront == False or responceBack == False or responceRight == False or responceLeft == False:
        responcefront = wiringpi.digitalRead(frontSonicInput)
        responceBack = wiringpi.digitalRead(backSonicInput)
        responceLeft = wiringpi.digitalRead(leftSonicInput)
        responceRight = wiringpi.digitalRead(rightSonicInput)
        if (time.time()-startingTime) > 1:
            print ("This is taking too long retrying.")
            retrySend = 1
            responcefront = True
            responceBack = True
            responceLeft = True
            responceRight = True
        elif responcefront:
            timeFront = time.time() - startingTime
        elif responceBack:
            timeBack = time.time() - startingTime
        elif responcefront:
            timeLeft = time.time() - startingTime
        elif responcefront:
            timeRight = time.time() - startingTime
        else:
            retrySend = 0

def ai1MovementCalc():
    global moveLeft
    global moveRight
    global moveBackByLeft
    global moveBackByRight
    moveBackByRight = 0
    if distanceNearFront < sensitivity:
        print ("Because the distance to the closest object is less than "+str(sensitivity)+"cm the robot will turn sharply to the right without moving forward.")
        moveRight = 100
        moveLeft = 0
        moveBackByLeft = 100
    else:
        print ("Because the distance to the closest object is more than "+str(sensitivity)+"cm the robot will move forward.")
        moveBackByLeft = 0
        moveLeft = 100
        moveRight = 100
    PWMMove()

def ai1MovementCalc2():
    
    pass

def checkSensitivityChange():
    global sensitivity
    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        if sensitivity<0.1:
            print("Already sensitivity is at its lowest")
        else:
            sensitivity = sensitivity-0.1
            print ("button 'up' was pressed. The robot will become less sensitive to near objects. The new sensitivity is "+str(sensitivity))
        while (wm.state['buttons'] & cwiid.BTN_DOWN):
            pass
    elif (wm.state['buttons'] & cwiid.BTN_UP):
        sensitivity=sensitivity+0.1
        print ("button 'up' was pressed. The robot will become more sensitive to near objects. The new sensitivity is "+str(sensitivity))
        while (wm.state['buttons'] & cwiid.BTN_UP):
            pass
    else:
        pass

def checkMovementPress():
    if (wm.state['buttons'] & cwiid.BTN_DOWN):
        print ("Due to the button 'down' being pressed the robot will move backwards while the button is held")
        while (wm.state['buttons'] & cwiid.BTN_DOWN):
            Backwards()
        Clean()
    elif (wm.state['buttons'] & cwiid.BTN_UP):
        print ("button 'up' pressed")
        while (wm.state['buttons'] & cwiid.BTN_UP):
            Forward()
        Clean()
    elif (wm.state['buttons'] & cwiid.BTN_LEFT):
        if (wm.state['buttons'] & cwiid.BTN_A):
            print ("button 'left' and 'A' pressed")
            while wm.state['buttons'] == 264:
                Left()
            Clean()
        elif (wm.state['buttons'] & cwiid.BTN_B):
            print ("button 'left' and 'B' pressed")
            while wm.state['buttons'] == 260:
                MoreLeft()
            Clean()
        else:
            print ("button 'left' pressed")
            while wm.state['buttons'] == 256:
                LessLeft()
            Clean()
    elif (wm.state['buttons'] & cwiid.BTN_RIGHT):
        if (wm.state['buttons'] & cwiid.BTN_A):
            print ("button 'right' and 'A' pressed")
            while wm.state['buttons'] == 520:
                Right()
            Clean()
        elif (wm.state['buttons'] & cwiid.BTN_B):
            print ("button 'right' and 'B' pressed")
            while wm.state['buttons'] == 516:
                MoreRight()
            Clean()
        else:
            print ("button 'right' pressed")
            while wm.state['buttons'] == 512:
                LessRight()
            Clean()
    else:
        pass

def checkShutdownPress():
    if (wm.state['buttons'] & cwiid.BTN_1):
        print ("Exiting")
        breakLoop = 1
        return breakLoop
    else:
        pass
Startingup()
wiringpi.softPwmWrite(pinOn,100)
wiringpi.softPwmWrite(pinError,100)
time.sleep(5) 
while breakLoop == 0:
    try:
        print ("Connecting")
        wm = cwiid.Wiimote()
        wm.rpt_mode = cwiid.RPT_BTN
        wiringpi.softPwmWrite(pinError,0)
        print ("Connected")
        Door()
        while breakLoop == 0:
            wm.state
            if ai == 1:
                if (wm.state['buttons'] & cwiid.BTN_HOME):
                    ai = 2
                    Clean()
                    print ("Wellcome to control mode 2 the control mode where the robot is controled only by the front ultrasonic sensor.")
                    while (wm.state['buttons'] & cwiid.BTN_HOME):
                        pass
                else:
                    pass
                checkShutdownPress()
                checkSpeedChange()
                checkHornPress()
                checkMovementPress()
            elif ai == 2:
                checkShutdownPress()
                checkSpeedChange()
                checkHornPress()
                checkSensitivityChange()
                if (wm.state['buttons'] & cwiid.BTN_HOME):
                    ai = 3
                    Clean()
                    print ("Wellcome to control mode 3 where all sensors are used!")
                    while (wm.state['buttons'] & cwiid.BTN_HOME):
                        pass
                else:
                    if retrySend == 1:
                        checkTemp()
                        speedSound = 33100 + (0.6*temperature)
                        sendSonicSig()
                        startingTime = time.time()
                        test = True
                        if test:
                            time.sleep(testTime)
                            testTime = testTime - 0.000001
                            retrySend = 0
                        else:
                            waitForResponceFront()
                    else:
                        endingTime = time.time()
                        print("Speed of sound is "+str(speedSound/100)+"m/s at "+str(temperature)+"deg and the time it has taken for the sound signal to travel to the nearest object and back was "+str(endingTime-startingTime)+" seconds. this means that the distance to the nearest object is "+str(((endingTime-startingTime)*speedSound)/2)+"cm away")
                        distanceNearFront = ((endingTime-startingTime)*speedSound)/2
                        ai1MovementCalc()
                        retrySend = 1
            elif ai == 3:
                checkShutdownPress()
                checkSpeedChange()
                checkHornPress()
                checkSensitivityChange()
                if (wm.state['buttons'] & cwiid.BTN_HOME):
                    ai = 1
                    Clean()
                    print ("Wellcome back to control mode 1. In this mode movement is controled by the wiimote.")
                    while (wm.state['buttons'] & cwiid.BTN_HOME):
                        pass
                else:
                    if retrySend == 1:
                        checkTemp()
                        speedSound = 33100 + (0.6*temperature)
                        sendSonicSig()
                        startingTime = time.time()
                        test = False
                        if test:
                            time.sleep(testTime)
                            testTime = testTime - 0.000001
                            retrySend = 0
                        else:
                            waitForResponceAll()
                    else:
                        endingTime = time.time()
                        print("Speed of sound is "+str(speedSound/100)+"m/s at "+str(temperature)+"deg and the time it has taken for the sound signal to travel to the nearest object and back was "+str(endingTime-startingTime)+" seconds. this means that the distance to the nearest object is "+str(((endingTime-startingTime)*speedSound)/2)+"cm away")
                        distanceNearFront = ((endingTime-startingTime)*speedSound)/2
                        ai1MovementCalc()
                        retrySend = 1
    except RuntimeError as e:
        print('Error')
        print(str(e))
        wiringpi.softPwmWrite(pinError,100)
        ErrorSound()
Clean()
wiringpi.softPwmWrite(pinError,100)
Poweroff()