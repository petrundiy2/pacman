__author__ = 'Petr'
import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
    pygame.init()
    pygame.display.set_mode((512, 512))
    pygame.display.set_caption('Pacman')


def draw_backgfloor(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size, map_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.tile_size = tile_size
        self.map_size = map_size
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts = []
    num = 2
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, 'C:/Users/Petr/PycharmProjects/pacman/resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()

        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                    self.x = 0
                    self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)

def draw_ghosts(screen):
    for g in Ghost.ghosts:
        g.draw(screen)
def create_ghosts(ts, ms):
    Ghost.ghosts = [Ghost(5, 5, ts, ms) for i in range(Ghost.num)]
def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()
class Point(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, 'C:/Users/Petr/PycharmProjects/pacman/resources/point.png', x, y, tile_size, map_size)
    def game_tick(self):
        super(Point, self).game_tick()

class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, 'C:/Users/Petr/PycharmProjects/pacman/resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
            if is_point(floor(self.x+self.velocity), self.y):
                MAP.map[int(self.y)].pop(floor(self.x+self.velocity))
                MAP.map[int(self.y)].insert(floor(self.x+self.velocity),[])
                self.velocity+=0.03
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
            if is_point(self.x, floor(self.y+self.velocity)):
                MAP.map[floor(self.y+self.velocity)].pop(int(self.x))
                MAP.map[floor(self.y+self.velocity)].insert(int(self.x),[])
                self.velocity+=0.03
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
            if is_point(floor(self.x - self.velocity), self.y):
                MAP.map[int(self.y)].pop(floor(self.x - self.velocity))
                MAP.map[int(self.y)].insert(floor(self.x-self.velocity),[])
                self.velocity+=0.03
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
            if is_point(self.x, floor(self.y - self.velocity)):
                MAP.map[floor(self.y - self.velocity)].pop(int(self.x))
                MAP.map[floor(self.y-self.velocity)].insert(int(self.x),[])
                self.velocity+=0.03
        self.set_coord(self.x, self.y)

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, 'C:/Users/Petr/PycharmProjects/pacman/resources/wall.png', x, y, tile_size, map_size)
    def game_tick(self):
        super(Wall, self).game_tick()

def is_wall(x, y):
    return isinstance(MAP.map[int(y)][int(x)], Wall)
def create_walls(coords, ts, ms):
    Wall.walls = [Wall(2, 4, ts, ms)]

def is_point(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Point)
def create_points(coords, ts, ms):
    Point.points = [Point(2, 4, ts, ms)]

def is_ghost(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Ghost)

class Map:
    def __init__(self, filename, tile_size, map_size):
        self.map = []
        f=open(filename, 'r')
        txt = f.readlines()
        f.close()
        for y in range(len(txt)):
            self.map.append([])
            for x in range(len(txt[y])):
                if txt[y][x] == "#":
                    self.map[-1].append(Wall(x, y, tile_size, map_size))
                elif txt[y][x]=='.':
                    self.map[-1].append(Point(x,y,tile_size, map_size))
                else:
                    self.map[-1].append(None)
        self.tile_size = tile_size
        self.map_size = map_size
    def draw(self,screen):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x]:
                    self.map[y][x].draw(screen)


def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0

if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 16
    create_ghosts(tile_size, map_size)
    pacman = Pacman(5, 5, tile_size, map_size)
    global MAP
    MAP = Map('C:/Users/Petr/PycharmProjects/pacman/map.txt', tile_size, map_size)
    backgfloor = pygame.image.load("C:/Users/Petr/PycharmProjects/pacman/resources/background.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(100)
        tick_ghosts()
        pacman.game_tick()
        draw_backgfloor(screen, backgfloor)
        pacman.draw(screen)
        draw_ghosts(screen)
        MAP.draw(screen)
        pygame.display.update()
