import pygame
import sys
import os

#获取当前文件的目录，方便在别的电脑运行时读取相应文件
Current_path = os.path.join(os.getcwd(), 'picture')
Current_path = Current_path.replace('\\', '/')

pygame.init()  # 初始化pygame
size = width, height = 734, 286  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
clock = pygame.time.Clock() #创建一个时间对象用于控制游戏运作的快慢

background1 = pygame.image.load(Current_path + '/background1.png')  # 加载图片
background2 = pygame.image.load(Current_path + '/background2.png')  # 加载图片
backgroundrect1 = background1.get_rect()  # 获取矩形区域
backgroundrect2 = background2.get_rect()  # 获取矩形区域
backgroundrect2[0] = backgroundrect1.right

dragon1 = pygame.image.load(Current_path + '/dragon1.png')
dragon2 = pygame.image.load(Current_path + '/dragon2.png')
dragonrect = dragon1.get_rect()
dragonrect = dragonrect.move(50, 210)    #将小恐龙移动到“地上”

flag = True #创建一个flag标志用于在循环中判断使用哪张图片
while True:  # 死循环确保窗口一直显示
    clock.tick(6)
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
            sys.exit()  #将窗口关闭

    screen.blit(background1, backgroundrect1)  # 将背景图片画到窗口上
    screen.blit(background2, backgroundrect2)

    #根据flag标志确定显示的图片，这样可以造成小恐龙在跑的现象
    if flag == True:
        screen.blit(dragon1, dragonrect)
    else:
        screen.blit(dragon2, dragonrect)
    flag = not flag

    backgroundrect1 = backgroundrect1.move(-10, 0)    #将背景向左移动
    backgroundrect2 = backgroundrect2.move(-10, 0)    #将背景向左移动
    if backgroundrect1.right < 0:   #判断第一个背景框如果移动到了窗口外面
        backgroundrect1[0] = backgroundrect2.right  #将第一个背景框移动到第二个背景框后面，形成循环
    if backgroundrect2.right < 0:   #和上面同理，最终实现的效果就是两个图片排着队从窗口前划过
        backgroundrect2[0] = backgroundrect1.right

    pygame.display.flip()  # 更新全部显示