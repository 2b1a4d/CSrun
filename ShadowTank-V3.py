# -*- coding: utf-8 -*
# GUI库
import tkinter
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
# 图像处理库
from PIL import Image
# 整数转字节
import struct

"""主要函数"""
# 导入里物
def input_below():
    global below
    global suffix
    global size
    name = askopenfilename()
    below = open(name, "rb")
    below = below.read()
    # 获取文件后缀及大小
    suffix = name[-4:]
    size = len(below)

# 导入表图
def input_above():
    global above
    above = Image.open(askopenfilename())
    above = above.convert("RGBA")

# 导出坦克
def encrypt():
    global below
    global suffix
    global size
    global above
    # 依文件大小重设图片大小
    origin_x, origin_y = above.size
    if origin_x * origin_y <= size+2:
        variety = ((size+2) - (origin_x * origin_y)) // (origin_x+origin_y)+1
        above = above.resize((origin_x+variety, origin_y+variety))
    max_x, max_y = above.size
    # 遍历整个图片并填充字节
    x = -1
    y = -1
    num = -1
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            if  num+1 != size:
                num += 1
                in_byte = below[num]
                P = above.getpixel((x,y))
                above.putpixel((x,y),en_turn(P,in_byte))
            else:
                break
    # 在倒数第一个像素填充文件大小
    above.putpixel((max_x-1, max_y-1),size_rgab(size))
    # 在倒数第二个像素填充文件后缀
    above.putpixel((max_x-2, max_y-1),suffix_rgba(suffix))
    above.save(asksaveasfilename()+".png")

# 导入坦克
def input_tank():
    global tank
    tank = Image.open(askopenfilename())
    tank = tank.convert("RGBA")

# 导出里物
def decrypt():
    global tank
    max_x, max_y = tank.size
    # 获取文件大小
    R,G,B,A = tank.getpixel((max_x-1, max_y-1))
    size = R*256**3+G*256**2+B*256+A
    # 获取文件后缀名
    suffix = rgba_suffix(tank.getpixel((max_x-2, max_y-1)))
    # 选取文件存储位置并命名
    below = open(asksaveasfilename(title = '保存文件')+suffix,'wb')
    # 遍历整个图片并取出字节
    x = -1
    y = -1
    num = 0
    while x < max_x - 1:
        x += 1
        y = -1
        while y < max_y - 1:
            y += 1
            if num != size:
                num += 1
                out_byte = de_turn(tank.getpixel((x,y)))
                out_byte = struct.pack('B',out_byte)
                below.write(out_byte)
            else:
                break

"""辅助函数"""
# 将值存于表图的像素后两位
def en_turn(P_truple,value):
    R = P_truple[0]//4*4 + value//64
    G = P_truple[1]//4*4 + (value-value//64*64)//16
    B = P_truple[2]//4*4 + (value-value//16*16)//4
    A = P_truple[3]//4*4 + value%4
    return (R,G,B,A)

# 提取像素四元的后两位
def de_turn(P_truple):
    value = P_truple[0]%4 *64 + P_truple[1]%4 *16 + P_truple[2]%4 *4 + P_truple[3]%4
    return value

# 将文件后缀名存于像素中
def suffix_rgba(suffix):
    R = ord(suffix[0])
    G = ord(suffix[1])
    B = ord(suffix[2])
    A = ord(suffix[3])
    return (R,G,B,A)

# 提取像素中的文件后缀名
def rgba_suffix(P_truple):
    suffix = chr(P_truple[0])+chr(P_truple[1])+chr(P_truple[2])+chr(P_truple[3])
    if  '.' in suffix:
        return suffix
    else:
        suffix = '.' + suffix
        return suffix

# 将文件大小存于像素中
def size_rgab(size):
    R = size // 256**3
    G = (size - size//256**3 * 256**3) // 256**2
    B = (size - size//256**2 * 256**2) // 256
    A = size % 256
    return (R,G,B,A)

"""GUI界面"""
window = tkinter.Tk()
window.title("PC端厄普西隆战车工厂")
window.minsize(500, 300)
input_1 = tkinter.Button(window, text="导入里物", width=10, height=2, command=input_below)
input_1.place(x=50, y=25)
input_2 = tkinter.Button(window, text="导入表图", width=10, height=2, command=input_above)
input_2.place(x=50, y=100)
output = tkinter.Button(window, text="导出坦克", width=10, height=2, command=encrypt)
output.place(x=50, y=175)
output = tkinter.Button(window, text="导入坦克", width=10, height=2, command=input_tank)
output.place(x=300, y=25)
output = tkinter.Button(window, text="导出里物", width=10, height=2, command=decrypt)
output.place(x=300, y=100)
window.mainloop()
