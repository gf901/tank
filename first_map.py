from wall import Wall

SCREEN_WIDTH = 70*13
SCREEN_HEIGHT = 680




def create_map1(MainGame):
    for i in [-1, 0, 1]:
        wall = Wall("img/wall/walls.gif", SCREEN_WIDTH / 2 - 30 + i * 60, SCREEN_HEIGHT - 120, 1)
        MainGame.wall_list.append(wall)
    for i in [-1, 1]:
        wall = Wall("img/wall/walls.gif", SCREEN_WIDTH / 2 - 30 + 60 * i, SCREEN_HEIGHT - 60, 1)
        MainGame.wall_list.append(wall)
    walls_list = []
    list1 = [1, 3, 5, 7, 9, 11]
    list2 = [4, 4, 3, 3, 4, 4]
    list3 = [1, 1, 2.5, 2.5, 1, 1]
    wall1 = Wall("img/wall/wall_net_h.gif", 0, SCREEN_HEIGHT/2, 0)
    wall2 = Wall("img/wall/wall_net_h.gif", SCREEN_WIDTH-60, SCREEN_HEIGHT/2, 0)
    for i in range(2):
        wall = Wall("img/wall/walls.gif", 120+60*i, SCREEN_HEIGHT/2, 1)
        MainGame.wall_list.append(wall)
    for i in range(2):
        wall = Wall("img/wall/walls.gif", SCREEN_WIDTH-240-60*i, SCREEN_HEIGHT/2, 0)
        MainGame.wall_list.append(wall)
    for i in range(6):
        wall_list = create_wall(70 * list1[i], 0, list2[i])
        walls_list.extend(wall_list)
    for i in range(6):
        wall_list = create_wall(70 * list1[i], SCREEN_HEIGHT - 60*4-60*list3[i], 4)
        walls_list.extend(wall_list)
    wall3 = Wall("img/wall/walls_net.gif", 6*70, 120, 0)
    wall4 = Wall("img/wall/walls.gif", SCREEN_WIDTH/2-30, SCREEN_HEIGHT/2+30, 1)
    walls_list.extend([wall1, wall2, wall3, wall4])
    MainGame.wall_list.extend(walls_list)


def create_wall(x, y, n):
    wall_list = []
    for i in range(1, n):
        wall = Wall("img/wall/walls.gif", x , y+60*i, 1)
        wall_list.append(wall)
    return wall_list