import socket
import json
import random
import threading
import time
import sqlite3
import queue

userSocket=[]
ROOM={}
player_room={}
s = socket.socket()
host = socket.gethostname()
print(host)
port = 12345
s.bind((host,port))
s.listen(60)


def Turner(num):
    if num==0:
        return 1
    if num==1:
        return 2
    if num==2:
        return 0

def send_message(socket,string):
    json={
    'status':200,
    'Operation':'message',
    'Card':[0],
    'message':''
    }
    json['message']=string
    socket.sendall(str.encode(str(json)))


def inform_king(socket,yon):
    json={
    'Status':200,
    'Operation':'InfK',
    'message':yon
    }
    socket.sendall(str.encode(str(json)))
    
def send_id(socket,you_id):
    json={
    'status':200,
    'Operation':'ID',
    'Card':[0],
    'message':0
    }
    json['message']=you_id
    socket.sendall(str.encode(str(json)))




def ask_select(socket):
    json={
    'Status':200,
    'Operation':'AskS'
    }
    socket.sendall(str.encode(str(json)))

def set_turn(socket,Type,value,seq_num,card):
    json={
    'Status':200,
    'Operation':'SetTurn',
    'type':Type,
    'value':value,
    'card':card
    }
    print('sent:type=',Type,' value=',value,' seq_num=',seq_num)
    socket.sendall(str.encode(str(json)))



def json_prase(room,js):
       recjs=eval(js)
       if recjs['Operation']=='AnsS':
              return recjs['message']
       elif recjs['Operation']=='AnsR':
              return recjs['message']
       elif recjs['Operation']=='AnsTurn':
              print(recjs)
              #这里会收到回牌
              if(recjs['type']=='bomb'):room.mul=room.mul*2
              json={
                     'Status':200,
                     'Operation':'Announce',
                     'id':recjs['id'],
                     'message':recjs['message'],
                     'mul':0,
                     'type':recjs['type'],
                     'value':recjs['value']
                     }
              json['mul']=room.mul
              room.mem[0].sendall(str.encode(str(json)))
              room.mem[1].sendall(str.encode(str(json)))
              room.mem[2].sendall(str.encode(str(json)))
              if recjs['type']=='Jump':
                     if room.jumpCounter==1:
                            room.type='init'
                            room.value=0
                            room.seq_num=0
                            room.jumpCounter=0
                            room.card=[]
                     else:
                            room.jumpCounter+=1
              else:
                     room.jumpCounter=0
                     room.card=recjs['message']
                     room.type=recjs['type']
                     room.value=recjs['value']
                     room.seq_num=recjs['seq_num']
              print('JC=',room.jumpCounter)
              time.sleep(0.5)
       elif recjs['Operation']=='Clear':
              json={
                     'Status':200,
                     'Operation':'AGAIN',
                     'id':recjs['id'],
                     'message':'Game over!'
                     }
              room.type = 'init'
              room.value = 0
              room.readynum = 0
              room.seq_num=0
              room.TURN = 0
              room.jumpCounter=0
              room.mem[0].sendall(str.encode(str(json)))
              room.mem[1].sendall(str.encode(str(json)))
              room.mem[2].sendall(str.encode(str(json)))
              return 0
       else:
              print('Unknown json')
              return -1
       return 1

class Room:
       def __init__(self, rid):
              self.rid = rid
              self.TURN = 0
              self.num = 0
              self.readynum = 0
              self.mul=1
              self.Q=queue.Queue()
              self.idorder = []
              self.FLAG=[0,0,0]
              self.mem = []
              self.type = 'init'
              self.card=[]
              self.value = 0
              self.seq_num = 0
              self.jumpCounter = 0
              self.POKER=list(range(1,55))

       def in_room(self,sock):
              if self.num>=3:
                     print('enough')
              else:
                     print(sock)
                     self.mem.append(sock)
                     send_message(sock,'hello!')
                     if self.num==2:
                            time.sleep(1)
                            for c in self.mem:
                                   send_message(c,'Players all connected')
                            time.sleep(1)
                     self.num+=1
       def out_room(self,sock):
           self.num-=1
           self.mem.remove(sock)
       def jiaodizhu(self):
              random.shuffle(self.mem)
              for sc in self.mem:
                     send_id(sc,self.mem.index(sc))
              while True:
                     time.sleep(2)
                     ask_select(self.mem[0])
                     Client_Number = 0  ##收到回应数
                     time.sleep(1)
                     # Waiting for Client 0
                     receive = self.Q.get()
                     if len(receive.strip()) == 0:
                            continue
                     else:
                            self.FLAG[0] = json_prase(self,receive)
                            Client_Number = Client_Number + 1
                            inform_king(self.mem[1],self.FLAG[0])
                            inform_king(self.mem[2],self.FLAG[0])
                     ask_select(self.mem[1])
                     # Waiting for Client 1
                     time.sleep(1)  # 等待buffer
                     receive1 = self.Q.get()
                     if len(receive1.strip()) == 0:
                            continue
                     else:
                            self.FLAG[1] = json_prase(self,receive1)
                            Client_Number = Client_Number + 1
                            inform_king(self.mem[0],self.FLAG[1])
                            inform_king(self.mem[2],self.FLAG[1])
                     # Waiting for Client 2
                     ask_select(self.mem[2])
                     time.sleep(1)
                     receive2 = self.Q.get()
                     if len(receive2.strip()) == 0:
                            continue
                     else:
                            self.FLAG[2] = json_prase(self,receive2)
                            Client_Number = Client_Number + 1
                            inform_king(self.mem[1],self.FLAG[2])
                            inform_king(self.mem[0],self.FLAG[2])
                     if Client_Number == 3:
                            callScorelist = self.FLAG
                            if (callScorelist == [1, 0, 0]):
                                   self.TURN = 0
                            elif (callScorelist == [1, 1, 1] or callScorelist==[1, 0, 1] or callScorelist==[1, 1, 0]):
                                   ask_select(self.mem[0])
                                   time.sleep(1)
                                   receivefinal = self.Q.get()
                                   if len(receivefinal.strip()) == 0:
                                          continue
                                   else:
                                          FLAG4 = json_prase(self,receivefinal)
                                          if FLAG4 == 1:
                                                 self.TURN = 0
                                                 if(callScorelist == [1, 1, 1]): self.mul=8
                                                 else: self.mul=4

                                          else:
                                                 if (callScorelist==[1, 1, 1] or callScorelist==[1, 0, 1]):
                                                        self.TURN = 2
                                                        if(callScorelist == [1, 1, 1]):self.mul=4
                                                        else:self.mul=2
                                                 else:
                                                        self.TURN = 1
                                                        self.mul=2
                            elif (callScorelist == [0, 1, 0]):
                                   self.TURN = 1
                            elif (callScorelist == [0, 1, 1]):
                                   ask_select(self.mem[1])
                                   time.sleep(1)
                                   receivefinal = self.Q.get()
                                   if len(receivefinal.strip()) == 0:
                                          continue
                                   else:
                                          FLAG4 = json_prase(self,receivefinal)
                                          if FLAG4 == 1:
                                                 self.TURN = 1
                                                 self.mul=4
                                          else:
                                                 self.TURN = 2
                                                 self.mul=2
                            elif (callScorelist == [0, 0, 1]):
                                   self.TURN = 2
                            elif (callScorelist == [0, 0, 0]):
                                   self.init_card()
                     json={
                            'status':200,
                            'Operation':'king',
                            'message':'',
                            'card':'',
                            'mul':''
                            }
                     json['message']=self.TURN
                     json['card'] = self.POKER[51:54]
                     json['mul']= self.mul
                     for sc in self.mem:
                            sc.sendall(str.encode(str(json)))
                            time.sleep(1)
                     break

       def init_card(self):
              random.shuffle(self.POKER)
              print(self.POKER)
              json={
                     'status':200,
                     'Operation':'init',
                     'Card':[0],
                     'message':''
                     }
              json['message']=self.POKER[0:17]
              self.mem[0].sendall(str.encode(str(json)))
              json['message']=self.POKER[17:34]
              self.mem[1].sendall(str.encode(str(json)))
              json['message']=self.POKER[34:51]
              self.mem[2].sendall(str.encode(str(json)))
              self.jiaodizhu()

def handle_c(id):
    ROOM[id]=Room(id)
    while True:
        if ROOM[id].readynum==3:
               ROOM[id].init_card()
               while True:
                      TURN=ROOM[id].TURN
                      type=ROOM[id].type
                      value=ROOM[id].value
                      seq_num=ROOM[id].seq_num
                      card=ROOM[id].card
                      set_turn(ROOM[id].mem[TURN], type, value, seq_num,card)
                      receive = ROOM[id].Q.get()
                      a=json_prase(ROOM[id],receive)
                      if not a:
                          ROOM[id].readynum=0
                          break
                      ROOM[id].TURN = Turner(TURN)


def Player(sc):
    while True:
        data=sc.recv(1024)
        if not data:
            break
        da=eval(data)
        if da['Operation'] == 'login':
            u_name=da['p_name']
            pw=da['p_pw']
            conn=sqlite3.connect('doudizhu.db')
            c=conn.cursor()
            try:
                c.execute('''SELECT passward FROM account WHERE name= \''''+u_name+"\'")
                r=c.fetchone()
                if(r[0]==pw):
                    da['text'] = "OK"
                    sc.sendall(str.encode(str(da)))
                else:
                    da['text']="WRONG"
                    sc.sendall(str.encode(str(da)))
                    continue
            except:
                da['text']="WRONG"
                sc.sendall(str.encode(str(da)))
                continue
            conn.close()
        elif da['Operation'] == 'creat_room':
            rid=len(ROOM)
            da['rid']=rid
            sc.sendall(str.encode(str(da)))
            threading.Thread(target=handle_c,args=(rid,)).start()
            ROOM[rid].in_room(sc)
            player_room[sc]=rid
        elif da['Operation'] == 'rand_in':
            flag=1
            for r in ROOM:
                if ROOM[r].num<3:
                    flag=0
                    ROOM[r].in_room(sc)
                    player_room[sc]=r
            if flag:
                rid=len(ROOM)
                threading.Thread(target=handle_c,args=(rid,)).start()
                ROOM[rid].in_room(sc)
                player_room[sc]=rid
        elif da['Operation'] == 'come_in':
            rid=da['rid']
            if ROOM[rid].num<3:
                da['text']="OK"
                ROOM[rid].in_room(sc)
                player_room[sc]=rid
                sc.sendall(str.encode(str(da)))
            else:
                da['text']="ENOUGH"
                sc.sendall(str.encode(str(da)))
        elif da['Operation'] == 'reg':
            u_name=da['p_name']
            pw=da['p_pw']
            conn=sqlite3.connect('doudizhu.db')
            c=conn.cursor()
            try:
                c.execute('''SELECT name FROM account''')
                r=c.fetchone()
                i=1
                for n in r:
                    if u_name==n:
                        da['text']="WRONG"
                        i=0
                if i:
                    da['text']="OK"
                    c.execute("INSERT INTO account VALUES(?,?,?)",[u_name,pw,10])
                    conn.commit()
                sc.sendall(str.encode(str(da)))
            except:
                pass
            conn.close()
        elif da['Operation'] == 'ready':
            ROOM[player_room[sc]].readynum+=1
        elif da['Operation'] == 'cancel_ready':
            ROOM[player_room[sc]].readynum-=1
        elif da['Operation'] == 'quit':
            ROOM[player_room[sc]].out_room(sc)
            del player_room[sc]
            sc.close()
        else:
            ROOM[player_room[sc]].Q.put(data)

while True:
    c, addr = s.accept()
    userSocket.append(c)
    #ROOM[1].in_room(c)
    player=threading.Thread(target=Player,args=(c,))
    player.start()
