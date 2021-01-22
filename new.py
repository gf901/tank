import pygame
import random


width = 660
height = 700


class Boss:
    def __init__(self, x, y):
        self.img = pygame.image.load("img/boss.gif")
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = True


class Wall:
    def __init__(self, x, y):
        self.img = pygame.image.load("img/walls(1).gif")
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = True


class Bullet:
    def __init__(self, tank, speed):
        self.img = pygame.image.load("img/tankmissile.gif")
        self.rect = self.img.get_rect()
        self.direction = tank.direction
        self.live = True
        self.speed = speed
        self.is_enemy = False if isinstance(tank, MyTank) else True
        if tank.direction == "U":
            self.rect.x = tank.rect.x + 30 - self.rect.width / 2
            self.rect.y = tank.rect.y + 10
        elif tank.direction == "D":
            self.rect.x = tank.rect.x + 30 - self.rect.width / 2
            self.rect.y = tank.rect.y + 30 + 10
        elif tank.direction == "L":
            self.rect.x = tank.rect.x - 30 - 10
            self.rect.y = tank.rect.y + 30 - self.rect.height / 2
        elif tank.direction == "R":
            self.rect.x = tank.rect.x + 30 + 10
            self.rect.y = tank.rect.y + 30 - self.rect.height / 2

    def move(self):
        if self.direction == "U":
            self.rect.y -= self.speed
        elif self.direction == "D":
            self.rect.y += self.speed
        elif self.direction == "L":
            self.rect.x -= self.speed
        elif self.direction == "R":
            self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            self.live = False

    def check_hit_wall(self, wall):
        if wall.live and pygame.sprite.collide_rect(self, wall):
            self.live = False
            wall.live = False

    def check_hit_tank(self, tank):
        if tank.live and pygame.sprite.collide_rect(self, tank):
            if not self.is_enemy and isinstance(tank, EnemyTank):
                tank.live = False
                self.live = False
            elif self.is_enemy and isinstance(tank, MyTank):
                pygame.quit()

    def check_hit_boss(self, boss):
        if boss.live and pygame.sprite.collide_rect(self, boss):
            pygame.quit()


class MyTank:
    def __init__(self, x, y, direction):
        self.images = {
            "U": "img/p1tankU.gif",
            "D": "img/p1tankD.gif",
            "R": "img/p1tankR.gif",
            "L": "img/p1tankL.gif",
        }
        self.direction = direction
        self.img = pygame.image.load(self.images[self.direction])
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.oldx = x
        self.oldy = y
        self.live = True
        self.speed = 4
        self.fire_limit = 20
        self.bullet_list = []

    def move(self, direction):
        self.direction = direction
        self.img = pygame.image.load(self.images[self.direction])
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        if direction == "U":
            if self.rect.y > 0:
                self.rect.y -= self.speed
        elif direction == "D":
            if self.rect.y < height - 60:
                self.rect.y += self.speed
        elif direction == "L":
            if self.rect.x > 0:

                self.rect.x -= self.speed
        elif direction == "R":
            if self.rect.x < width - 60:
                self.rect.x += self.speed

    def check_hit_wall(self, wall):
        if wall.live and pygame.sprite.collide_rect(self, wall):
            self.rect.x = self.oldx
            self.rect.y = self.oldy

    def fire(self):
        if self.fire_limit < 0:
            bullet = Bullet(self, 5)
            self.bullet_list.append(bullet)
            self.fire_limit = 20


class EnemyTank:
    def __init__(self, x, y, direction):
        self.images = {
            "U": "img/p1tankU.gif",
            "D": "img/p1tankD.gif",
            "R": "img/p1tankR.gif",
            "L": "img/p1tankL.gif",
        }
        self.direction = direction
        self.img = pygame.image.load(self.images[self.direction])
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.oldx = x
        self.oldy = y
        self.live = True
        self.speed = 1
        self.fire_limit = 80
        self.bullet_list = []
        self.change_direction_rate = 200

    def move(self):
        self.img = pygame.image.load(self.images[self.direction])
        self.oldx = self.rect.x
        self.oldy = self.rect.y
        if self.direction == "U":
            if self.rect.y > 0:
                self.rect.y -= self.speed
        elif self.direction == "D":
            if self.rect.y < height - 60:
                self.rect.y += self.speed
        elif self.direction == "L":
            if self.rect.x > 0:
                self.rect.x -= self.speed
        elif self.direction == "R":
            if self.rect.x < width - 60:
                self.rect.x += self.speed

    def check(self, wall_list):
        for wall in wall_list:
            if wall.live and pygame.sprite.collide_rect(self, wall):
                direction_list = ["U", "D", "R", "L"]
                direction_list.remove(self.direction)
                self.direction = random.choice(direction_list)
        if self.rect.y <= 0 or self.rect.y >= height - 60 or self.rect.x <= 0 or self.rect.x >= width - 60 or self.change_direction_rate <= 0:
            direction_list = ["U", "D", "R", "L"]
            direction_list.remove(self.direction)
            self.direction = random.choice(direction_list)
            self.change_direction_rate = random.randint(200, 500)
        self.change_direction_rate -= 1
        self.fire_limit -= 1

    def fire(self):
        if self.fire_limit < 0:
            bullet = Bullet(self, 3)
            self.bullet_list.append(bullet)
            self.fire_limit = 80


def start():

    enemy_gen_limit = 100
    eneym_list = []

    screen = pygame.display.set_mode((width, height))
    wall_list = []

    boss = Boss(width / 2 - 30, height - 60)
    wall = Wall(width / 2 - 30, height - 60 * 2)
    wall_list.append(wall)
    wall = Wall(width / 2 - 30 - 60, height - 60 * 2)
    wall_list.append(wall)
    wall = Wall(width / 2 - 30 + 60, height - 60 * 2)
    wall_list.append(wall)
    wall = Wall(width / 2 - 30 - 60, height - 60)
    wall_list.append(wall)
    wall = Wall(width / 2 - 30 + 60, height - 60)
    wall_list.append(wall)

    p1 = MyTank(width / 2 - 30 - 60 * 2 - 10, height - 60, "U")

    for i in range(11):
        wall = Wall(0 + 60 * i, 300)
        wall_list.append(wall)

    clock = pygame.time.Clock()
    while True:
        clock.tick(100)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()

        screen.fill(pygame.color.Color(0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == 1:
            p1.move("U")
        if keys[pygame.K_DOWN] == 1:
            p1.move("D")
        if keys[pygame.K_LEFT] == 1:
            p1.move("L")
        if keys[pygame.K_RIGHT] == 1:
            p1.move("R")
        if keys[pygame.K_SPACE] == 1:
            p1.fire()

        screen.blit(boss.img, boss.rect)

        for wall in wall_list:
            if wall.live:
                screen.blit(wall.img, wall.rect)

        screen.blit(p1.img, p1.rect)
        for bullet in p1.bullet_list:
            if bullet.live:
                screen.blit(bullet.img, bullet.rect)
                bullet.move()
                bullet.check_hit_boss(boss)
                for wall in wall_list:
                    if wall.live:
                        bullet.check_hit_wall(wall)
                for enemy in eneym_list:
                    bullet.check_hit_tank(enemy)
        for wall in wall_list:
            p1.check_hit_wall(wall)

        if enemy_gen_limit <= 0 and len(eneym_list) < 10:
            enemy = EnemyTank(random.randint(0, width - 60), 0, random.choice(["D", "L", "R"]))
            eneym_list.append(enemy)
            enemy_gen_limit = 100
        for enemy in eneym_list:
            if enemy.live:
                enemy.check(wall_list)
                enemy.move()
                enemy.fire()
                screen.blit(enemy.img, enemy.rect)
                for bullet in enemy.bullet_list:
                    if bullet.live:
                        screen.blit(bullet.img, bullet.rect)
                        bullet.check_hit_tank(p1)
                        bullet.move()
                        bullet.check_hit_boss(boss)
                        for wall in wall_list:
                            if wall.live:
                                bullet.check_hit_wall(wall)

        p1.fire_limit -= 1
        enemy_gen_limit -= 1

        pygame.display.update()


start()
