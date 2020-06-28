import pygame
class CARD():
    def __init__(self,s):
        self.image=pygame.image.load("../card/"+str(s)+".jpg")
        self.num=s
        self.position=False
        self.y=550

    def check(self,y,shotcard):
        if self.position and 520<y<628:
            self.position=False
            self.y=550
            shotcard.remove(self.num)
            
        elif 550<y<658:
            self.position=True
            self.y=520
            shotcard.append(self.num)
        return shotcard

    def draw(self,x,y,surface):
        surface.blit(self.image, (x,y))

    def draw_short(self,x,surface):
        self.image=pygame.transform.smoothscale(self.image, (50,72))
        surface.blit(self.image, (x,self.y))