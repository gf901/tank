import pygame
import sys
import random
import time
from first_map import create_map1
from second_map import create_map2


# 屏幕尺寸
SCREEN_WIDTH = 910
SCREEN_HEIGHT = 680
#　背景色
COLOR_BLACK = pygame.color.Color(0, 0, 0)
# 敌方tank数量
ENEMY_COUNT = 10
# p1初始位置
P1_BORN_X = SCREEN_WIDTH/2 - 180
P1_BORN_Y = SCREEN_HEIGHT - 60
# p2初始位置
P2_BORN_X = SCREEN_WIDTH/2 + 120
P2_BORN_Y = SCREEN_HEIGHT - 60
# 我方初始生命值
HP = 3


# 坦克父类
class BaseTank:
    def __init__(self, x, y):
        # 图片集
        self.image_dict = {
            "U": pygame.image.load("img/p1tankU.gif"),
            "D": pygame.image.load("img/p1tankD.gif"),
            "R": pygame.image.load("img/p1tankR.gif"),
            "L": pygame.image.load("img/p1tankL.gif")
        }
        self.born_images = [
            pygame.image.load("img/born1.gif"),
            pygame.image.load("img/born2.gif"),
            pygame.image.load("img/born3.gif"),
            pygame.image.load("img/born4.gif")
        ]
        # 当前方向
        self.direction = "U"
        # 当前图片
        self.image = self.image_dict[self.direction]
        # 移动速度
        self.speed = 5
        # 生存状态
        self.live = True
        # 图片区域
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_born = 0
        self.born_step = 10
        self.born_num = 0

    # 展示出生
    def display_born(self, x, y):
        if self.live:
            if not self.is_born:
                if self.born_step > 0:
                    self.born_step -= 1
                else:
                    MainGame.window.blit(self.born_images[self.born_num], (x, y))
                    self.born_num += 1
                    self.born_step = 10
            if self.born_num == len(self.born_images):
                self.is_born = 1
                self.born_step = 0
                self.born_num = 0

    # 绘制tank
    def display_tank(self):
        if self.is_born:
            # 根据tank方向设置图片
            self.image = self.image_dict[self.direction]
            MainGame.window.blit(self.image, self.rect)
        else:
            self.display_born(self.rect.x, self.rect.y)

    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        if self.direction == "U":
            if self.rect.y > 0:
                self.rect.y -= self.speed
        elif self.direction == "D":
            if self.rect.y + self.rect.height < SCREEN_HEIGHT:
                self.rect.y += self.speed
        elif self.direction == "R":
            if self.rect.x + self.rect.width < SCREEN_WIDTH:
                self.rect.x += self.speed
        elif self.direction == "L":
            if self.rect.x > 0:
                self.rect.x -= self.speed

    # 坐标还原
    def stay(self):
        self.rect.x = self.oldx
        self.rect.y = self.oldy
        if isinstance(self, EnemyTank):
            direction_list = ["U", "D", "R", "L"]
            direction_list.remove(self.direction)
            self.direction = random.choice(direction_list)

    # 坦克撞墙
    def hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
                return True
        for water in MainGame.water_list:
            if pygame.sprite.collide_rect(self, water):
                self.stay()

    # 发射子弹
    def fire(self):
        return Bullet(self, "img/tankmissile.gif")


# 我方坦克类
class MyTank(BaseTank):
    def __init__(self, x, y, player=1):
        super(MyTank, self).__init__(x, y)
        if player == 1:
            self.image_dict = {
                "U": pygame.image.load("img/p1tankU.gif"),
                "D": pygame.image.load("img/p1tankD.gif"),
                "R": pygame.image.load("img/p1tankR.gif"),
                "L": pygame.image.load("img/p1tankL.gif")
            }
        elif player == 2:
            self.image_dict = {
                "U": pygame.image.load("img/p2tankU.gif"),
                "D": pygame.image.load("img/p2tankD.gif"),
                "R": pygame.image.load("img/p2tankR.gif"),
                "L": pygame.image.load("img/p2tankL.gif")
            }
        self.bullet_list = []
        self.hp = HP
        self.shot_enemy = 0
        self.is_hit = False
        self.oldx = self.rect.x
        self.oldy = self.rect.y - self.rect.height * 2
        self.my_bullet_create_speed = 10
        self.player = player

    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        if self.is_born:
            key_list = pygame.key.get_pressed()
            if self.player == 1:
                if key_list[pygame.K_w]:
                    self.direction = "U"
                    super().move()
                elif key_list[pygame.K_s]:
                    self.direction = "D"
                    super().move()
                elif key_list[pygame.K_d]:
                    self.direction = "R"
                    super().move()
                elif key_list[pygame.K_a]:
                    self.direction = "L"
                    super().move()
            elif self.player == 2:
                if key_list[pygame.K_UP]:
                    self.direction = "U"
                    super().move()
                elif key_list[pygame.K_DOWN]:
                    self.direction = "D"
                    super().move()
                elif key_list[pygame.K_RIGHT]:
                    self.direction = "R"
                    super().move()
                elif key_list[pygame.K_LEFT]:
                    self.direction = "L"
                    super().move()

    # 我方坦克撞敌方坦克
    def hit_tank(self):
        for enemy in MainGame.enemy_list:
            if pygame.sprite.collide_rect(self, enemy):
                self.stay()
                enemy.stay()

    # 绘制tank
    def display_tank(self):
        if self.is_born:
            # 根据tank方向设置图片
            self.image = self.image_dict[self.direction]
            MainGame.window.blit(self.image, self.rect)
        else:
            self.display_born(P1_BORN_X, P1_BORN_Y)


# 敌方坦克类
class EnemyTank(BaseTank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bullet_list = []
        self.image_dict = {
            "U": pygame.image.load("img/enemy1U.gif"),
            "D": pygame.image.load("img/enemy1D.gif"),
            "R": pygame.image.load("img/enemy1R.gif"),
            "L": pygame.image.load("img/enemy1L.gif")
        }
        self.direction = random.choice(["D", "R", "L"])
        self.speed = random.randint(4, 6)
        self.step = 50
        self.live = True
        self.oldx = x
        self.oldy = y

    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        if self.is_born:
            if self.step > 0:
                self.enemy_move()
                self.step -= 1
            else:
                direction_list = ["U", "D", "R", "L"]
                direction_list.remove(self.direction)
                self.direction = random.choice(direction_list)
                self.step = random.randint(100, 300)
                self.enemy_move()

    def enemy_move(self):
        if self.direction == "U":
            if self.rect.y > 0:
                self.rect.y -= self.speed
            else:
                self.stay()
        elif self.direction == "D":
            if self.rect.y + self.rect.height < SCREEN_HEIGHT:
                self.rect.y += self.speed
            else:
                self.stay()
        elif self.direction == "R":
            if self.rect.x + self.rect.width < SCREEN_WIDTH:
                self.rect.x += self.speed
            else:
                self.stay()
        elif self.direction == "L":
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.stay()

    def hit_wall(self):
        is_hit = super().hit_wall()
        if is_hit:
            direction_list = ["U", "D", "R", "L"]
            direction_list.remove(self.direction)
            self.direction = random.choice(direction_list)

    def hit_tank(self):
        for enemy in MainGame.enemy_list:
            if enemy == self:
                continue
            if pygame.sprite.collide_rect(self, enemy):
                self.stay()
                enemy.stay()

    def fire(self):
        if self.is_born:
            flag = random.randint(0, 400)
            if 95 < flag < 105:
                bullet = Bullet(self, "img/enemymissile.gif")
                self.bullet_list.append(bullet)


# 子弹类
class Bullet:
    def __init__(self, tank, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.direction = tank.direction
        self.speed = 9
        self.live = True
        if self.direction == "U":
            self.rect.x = tank.rect.x + tank.rect.width/2 - self.rect.width/2
            self.rect.y = tank.rect.y - self.rect.height
        elif self.direction == "D":
            self.rect.x = tank.rect.x + tank.rect.width/2 - self.rect.width/2
            self.rect.y = tank.rect.y + tank.rect.height
        elif self.direction == "R":
            self.rect.x = tank.rect.x + tank.rect.width
            self.rect.y = tank.rect.y + tank.rect.height/2 - self.rect.height/2
        elif self.direction == "L":
            self.rect.x = tank.rect.x - self.rect.width
            self.rect.y = tank.rect.y + tank.rect.height/2 - self.rect.height/2

    def display_bullet(self):
        MainGame.window.blit(self.image, self.rect)

    def move(self):
        if self.direction == "U":
            self.rect.y -= self.speed
        elif self.direction == "D":
            self.rect.y += self.speed
        elif self.direction == "R":
            self.rect.x += self.speed
        elif self.direction == "L":
            self.rect.x -= self.speed
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.live = False

    def hit_tank(self, tank):
        if tank.is_born and tank.live:
            if pygame.sprite.collide_rect(self, tank):
                MainGame.bomb_list.append(Bomb(tank.rect))
                self.live = False
                if isinstance(tank, MyTank):
                    tank.hp -= 1
                    if tank.hp < 1:
                        tank.live = False
                else:
                    tank.live = False
                return 1

    def hit_boss(self):
        if pygame.sprite.collide_rect(self, MainGame.boss):
            MainGame.boss.live = 0

    def hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.live = False
                if wall.type == 1:
                    wall.live = False
                    MainGame.wall_list.remove(wall)


# 爆炸类
class Bomb:
    def __init__(self, rect):
        self.image_list = [
            pygame.image.load("img/blast0.gif"),
            pygame.image.load("img/blast1.gif"),
            pygame.image.load("img/blast2.gif"),
            pygame.image.load("img/blast3.gif"),
            pygame.image.load("img/blast4.gif"),
            pygame.image.load("img/blast5.gif"),
            pygame.image.load("img/blast6.gif"),
            pygame.image.load("img/blast7.gif")
        ]
        self.rect = rect
        self.live = True
        self.step = 1
        self.img_num = 0

    def display_bomb(self):
        if self.live:
            if self.step > 0:
                self.step -= 1
            else:
                MainGame.window.blit(self.image_list[self.img_num], self.rect)
                self.img_num += 1
                self.step = 1
            if self.img_num == len(self.image_list):
                self.live = False


# 墙壁类
class Wall:
    def __init__(self,img, x, y, type):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = True
        self.type = type


# Boss类
class Boss:
    def __init__(self,img, x, y):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = 1


# 主逻辑类
class MainGame:
    window = None
    enemy_list = []
    my_list = [None, None]
    player_count = 1
    is_choice = 0
    bomb_list = []
    wall_list = []
    water_list = []
    enemy_count = 0
    step = 500
    boss = None
    game_num = 2
    this_num = 1
    this_pass = 1
    is_defeat = 0

    # 事件处理
    def deal_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game_over("Game Over!")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    MainGame.player_count = 1
                    self.create_my_tank()
                    self.start_game()
                elif event.key == pygame.K_2:
                    MainGame.player_count = 2
                    self.create_my_tank()
                    self.create_my_tank2()
                    self.start_game()


    # 创建地图
    def create_map(self):
        # 创建老窝
        MainGame.boss = Boss("img/boss.gif", SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 60)
        if MainGame.this_num == 1:
            create_map1(MainGame)
        else:
            MainGame.wall_list.clear()
            create_map2(MainGame)

    # 加载地图
    def load_map(self):
        MainGame.window.blit(MainGame.boss.image, MainGame.boss.rect)
        for wall in MainGame.wall_list:
            if wall.live:
                MainGame.window.blit(wall.image, wall.rect)
        for water in MainGame.water_list:
            MainGame.window.blit(water.image, water.rect)

    # 选择玩家
    def choice_player(self):
        # 创建游戏窗口
        MainGame.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        while 1:
            self.show_font("kaiti", 50, "按数字键选择：", (248, 156, 73), (SCREEN_WIDTH / 2-120, SCREEN_HEIGHT/2-150))
            self.show_font("kaiti", 50, "1.单人游戏", (248, 156, 73), (SCREEN_WIDTH / 2-90, SCREEN_HEIGHT/2-100))
            self.show_font("kaiti", 50, "2.双人游戏", (248, 156, 73), (SCREEN_WIDTH / 2-90, SCREEN_HEIGHT/2-50))
            self.show_font("kaiti", 30, "p1:移动：w s a d  射击：space(空格)", (248, 156, 73), (SCREEN_WIDTH / 2-200, SCREEN_HEIGHT/2+50))
            self.show_font("kaiti", 30, "p2:移动：↑ ↓ ← →  射击：L", (248, 156, 73), (SCREEN_WIDTH / 2-200, SCREEN_HEIGHT/2+80))
            self.deal_events()
            pygame.display.update()

    # 创建我方P1 tank
    def create_my_tank(self):
        flag = 0
        p1 = MyTank(P1_BORN_X, P1_BORN_Y, 1)
        MainGame.my_list[0] = p1
        for enemy in MainGame.enemy_list:
            if pygame.sprite.collide_rect(MainGame.my_list[0], enemy):
                flag = 1
        if flag == 1:
            MainGame.my_list[0].rect.y -= MainGame.my_list[0].rect.height

    # 创建我方p2 tank
    def create_my_tank2(self):
        flag = 0
        p2 = MyTank(P2_BORN_X, P2_BORN_Y, 2)
        MainGame.my_list[1] = p2
        for enemy in MainGame.enemy_list:
            if pygame.sprite.collide_rect(MainGame.my_list[1], enemy):
                flag = 1
        if flag == 1:
            MainGame.my_list[1].rect.y -= MainGame.my_list[1].rect.height

    # 加载我方tank
    def load_my_tank(self):
        for i in range(MainGame.player_count):
            if MainGame.my_list[i].live:
                MainGame.my_list[i].display_tank()
                MainGame.my_list[i].move()
                MainGame.my_list[i].hit_wall()
                MainGame.my_list[i].hit_tank()

    # 展示文本信息
    def show_font(self, font, size, content, color, location):
        # 输入的数字，调用pygame的文字方法
        pygame.font.init()  # 文字初始化
        # 给出指定字体，字号
        font = pygame.font.SysFont(font, size)
        # 给出要输入的内容，抗锯齿，颜色
        sf = font.render(content, True, color)
        MainGame.window.blit(sf, location)

    # 展示我方信息
    def show_my_info(self):
        # 展示剩余tank数
        left_enmy = ENEMY_COUNT-MainGame.my_list[0].shot_enemy
        if MainGame.player_count == 2:
            left_enmy -= MainGame.my_list[1].shot_enemy

            # 展示p2生命值
            self.show_font("kaiti", 30, "生命值:{}".format(MainGame.my_list[1].hp), (248, 156, 73), (SCREEN_WIDTH-120, 620))
            # 展示p2杀敌数
            self.show_font("kaiti", 30, "杀敌数:{}".format(MainGame.my_list[1].shot_enemy), (248, 156, 73), (SCREEN_WIDTH-120, 650))

        self.show_font("kaiti", 30, "剩余tank数:{}".format(left_enmy)
                       , (248, 156, 73), (SCREEN_WIDTH/2 - 70, 0))
        # 展示p1生命值
        self.show_font("kaiti", 30, "生命值:{}".format(MainGame.my_list[0].hp), (248, 156, 73), (0, 620))
        # 展示p1杀敌数
        self.show_font("kaiti", 30, "杀敌数:{}".format(MainGame.my_list[0].shot_enemy), (248, 156, 73), (0, 650))

    # 创建敌方tank
    def create_enemy_tank(self, enemy_create_speed):
        if enemy_create_speed > 100:
            flag = 0
            # 已生成敌方tank数小于敌方tank总数
            if MainGame.enemy_count < ENEMY_COUNT:
                new_enemy = EnemyTank(random.randint(0, SCREEN_WIDTH-60), 0)
                for enemy in MainGame.enemy_list:
                    if pygame.sprite.collide_rect(new_enemy, enemy):
                        flag = 1
                for water in MainGame.water_list:
                    if pygame.sprite.collide_rect(new_enemy, water):
                        flag = 1
                if not pygame.sprite.collide_rect(new_enemy, MainGame.my_list[0]) and flag == 0:
                    MainGame.enemy_list.append(new_enemy)
                    MainGame.enemy_count += 1

    # 加载敌方tank
    def load_enemy_tank(self):
        for e in MainGame.enemy_list:
            if e.live == True:
                e.display_tank()
                e.move()
                e.hit_wall()
                e.hit_tank()
                e.fire()

    # 创建我方子弹
    def create_my_bullet(self):
        for i in range(MainGame.player_count):
            if MainGame.my_list[i].my_bullet_create_speed < 0:
                if MainGame.my_list[i].is_born and MainGame.my_list[i].live:
                    key_list = pygame.key.get_pressed()
                    if MainGame.my_list[i].player == 1:
                        if key_list[pygame.K_SPACE]:
                            bullet = MainGame.my_list[i].fire()
                            MainGame.my_list[i].bullet_list.append(bullet)
                            MainGame.my_list[i].my_bullet_create_speed = 20
                    elif MainGame.my_list[i].player == 2:
                        if key_list[pygame.K_l]:
                            bullet = MainGame.my_list[i].fire()
                            MainGame.my_list[i].bullet_list.append(bullet)
                            MainGame.my_list[i].my_bullet_create_speed = 20
            else:
                MainGame.my_list[i].my_bullet_create_speed -= 1

    # 加载我方子弹
    def load_my_bullet(self):
        for i in range(MainGame.player_count):
            for bullet in MainGame.my_list[i].bullet_list:
                if bullet.live:
                    # 绘制子弹
                    bullet.display_bullet()
                    # 子弹移动
                    bullet.move()
                    # 碰撞检测
                    bullet.hit_wall()
                    bullet.hit_boss()
                    for tank in MainGame.enemy_list:
                        f = bullet.hit_tank(tank)
                        if f:
                            # 杀敌数加1
                            MainGame.my_list[i].shot_enemy += 1
                            # 移除敌方tank
                            MainGame.enemy_list.remove(tank)

    # 加载敌方子弹
    def load_enemy_bullet(self):
        # 遍历敌方tank列表
        for enemy in MainGame.enemy_list:
            # 遍历敌方tank字典列表
            for bullet in enemy.bullet_list:
                # 子弹存活时
                if bullet.live:
                    # 绘制子弹
                    bullet.display_bullet()
                    # 子弹移动
                    bullet.move()
                    #碰撞检测
                    bullet.hit_wall()
                    bullet.hit_boss()
                    is_hit = bullet.hit_tank(MainGame.my_list[0])
                    if is_hit:
                        MainGame.my_list[0].is_hit = 1
                        MainGame.my_list[0].is_born = 0
                        MainGame.my_list[0].direction = "U"
                    if MainGame.player_count == 2:
                        is_hit = bullet.hit_tank(MainGame.my_list[1])
                        if is_hit:
                            MainGame.my_list[1].is_hit = 1
                            MainGame.my_list[1].is_born = 0
                            MainGame.my_list[1].direction = "U"

    # 加载爆炸特效
    def load_bomb(self):
        for bomb in MainGame.bomb_list:
            if bomb.live:
                bomb.display_bomb()
            else:
                MainGame.bomb_list.remove(bomb)

    # 被击中时，重置我方tank位置
    def reset_my_location(self):
        for i in range(MainGame.player_count):
            if MainGame.my_list[i].is_born == 1:
                # 被击中时
                if MainGame.my_list[i].is_hit:
                    if i == 0:
                        MainGame.my_list[i].rect.x = P1_BORN_X
                        MainGame.my_list[i].rect.y = P1_BORN_Y
                    elif i == 1:
                        MainGame.my_list[i].rect.x = P2_BORN_X
                        MainGame.my_list[i].rect.y = P2_BORN_Y
                    MainGame.my_list[i].is_hit = False

    # 下一关
    def next_game(self):
        self.show_font("kaiti", 70, "第{}关".format(MainGame.this_num),
                       (248, 156, 73), (SCREEN_WIDTH/2-70, SCREEN_HEIGHT/2-35))

    # 胜利
    def victory(self):
        self.show_font("kaiti", 70, "You are WIN!",
                       (248, 156, 73), (SCREEN_WIDTH/2-210, SCREEN_HEIGHT/2-35))

    # 失败
    def defeat(self):
        self.show_font("kaiti", 70, "You are LOSE!",
                       (248, 156, 73), (SCREEN_WIDTH/2-210, SCREEN_HEIGHT/2-35))

    # 显示关卡
    def show_game_num(self):
        MainGame.step -= 1
        self.next_game()
        if MainGame.step < 0:
            MainGame.step = 1000
            MainGame.this_pass = 0

    # 死亡
    def die(self):
        MainGame.step -= 1
        MainGame.is_defeat = 1
        self.defeat()
        if MainGame.step < 0:
            self.game_over("You are die!")

    # 开始游戏
    def start_game(self):
        global ENEMY_COUNT
        # # 创建游戏窗口
        # MainGame.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # # 选择玩家
        # self.choice_player()
        # # 创建我方tank
        # self.create_my_tank()

        # MainGame.player_count = 2
        # self.create_my_tank()
        # self.create_my_tank2()
        # 创建地图
        self.create_map()
        # 控制敌方tank生成速度
        enemy_create_speed = 80
        while True:
            # 修改背景色
            MainGame.window.fill(COLOR_BLACK)
            # Game Over
            if MainGame.boss.live == 0:
                self.die()
            elif not MainGame.my_list[0].live and not MainGame.my_list[1]:
                self.die()
            elif not MainGame.my_list[0].live and MainGame.my_list[1]:
                if not MainGame.my_list[1].live:
                    self.die()
            if not MainGame.is_defeat:
                # 显示关卡
                if MainGame.this_pass and MainGame.this_num <= MainGame.game_num:
                    self.show_game_num()
                # 下一关
                elif MainGame.this_num < MainGame.game_num and MainGame.enemy_count == ENEMY_COUNT and len(MainGame.enemy_list) == 0:
                    MainGame.step -= 1
                    MainGame.this_num += 1
                    MainGame.this_pass = 1
                    MainGame.enemy_count = 0
                    for i in range(MainGame.player_count):
                        if i == 0:
                            MainGame.my_list[i].rect.x = P1_BORN_X
                            MainGame.my_list[i].rect.y = P1_BORN_Y
                        else:
                            MainGame.my_list[i].rect.x = P2_BORN_X
                            MainGame.my_list[i].rect.y = P2_BORN_Y
                        MainGame.my_list[i].direction = "U"
                        MainGame.my_list[i].is_born = 0
                        MainGame.my_list[i].shot_enemy = 0
                        MainGame.my_list[i].bullet_list.clear()
                        MainGame.bomb_list.clear()
                        self.create_map()
                        ENEMY_COUNT += 5
                # 胜利
                elif MainGame.this_num >= MainGame.game_num and MainGame.enemy_count == ENEMY_COUNT and len(MainGame.enemy_list) == 0:
                    MainGame.step -= 1
                    self.victory()
                    if MainGame.step < 0:
                        self.game_over("You are win!")
                else:
                    # 事件处理
                    self.deal_events()
                    # 加载地图
                    self.load_map()
                    # 加载我方tank
                    self.load_my_tank()
                    # 展示生命值
                    self.show_my_info()
                    # 创建敌方tank
                    self.create_enemy_tank(enemy_create_speed)
                    # 加载敌方tank
                    self.load_enemy_tank()
                    # 创建我方子弹
                    self.create_my_bullet()
                    # 加载我方子弹
                    self.load_my_bullet()
                    # 加载敌方子弹
                    self.load_enemy_bullet()
                    # 加载爆炸特效
                    self.load_bomb()
                    # 重置我方tank位置
                    self.reset_my_location()
                    time.sleep(0.015)
                    enemy_create_speed += MainGame.this_num
                    if enemy_create_speed > 102:
                        enemy_create_speed = 1
            # 刷新窗口
            pygame.display.update()

    # 结束游戏
    def game_over(self, content):
        print(content)
        print("Game Stop!")
        sys.exit()


if __name__ == '__main__':
    game = MainGame()
    game.choice_player()
