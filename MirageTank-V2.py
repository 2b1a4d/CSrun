# -*- coding: utf-8 -*-
import tkinter
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageEnhance
#导入里图
def input_below():
    global below
    below = Image.open(askopenfilename())
#导入表图
def input_adove():
    global above
    above = Image.open(askopenfilename())
#两图均先去色并设置为RGBA模式，大小以里图为准
def process():
    global below
    global above
    below = below.convert("L")
    below = below.convert('RGBA')
    below = ImageEnhance.Brightness(below).enhance(0.6)
    above = above.convert("L")
    above = above.convert('RGBA')
    above = ImageEnhance.Brightness(above).enhance(1.2)
    above = above.resize(below.size)
    max_x, max_y = below.size
    #遍历整个图
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            #很明显大家都喜欢调整红色通道
            P_above = above.getpixel((x , y))[0]
            P_below = below.getpixel((x , y))[0]
            #获取幻影坦克的色彩值与透明度
            alpha = 255 - P_above + P_below
            P_MirageTank = P_below * 255 // alpha
            below.putpixel((x , y),(P_MirageTank,P_MirageTank,P_MirageTank,alpha))
    #保存里图为png格式
    below.save(str(asksaveasfilename())+".png")
#GUI界面
window = tkinter.Tk()
window.title("PC端盟军战车工厂")
window.minsize(500,300)
input_1 = tkinter.Button(window,text = "输入里图",width = 10,height = 2,command = input_below)
input_1.place(x=50,y=50)
input_2 = tkinter.Button(window,text = "输入表图",width = 10,height = 2,command = input_adove)
input_2.place(x=150,y=50)
output = tkinter.Button(window,text = "输出坦克",width = 10,height = 2,command = process)
output.place(x=250,y=50)
window.mainloop()