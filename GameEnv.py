import pygame
import math
import numpy as np
from Walls import Wall
from Walls import getWalls
from Goals import Goal
from Goals import getGoals
import os, sys
import matplotlib.pyplot as plt
#os.environ["SDL_VIDEODRIVER"] = "dummy"

one_cm = 0.1732 #pix_to_cm_scale
# Initial Position
begin_x = 1450
begin_y = 165
angle_ss = 90

#Noise
mean_center = 0
sensor_uncertain = 1 #cm of uncertainity
loc_unc = 0 #cm of location uncertainity 
ang_unc = 0 #angle uncertainity in degrees
sensor_range = 2000# 22.5 m range 
dangerlimit = 100 #60 cm safelimit
nmp = 7 #no of missing points
gap = 10
cmp = 5 
noise_points = 4
limter = 0.5

#Reward
GOALREWARD = 10
LIFE_REWARD = 0
SAFEZONE_REWARD = 1
encourage_reward = 0

#Penalty
PENALTY = -10
GOALPENALTY = 0
ZONEPENALTY = -1
discourge_reward = 0

ang_unc = math.radians(ang_unc)
ellai = 0

##################################################################################    
def distance(pt1, pt2):
    return(((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)**0.5)

def rotate(origin,point,angle):
    qx = origin.x + math.cos(angle) * (point.x - origin.x) - math.sin(angle) * (point.y - origin.y)
    qy = origin.y + math.sin(angle) * (point.x - origin.x) + math.cos(angle) * (point.y - origin.y)
    q = myPoint(qx, qy)
    return q

def rotateRect(pt1, pt2, pt3, pt4, angle):

    pt_center = myPoint((pt1.x + pt3.x)/2, (pt1.y + pt3.y)/2)

    pt1 = rotate(pt_center,pt1,angle)
    pt2 = rotate(pt_center,pt2,angle)
    pt3 = rotate(pt_center,pt3,angle)
    pt4 = rotate(pt_center,pt4,angle)

    return pt1, pt2, pt3, pt4
class myPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class myLine:
    def __init__(self, pt1, pt2):
        self.pt1 = myPoint(pt1.x, pt1.y)
        self.pt2 = myPoint(pt2.x, pt2.y)

class Ray:
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle

    def cast(self, wall):
        x1 = wall.x1 
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        vec = rotate(myPoint(0,0), myPoint(0,-2482), self.angle)
        
        x3 = self.x
        y3 = self.y
        x4 = self.x + vec.x
        y4 = self.y + vec.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            
        if(den == 0):
            den = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = myPoint(math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1)))
                return(pt)

 
####################################################################################

class Car:
    def __init__(self, x, y):
        self.pt = myPoint(x, y)
        self.x = x 
        self.y = y 
        self.width = 3#int(15*one_cm) #agalam
        self.height = 5#int(30*one_cm) #neelam 

        self.points = 0

        self.original_image = pygame.image.load("car1.png").convert()
        self.image = self.original_image  # This will reference the rotated image.
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect().move(self.x, self.y)

        self.angle = math.radians(angle_ss)
        self.soll_angle = self.angle

        self.dvel = 2 #acc
        self.vel = -5
        self.velX = 0
        self.velY = 0
        self.maxvel = 15#athiga batcha visai

        
        self.soll_angle = self.angle

        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
        self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

        self.distances = []
    

    def action(self, choice):
    
        if choice == 0:
            
            self.turn(-1)#Left turn
        elif choice == 1:
            
            self.turn(1)#Right Turn
        elif choice == 2:
            # Straight
            pass
        
        '''if choice == 0:
            self.accelerate(-self.dvel)#accelarate
        elif choice == 1:
            self.accelerate(self.dvel)#reverse
        elif choice == 2:
            if (self.vel ==0):
                self.accelerate(-self.dvel)
                self.turn(-1)#right
            else:
                self.turn(-1)#rights
        elif choice == 3:
            if (self.vel ==0):
                self.accelerate(-self.dvel)
                self.turn(1)#right
            else:
                self.turn(1)#right   
        elif choice == 4:
            if (self.vel ==0):
              self.accelerate(-self.dvel)
            else:pass ''' 
            
        
    
    def accelerate(self,dvel):
        #dvel = dvel * 2
        #நிலையான வேகத்தில் துரிதப்படுத்தப்பட்டது
        self.vel = self.vel + dvel

        if self.vel > self.maxvel:
            self.vel = self.maxvel
        
        if self.vel < -self.maxvel:
            self.vel = -self.maxvel
        
        
    def turn(self, dir):
        
        
        self.soll_angle = self.soll_angle + dir * math.radians(15)
    
    def update(self):

        
        self.angle = self.soll_angle

        vec_temp = rotate(myPoint(0,0), myPoint(0,self.vel), self.angle)
        self.velX, self.velY = vec_temp.x, vec_temp.y

        self.x = self.x + self.velX
        self.y = self.y + self.velY

        self.rect.center = self.x, self.y

        self.pt1 = myPoint(self.pt1.x + self.velX, self.pt1.y + self.velY)
        self.pt2 = myPoint(self.pt2.x + self.velX, self.pt2.y + self.velY)
        self.pt3 = myPoint(self.pt3.x + self.velX, self.pt3.y + self.velY)
        self.pt4 = myPoint(self.pt4.x + self.velX, self.pt4.y + self.velY)

        self.p1 ,self.p2 ,self.p3 ,self.p4  = rotateRect(self.pt1, self.pt2, self.pt3, self.pt4, self.soll_angle)

        self.image = pygame.transform.rotate(self.original_image, 90 - self.soll_angle * 180 / math.pi)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)

    def cast(self, walls):
        self.rays = [Ray(self.x, self.y, self.soll_angle)]
        for i in range(1,180,1):
            self.rays.append(Ray(self.x, self.y, self.soll_angle - math.radians( i )))
        self.rays.append(Ray(self.x, self.y, self.soll_angle - math.radians( 180 )))
        for i in range(179,0,-1):
            self.rays.append(Ray(self.x, self.y, self.soll_angle + math.radians( i )))    
 
        observations = []
        self.closestRays = []
        
        noi = np.random.randint(1,360,noise_points)
        
        
        for count,ray in enumerate(self.rays):
          
            
            closest = None #myPoint(0,0)
            record = math.inf
       
            for wall in walls:
            
                pt = ray.cast(wall)
                if pt:
                    dist = distance(myPoint(self.x, self.y),pt)
                    #print(pt.x,pt.y)
                    if dist < record:
                        record = dist
                        closest = pt

            if closest: 
                #append distance for   current ray 
                rand = np.random.rand()
                if(count in noi and rand<limter):
                    closest.x = self.x + np.random.randint(-50,50)
                    closest.y = self.y + np.random.randint(-50,50)
                    record = distance(myPoint(self.x, self.y),closest)
                    if (abs(record)<(dangerlimit*one_cm)):
                      record = (dangerlimit*one_cm)+1
                      closest.x = int((dangerlimit*one_cm)+1)
                      closest.x = int((dangerlimit*one_cm)+1)
                self.closestRays.append(closest)
                observations.append(record)
               
            else:
                observations.append(2482)
              
        if ((self.actvalue%cmp) == 0) :
        
            mp = np.random.randint(0,(360-gap),nmp)
            self.mislis = []
            for n in mp:
                self.mislis+=list(np.linspace(n-(gap/2),n+((gap/2)-1),gap)) 
        for i in self.mislis:
            observations[int(i)] = 0
       
        # 22.5m range        
        for i in range(len(observations)):
            if (observations[i]>int(sensor_range*one_cm)): 
              observations[i] = 0
            elif (observations[i]<int(30*one_cm)): 
              observations[i] = 0  
            elif (observations[i]>int((0.7*sensor_range)*one_cm)):
               if(np.random.rand() < 0.5):observations[i] = 0 
                
                
            else:
              observations[i]+=int(np.random.normal(mean_center,sensor_uncertain)*one_cm)# one_cm pixel = 1cm   
        
        observations = [i/(sensor_range*one_cm) for i in observations]
        
        
        #observations.append(self.vel / self.maxvel)
        
        
        return observations

    def collision(self, wall):

        line1 = myLine(self.p1, self.p2)
        line2 = myLine(self.p2, self.p3)
        line3 = myLine(self.p3, self.p4)
        line4 = myLine(self.p4, self.p1)

        x1 = wall.x1 
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        lines = []
        lines.append(line1)
        lines.append(line2)
        lines.append(line3)
        lines.append(line4)

        for li in lines:
            
            x3 = li.pt1.x
            y3 = li.pt1.y
            x4 = li.pt2.x
            y4 = li.pt2.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            
            if(den == 0):
                den = 0
            else:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

                if t > 0 and t < 1 and u < 1 and u > 0:
                    return(True)
        
        return(False)
    
    def score(self, goal,n):
        
        line1 = myLine(self.p1, self.p3)

        vec = rotate(myPoint(0,0), myPoint(0,-50), self.angle)
        line1 = myLine(myPoint(self.x,self.y),myPoint(self.x + vec.x, self.y + vec.y))

        x1 = goal.x1 
        y1 = goal.y1
        x2 = goal.x2
        y2 = goal.y2
            
        x3 = line1.pt1.x
        y3 = line1.pt1.y
        x4 = line1.pt2.x
        y4 = line1.pt2.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if(den == 0):
            den = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1))

                d = distance(myPoint(self.x, self.y), myPoint(pt[0], pt[1]))
                if d < 20:
                    #pygame.draw.circle(win, (0,255,0), pt, 5)
                    if n:
                        self.points += GOALREWARD
                    else:
                        self.points +=GOALPENALTY
                    return(True)

        return(False)

    def reset(self):

        self.x = begin_x
        self.y = begin_y
        self.velX = 0
        self.velY = 0
        self.vel = 0
        self.angle = math.radians(angle_ss)
        self.soll_angle = self.angle
        self.points = 0
        self.actvalue = 0
        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
        self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

    def draw(self, win):
        win.blit(self.image, self.rect)
  

class RacingEnv:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.status = ''
        self.fps = 120
        self.width = 1920
        self.height = 1080
        self.history = []
        self.minrec = 0
        self.minlis =[]
        self.active_goal_x =0
        self.active_goal_y =0
        self.goal_rec = 0
        self.active_goal = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulation")
        self.screen.fill((0,0,0))
        self.back_image = pygame.image.load("track_.png").convert()
        self.back_rect = self.back_image.get_rect().move(0, 0) 
        self.action_space = None
        self.observation_space = None
        self.game_reward = 0
        self.score = 0
        self.cg =0
        self.actvalue=0
        self.reset()


    def reset(self):
        self.screen.fill((0, 0, 0))
        self.cg = 0
        self.car = Car(begin_x, begin_y)
        self.walls = getWalls()
        self.goals = getGoals()
        self.game_reward = 0
        self.minrec = 0
        self.minlis =[]
        self.active_goal_x =0
        self.active_goal_y =0
        self.goal_rec = 0
        self.active_goal = 0 
        self.actvalue=0
    def step(self, action):
        
        Car.actvalue = self.actvalue
        self.status = ''
        done = False
        
        #uncertainities
        loc_err_x = np.random.normal(0,loc_unc*one_cm)
        loc_err_y = np.random.normal(0,loc_unc*one_cm)
        ang_err = np.random.normal(0,ang_unc)
        self.car.x += int(loc_err_x)
        self.car.y += int(loc_err_y)
        self.car.soll_angle+=ang_err
        
        self.car.action(action)      
        self.car.update()
        reward = LIFE_REWARD
       
        index = 0
        i =0
        
        
######################################################################################################
        active_goal = self.goals[self.active_goal]
        self.active_goal_x =(active_goal.x1+active_goal.x2)/2
        self.active_goal_y = (active_goal.y1+active_goal.y2)/2
        goal_dist = np.sqrt((self.car.x - self.active_goal_x)**2+(self.car.y -self.active_goal_y)**2)
        if self.car.score(active_goal,True):
            self.goals[self.active_goal].isactiv = False
            self.active_goal+=1
            if (self.active_goal >= len(self.goals)):
                done = True 
            else:
                self.goals[self.active_goal].isactiv = True
            #
            
            goal_dist = 1000
            #print(self.active_goal)
            #()
            reward += GOALREWARD 
            self.cg+=1
            self.status+= "Reached Goal"
        if(self.active_goal>1):    
            if self.car.score(self.goals[self.active_goal-2],False):
                self.status+= "Wrong Goal"
                reward += GOALPENALTY
                ##
                #print("tha")
                ##()



        
        
#######################################################################################################

########################################################################################            
        #check if car crashed in the wall
        w = 0
        for wall in self.walls:
            w+=1
            
            if self.car.collision(wall):
                #
                #print("Crash detected on wall", w ,"/", len(self.walls))
                #()
                reward += PENALTY
                self.status+= "Crashed"
                done = True
        if (reward < (PENALTY)): reward = PENALTY    
############################################################################################################        
        
        new_state = self.car.cast(self.walls)
        #normalize states
        if done:
            new_state = self.car.cast(self.walls)
#########################################################################################################        
        #If drive back
        if(self.car.x < ellai):
          reward +=PENALTY
          self.status+= "Wrong way"
          done = True
##################################################################################################################        
        #Danger Zone        
        dangerzone = False
        approach = None
        safezone = True
                 
        for i in range(360):
          #print(new_state[i],(dangerlimit*one_cm)/(sensor_range*one_cm))
          if ((new_state[i]<((dangerlimit*one_cm)/(sensor_range*one_cm))and new_state[i]>0)):
            if (new_state[i]<self.minrec):
              approach = True
              dangerzone = True
              safezone = False              
            else: 
              dangerzone = True
              safezone = False   
              
       # updating closet distance
        x = new_state[:-1]
        while 0 in x: x.remove(0)
        if (len(x) != 0):
          self.minrec = min(x)
        
########################################################################################          
        #dangerzone reward 
        if(dangerzone):
          if (approach):
            reward += ZONEPENALTY
            self.status+= "About to crash"
          if (not approach):
            self.status+= "Avoiding walls"
            reward += SAFEZONE_REWARD          
        #safezone rewards 
        if (goal_dist != 1000):
            if (safezone):
              if goal_dist<self.goal_rec:
                self.status+= "Approaching Goal"
                reward+= encourage_reward
              else:  
                self.status+= "Moving away from goal"
                reward+= discourge_reward 
#################################################################################################             
            
        self.goal_rec = goal_dist
        return new_state, reward, done

    def render(self, action,score,memory =0, ep = 0):

        DRAW_WALLS = False
        DRAW_GOALS = True
        DRAW_RAYS = True
        DRAW_DZ = True
        pygame.draw.circle(self.screen, (0,255,0), ((self.car.p1.x + self.car.p2.x)/2, (self.car.p1.y + self.car.p2.y)/2), 15)
        pygame.time.delay(10)

        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.back_image, self.back_rect)
        
        if DRAW_WALLS:
           
            for wall in self.walls:
                
               wall.draw(self.screen)      
     

        if DRAW_RAYS:
            i = 0
            for pt in self.car.closestRays:
                
                i+=1
                if(i in self.car.mislis):continue
                dist = np.sqrt((self.car.x-pt.x)**2+(self.car.y-pt.y)**2)
                if (dist<(sensor_range*one_cm)):
                  
                  if (dist<(dangerlimit*one_cm)):
                    #pygame.draw.line(self.screen, (255,0,0), (self.car.x, self.car.y), (pt.x, pt.y), 1)
                    pygame.draw.circle(self.screen, (255,0,0), (pt.x, pt.y), 3)
                    
                  else:
                    #pygame.draw.line(self.screen, (0,255,255), (self.car.x, self.car.y), (pt.x, pt.y), 1)
                    pygame.draw.circle(self.screen, (0,0,255), (pt.x, pt.y), 3)
                        
        self.car.draw(self.screen)
        if DRAW_GOALS:
  
            for goal in self.goals:
            
                goal.draw(self.screen)
                if goal.isactiv:
                    goal.draw(self.screen)
        #render controll
        
        # score
        ep +=100
        text_surface = self.font.render(f'Episode : {ep}', True, pygame.Color('red'))
        self.screen.blit(text_surface, dest=(800, 400))
        text_surface = self.font.render(f'Score : {score}', True, pygame.Color('red'))
        self.screen.blit(text_surface, dest=(800, 450))
        # speed
        text_surface = self.font.render(f'actions taken: {memory}', True, pygame.Color('red'))
        self.screen.blit(text_surface, dest=(800, 500))
        text_surface = self.font.render(f'Status:  {self.status}', True, pygame.Color('red'))
        self.screen.blit(text_surface, dest=(800, 550))
        text_surface = self.font.render(f'Crossed Goals: {self.cg}', True, pygame.Color('red'))
        self.screen.blit(text_surface, dest=(800, 600))
        self.clock.tick(self.fps)
        pygame.display.update()

    def close(self):
        pygame.quit()



