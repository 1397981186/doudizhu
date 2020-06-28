import pygame
pygame.mixer.init()
qiangS = pygame.mixer.Sound('../sound/Rob1.ogg')
buqiangS = pygame.mixer.Sound('../sound/NoRob.ogg')
buyaoS = pygame.mixer.Sound('../sound/buyao4.ogg')
single3 = pygame.mixer.Sound('../sound/1.ogg')
single4 = pygame.mixer.Sound('../sound/2.ogg')
single5 = pygame.mixer.Sound('../sound/3.ogg')
single6 = pygame.mixer.Sound('../sound/4.ogg')
single7 = pygame.mixer.Sound('../sound/5.ogg')
single8 = pygame.mixer.Sound('../sound/6.ogg')
single9 = pygame.mixer.Sound('../sound/7.ogg')
single10 = pygame.mixer.Sound('../sound/8.ogg')
singleJ = pygame.mixer.Sound('../sound/9.ogg')
singleQ = pygame.mixer.Sound('../sound/10.ogg')
singleK = pygame.mixer.Sound('../sound/11.ogg')
singleA = pygame.mixer.Sound('../sound/12.ogg')
single2 = pygame.mixer.Sound('../sound/13.ogg')
singlew = pygame.mixer.Sound('../sound/14.ogg')
singleW = pygame.mixer.Sound('../sound/15.ogg')
pair3 = pygame.mixer.Sound('../sound/dui1.ogg')
pair4 = pygame.mixer.Sound('../sound/dui2.ogg')
pair5 = pygame.mixer.Sound('../sound/dui3.ogg')
pair6 = pygame.mixer.Sound('../sound/dui4.ogg')
pair7 = pygame.mixer.Sound('../sound/dui5.ogg')
pair8 = pygame.mixer.Sound('../sound/dui6.ogg')
pair9 = pygame.mixer.Sound('../sound/dui7.ogg')
pair10 = pygame.mixer.Sound('../sound/dui8.ogg')
pairJ = pygame.mixer.Sound('../sound/dui9.ogg')
pairQ = pygame.mixer.Sound('../sound/dui10.ogg')
pairK = pygame.mixer.Sound('../sound/dui11.ogg')
pairA = pygame.mixer.Sound('../sound/dui12.ogg')
pair2 = pygame.mixer.Sound('../sound/dui13.ogg')

trio3 = pygame.mixer.Sound('../sound/tuple1.ogg')
trio4 = pygame.mixer.Sound('../sound/tuple2.ogg')
trio5 = pygame.mixer.Sound('../sound/tuple3.ogg')
trio6 = pygame.mixer.Sound('../sound/tuple4.ogg')
trio7 = pygame.mixer.Sound('../sound/tuple5.ogg')
trio8 = pygame.mixer.Sound('../sound/tuple6.ogg')
trio9 = pygame.mixer.Sound('../sound/tuple7.ogg')
trio10 = pygame.mixer.Sound('../sound/tuple8.ogg')
trioJ = pygame.mixer.Sound('../sound/tuple9.ogg')
trioQ = pygame.mixer.Sound('../sound/tuple10.ogg')
trioK = pygame.mixer.Sound('../sound/tuple11.ogg')
trioA = pygame.mixer.Sound('../sound/tuple12.ogg')
trio2 = pygame.mixer.Sound('../sound/tuple13.ogg')

wangzha = pygame.mixer.Sound('../sound/wangzha.ogg')
zhadan = pygame.mixer.Sound('../sound/zhadan.ogg')
triosingle = pygame.mixer.Sound('../sound/sandaiyi.ogg')
triopair = pygame.mixer.Sound('../sound/sandaiyidui.ogg')

seqsingle = pygame.mixer.Sound('../sound/shunzi.ogg')
seqpair = pygame.mixer.Sound('../sound/liandui.ogg')
seq_trio = pygame.mixer.Sound('../sound/feiji.ogg')

def cardAnaSound(re):
    # 单张
    if re['type'] == "single":
        if re['value'] == 0:
            single3.play()
        elif re['value'] == 1:
            single4.play()
        elif re['value'] == 2:
            single5.play()
        elif re['value'] == 3:
            single6.play()
        elif re['value'] == 4:
            single7.play()
        elif re['value'] == 5:
            single8.play()
        elif re['value'] == 6:
            single9.play()
        elif re['value'] == 7:
            single10.play()
        elif re['value'] == 8:
            singleJ.play()
        elif re['value'] == 9:
            singleQ.play()
        elif re['value'] == 10:
            singleK.play()
        elif re['value'] == 11:
            singleA.play()
        elif re['value'] == 12:
            single2.play()
        elif re['value'] == 13:
            singlew.play()
        elif re['value'] == 14:
            singleW.play()
    # 对子
    elif re['type'] == "pair":
        if re['value'] == 0:
            pair3.play()
        elif re['value'] == 1:
            pair4.play()
        elif re['value'] == 2:
            pair5.play()
        elif re['value'] == 3:
            pair6.play()
        elif re['value'] == 4:
            pair7.play()
        elif re['value'] == 5:
            pair8.play()
        elif re['value'] == 6:
            pair9.play()
        elif re['value'] == 7:
            pair10.play()
        elif re['value'] == 8:
            pairJ.play()
        elif re['value'] == 9:
            pairQ.play()
        elif re['value'] == 10:
            pairK.play()
        elif re['value'] == 11:
            pairA.play()
        elif re['value'] == 12:
            pair2.play()
    # 三张
    elif re['type'] == "trio":
        if re['value'] == 0:
            trio3.play()
        elif re['value'] == 1:
            trio4.play()
        elif re['value'] == 2:
            trio5.play()
        elif re['value'] == 3:
            trio6.play()
        elif re['value'] == 4:
            trio7.play()
        elif re['value'] == 5:
            trio8.play()
        elif re['value'] == 6:
            trio9.play()
        elif re['value'] == 7:
            trio10.play()
        elif re['value'] == 8:
            trioJ.play()
        elif re['value'] == 9:
            trioQ.play()
        elif re['value'] == 10:
            trioK.play()
        elif re['value'] == 11:
            trioA.play()
        elif re['value'] == 12:
            trio2.play()
    # 炸弹
    elif re['type'] == "bomb":
        if re['value'] == 13:
            wangzha.play()
        else:
            zhadan.play()
    # 三带一
    elif re['type'] == "trio_single":
        triosingle.play()
    elif re['type'] == "trio_pair":
        triopair.play()
    elif re['type'] == "seq_pair3" or re['type'] == "seq_pair4"\
        or re['type'] == "seq_pair5" or re['type'] == "seq_pair6"\
            or re['type'] == "seq_pair7" or re['type'] == "seq_pair8"\
                or re['type'] == "seq_pair9" or re['type'] == "seq_pair10"\
                    or re['type'] == "seq_pair11" or re['type'] == "seq_pair12":
                    seqpair.play()
    elif re['type'] == "seq_single5" or re['type'] == "seq_single6"\
        or re['type'] == "seq_single7" or re['type'] == "seq_single8"\
            or re['type'] == "seq_single9" or re['type'] == "seq_single10"\
                or re['type'] == "seq_single11" or re['type'] == "seq_single12":
                seqsingle.play()
    elif re['type'] == "seq_trio2" or re['type'] == "seq_trio3"\
        or re['type'] == "seq_trio4" or re['type'] == "seq_trio5"\
            or re['type'] == "seq_trio6" or re['type'] == "seq_trio_pair2"\
                or re['type'] == "seq_trio_pair3" or re['type'] == "seq_trio_pair4"\
                    or re['type'] == "seq_trio_pair5" or re['type'] == "seq_trio_single2"\
                        or re['type'] == "seq_trio_single3" or re['type'] == "seq_trio_single4"\
                            or re['type'] == "seq_trio_single5":
            seq_trio.play()
