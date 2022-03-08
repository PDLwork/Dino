import pygame
import sys
import os

#获取当前文件的目录，方便在别的电脑运行时读取相应文件
Current_path = os.path.join(os.getcwd(), 'pygame', 'dragon', 'picture')
Current_path = Current_path.replace('\\', '/')

pygame.init()  # 初始化pygame
size = width, height = 734, 286  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
clock = pygame.time.Clock() #创建一个时间对象用于控制游戏运作的快慢

background = pygame.image.load(Current_path + '/background1.png')  # 加载图片
backgroundrect = background.get_rect()  # 获取矩形区域

dragon1 = pygame.image.load(Current_path + '/dragon1.png')
dragon2 = pygame.image.load(Current_path + '/dragon2.png')
dragonrect = dragon1.get_rect()
dragonrect = dragonrect.move(50,210)    #将小恐龙移动到“地上”

flag = True #创建一个flag标志用于在循环中判断使用哪张图片
while True:  # 死循环确保窗口一直显示
    clock.tick(6)
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
            sys.exit()  #将窗口关闭

    screen.blit(background, backgroundrect)  # 将背景图片画到窗口上

    #根据flag标志确定显示的图片，这样可以造成小恐龙在跑的现象
    if flag == True:
        screen.blit(dragon1, dragonrect)
    else:
        screen.blit(dragon2, dragonrect)
    flag = not flag

    pygame.display.flip()  # 更新全部显示