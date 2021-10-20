from numpy.random import choice

from Ship import Ship
from sources import *


class Chick(Ship):
    velocity = 1
    
    def __init__(self, x, y, ):
        super().__init__(x, y, )
        self.type = choice(['yellow', 'blue', 'red'], p=[.2, .3, .5])
        self.image = YELLOW_CHICK_IMG if self.type == 'yellow' else BLUE_CHICK_IMG if self.type == 'blue' else RED_CHICK_IMG if self.type == 'red' else ''
        self.lives = 1 if self.type == 'yellow' else 2 if self.type == 'blue' else 3 if self.type == 'red' else 0
        self.bullet = EGG_IMG
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self,bulls,chicks):
        # print('chick', self.x, self.y)
        self.x += Chick.velocity
        for bul in bulls.lasers:
            if bul.x in range(self.x - int(LASER_IMG.get_width()),
                              self.x + size_of_chick) and bul.y + LASER_IMG.get_height() > self.y:
                # if bul.x in range(0 if self.x-LASER_IMG.get_width()-1<0 else self.x-LASER_IMG.get_width()-1,(WIDTH-size_of_chick) if self.x+size_of_chick+1>WIDTH else WIDTH-size_of_chick):
                # if chicken more left from laser
                if self.x + size_of_chick / 2 - bul.x + LASER_IMG.get_width() / 2 < 0:
                    # move left
                    # if no start of map
                    if self.x - abs(self.velocity) > 0:
                        self.x -= abs(self.velocity) * 2
                    # else move right
                    else:
                        self.x += abs(self.velocity) * 20
                elif self.x + size_of_chick / 2 - bul.x + LASER_IMG.get_width() / 2 > 0:
                    # move right
                    # if not end of map
                    if self.x + size_of_chick + abs(self.velocity) < WIDTH:
                        self.x += abs(self.velocity) * 2
                    # else move left
                    else:
                        print(chicks)
                        chicks.move(bulls.copy_object())
                        
                        self.x -= abs(self.velocity) * 20

    def copy_object(self):
        res = Chick(self.x,self.y)
        res.type = self.type
        res.image = self.image
        res.lives = self.lives
        return res


class Dummy(Chick):
    def move(self, bulls, chicks):
        self.x += Dummy.velocity