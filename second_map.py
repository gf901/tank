from wall import Wall
from water import Water

SCREEN_WIDTH = 70*13
SCREEN_HEIGHT = 680


def create_map2(MainGame):
    for i in [-1, 0, 1]:
        wall = Wall("img/wall/walls.gif", SCREEN_WIDTH / 2 - 30 + i * 60, SCREEN_HEIGHT - 120, 1)
        MainGame.wall_list.append(wall)
    for i in [-1, 1]:
        wall = Wall("img/wall/walls.gif", SCREEN_WIDTH / 2 - 30 + 60 * i, SCREEN_HEIGHT - 60, 1)
        MainGame.wall_list.append(wall)

    MainGame.water_list.extend(create_water_h(0, 60, 1))
    MainGame.water_list.extend(create_water_s(180, 0))
    MainGame.water_list.extend(create_water_h(420, 60, 3))
    MainGame.water_list.extend(create_water_h(240, 60, 1))
    MainGame.water_list.extend(create_water_s(540, 0, 3))
    MainGame.water_list.extend(create_water_s(720, 60))
    MainGame.water_list.extend(create_water_h(720, 60))
    MainGame.water_list.extend(create_water_s(840, 60))
    MainGame.wall_list.append(Wall("img/wall/walls.gif", 120, 120, 1))
    MainGame.water_list.extend(create_water_h(60, 180, 3))
    MainGame.water_list.extend(create_water_h(0, 300))
    MainGame.water_list.extend(create_water_s(180, 240, 3))
    MainGame.water_list.extend(create_water_h(300, 300))
    MainGame.water_list.extend(create_water_h(360, 240, 1))
    MainGame.wall_list.append(Wall("img/wall/walls_net.gif", 360, 180, 0))
    MainGame.wall_list.append(Wall("img/wall/walls.gif", 300, 180, 1))
    MainGame.wall_list.extend(create_wall_h(420, 180))
    MainGame.water_list.extend(create_water_h(480, 240, 5))
    MainGame.wall_list.extend(create_wall_h(780, 240))
    MainGame.water_list.extend(create_water_s(660, 300, 2))
    MainGame.wall_list.extend(create_wall_h(180, 420, 3))
    MainGame.wall_list.extend(create_wall_h(180, 420, 4))
    MainGame.wall_list.append(Wall("img/wall/walls_net.gif", 420, 420, 0))
    MainGame.wall_list.extend(create_wall_h(480, 420, 4))
    MainGame.wall_list.extend(create_wall_s(60, 360, 4))
    MainGame.wall_list.extend(create_wall_s(13*60, 300, 6))


# 创建横向ｎ个water
def create_water_h(x, y, n=2):
    water_list = []
    for i in range(n):
        water = Water(x+60*i, y)
        water_list.append(water)
    return water_list


# 创建竖向ｎ个water
def create_water_s(x, y, n=2):
    wall_list = []
    for i in range(n):
        wall = Water(x, y+60*i)
        wall_list.append(wall)
    return wall_list


# 创建横向ｎ个wall
def create_wall_h(x, y, n=2, image="img/wall/walls.gif", type=1):
    wall_list = []
    for i in range(n):
        wall = Wall(image, x+60*i, y, type)
        wall_list.append(wall)
    return wall_list


# 创建竖向ｎ个wall
def create_wall_s(x, y, n=2, image="img/wall/walls.gif", type=1):
    wall_list = []
    for i in range(n):
        wall = Wall(image, x, y+60*i, type)
        wall_list.append(wall)
    return wall_list
