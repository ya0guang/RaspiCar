import RPi.GPIO as GPIO
import sys
import select
import termios
import tty

class Motor:
    dutyCycle = 20
    maxdc = 100
    mindc = 0
    pin = 20

    def __init__(self, pin, maxdc = 10, mindc = 5, initdc = 7.5):
        # motor init
        # duty cycle of motor: 0<x<100
        self.dutyCycle = initdc
        self.maxdc = maxdc
        self.mindc = mindc
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.motor = GPIO.PWM(self.pin, 50)
        self.motor.start(self.dutyCycle)

    def __str__(self):
        return [k for k,v in globals().items() if v is self]

    def dcincrease(self, rate = 0.2):
        self.dutyCycle += rate

    def dcdecrease(self, rate = 0.2):
        self.dutyCycle -= rate

    def update(self):
        # only fresh PWM output
        if self.dutyCycle > self.maxdc:
            self.dutyCycle = self.maxdc
        if self.dutyCycle < self.mindc:
            self.dutyCycle = self.mindc
        self.motor.ChangeDutyCycle(self.dutyCycle)
        if debug:
            print(self.__str__(), " ---- dutyCycle ---- ", self.dutyCycle)

class Servo(Motor):
    def __init__(self, pin = 20, maxdc = 10, mindc = 5, initdc = 7.3):
        # servo init: GPIO20 output
        # duty cycle of servo: 5<x<10
        Motor.__init__(self, pin, maxdc, mindc, initdc)

class Engine(Motor):
    position = 0

    def __init__(self, pinPWM, pinBackPWM, pinSensor, maxdc = 100, mindc = 0, initdc = 0):
        Motor.__init__(self, pinPWM, maxdc, mindc, initdc)
        self.pinBack = pinBackPWM
        self.pinFeedback = pinSensor
        self.direction = True
        # set up pins
        GPIO.setup(self.pinBack, GPIO.OUT)
        GPIO.setup(self.pinFeedback, GPIO.IN)
        GPIO.setup(self.pinFeedback, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # set up reverse pin with 0 duty cycle
        self.motorBack = GPIO.PWM(self.pinBack, 50)
        self.motorBack.start(0)
        # set up feedback event
        GPIO.add_event_detect(self.pinFeedback, GPIO.RISING, callback=self.feedback)
        self.update()

    def reverse(self):
        self.direction = not self.direction
        self.update()

    def update(self):
        # fresh PWM output
        if self.dutyCycle > self.maxdc:
            self.dutyCycle = self.maxdc
        if self.dutyCycle < self.mindc:
            self.dutyCycle = self.mindc

        if self.direction:
            self.motor.ChangeDutyCycle(self.dutyCycle)
            self.motorBack.ChangeDutyCycle(0)
        if not self.direction:
            self.motor.ChangeDutyCycle(0)
            self.motorBack.ChangeDutyCycle(self.dutyCycle)
        if debug:
            print(self.__str__(), " ---- Position of ---- ",  self.position)
            print(self.__str__(), " ---- dutyCycle ---- ", self.dutyCycle)
            print(self.__str__(), " ---- direction ---- ", self.direction)

    def feedback(self, channel):
        self.position += 1

def execute(servo1, servo2, engine1, engine2):
    # output duty cycle
    servo1.update()
    servo2.update()
    engine1.update()
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
        engineMain.dcincrease(1)
    if controlSignal == "_":
        engineMain.dcdecrease(1)
    if controlSignal == "R":
        engineMain.reverse()

    # sub engine mannual control
    if controlSignal == "=" :
        engineSub.dcincrease(1)
    if controlSignal == "-":
        engineSub.dcdecrease(1)
    if controlSignal == "r":
        engineSub.reverse()

def getchar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
    return sys.stdin.read(1)

def main():
    global debug
    debug = 1

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