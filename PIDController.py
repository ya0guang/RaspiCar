import time

class PIDController:
    def __init__(self, P=0.0, I=0.0, D=0.0, sample=0.0):
        self.last_error = 0
        # set PID parameters
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = sample
        # initialize time
        self.current_time = time.time()
        self.last_time = self.current_time
        self.clear()
		
    def clear(self):
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.output = 0.0

    def update(self, positionL, positionR):
        error = positionL - positionR
		
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
		# Calculate PID terms
        if (delta_time >= self.sample_time):
            self.PTerm = error
			self.ITerm += error * delta_time
            self.DTerm = delta_error

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = (self.Kp * self.PTerm) + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time
