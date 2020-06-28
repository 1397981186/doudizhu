import pygame
import socket
from pygame.locals import *
from sys import exit
import threading
import json
import time
import cardAna
import math
from card import CARD
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import ImageTk, Image
import sound
import my_img
from rule import rule


class LoginPage(Frame):
    def __init__(self,sc):
        super().__init__()
        self.sock=sc
        self.photo = ImageTk.PhotoImage(my_img.img)
        self.grid_propagate(0)
        self.username = StringVar()
        self.password = StringVar()
        self.pack()
        self.createForm()

 
    def createForm(self):
        canvas = Canvas(self, width=450,height=310,bd=0, highlightthickness=0)
        canvas.create_image(0,0,image=self.photo,anchor=NW)
        canvas.pack()
        Label(self, text = '账户').place(x=130,y=100)
        Entry(self, textvariable=self.username).place(x=180,y=100)
        Label(self, text = '密码').place(x=130,y=160)
        Entry(self, textvariable=self.password, show='*').place(x=180,y=160)
        Button(self, text='登录', command=self.loginCheck).place(x=130,y=200)
        Button(self, text='注册', command=self.toReg).place(x=290,y=200)

 
    def loginCheck(self):
        if(len(self.username.get())==0 or len(self.password.get())==0):
            showinfo(title='错误', message='请同时输入用户名和密码！')
        else:
            name = self.username.get()
            secret = self.password.get()
            json = {
                'Status': 200,
                'Operation': 'login',
                'p_name':name,
                'p_pw':secret
                }
            self.sock.sendall(str.encode(str(json)))
            data = self.sock.recv(1024)
            da=eval(data)
            if(da['text']=="OK"):
                self.destroy()
                root.destroy()
            else:
                showinfo(title='错误', message='用户名或密码错误！')
    def toReg(self):
        s=self.sock
        self.destroy()
        RegPage(s)


class RegPage(Frame):
    def __init__(self,sc):
        super().__init__()
        self.sock=sc
        self.photo = ImageTk.PhotoImage(my_img.img)
        self.grid_propagate(0)
        self.username = StringVar()
        self.password = StringVar()
        self.passwordAgain = StringVar()
        self.pack()
        self.createForm()

 
    def createForm(self):
        canvas = Canvas(self, width=450,height=310,bd=0, highlightthickness=0)
        canvas.create_image(0,0,image=self.photo,anchor=NW)
        canvas.pack()
        Label(self, text = '账户').place(x=130,y=80)
        Entry(self, textvariable=self.username).place(x=180,y=80)
        Label(self, text = '密码').place(x=130,y=130)
        Entry(self, textvariable=self.password, show='*').place(x=180,y=130)
        Label(self, text = '确认密码').place(x=115,y=180)
        Entry(self, textvariable=self.passwordAgain, show='*').place(x=180,y=180)
        Button(self, text='注册', command=self.register).place(x=220,y=230)
         
    def register(self):
        if(len(self.username.get())==0 or len(self.password.get())==0 \
           or len(self.passwordAgain.get())==0):
            showinfo(title='错误', message='请同时输入用户名和密码！')
        elif self.passwordAgain.get() != self.password.get():
            showinfo(title='错误', message='两次输入密码不一致！')
        else:
            name = self.username.get()
            secret = self.password.get()
            json = {
                'Status': 200,
                'Operation': 'reg',
                'p_name':name,
                'p_pw':secret
            }
            self.sock.sendall(str.encode(str(json)))
            data = self.sock.recv(1024)
            da=eval(data)
            if(da['text']=="OK"):
                s=self.sock
                self.destroy()
                LoginPage(s)
            else:
                showinfo(title='提示', message='用户名已存在')

def EXIT():
    root.destroy()
    exit()


s = socket.socket()  # 创建 socket 对象
host = '10.162.234.140' # 获取本地主机名
#host = socket.gethostname()

port = 12345  # 设置端口号
s.connect((host, port))


root = Tk()
root.title('斗地主')
root.protocol(name='WM_DELETE_WINDOW',func=EXIT)
LoginPage(s)
root.mainloop()



pygame.init()

whois = 0
who_turn=[]
clear_turn = []
select_king_flag = 0
mycards = []
dizhu_cards_add = []
left = []
right = []
leftnum = 17
rightnum = 17
mul=1
# my,left,right
myshot = []
turn = 0
shot = []
T = ""
V = 0
kingwin=0
all_time = 20
hint_cards=[]
last_cards=[]
hint_flag=0

def countdown():
    global all_time
    while True:
        time.sleep(1)
        all_time-=1
        if all_time == -1:
            all_time = 20

def bgmusic():
    pygame.mixer.init()
    pygame.mixer.music.load('../sound/MusicEx_Normal.ogg')
    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()



def card_Analyse(s):  # 仅仅要求用户输入要发的牌，返回type和value 刷新CURRENT。
    res = ['', 0, 0, 0]  # 牌型，value，牌数，是否符合规则
    SELECT = s
    SELECT = sorted(SELECT)  # 排序
    cardAna.card_analyse(SELECT, res)
    # res[0]类型
    # res[1]序号
    # res[2]张数
    # res[3]是否符合规则
    return res


def json_parse(js):
    recjs = eval(js)
    # change
    global count
    global whois
    global who_turn
    global mycards
    global dizhu_cards_add
    global left
    global right
    global leftnum
    global rightnum
    global myshot
    global turn
    global game
    global T
    global V
    global do_not_show_yaobuqi_l
    global do_not_show_yaobuqi_r
    global mul
    global kingwin
    global all_time
    global clear_turn
    global select_king_flag
    global last_cards
    if recjs['Operation'] == 'message':
        print(recjs['message'])
    
    elif recjs['Operation'] == 'init':
        game = 3
        mycards = recjs['message']
        mycards = sorted(mycards)
        all_time = 20
    elif recjs['Operation'] == 'AskS':
        select_king_flag = 1
    elif recjs['Operation'] == 'InfK':
        whois = 1
        if recjs['message'] == 1:
            sound.qiangS.play()
        else:
            sound.buqiangS.play()
    elif recjs['Operation'] == 'ID':
        global myself
        myself = player(recjs['message'])
        who_turn=myself.who_turn
        clear_turn = myself.clear_turn
        
    elif recjs['Operation'] == 'king':
        myself.king = recjs['message']
        myself.to_get_alarm(myself.king)
        who_turn=myself.who_turn
        clear_turn = myself.clear_turn
        leftnum = myself.leftcard
        rightnum = myself.rightcard
        game = 4
        if myself.king == myself.myid:
            mycards.extend(recjs['card'])
            mycards = sorted(mycards)
            turn = 1
        dizhu_cards_add=recjs['card']
        dizhu_cards_add = sorted(dizhu_cards_add)
        mul=recjs['mul']
    elif recjs['Operation'] == 'SetTurn':
        # 开始和用户交互发牌
        # 返回发牌情况给服务器
        T = recjs['type']
        V = recjs['value']
        last_cards = recjs['card']
        turn = 1
        # 如果cardnum是0，返回情况给服务器
        # print(recjs)
    elif recjs['Operation'] == 'AGAIN':
        print(recjs['message'])
        if(myself.king==recjs['id']):kingwin=1
        else: kingwin=0
        game=5
        who_turn=[]
        clear_turn = []
        dizhu_cards_add = []
        left=[]
        right=[]
        leftnum = 17
        rightnum = 17
        myshot = []
        shot = []
        mul=1
        do_not_show_yaobuqi_l=0
        do_not_show_yaobuqi_r=0

    elif recjs['Operation'] == 'Announce':
        if recjs['id'] == myself.leftid:
            whois = 1
            left = recjs['message']
            leftnum = leftnum - len(recjs['message'])
            if recjs['type'] == 'Jump':
                do_not_show_yaobuqi_l = 1
            else:
                do_not_show_yaobuqi_l = 0
            sound.cardAnaSound(recjs)
        elif recjs['id'] == myself.rightid:
            whois = 1
            right = recjs['message']
            rightnum = rightnum - len(recjs['message'])
            if recjs['type'] == 'Jump':
                do_not_show_yaobuqi_r = 1
            else:
                do_not_show_yaobuqi_r = 0
            sound.cardAnaSound(recjs)
        mul=recjs['mul']
    else:
        print('Unknown json')



class player():
    def __init__(self, getid):
        self.myid = getid
        self.king = 0
        if getid==0:
            self.who_turn = [(570,410),(950,390),(100,390)]
        elif getid==1:
            self.who_turn = [(100,390),(570,410),(950,390)]
        elif getid==2:
            self.who_turn = [(950,390),(100,390),(570,410)]

        self.clear_turn = ['medium', 'right', 'left']
        self.mycard = 0
        self.leftid = (getid+2)%3
        self.leftcard = 0
        self.rightid = (getid+1)%3
        self.rightcard = 0

    def to_get_alarm(self,K):
        if K == self.myid:
            self.who_turn = [(570, 410), (950, 390), (100, 390)]
            self.clear_turn = ['medium', 'right', 'left']  
            self.mycard = 20
            self.leftcard = 17
            self.rightcard = 17
        elif K == self.rightid:
            self.who_turn = [(950, 390), (100, 390), (570, 410)]
            self.clear_turn = ['right', 'left', 'medium']
            self.mycard = 17
            self.leftcard = 17
            self.rightcard = 20
        elif K == self.leftid:
            self.who_turn = [(100, 390), (570, 410), (950, 390)]
            self.clear_turn = ['left', 'medium', 'right']
            self.mycard = 17
            self.leftcard = 20
            self.rightcard = 17

def recvMsg():
    while True:
        try:
            data = s.recv(1024)
        except:
            continue
        else:
            json_parse(data)


# alarmchange
def draw_alarm(surface, time, pos):
    surface.blit(my_img.alarmimg, who_turn[0])
    time_left = my_img.time_font.render(str(time), True, (0, 0, 0))
    surface.blit(time_left, (who_turn[0][0]+19, who_turn[0][1]+20))


# 创建一个窗口
screen = pygame.display.set_mode((1100, 730), 0, 32)

# 设置窗口标题
pygame.display.set_caption("hello,world!")


count = threading.Thread(target=countdown, args=())
count.start()


####
# 画其他人的牌
do_not_show_yaobuqi_l=0

def draw_play_l_pokers(screen, pokers, x, y):
    global do_not_show_yaobuqi_l
    if do_not_show_yaobuqi_l == 1 and len(pokers) == 0:
        screen.blit(my_img.img_yaobuqi, (x - 40, y + 50))
        return
    width = 38
    for i in range(len(pokers)):
        img = card[pokers[i]]
        img = pygame.transform.scale(img.image, (57, 78))
        screen.blit(img, (math.floor(x + i * width * 0.5), math.floor(y)))


do_not_show_yaobuqi_r = 0
def draw_play_r_pokers(screen, pokers,x, y):
    global do_not_show_yaobuqi_r
    if do_not_show_yaobuqi_r == 1 and len(pokers) == 0:
        screen.blit(my_img.img_yaobuqi, (x - 57, y+50))
        return
    width = 38
    x -= (len(pokers) * width * 0.5 + width - width * 0.5)
    for i in range(len(pokers)):
        img = card[pokers[i]]
        img = pygame.transform.scale(img.image, (57, 78))
        screen.blit(img, (math.floor(x + i * width * 0.5), math.floor(y)))

def draw_mul(screen):
    global mul
    img_lord=pygame.image.load('../times/mul'+str(mul)+'.png')
    img=pygame.transform.smoothscale(img_lord,(144,42))
    screen.blit(img,(935,650))

def draw_kingwin(screen):
    screen.blit(my_img.img_k_win, (400, 300))

def draw_farmerwin(screen):
    screen.blit(my_img.img_f_win, (350, 100))

def draw_player_gamming(screen, left):
    x0, y0 = 100, 478  # 我的头像坐标
    x1, y1 = 10, 280  # play1 左上
    x2, y2 = 979, 280  # play2 右上
    if myself.king == myself.myid:
        screen.blit(my_img.img_landlord, (x0, y0))
        screen.blit(my_img.img_farmer, (x1, y1))
        screen.blit(pygame.transform.flip(my_img.img_farmer, True, False), (x2, y2))
    elif myself.king == myself.leftid:
        screen.blit(my_img.img_farmer, (x0, y0))
        screen.blit(my_img.img_landlord, (x1, y1))
        screen.blit(pygame.transform.flip(my_img.img_farmer, True, False), (x2, y2))
    else:
        screen.blit(my_img.img_farmer, (x0, y0))
        screen.blit(my_img.img_farmer, (x1, y1))
        screen.blit(pygame.transform.flip(my_img.img_landlord, True, False), (x2, y2))

    img_left1 = my_img.my_font.render(str(left[0]), True, (255, 0, 0))
    img_left2 = my_img.my_font.render(str(left[1]), True, (255, 0, 0))

    screen.blit(my_img.img_left_bg, (x1 + 20, y1 - 120))
    rect_left1 = img_left1.get_rect()
    screen.blit(img_left1, (
    x1 + 20 + my_img.rect_bg.width / 2 - rect_left1.width / 2, y1 - 120 + my_img.rect_bg.height / 2 - rect_left1.height / 2))

    screen.blit(my_img.img_left_bg, (x2 + 30, y2 - 120))
    rect_left2 = img_left2.get_rect()
    screen.blit(img_left2, (
    x2 + 30 + my_img.rect_bg.width / 2 - rect_left2.width / 2, y2 - 120 + my_img.rect_bg.height / 2 - rect_left2.height / 2))



def draw_player_asking(screen):
    x0, y0 = 100, 478  # 我的头像坐标
    x1, y1 = 10, 280  # play1 左上
    x2, y2 = 979, 280  # play2 右上

    screen.blit(my_img.img_photo, (x0, y0))
    screen.blit(my_img.img_photo, (x1, y1))
    screen.blit(pygame.transform.flip(my_img.img_photo, True, False), (x2, y2))

def come():
    try:
        rid=int(e.get())
        json = {
            'Status': 200,
            'Operation': 'come_in',
            'rid':rid
            }
        s.sendall(str.encode(str(json)))
        data = s.recv(1024)
        da=eval(data)
        if da['text'] == 'OK':
            root.destroy()
            threading.Thread(target=recvMsg, args=()).start()
            game=1
        else:
            showinfo(title='提示', message='房间人数已满')
    except:
        showinfo(title='错误', message='请输入整数')
            
            
        
# 游戏主循环
game = 0
card = {}
card_dizhu_add = {}
buttons = {}
# alarmchange

bgt = threading.Thread(target=bgmusic, args=())
bgt.setDaemon(True)
bgt.start()

while True:
    del buttons
    buttons={}
    butt_press = None
    screen.blit(my_img.background, (0, 0))
    if game == 0:
        buttons = my_img.button_0
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                exit()
            if event.type == MOUSEBUTTONUP and event.button == 1:
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        butt_press = button_name
                        break
        for button in buttons.values():
            button.render(screen)
        if butt_press is not None:
            if butt_press == "exit":
                json = {
                    'Status': 200,
                    'Operation': 'rand_in'
                    }
                s.sendall(str.encode(str(json)))
                threading.Thread(target=recvMsg, args=()).start()
                game = 1
            elif butt_press == "quick":
                root=Tk()
                e=Entry(root)
                e.pack()
                b=Button(root,text="进入",command=come)
                b.pack()
                root.mainloop()
            elif butt_press == "start":
                json = {
                    'Status': 200,
                    'Operation': 'creat_room'
                    }
                s.sendall(str.encode(str(json)))
                data = s.recv(1024)
                da=eval(data)
                threading.Thread(target=recvMsg, args=()).start()
                root = Tk()
                root.withdraw()
                showinfo(title='提示', message='创建的房间号是'+str(da['rid']))
                root.destroy()
                game = 1
    elif game == 1:
        buttons = my_img.button_1
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                json = {
                    'Status': 200,
                    'Operation': 'quit',
                    'message': 1
                    }
                s.sendall(str.encode(str(json)))
                s.close()
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONUP and event.button == 1:
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        butt_press = button_name
                        break
        for button in buttons.values():
            button.render(screen)
        if butt_press is not None:
            if butt_press == 'ready':
                json = {
                    'Status': 200,
                    'Operation': 'ready',
                    'message': 1
                    }
                s.sendall(str.encode(str(json)))
                for i in range(54):
                    card[i + 1] = CARD(i + 1)
                game = 2
    # 准备就绪
    elif game == 2:
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                pass
        screen.blit(my_img.readypic, (185, 65))
    # 叫地主
    elif game == 3:
        draw_player_asking(screen)
        buttons = my_img.button_3
        num = 17
        card_x0 = 340
        card_x1 = 851
        for c in mycards:
            if c > 0:
                card[c].draw(card_x0, card[c].y, screen)
                card_x0 += 30
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                pass
            if event.type == MOUSEBUTTONUP and event.button == 1:
                print(event.pos)
                if card_x0 < event.pos[0] < card_x1 and 520 < event.pos[1] < 658:
                    print('test')
                    which_card = int((event.pos[0] - card_x0) / 30)
                    if (which_card >= num):
                        which_card = num - 1
                    shot = card[mycards[which_card]].check(event.pos[1], shot)
                else:
                    for button_name, button in buttons.items():
                        if button.is_over(event.pos):
                            butt_press = button_name
                            break
        if select_king_flag == 1:
            for button in buttons.values():
                button.render(screen)
        else:
            butt_press = None
        # timechange
        if all_time==1 and select_king_flag:
            butt_press = 'notcall'
        
        if butt_press is not None:
            print(butt_press)
            if butt_press == 'calllord':
                json = {
                    'Status': 200,
                    'Operation': 'AnsS',
                    'message': 1
                }
                s.sendall(str.encode(str(json)))
                select_king_flag = 0
                whois = 1
                sound.qiangS.play()
            elif butt_press == 'notcall':
                json = {
                    'Status': 200,
                    'Operation': 'AnsS',
                    'message': 0
                }
                s.sendall(str.encode(str(json)))
                select_king_flag = 0
                whois = 1
                sound.buqiangS.play()
        if whois:
            x=who_turn.pop(0)
            y = clear_turn.pop(0)
            who_turn.append(x)
            clear_turn.append(y)
            whois = 0
            all_time = 20
            del x

        if len(who_turn):
            # alarmchange
            draw_alarm(screen, all_time, who_turn[0])
            # screen.blit(my_img.alarmimg, who_turn[0])

    elif game == 4:
        draw_play_l_pokers(screen, left, 250, 265)
        draw_play_r_pokers(screen, right, 800, 265)
        draw_player_gamming(screen, [leftnum, rightnum])
        draw_mul(screen)
        buttons = my_img.button_4

        num = len(mycards)
        card_x0 = (600 - num * 30) / 2 + 250
        card_x1 = 596 + num * 15

        card_x3 = 475
        for p in dizhu_cards_add:  # 地主加的牌
            card[p].draw(card_x3, 0, screen)
            card_x3 += 50
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                pass
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if card_x0 < event.pos[0] < card_x1 and 520 < event.pos[1] < 658:
                    which_card = int((event.pos[0] - card_x0) / 30)
                    if (which_card >= num):
                        which_card = num - 1
                    shot = card[mycards[which_card]].check(event.pos[1], shot)

                else:
                    for button_name, button in buttons.items():
                        if button.is_over(event.pos):
                            butt_press = button_name
                            break
        # timechange
        if turn and all_time == 0:
            if T != 'init':
                butt_press = "pass"
            else:
                for c in shot:
                    card[c].position = False
                    card[c].y = 550
                shot = []
                shot = card[mycards[0]].check(600, shot)
                butt_press = "shot"
    
        if turn:
            for button in buttons.values():
                button.render(screen)
        else:
            butt_press = None
            shot_x = (600 - len(myshot) * 30) / 2 + 250
            for i in myshot:
                card[i].draw(shot_x, 370, screen)
                shot_x += 30

        if butt_press is not None:
            if butt_press == "pass" and T != 'init':
                hint_flag = 0
                whois = 1
                json = {
                    'Status': 200,
                    'Operation': 'AnsTurn',
                    'type': '',
                    'id': myself.myid,
                    'seq_num': 0,
                    'message': '',
                    'value': 0
                }
                json['type'] = 'Jump'
                sound.buyaoS.play()
                s.sendall(str.encode(str(json)))
                for c in shot:
                    card[c].position = False
                    card[c].y = 550
                shot = []
                myshot = []
                turn = 0

            elif butt_press == "hint":
                for c in shot:
                    card[c].position = False
                    card[c].y = 550
                if not hint_flag:
                    shot = rule.cards_above(mycards,last_cards)
                    hint_flag = 1
                else:
                    shot=rule.cards_above(mycards,hint_cards)
                hint_cards = shot
                print(mycards)
                print(last_cards)
                print(shot)
                if shot == []:
                    hint_flag = 0
                else:
                    for c in shot:
                        card[c].position = True
                        card[c].y = 520    

            elif butt_press == "shot" and len(shot) > 0:
                hint_flag = 0
                json = {
                    'Status': 200,
                    'Operation': 'AnsTurn',
                    'type': '',
                    'id': myself.myid,
                    'seq_num': 0,
                    'message': '',
                    'value': 0
                }
                res = card_Analyse(shot)
                if T == 'init':
                    if res[0] != "" and res[2] > 0:
                        json['type'] = res[0]
                        json['value'] = res[1]
                        json['seq_num'] = res[2]
                        if len(mycards) - len(shot) == 0:
                            json['Operation'] = 'Clear'
                        json['message'] = sorted(shot)
                        s.sendall(str.encode(str(json)))
                        turn = 0
                        sound.cardAnaSound(json)

                elif res[0] != 'bomb' and res[0] != T:
                    print("类型不符")
                elif res[0] != 'bomb' and res[1] <= V:
                    print("点数不够大")
                else:
                    json['type'] = res[0]
                    json['value'] = res[1]
                    json['seq_num'] = res[2]
                    if len(mycards) - len(shot) == 0:
                        json['Operation'] = 'Clear'
                    json['message'] = sorted(shot)
                    s.sendall(str.encode(str(json)))
                    turn = 0
                    #播放音频
                    sound.cardAnaSound(json)

                if not turn:
                    whois = 1
                    for i in shot:
                        mycards.remove(i)
                    myshot = sorted(shot)
                    shot = []
        for c in mycards:
            if c > 0:
                card[c].draw(card_x0, card[c].y, screen)
                card_x0 += 30
        if whois:
            x=who_turn.pop(0)
            y = clear_turn.pop(0)
            who_turn.append(x)
            clear_turn.append(y)
            print(who_turn)
            print(clear_turn)
            whois = 0
            all_time = 20
            del x

        if len(who_turn):
            # alarmchange
            draw_alarm(screen, all_time, who_turn[0])
            # screen.blit(my_img.alarmimg, who_turn[0])
            if (clear_turn[0] == 'left'):
                do_not_show_yaobuqi_l = 0
                left = []
            elif (clear_turn[0] == 'right'):
                do_not_show_yaobuqi_r = 0
                right = []
    elif game==5:
        draw_mul(screen)
        if(kingwin==1):draw_kingwin(screen)
        else:draw_farmerwin(screen)
        buttons = my_img.button_5
        for event in pygame.event.get():
            if event.type == QUIT:
                
                # 接收到退出时间后退出程序
                pass
            if event.type == MOUSEBUTTONUP and event.button == 1:
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        butt_press = button_name
                        break
        for button in buttons.values():
            button.render(screen)
        if butt_press is not None:
            if butt_press == 'ok':
                game = 1
    pygame.display.update()
