#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import time
from datetime import datetime
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
import numpy as np
from jetracer.nvidia_racecar import NvidiaRacecar
import signal 

#hyper parameters
max_power = 0.19
stay = 0
#left = stay- 0.35 #-0.338
#right = stay + 0.35 #0.142
steer = 0.20# * car.steering
left = -0.4
right = 0.4
sensor_range = 22.
printflag = True
plot = 0


class Rosbot():
	# 0: front, 90: left, 180: behind, 270:right
	def __init__(self, start_angle, end_angle, angle_increment): # end_angle is exclusive
		rospy.init_node("rosbot_test", anonymous = True)
		self.rosbot_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
		self.t = 0.0
		self.ctrl_c = False
		self.len = 1947
		self.idx = [int((i*angle_increment) / (360.0/self.len)) for i in range(int((end_angle - start_angle) / angle_increment))]
		self.res = []
		#self.rate = rospy.Rate (10) # 10hz
		rospy.on_shutdown(self.shutdownhook)

	def scan_callback(self, msg): 
		#self.len = len(msg.ranges)
		if not self.ctrl_c:
			self.res = [msg.ranges[i] if msg.ranges[i] < 25 else 0 for i in self.idx ]
		#print(self.idx)
		#print(time()-self.t)		
		#self.t = time()

	def read_laser(self):
		#while not self.ctrl_c:
			#print(self.res)
		return self.res

	def shutdownhook(self):

		self.ctrl_c = True




#######################################################################
#intialize car and sensors
rosbot_object = Rosbot(start_angle=0, end_angle=360, angle_increment=1)
car = NvidiaRacecar()
def handler(signum, frame):
    car.throttle = 0.0
    print("\nRecord LIDAR data. Press 1 to record, 0 to exit")
    data = []
    np.save("statespace", np.array(samples))
    np.save("actionspace", np.array(actions_sample))
    exit(1)
signal.signal(signal.SIGINT, handler)


action_map = {0: "Left", 1: "Right", 2: "Stay", 3: "xRight", 4: "Stay"}


#########################################Normalize_state#################################################
def normalize_state1(st):
    st/=sensor_range
    return st.reshape(1,360)
    
    
    

########################################Load Model##################################################
model_name = "model_nervazhi.h5"
model = load_model(model_name, compile = False)
print("Model",model_name, "loaded")


###################################################################################################
counter = 0  
samples = []
actions_sample = []
car.steering_offset=0.035
while True:
    state_ = rosbot_object.read_laser() 
    state = normalize_state1(np.array(state_))
    actions = model.predict(state)
    action = np.argmax(actions)
    
    samples.append(state)
    actions_sample.append(action)
    
    car.throttle=max_power
    
    
########################################Action execution################################################    
    '''
    if (action == 0):
        car.steering = left
    elif (action == 1):
        car.steering = right
    elif (action == 2):
        car.steering_offset=0
        car.steering = stay
    '''
    
    
    if (action == 0):
        if car.steering >0 : car.steering = 0
        else: 
            if  car.steering > left:
                 car.steering -= steer
            else: 
                car.steering = left   
    elif (action == 1):
        if car.steering <0 : car.steering = 0
        else:    
            if  car.steering < right:
                 car.steering += steer
            else: 
                car.steering = right        
    elif (action == 2):
        #if car.steering >stay:car.steering-=steer
        #if car.steering <stay:car.steering+=steer
        car.steering = stay
############################################################################################
    
    np.save("X", samples)
    np.save("Y", action_sample)
    if printflag:print(f"Counter: {counter} {action}, action: {action_map[action]}", "Throttle=", car.throttle, "Steering=", car.steering, "time =", datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    counter +=1 

car.throttle=0.0