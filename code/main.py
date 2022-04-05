#开发者：庞德霖、谢泉生
import pygame
import sys
import os

#获取当前文件的目录，方便在别的电脑运行时读取相应文件
Current_path = os.path.join(os.getcwd(), 'picture')
Current_path = Current_path.replace('\\', '/')

'''定义一个小恐龙的类'''
class Dragon:
    #小恐龙的默认参数
    def __init__(self):
        self.rectangle = pygame.Rect(50, 210, 40, 45)    #小恐龙的边框,预先设计好就不需要移动到地上
        #定义小恐龙的两种状态(读取图片放在列表里)
        self.status = [
            pygame.image.load(Current_path + '/dragon1.png'),
            pygame.image.load(Current_path + '/dragon2.png')
        ]
        self.Y_axis = 210    #小恐龙所在Y轴坐标
        self.jump_flag = False   #跳跃标志，判断小恐龙是否跳跃
        self.jump_speed = 0  #小恐龙的跳跃速度，当为正的时候上升，为负的时候下降
        self.alive = True    #生命状态，默认为活着
        self.jump_permission = True #小恐龙的跳跃权限，如果在空中时不给跳跃

    #更新小恐龙的状态
    def dragon_update(self):
        if self.jump_flag:   #如果检测到按下跳跃
            self.jump_speed = 10 #将上升速度调为10
            self.jump_permission = False     #跳跃期间不给小恐龙再次跳跃
            self.jump_flag = False   #设置好后回复默认值等待下次跳跃
        if self.jump_speed != 0:   #如果小恐龙的跳跃速度不为0，说明正在跳跃周期
            self.Y_axis -= self.jump_speed    #移动小恐龙的Y坐标
            if self.Y_axis > 210:    #防止将小恐龙移动到地下
                self.Y_axis = 210
                self.jump_permission = True  #回到地上，允许跳跃
            self.rectangle[1] = self.Y_axis   #将框真正移动
        if self.jump_permission == False:    #如果此时不允许跳跃，即正在跳跃过程中
            self.jump_speed -= 1 #将速度降低，效果为上升越来越慢，下降越来越快

pygame.init()  # 初始化pygame
size = width, height = 734, 286  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
clock = pygame.time.Clock() #创建一个时间对象用于控制游戏运作的快慢

background1 = pygame.image.load(Current_path + '/background1.png')  # 加载图片
background2 = pygame.image.load(Current_path + '/background2.png')  # 加载图片
backgroundrect1 = background1.get_rect()  # 获取矩形区域
backgroundrect2 = background2.get_rect()  # 获取矩形区域
backgroundrect2[0] = backgroundrect1.right

dragon = Dragon()

# 定义一个更新画面的函数（这样做可能更合理）
flag = True #创建一个flag标志用于在循环中判断使用哪张图片
def map_update():
    '''更新背景'''
    screen.blit(background1, backgroundrect1)  # 将背景图片画到窗口上
    screen.blit(background2, backgroundrect2)

    '''更新小恐龙'''
    global flag
    #根据flag标志确定显示的图片，这样可以造成小恐龙在跑的现象
    if flag == True:
        screen.blit(dragon.status[0], dragon.rectangle)
    else:
        screen.blit(dragon.status[1], dragon.rectangle)
    flag = not flag

while True:  # 死循环确保窗口一直显示
    clock.tick(60)
    dragon_jump = False
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
            sys.exit()  # 将窗口关闭
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if dragon.jump_permission:
                dragon.jump_flag = True

    backgroundrect1 = backgroundrect1.move(-10, 0)    #将背景向左移动
    backgroundrect2 = backgroundrect2.move(-10, 0)    #将背景向左移动
    if backgroundrect1.right < 0:   #判断第一个背景框如果移动到了窗口外面
        backgroundrect1[0] = backgroundrect2.right  #将第一个背景框移动到第二个背景框后面，形成循环
    if backgroundrect2.right < 0:   #和上面同理，最终实现的效果就是两个图片排着队从窗口前划过
        backgroundrect2[0] = backgroundrect1.right

    dragon.dragon_update()
    map_update()

    pygame.display.flip()  # 更新全部显示

if __name__ == "__main__":
    pass