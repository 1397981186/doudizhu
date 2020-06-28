from PIL import ImageTk, Image
import pygame
from pygame.locals import *
from button import Button as Bt
pygame.init()

button_0={}
button_1={}
button_3={}
button_4={}
button_5={}

imgpath = '../gameButPic/1.png'
img = Image.open(imgpath)

background_image_filename = '../gameButPic/bg1.png'
background = pygame.image.load(background_image_filename)

yaobuqi = pygame.image.load('../gameButPic/yaobuqi.png')
img_yaobuqi = pygame.transform.scale(yaobuqi, ( 146 , 52))

img_landlord = pygame.image.load('../profilePic/landlord.png')
img_farmer = pygame.image.load('../profilePic/farmer.png')
img_left_bg = pygame.transform.scale(pygame.image.load('../gameButPic/left_bg.jpg'), (50, 68))
rect_bg = img_left_bg.get_rect()
my_font = pygame.font.SysFont("arial", 30)
time_font = pygame.font.SysFont("arial", 20)

readypic = pygame.image.load('../gameButPic/readynow.png')

alarmimg_i = pygame.image.load("../gameButPic/alarm.png")
alarmimg = pygame.transform.smoothscale(alarmimg_i, (60, 60))

img_photo = pygame.image.load('../profilePic/farmer1_win.png')

img_f_w = pygame.image.load('../gameButPic/farmerwin.png')
img_f_win = pygame.transform.smoothscale(img_f_w, (400, 400))

img_k_w = pygame.image.load('../gameButPic/kingwin.png')
img_k_win = pygame.transform.smoothscale(img_k_w, (300, 100))

button_0['exit'] = Bt('../gameButPic/exit.png', (550, 547.5))
button_0['quick'] = Bt('../gameButPic/quick.png', (550, 365))
button_0['start'] = Bt('../gameButPic/start.png', (550, 182.5))

button_1['ready'] = Bt('../gameButPic/ready.png', (550, 500))

button_3['calllord'] = Bt('../gameButPic/calllord.png', (490, 490))
button_3['calllord'].transform(180, 65)
button_3['notcall'] = Bt('../gameButPic/notcall.png', (670, 490))
button_3['notcall'].transform(120, 60)

button_4['pass'] = Bt('../gameButPic/pass.png', (385, 490))
button_4['hint'] = Bt('../gameButPic/hint.png', (573, 490))
button_4['shot'] = Bt('../gameButPic/shot.png', (761, 490))

button_5['ok'] = Bt('../gameButPic/ok.png', (550, 600))
