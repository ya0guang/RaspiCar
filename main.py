import RPi.GPIO as GPIO
import sys
import select
import termios
import tty
from drive import *

def execute(servo1, servo2, engine1, engine2):
    # output duty cycle
    # if debug:
    #     print("======ServoL=======")
    servo1.update()
    # if debug:
    #     print("======ServoR=======")
    servo2.update()
    if debug:
        print("======engineL=======")
    engine1.update()
    if debug:
        print("======engineR=======")
    engine2.update()

def cycle(controlSignal, servoMain, servoSub, engineMain, engineSub):
    # servo control part
    # ">" for decreasing angle
    if controlSignal == "<":
        servoMain.dcincrease(0.2)
    # "<" for decreasing angle
    if controlSignal == ">":
        servoMain.dcdecrease(0.2)
    servoSub.dutyCycle = 14.35 - servoMain.dutyCycle

    # engine control part
    # "+" for accelerating, "r" for change direction
    # main engine mannual control
    if controlSignal == "+" :
        engineMain.speedInc()
        engineSub.speedInc()
    if controlSignal == "_":
        engineMain.speedDec()
    if controlSignal == "R":
        engineMain.reverse()

    # sub engine mannual control
    if controlSignal == "=" :
        engineSub.speedInc()
    if controlSignal == "-":
        engineSub.speedDec()
    if controlSignal == "r":
        engineSub.reverse()

def getchar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
    return sys.stdin.read(1)

def main():
    global debug
    debug = 1

    initializeDrive(debug)
    #initialize
    global servoL, servoR, engineL, engineR
    servoL = Servo(22)
    servoR = Servo(24)
    engineL = Engine(11, 8, 27)
    engineR = Engine(10, 9, 23)

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        while 1:
            tty.setcbreak(sys.stdin.fileno())
            control = getchar(False)
            cycle(control, servoL, servoR, engineL, engineR)
            execute(servoL, servoR, engineL, engineR)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == '__main__':
    main()
