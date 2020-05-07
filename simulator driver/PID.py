import numpy as np 

class PID_Controller:
    def __init__(self, gp, gi, gd, time_steps=10):
        self.GP = gp
        self.GI = gi
        self.GD = gd
        self.Measurements = [(0 , 0)] * time_steps
        self.Time_Steps = time_steps
        
    def update_sequence(self, desired_speed, current_speed):
        self.Measurements = self.Measurements[1:]
        # update the measurements 
        self.Measurements.append((desired_speed, current_speed))
        return 
        
    def integrate_error(self):
        IE = 0
        for desired , measured  in self.Measurements:
            IE += (desired - measured)
        return IE
        
    def derivative_error(self):
        # this is hapda 
        # derivative over 10 time steps 
        speed_at_time_step10 = self.Measurements[9][0]  # desired 
        speed_at_time_step1 = self.Measurements[4][1]   # current back then 
        return speed_at_time_step10 - speed_at_time_step1
        
    def update_speed(self , desired_speed, current_speed):
        """
            desired speed is the speed comming from my DeepLeaning model 
            current_speed is the speed measured by the sensors from the simulator 
            current speed always comes form the simulator 
        """
        
        self.update_sequence(desired_speed, current_speed)
        
        # proportional error 
        error = desired_speed  - current_speed
        Proportional_error = self.GP * error
        
        # integral error 
        Integreal_error = self.GI * self.integrate_error()
        
        # Derivative Error 
        Derivative_error = self.GD * self.derivative_error()
         
        print("errors ", Proportional_error, Integreal_error, Derivative_error)
        
        throttle = Proportional_error + Integreal_error + Derivative_error
        
        return throttle
