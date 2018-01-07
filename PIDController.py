import time

class PIDController:

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

    def update(self, setpoint, feedback):
        error = setpoint - feedback

        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError
		# Calculate PID terms
        self.PTerm = error
        self.ITerm += error * self.sampleTime
        self.DTerm = deltaError

        # Remember last time and last error for next calculation
        self.lastTime = self.currentTime
        self.lastError = error

        self.output = (self.Kp * self.PTerm) + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
