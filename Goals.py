import pygame

class Goal:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.isactiv = False
    
    def draw(self, win):
        if self.isactiv:
            pygame.draw.line(win, (0,255,0), (self.x1, self.y1), (self.x2, self.y2), 5)

        #pygame.draw.line(win, (255,0,0), (self.x1, self.y1), (self.x2, self.y2), 2)
        
# the file of shame
def getGoals():
    goals = []

    goal1  = Goal ( 500 , 100, 500  , 300)
    goal2  = Goal ( 550 , 100, 550  , 300)
    goal3  = Goal ( 600 , 100, 600  , 300)
    goal4  = Goal ( 650 , 100, 650  , 300)
    goal5  = Goal ( 700 , 100, 700  , 300)
    goal6  = Goal ( 750 , 100, 750  , 300)
    goal7  = Goal ( 800 , 100, 800  , 300)
    goal8  = Goal ( 850 , 100, 850  , 300)
    goal9  = Goal ( 900 , 100, 900  , 300)
    goal10  = Goal ( 950 , 100, 950  , 300)
    goal11  = Goal ( 1000 , 100, 1000  , 300)
                   
    goal12  = Goal ( 1050 , 130, 1050  , 195)
    goal13  = Goal ( 1100 , 130, 1100  , 195)
    goal14  = Goal ( 1150 , 130, 1150  , 195)
    goal15  = Goal ( 1200 , 130, 1200  , 195)
    goal16  = Goal ( 1250 , 130, 1250  , 195)
    goal17  = Goal ( 1300 , 130, 1300  , 195)
    goal18  = Goal ( 1350 , 130, 1350  , 195)
    goal19  = Goal ( 1400 , 130, 1400  , 195)
    goal20  = Goal ( 1450 , 130, 1450  , 195)
    goal21  = Goal ( 1500 , 130, 1500  , 195)
    goal22  = Goal ( 1550 , 130, 1550  , 195)
    goal23  = Goal ( 1600 , 130, 1600  , 195)
    
    goalturnbonus1  = Goal ( 1600 , 182, 1635 , 165)
                   
    goal24  = Goal (1550, 200 ,1705 , 200 )
    goal25  = Goal (1550, 250 ,1705 , 250 )
    goal26  = Goal (1550, 300 ,1705 , 300 )
    goal27  = Goal (1550, 350 ,1705 , 350 )
    goal28  = Goal (1550, 400 ,1705 , 400 )
    goal29  = Goal (1550, 450 ,1705 , 450 )
    goal30  = Goal (1550, 500 ,1705 , 500 )
    goal31  = Goal (1550, 550 ,1705 , 550 )
    goal32  = Goal (1550, 600 ,1705 , 600 )
    goal33  = Goal (1550, 650 ,1705 , 650 )
    goal34  = Goal (1550, 700 ,1705 , 700 )
    goal35  = Goal (1550, 750 ,1705 , 750 )
    goal36  = Goal (1550, 800 ,1705 , 800 )
                   
    goal37  = Goal (1510, 650 ,1775 , 650 )
    goal38  = Goal (1510, 600 ,1775 , 600 )
    goal39  = Goal (1510, 550 ,1775 , 550 )
    goal40  = Goal (1510, 500 ,1775 , 500 )
    goal41  = Goal (1510, 450 ,1775 , 450 )
    goal42  = Goal (1510, 400 ,1775 , 400 )
    goal43  = Goal (1510, 350 ,1775 , 350 )
    goal44  = Goal (1510, 300 ,1795 , 300 )
    goal45  = Goal (1510, 250 ,1795 , 250 )
    goal46  = Goal (1510, 200 ,1795 , 200 )
   
    
    goalturnbonus2  = Goal ( 1600 , 182, 1635 , 135)
                   
    goal50  = Goal ( 1550 , 130, 1550  , 195)
    goal51  = Goal ( 1500 , 130, 1500  , 195)
    goal52  = Goal ( 1450 , 130, 1450  , 195)
    goal53  = Goal ( 1400 , 130, 1400  , 195)
    goal54  = Goal ( 1350 , 130, 1350  , 195)
    goal55  = Goal ( 1300 , 130, 1300  , 195)
    goal56  = Goal ( 1250 , 130, 1250  , 195)
    goal57  = Goal ( 1200 , 130, 1200  , 195)
    goal58  = Goal ( 1150 , 130, 1150  , 195)
    goal59  = Goal ( 1100 , 130, 1100  , 195)
    goal60  = Goal ( 1050 , 130, 1050  , 195)
    
                   
    goal62  = Goal ( 1000 , 150, 1000  , 200)
    goal63  = Goal ( 950 , 150, 950  , 200)
    goal64  = Goal ( 900 , 150, 900  , 200)
    goal65  = Goal ( 850 , 150, 850  , 200)
    goal66  = Goal ( 800 , 150, 800  , 200)
    goal67  = Goal ( 750 , 150, 750  , 200)
    goal68  = Goal ( 700 , 150, 700  , 200)
    goal69  = Goal ( 650 , 150, 650  , 200)
    goal70  = Goal ( 600 , 150, 600  , 200)
    goal71  = Goal ( 550 , 150, 550  , 200)
    goal72  = Goal ( 500 , 150, 500  , 200)
    '''
    goals.append(goal1 )
    goals.append(goal2 )
    goals.append(goal3 )
    goals.append(goal4 )
    goals.append(goal5 )
    goals.append(goal6 )
    goals.append(goal7 )
    goals.append(goal8 )
    goals.append(goal9 )
    goals.append(goal10 )
    goals.append(goal11 )
    goals.append(goal12 )
    goals.append(goal13 )
    goals.append(goal14 )
    goals.append(goal15 )
    goals.append(goal16 )
    goals.append(goal17 )
    goals.append(goal18 )
    goals.append(goal19 )
    goals.append(goal20 )'''
    goals.append(goal21 )
    goals.append(goal22 )
    goals.append(goal23 )
    goals.append(goalturnbonus1)
    goals.append(goal24 )
    goals.append(goal25 )
    goals.append(goal26 )
    goals.append(goal27 )
    goals.append(goal28 )
    goals.append(goal29 )
    goals.append(goal30 )
    goals.append(goal31 )
    goals.append(goal32 )
    goals.append(goal33 )
    goals.append(goal34 )
    goals.append(goal35 )
    #goals.append(goal36 )
    goals.append(goal37 )
    goals.append(goal38 )
    goals.append(goal39 )
    goals.append(goal40 )
    goals.append(goal41 )
    goals.append(goal42 )
    goals.append(goal43 )
    goals.append(goal44 )
    goals.append(goal45 )
    goals.append(goal46 )
    #goals.append(goal47 )
    #goals.append(goal48 )
    #goals.append(goal49 )
    
    goals.append(goalturnbonus2)
    
    goals.append(goal50 )
    goals.append(goal51 )
    goals.append(goal52 )
    goals.append(goal53 )
    goals.append(goal54 )
    goals.append(goal55 )
    goals.append(goal56 )
    goals.append(goal57 )
    goals.append(goal58 )
    goals.append(goal59 )
    goals.append(goal60 )
    #goals.append(goal61 )
    goals.append(goal62 )
    goals.append(goal63 )
    goals.append(goal64 )
    goals.append(goal65 )
    goals.append(goal66 )
    goals.append(goal67 )
    goals.append(goal68 )
    goals.append(goal69 )
    goals.append(goal70 )
    goals.append(goal71 )
    goals.append(goal72 )
    


    
    #goals = list(reversed(goals))
    goals[0].isactiv = True

    return(goals)
