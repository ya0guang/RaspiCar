import time

class PIDController():
	
    def __init__(self, P=0.0, I=0.0, D=0.0, sample=1.0):

        # set PID parameters
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sampleTime = sample

        # initialize time
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.clear()
		
    def clear(self):
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.lastError = 0.0
        self.output = 0.0
        self.lastoutput = 0.0

    def update(self, setpoint, feedback):
        error = setpoint - feedback
		
        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError
		# Calculate PID terms
        if (delta_Time >= self.sampleTime):#how to get delta_time?????
            self.PTerm = error
            self.ITerm += error * deltaTime
            self.DTerm = deltaError

            # Remember last time and last error for next calculation
            self.lastTime = self.currentTime
            self.lastError = error

            self.output = (self.Kp * self.PTerm) + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)+self.lastoutput
            self.lastoutput=self.output

class EngineController():
    # Feedback impluses received per sample period
    #speed = (1350/4, 1350/3, 1350/2, 1350)
	
    def __init__(self, level):
        self.controllerMain = PIDController()
        #self.controllerSub = PIDController()
        # Speed level
        self.speed = 0
        #self.speedR=0
		
    # def configure(self, num, P=0.0, I=0.0, D=0.0, sample=1.0):
    #     # Main controller
    #     self.controllerMain = PIDController(P=0.0, I=0.0, D=0.0, sample=1.0)
    #     # if num == 1:
    #         # self.controllerMain = PIDController(P=0.0, I=0.0, D=0.0, sample=1.0)
    #     # Sub controller
    #     # if num == 2:
    #         # self.controllerSub = PIDController(P=0.0, I=0.0, D=0.0, sample=1.0)
	
    def update(self, speed, sepdet):
        self.controllerMain.update(speed, sepdet)
         # Take the left engine as main engine
        # self.controllerSub.update(speedR, sepdetR)
		
    def setSpeed(self, level):
         self.level = level
