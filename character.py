import pygame as pg

class Caracter(pg.sprite.Sprite):
    def __init__(self,x=0,y=0,speed=0.06, count_frames=8):
        self.count_frames = count_frames
        self.status = "Run"
        self.load_frames(self.status)
        self.image = self.frames[int(self.current_frame)]
        # self.image = pg.image.load("assets/player/sprite_1.png")
        # self.image_left = pg.transform.flip(self.image,True,False)
        # self.image_right = pg.transform.flip(self.image,False,False)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.rect.x = x
        self.rect.y = y
        self.rect.width = int(self.rect.width*0.5)
        self.speed = speed
        self.alive = True

    def load_frames(self,folder_name):
        frames = []
        for i in range(1,self.count_frames+1):
            frame = pg.image.load(f"assets/player/{folder_name}/{folder_name} ({i}).png")
            frames.append(frame) 
        pg.sprite.Sprite.__init__(self)
        self.frames = frames
        self.current_frame = 0
        
        
    
    def update(self):
        if self.alive == True:
            self.current_frame += self.speed
            if self.current_frame >= self.count_frames:
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
            old_pos = self.rect.topleft
            self.image = pg.transform.scale(self.image,(265,400))
            self.rect = self.image.get_rect(topleft=old_pos)
            self.rect.width = int(self.rect.width*0.5)
            if self.status == "Jump":
                if self.direction == "up":
                    self.rect.y -=1.5
                elif self.direction == "down":
                    self.rect.y +=1.5

                if self.rect.y <= 100:
                    self.direction = "down"
                elif self.rect.y >= 400:
                    self.rect.y = 400
                    self.run()
    
            



    def run(self):
        if self.status != "Run":
            self.status = "Run"
            self.count_frames = 8
            self.load_frames(self.status)


    def jump(self):
        if self.status != "Jump":
            self.status = "Jump"
            self.count_frames = 12
            self.load_frames(self.status)
            self.direction = "up"



if __name__ == "__main__":
    q = Caracter()
        # keys = pg.key.get_pressed()


        # if keys[pg.K_a]:
        #     if self.rect.left >= 30:
        #         self.rect.x -= 2
        #         self.direction = "left"
        # if keys[pg.K_d]:
        #     if self.rect.right <= 1890:
        #         self.rect.x += 2
        #         self.direction = "right"
