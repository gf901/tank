import pygame
import sys


# 屏幕尺寸
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 680
COLOR_BLACK = pygame.color.Color(0, 0, 0)
# 敌方tank数量
ENEMY_COUNT = 10
# 我方初始生命值
HP = 3


class Boss:
    def __init__(self, x, y):
        self.img = pygame.image.load("img/boss.gif")
        self.live = True
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall:
    def __init__(self, x, y):
        self.img = pygame.image.load("img/wall/walls.gif")
        self.live = True
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet:
    def __init__(self, tank):
        self.img = pygame.image.load("img/tankmissile.gif")
        self.rect = self.img.get_rect()
        self.live = True
        self.speed = 9
        self.is_enemy = False if isinstance(tank, MyTank) else True

        self.direction = tank.direction
        if self.direction == "U":
            self.rect.x = tank.rect.x + tank.rect.width / 2 - self.rect.width / 2
            self.rect.y = tank.rect.y - self.rect.height
        elif self.direction == "D":
            self.rect.x = tank.rect.x + tank.rect.width / 2 - self.rect.width / 2
            self.rect.y = tank.rect.y + tank.rect.height
        elif self.direction == "R":
            self.rect.x = tank.rect.x + tank.rect.width
            self.rect.y = tank.rect.y + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == "L":
            self.rect.x = tank.rect.x - self.rect.width
            self.rect.y = tank.rect.y + tank.rect.height / 2 - self.rect.height / 2

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
        if tank.live:
            if pygame.sprite.collide_rect(self, tank):
                self.live = False
                if self.is_enemy and isinstance(tank, MyTank):
                    tank.hp -= 1
                    if tank.hp < 1:
                        tank.live = False
                elif not self.is_enemy and not isinstance(tank, MyTank):
                    tank.live = False

    def hit_wall(self, wall_list):
        for wall in wall_list:
            if wall.live:
                if pygame.sprite.collide_rect(self, wall):
                    wall.live = False
                    self.live = False

    def hit_boss(self, boss):
        if pygame.sprite.collide_rect(self, boss):
            boss.live = 0


class MyTank:
    def __init__(self, x, y):
        self.img_dict = {
            "U": "img/p1tankU.gif",
            "R": "img/p1tankR.gif",
            "D": "img/p1tankD.gif",
            "L": "img/p1tankL.gif",
        }
        self.direction = "U"
        self.img = pygame.image.load(self.img_dict[self.direction])
        self.live = True
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.oldx = x
        self.oldy = y
        self.hp = HP
        self.bullet_speed = 10

    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y

        key_list = pygame.key.get_pressed()
        if key_list[pygame.K_UP]:
            self.direction = "U"
            if self.rect.y > 0:
                self.rect.y -= self.speed
        elif key_list[pygame.K_DOWN]:
            self.direction = "D"
            if self.rect.y < SCREEN_HEIGHT - 60:
                self.rect.y += self.speed
        elif key_list[pygame.K_LEFT]:
            self.direction = "L"
            if self.rect.x > 0:
                self.rect.x -= self.speed
        elif key_list[pygame.K_RIGHT]:
            self.direction = "R"
            if self.rect.x < SCREEN_WIDTH - 60:
                self.rect.x += self.speed
        self.img = pygame.image.load(self.img_dict[self.direction])

    def hit_wall(self, wall_list):
        for wall in wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.rect.x = self.oldx
                self.rect.y = self.oldy

    def fire(self):

        return Bullet(self)


class MainGame:
    boss = None
    wall_list = []
    enemy_list = []
    bullet_list = []
    p1 = None

    def main(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.init_map()
        clock = pygame.time.Clock()

        while True:
            clock.tick(100)
            event = pygame.event.poll()
            if event == pygame.QUIT:
                pygame.quit()
            screen.fill(COLOR_BLACK)

            self.load_map(screen)
            self.load_tank(screen)
            self.load_bullet(screen)
            pygame.display.update()

    def load_tank(self, screen):
        self.p1.move()
        self.p1.hit_wall(self.wall_list)
        screen.blit(self.p1.img, self.p1.rect)

    def load_bullet(self, screen):
        if self.p1.bullet_speed <= 0:
            key_list = pygame.key.get_pressed()
            if key_list[pygame.K_SPACE]:
                bullet = self.p1.fire()
                self.bullet_list.append(bullet)
            self.p1.bullet_speed = 10
        else:
            self.p1.bullet_speed -= 1

        for bullet in self.bullet_list:
            if bullet.live:
                bullet.move()
                bullet.hit_wall(self.wall_list)
                bullet.hit_boss(self.boss)
                screen.blit(bullet.img, bullet.rect)

        if not self.boss.live:
            self.game_over(screen)

    def init_map(self):
        # boss
        self.boss = Boss(SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 60)
        # tank p1
        self.p1 = MyTank(SCREEN_WIDTH / 2 - 30 - 60 - 60 - 10, SCREEN_HEIGHT - 60)
        # wall
        wall = Wall(SCREEN_WIDTH / 2 - 30 - 60, SCREEN_HEIGHT - 60)
        self.wall_list.append(wall)

        wall = Wall(SCREEN_WIDTH / 2 - 30 - 60, SCREEN_HEIGHT - 120)
        self.wall_list.append(wall)

        wall = Wall(SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 120)
        self.wall_list.append(wall)

        wall = Wall(SCREEN_WIDTH / 2 - 30 + 60, SCREEN_HEIGHT - 120)
        self.wall_list.append(wall)

        wall = Wall(SCREEN_WIDTH / 2 - 30 + 60, SCREEN_HEIGHT - 60)
        self.wall_list.append(wall)

        for i in range(15):
            wall = Wall(i * 60, 200)
            self.wall_list.append(wall)

    def load_map(self, screen):
        screen.blit(self.boss.img, self.boss.rect)
        for wall in self.wall_list:
            if wall.live:
                screen.blit(wall.img, wall.rect)

    def game_over(self, screen):
        sys.exit()

MainGame().main()
