import numpy as np
from ddqn_keras import DDQNAgent
from collections import deque
import random, math
import keyboard 
import matplotlib.pyplot as plt
#Set true to control by keys
key = False
import sys,os
import psutil

TOTAL_GAMETIME = 10000
N_EPISODES = 10000
REPLACE_TARGET = 10#Swap Weights after "REPLACE_TARGET" Episodes


GameTime = 0 
GameHistory = []
renderFlag = True
plot = False
#Initializing Agent
ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=3, epsilon=0.002, epsilon_end=0.01, epsilon_dec=0.999, replace_target= REPLACE_TARGET, batch_size=64, input_dims=360,fname='ddqn_model.h5')
os.system('cls')
ren  = input("Should I render? [yes/no]: ")
if(ren == 'no'):os.environ["SDL_VIDEODRIVER"] = "dummy"
k  = input("Do you want to control with keyboard? [yes/no]: ")
if(k == 'yes'):key = True
mn = input("Enter model or episode number: ")
ddqn_agent.model_file = "model"+str(mn)+".h5"
# Load Trained Model
ddqn_agent.load_model()

ddqn_scores = []
eps_history = []
import GameEnv
# Initiate Environment
game = GameEnv.RacingEnv()
game.fps = 60

import pygame
action_map = {0: "F",1: "B",2: "L",3: "R",4:"S" }
os.system('cls')
def run():
    
    process = psutil.Process(pid=os.getpid())
    if plot:fig, ax = plt.subplots()
    for e in range(N_EPISODES):
        #reset env 
        game.reset()

        done = False
        score = 0
        counter = 0

        gtime = 0

        #first step
        observation_, reward, done = game.step(0)
        observation = np.array(observation_)
        act = 0
        loccg = 0
        cg_counter = 0
        while not done:
            
            act+=1
            game.actvalue+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
                    return

            #Choosing action
            
            action = ddqn_agent.choose_action(observation)
            if (key):
                y = 'enter'
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    y = event.name
        
                if y == 'up':action =2
                elif(y == 'down'):action =2
                elif (y == 'left'):action =0
                elif(y =='right'):action =1
                else:action = 4
                
            #Perform Single step calculation
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)
           
            #print(reward)
            
            if reward == 0:
                counter += 1
                if counter > 100:
                    done = False
            else:
                counter = 0

            score += reward

            observation = observation_

            gtime += 1
            if plot:
                ax.clear()
                ax.set_ylim(0,1)
                ax.set_xlim(0,360)
                
                ax.plot(observation)
                
                ax.set_title(f"Action: {act}")
                
                plt.pause(0.1)
            
            if (loccg == game.cg):cg_counter+=1
            if (loccg != game.cg):cg_counter = 0
            if (cg_counter > 500):done = True
            loccg = game.cg
            if renderFlag:
                game.render(action,score,act,ep = e)
            if(game.car.x <1000):sector = 1
            elif(game.car.x >1000 and game.car.x < 1600):sector = 2
            elif(game.car.x >1600):sector = 3
            memsta = "Memory usage: " +  str(round(process.memory_info().rss / (1024 * 1024),2))+"MB"
            print("\r","முயற்சி : {0} | பிரிவு: {8} | செயல்களின் எண்:{1} | மதிப்பெண்: {2} | இலக்குகளைத் தாண்டியது:{3} | epsilon: {4} | எடுக்கப்பட்ட  நடவடிக்கை : {5} |நினைவக அளவு: {6}/{7}_ ".format(e,act,score,game.cg,round(ddqn_agent.epsilon,4),action_map[action],ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size,ddqn_agent.memory.mem_size,sector),memsta,end = "")
                


print("Running using model ",str(mn) , "....Good luck!!!!")
run()
        
