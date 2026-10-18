import pygame as pg

class Wheel(pg.sprite.Sprite):
    def __init__(self,x=0,y=0):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"assets/wheel/wheel.png")
        # self.image = pg.image.load("assets/player/sprite_1.png")
        # self.image_left = pg.transform.flip(self.image,True,False)
        # self.image_right = pg.transform.flip(self.image,False,False)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
      old_pos = self.rect.topleft
      self.image = pg.transform.scale(self.image,(111,111))
      self.rect = self.image.get_rect(topleft=old_pos)
      self.rect.x -= 2
      if self.rect.right < 0:
          self.kill()
if __name__ == "__main__":
    q = Wheel()
        # keys = pg.key.get_pressed()


        # if keys[pg.K_a]:
        #     if self.rect.left >= 30:
        #         self.rect.x -= 2
        #         self.direction = "left"
        # if keys[pg.K_d]:
        #     if self.rect.right <= 1890:
        #         self.rect.x += 2
        #         self.direction = "right"
