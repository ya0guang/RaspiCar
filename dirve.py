import RPi.GPIO as GPIO

def initializeDrive(deb):
    global debug
    debug = deb

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
