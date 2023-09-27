## வியாழன் 14.02.2023
## Agent வெகுமதியைப் பெறும்போது மட்டுமே பயிற்சி செய்யுங்கள்
## துறை இரண்டில் இருந்து தொடங்குகிறது
## நிலையான வேகத்தில் துரிதப்படுத்தப்பட்டது
## தலைகீழ் இல்லை
import sys, os
ren  = input("Should I render? [yes/no]: ")
if(ren == 'no'):os.environ["SDL_VIDEODRIVER"] = "dummy"
import GameEnv
import pygame
import numpy as np
from ddqn_keras import DDQNAgent
from collections import deque
import random, math
import tamil 
import keyboard 
import psutil
import tensorflow as tf
key = False

File_name = "Thavarugalil irundu katrukol"
# Restore

TOTAL_GAMETIME = 10000000 # Max game time for one episode
N_EPISODES = 50
REPLACE_TARGET = 10 

game = GameEnv.RacingEnv()
game.fps = 60

GameTime = 0 
GameHistory = []
renderFlag = False
batch = 32
mem_size = 1024
ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=3, epsilon=1.0, epsilon_end=0.1, epsilon_dec=0.99995, replace_target= REPLACE_TARGET,mem_size = mem_size, batch_size=batch, input_dims=360)

#os.environ["SDL_VIDEODRIVER"] = "dummy"
#ddqn_agent.model_file =  'model110.h5'
#ddqn_agent.load_model()

ddqn_scores = []
eps_history = []
action_map = {0: "L",1: "R",2: "S",3: "_",4:"_" }
os.system('cls')

def run():
    Save = False
    avg_score=0
    process = psutil.Process(pid=os.getpid())
    for e in range(N_EPISODES):
        #tf.keras.backend.get_session().close()
        tf.keras.backend.clear_session()
        game.reset() #reset env 

        done = False
        score = 0
        counter = 0
        cg_counter = 0
        observation_, reward, done = game.step(0)
        observation = np.array(observation_)

        gtime = 0 # set game time back to 0
        
        renderFlag = False# if you want to render every episode set to true

        if (e % 20 == 0 and e > 0) or (e<5): # render every 10 episodes
            renderFlag = True
        act =0
        premem = 0
        loccg = 0
        
        while not done:
            act+=1
            game.actvalue+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    return

            action = ddqn_agent.choose_action(observation)
            
            if (key):
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    y = event.name
        
                if y == 'up':action =0
                elif(y == 'down'):action =1
                elif (y == 'left'):action =2
                elif(y =='right'):action =3
                else:action = 4
            observation_, reward, done = game.step(action)
            observation_ = np.array(observation_)
            
            # This is a countdown if no reward is collected the car will be done within 100 ticks
            if reward == 0:
                counter += 1
                if counter > 1000:
                    done = False
            else:
                counter = 0

            score += reward

            
            if(reward !=0):
                ddqn_agent.remember(observation, action, reward, observation_, int(done))
                premem+=1
                ddqn_agent.learn()
            observation = observation_
            
            
            gtime += 1
            
            ddqn_agent.model_file = "model" + str(e) + ".h5"
            if(game.car.x <1000):sector = 1
            elif(game.car.x >1000 and game.car.x < 1600):sector = 2
            elif(game.car.x >1600):sector = 3
            
            st = "Attiyayam: {0} | Thoguthi: {1} | Seyal: {2} | Mathipen: {3} | Kadadha ilaku:{4} | epsilon: {5} | Seyal yen: {6} | ninaivu: {7}/{8} ".format(e,sector,act,score,game.cg,round(ddqn_agent.epsilon,4),action_map[action],ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size,ddqn_agent.memory.mem_size)
            print('\r',st,loccg,end = "")
            
            
            if (loccg == game.cg):cg_counter+=1
            if (cg_counter > 50):done = True
            loccg = game.cg
            
            if renderFlag:
              pass
            game.render(action,score,ddqn_agent.memory.mem_cntr)

        eps_history.append(ddqn_agent.epsilon)
        ddqn_scores.append(score)
        avg_score = np.mean(ddqn_scores[max(0, e-100):(e+1)])
        
        if e % REPLACE_TARGET == 0 and e > 25:
            ddqn_agent.update_network_parameters()
            
        if((ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)>batch):Save = True
        if e % 10 == 0 and Save:
            ddqn_agent.save_model()
            
        stat ='\n' + "Attiyayam: " +str(e)+"| seyal: "+str(act)+ " buffer size" + str(ddqn_agent.memory.mem_cntr)+ "/5120"+"| Mathipen: "+str(score)+"| Sarasari mathipen " +str(round(avg_score,2))+"| epsilon: "+str(round(ddqn_agent.epsilon,4))+str(' |')+"Kadandha ilaku ___"+str(game.cg)+"_____"+ File_name
        f.write(stat)
        memsta = "Memory usage: " +  str(round(process.memory_info().rss / (1024 * 1024),2))+"MB"
        sys.stdout.write('\033[2K\033[1G')
        print('Attiyayam: ', e,'score: %.2f' % score,
              'Average Score %.2f' % avg_score,
              'Epsilon: ', round(ddqn_agent.epsilon,4),
              'storage/action', premem ,'/',game.actvalue,
              'crossed Goals: ',game.cg,
              'File Name:',File_name, memsta)   
f = open("log.txt", "w")

       
run()        
f.close() 