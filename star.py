import pygame as pg
import random

class Star(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("star.png")
        self.image = pg.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50,1750)
        self.rect.y = random.randint(50,350)
    
    def update(self):
        random_int = random.randint(0,3)
        if random_int == 0:
            self.rect.x += 1
        if random_int == 1:
            self.rect.x -= 1
        if random_int == 2:
            self.rect.y += 1
        if random_int == 3:
            self.rect.y -= 1
