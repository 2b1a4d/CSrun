# -*- coding: utf-8 -*-
import tkinter
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from PIL import Image
#导入里图
def input_below():
    global below
    below = Image.open(askopenfilename())
#导入表图
def input_adove():
    global above
    above = Image.open(askopenfilename())
#导入魔影坦克
def input_tank():
    global tank
    tank = Image.open(askopenfilename())
#对图片编码
def encode():
    global key
    tank = Image.open(askopenfilename())
    max_x, max_y = tank.size
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            R,G,B,A = tank.getpixel((x,y))
            NR = R//4*4 + int(key[R%4])
            NG = G//4*4 + int(key[G%4])
            NB = B//4*4 + int(key[B%4])
            NA = A//4*4 + int(key[A%4])
            tank.putpixel((x,y),(NR,NG,NB,NA))
    tank.save(asksaveasfilename() + ".png")
#对图片解码
def decode():
    global key
    tank = Image.open(askopenfilename())
    max_x, max_y = tank.size
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            R,G,B,A = tank.getpixel((x,y))
            NR = R//4*4 + key.index(str(R%4))
            NG = G//4*4 + key.index(str(G%4))
            NB = B//4*4 + key.index(str(B%4))
            NA = A//4*4 + key.index(str(A%4))
            tank.putpixel((x, y), (NR, NG, NB, NA))
    tank.save(asksaveasfilename() + ".png")
#将值存于表图的像素后两位
def en_turn(P_truple,value):
    R = P_truple[0]//4*4 + value//64
    G = P_truple[1]//4*4 + (value-value//64*64)//16
    B = P_truple[2]//4*4 + (value-value//16*16)//4
    A = P_truple[3]//4*4 + value%4
    return (R,G,B,A)
#提取像素四元的后两位
def de_turn(P_truple):
    V = P_truple[0]%4 *64 + P_truple[1]%4 *16 + P_truple[2]%4 *4 + P_truple[3]%4
    return V
#处理为魔影坦克
def encrypt():
    global below
    global above
    below = below.convert("RGBA")
    above = above.convert("RGBA")
    max_x, max_y = below.size
    above = above.resize((max_x*2,max_y*2))
    #遍历整个图
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            #提取里图
            R,G,B,A = below.getpixel((x,y))
            P = above.getpixel((x*2,y*2))
            #第二象限为R第一象限为G第三象限为B第四象限为A
            above.putpixel((x*2,y*2),en_turn(P,R))
            above.putpixel((x*2+1,y*2),en_turn(P,G))
            above.putpixel((x*2,y*2+1),en_turn(P,B))
            above.putpixel((x*2+1,y*2+1),en_turn(P,A))
    #保存里图为png格式
    above.save(asksaveasfilename()+".png")
#解码魔影坦克
def decrypt():
    global tank
    tank = tank.convert("RGBA")
    below = tank
    max_x, max_y = tank.size
    below = below.resize((max_x//2,max_y//2))
    max_x, max_y = below.size
    #遍历坦克
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            #第二象限为R第一象限为G第三象限为B第四象限为A
            R = de_turn(tank.getpixel((x*2,y*2)))
            G = de_turn(tank.getpixel((x*2+1,y*2)))
            B = de_turn(tank.getpixel((x*2,y*2+1)))
            A = de_turn(tank.getpixel((x*2+1,y*2+1)))
            below.putpixel((x,y),(R,G,B,A))
    below.save(asksaveasfilename()+".png")
#GUI相关
def getkey():
    global key
    key = input5.get()
#GUI界面
window = tkinter.Tk()
window.title("PC端厄普西隆战车工厂")
window.minsize(500,300)
input1 = tkinter.Button(window,text = "导入里图",width = 10,height = 2,command = input_below)
input1.place(x=50,y=25)
input2 = tkinter.Button(window,text = "导入表图",width = 10,height = 2,command = input_adove)
input2.place(x=50,y=100)
output1 = tkinter.Button(window,text = "导出坦克",width = 10,height = 2,command = encrypt)
output1.place(x=50,y=175)
input3 = tkinter.Button(window,text = "导入坦克",width = 10,height = 2,command = input_tank)
input3.place(x=200,y=25)
output2 = tkinter.Button(window,text = "导出里图",width = 10,height = 2,command = decrypt)
output2.place(x=200,y=100)
input4 = tkinter.Button(window,text = "编码坦克",width = 10,height = 2,command = encode)
input4.place(x=350,y=25)
output3 = tkinter.Button(window,text = "解码坦克",width = 10,height = 2,command = decode)
output3.place(x=350,y=100)
input5 = tkinter.Spinbox(window,values = ('未选择',"1032","1230","1302","2031","2301","2310","3012","3210","3210"),command = getkey)
input5.place(x=325,y=175)

window.mainloop()