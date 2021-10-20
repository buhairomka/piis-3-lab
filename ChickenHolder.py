# chicken holder
import random
import time
import pygame

from Chick import Chick, Dummy
from sources import size_of_chick, WIDTH, start_time, write_to_csv, score, get_score


def invert(img):
    return pygame.transform.flip(img, True, False)




class ChicksHolder:
    
    def __init__(self):
        self.chicks = []
        self.len = len(self.chicks)
    
    def set_chicks(self):
        global start_time
        print("--- %s seconds ---" % (time.time() - start_time))
        write_to_csv('win',"%s s" % (time.time() - start_time),get_score(),'emm')
        Chick.velocity = 1
        for i in range(1):
            for j in range(2):
                self.chicks.append(Chick((j + 3) * (size_of_chick + random.randint(0,40)), (i + 2) * (size_of_chick + random.randint(0,30))))
                self.chicks.append(Dummy((j + 3) * (size_of_chick + random.randint(0, 40)),
                                         (i + 2) * (size_of_chick + random.randint(0, 30))))
        start_time=time.time()
    
    def draw_all(self, window):
        if len(self.chicks) > 0:
            for each in self.chicks:
                each.draw(window)
    
    def move(self, bulls):
        for i in self.chicks:
            if i.x + i.image.get_width() + Chick.velocity > WIDTH or i.x + Chick.velocity < 0:
                Chick.velocity *= -1
                for i in self.chicks:
                    i.image = invert(i.image)
                break
            else:
                i.move(bulls, self)
    
    def copy_object(self):
        res = ChicksHolder()
        for chick in self.chicks:
            res.chicks.append(chick.copy_object())
        return res
