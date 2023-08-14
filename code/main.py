import pygame
import sys

'''定义一个小恐龙的类'''
class Dragon:
    #小恐龙的默认参数
    def __init__(self):
        self.rectangle = pygame.Rect(50, 210, 40, 45)    #小恐龙的边框,预先设计好就不需要移动到地上
        #定义小恐龙的两种状态(读取图片放在列表里)
        self.status = [
            pygame.image.load('./picture/dragon1.png'),
            pygame.image.load('./picture/dragon2.png')
        ]
        self.Y_axis = 210    #小恐龙所在Y轴坐标
        self.jump_flag = False   #跳跃标志，判断小恐龙是否跳跃
        self.jump_speed = 0  #小恐龙的跳跃速度，当为正的时候上升，为负的时候下降
        self.alive = True    #生命状态，默认为活着
        self.jump_permission = True #小恐龙的跳跃权限，如果在空中时不给跳跃

    #更新小恐龙的状态
    def update(self):
        if self.jump_flag:   #如果检测到按下跳跃
            self.jump_speed = 15 #将上升速度调为10
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

'''定义一个地图的类'''
class Map:
    #默认参数
    def __init__(self):
        self.speed = 3
        self.background_1 = pygame.image.load('./picture/background1.png')  # 加载图片
        self.background_2 = pygame.image.load('./picture/background2.png')
        self.background_rectangle_1 = self.background_1.get_rect()    # 获取图片大小的矩形区域
        self.background_rectangle_2 = self.background_2.get_rect()
        self.background_rectangle_2[0] = self.background_rectangle_1.right

    def update(self):
        self.background_rectangle_1 = self.background_rectangle_1.move(-self.speed, 0)    #将背景向左移动
        self.background_rectangle_2 = self.background_rectangle_2.move(-self.speed, 0)
        if self.background_rectangle_1.right < 0:   #判断第一个背景框如果移动到了窗口外面
            self.background_rectangle_1[0] = self.background_rectangle_2.right  #将第一个背景框移动到第二个背景框后面，形成循环
        if self.background_rectangle_2.right < 0:   #和上面同理，最终实现的效果就是两个图片排着队从窗口前划过
            self.background_rectangle_2[0] = self.background_rectangle_1.right

# 定义一个更新画面的函数（这样做可能更合理）
flag = True #创建一个flag标志用于在循环中判断使用哪张图片
count = 0
def screen_update(jump_permission):
    '''更新背景'''
    screen.blit(map.background_1, map.background_rectangle_1)  # 将背景图片画到窗口上
    screen.blit(map.background_2, map.background_rectangle_2)

    # bird = pygame.image.load('./picture/bird1.png')
    # bird_rectangle = pygame.Rect(100, 100, 40, 40)
    # screen.blit(bird, bird_rectangle)

    global count
    count += 1
    count %= 100

    if jump_permission:     #这个if语句是实现小恐龙踏步的
        if count % 15 == 0:     #为了控制小恐龙踏步的速度
            '''更新小恐龙'''
            global flag
            #根据flag标志确定显示的图片，这样可以造成小恐龙在跑的现象
            if flag == True:
                screen.blit(dragon.status[0], dragon.rectangle)
            else:
                screen.blit(dragon.status[1], dragon.rectangle)
            flag = not flag
        else:
            if flag == True:
                screen.blit(dragon.status[0], dragon.rectangle)
            else:
                screen.blit(dragon.status[1], dragon.rectangle)
    else:   #如果在空中那就显示两个图片，效果就是两个脚都平行（没有太大意义）
        screen.blit(dragon.status[0], dragon.rectangle)
        screen.blit(dragon.status[1], dragon.rectangle) 

#主程序
if __name__ == "__main__":
    "-------------------------------初始化部分-------------------------------"
    pygame.init()  # 初始化pygame
    screen = pygame.display.set_mode([734, 286])  # 创建并显示窗口
    pygame.display.set_caption('Dino')  #设置窗口标题
    clock = pygame.time.Clock() #创建一个时间对象用于控制游戏运作的快慢

    map = Map()     #创建地图实例
    dragon = Dragon()   #创建小恐龙实例
    score = 0   #设置初始分数

    "-------------------------------主循环部分-------------------------------"
    while True:  # 死循环确保窗口一直显示
        clock.tick(60)      #越大越快
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
                sys.exit()  # 将窗口关闭
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if dragon.jump_permission:  #如果检测到按键按下并且当前允许跳跃
                    dragon.jump_flag = True

        map.update()    #更新地图元素框的位置
        dragon.update()     #更新小恐龙元素框的位置
        screen_update(dragon.jump_permission)   #根据框显示图片

        #这部分暂时测试用 现在背景的移动速度和时间成正比
        score += 1
        if score % 100 == 0:
            map.speed += 0.5

        pygame.display.flip()  # 更新全部显示