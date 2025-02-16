# -*- coding: utf-8 -*-
import tkinter
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from PIL import Image
#先感谢一下大佬https://zhuanlan.zhihu.com/p/33148445
#底图 = below,表图 = above
def input_below():
    global below
    below = Image.open(askopenfilename())
#导入底图与表图
def input_adove():
    global above
    above = Image.open(askopenfilename())
#两图均先去色并设置为RGBA模式，大小以底图为准
def process():
    global below
    global above
    below = below.convert("L")
    below = below.convert('RGBA')
    above = above.convert("L")
    above = above.convert('RGBA')
    above = above.resize(below.size)
    max_x, max_y = below.size
    #遍历整个底图
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            #很明显大家都喜欢调整红色通道
            R_below = below.getpixel((x, y))[0]
            below.putpixel((x, y), (255, 255, 255, R_below))
            #处理底图的（奇数，奇数）点（偶数，偶数）点
            if x % 2 == 1:
                if y % 2 == 1:
                    below.putpixel((x, y), (0, 0, 0, 0))
            else:
                if y % 2 == 0:
                    below.putpixel((x, y), (0, 0, 0, 0))
    #遍历整个表图
    x = -1
    y = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1

            R_above = above.getpixel((x, y))[0]
            above.putpixel((x, y), (0, 0, 0, 255 - R_above))
            # 处理表图的（偶数，奇数）点（奇数，偶数）点
            if x % 2 == 0:
                if y % 2 == 1:
                    above.putpixel((x, y), (0, 0, 0, 0))
            else:
                if y % 2 == 0:
                    above.putpixel((x, y), (0, 0, 0, 0))

    x = -1
    y = -1

    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            # 用表图对应点处理底图的（奇数，奇数）点（偶数，偶数）点
            if x % 2 == 1:
                if y % 2 == 1:
                    below.putpixel((x, y), above.getpixel((x, y)))
            else:
                if y % 2 == 0:
                    below.putpixel((x, y), above.getpixel((x, y)))
    #保存底图为png格式
    below.save(str(asksaveasfilename())+".png")
#GUI界面
window = tkinter.Tk()
window.title("PC端盟军战车工厂")
window.minsize(500,300)
input_1 = tkinter.Button(window,text = "输入底图",width = 10,height = 2,command = input_below)
input_1.place(x=50,y=50)
input_2 = tkinter.Button(window,text = "输入表图",width = 10,height = 2,command = input_adove)
input_2.place(x=150,y=50)
output = tkinter.Button(window,text = "输出坦克",width = 10,height = 2,command = process)
output.place(x=250,y=50)
window.mainloop()