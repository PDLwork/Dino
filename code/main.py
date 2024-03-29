import pygame

'''-------------------------------定义一个小恐龙的类-------------------------------'''
class Dragon:
    #实例化的时候需要输入创建的游戏窗口对象
    def __init__(self, Screen):
        #小恐龙的默认参数
        self.screen = Screen
        self.rectangle = pygame.Rect(50, 210, 40, 45)    #小恐龙的边框,预先设计好就不需要移动到地上
        self.status = True #两种状态对应两个图片
        #定义小恐龙的两种状态(读取图片放在列表里)
        self.StatusPicture = [
            pygame.image.load('./picture/dragon1.png'),
            pygame.image.load('./picture/dragon2.png')
        ]
        self.jump_speed = 0  #小恐龙的跳跃速度，当为正的时候上升，为负的时候下降
        self.alive = True    #生命状态
        self.jump_flag = False   #跳跃标志，判断小恐龙是否跳跃
        self.count = 0

    #更新小恐龙的状态
    def update(self):
        #如果当前没有检测到跳跃且小恐龙在地上,轮流显示图片
        if self.jump_flag == False and self.rectangle[1] == 210:
            if self.count % 15 == 0:    #控制小恐龙踏步速度
                self.status = not self.status
            #轮流显示图片，这样可以造成小恐龙在跑的现象
            if self.status:
                screen.blit(self.StatusPicture[0], self.rectangle)
            else:
                screen.blit(self.StatusPicture[1], self.rectangle)
            self.count += 1
            self.count %= 10000  #防止溢出

        #如果检测到按下跳跃并且小恐龙在地上那就判定为有效跳跃
        if self.jump_flag and self.rectangle[1] == 210:
            self.jump_speed = 15 #将上升速度调为15

        #如果小恐龙的跳跃速度不为0，或者当前在空中，说明正在跳跃周期
        if self.jump_speed != 0 or self.rectangle[1] != 210:
            self.rectangle[1] -= self.jump_speed   #将小恐龙框移动
            self.jump_speed -= 1 #将速度降低，效果为上升越来越慢，下降越来越快
            if self.rectangle[1] >= 210:    #防止将小恐龙移动到地下
                #落地后恢复默认值等待下次跳跃
                self.Y_axis = 210
                self.jump_speed = 0
                self.jump_flag = False
            #如果在空中那就显示两个图片，效果就是两个脚都伸直（没有太大意义）
            self.screen.blit(self.StatusPicture[0], self.rectangle)
            self.screen.blit(self.StatusPicture[1], self.rectangle)   

'''-------------------------------定义一个地图的类-------------------------------'''
class Map:
    #实例化的时候需要输入创建的游戏窗口对象
    def __init__(self, Screen):
        self.screen = Screen
        self.speed = 3  #初始速度（像素）
        self.background_1 = pygame.image.load('./picture/background1.png')  # 加载图片
        self.background_2 = pygame.image.load('./picture/background2.png')
        self.background_rectangle_1 = self.background_1.get_rect()    # 获取图片大小的矩形区域
        self.background_rectangle_2 = self.background_2.get_rect()
        self.background_rectangle_2[0] = self.background_rectangle_1.right

    def update(self):
        #移动框
        self.background_rectangle_1 = self.background_rectangle_1.move(-self.speed, 0)
        self.background_rectangle_2 = self.background_rectangle_2.move(-self.speed, 0)

        if self.background_rectangle_1.right < 0:   #判断第一个背景框如果移动到了窗口外面
            self.background_rectangle_1[0] = self.background_rectangle_2.right  #将第一个背景框移动到第二个背景框后面，形成循环
        if self.background_rectangle_2.right < 0:   #和上面同理，最终实现的效果就是两个图片排着队从窗口前划过
            self.background_rectangle_2[0] = self.background_rectangle_1.right

        #将图片放到框里面
        self.screen.blit(self.background_1, self.background_rectangle_1)
        self.screen.blit(self.background_2, self.background_rectangle_2)

#主程序
if __name__ == "__main__":
    "-------------------------------初始化部分-------------------------------"
    pygame.init()  # 初始化pygame
    pygame.display.set_caption('Dino')  #设置窗口标题
    screen = pygame.display.set_mode([734, 286])  # 创建并显示窗口，设置这个大小是因为一张背景图就是这么大
    clock = pygame.time.Clock() #创建一个时间对象用于控制游戏运作的快慢

    map = Map(screen)     #创建地图实例
    dragon = Dragon(screen)   #创建小恐龙实例
    score = 0   #设置初始分数

    "-------------------------------主循环部分-------------------------------"
    running = True
    while running:  # 死循环确保窗口一直显示
        clock.tick(60)      #越大越快
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果程序发现单击关闭窗口按钮
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                dragon.jump_flag = True

        map.update()    #更新地图元素框的位置
        dragon.update()     #更新小恐龙元素框的位置

        #这部分暂时测试用 现在背景的移动速度和时间成正比
        score += 1
        if score % 100 == 0:
            map.speed += 0.5

        pygame.display.flip()  # 更新全部显示

    pygame.quit()