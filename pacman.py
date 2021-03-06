import sys
import pygame
from pygame.locals import *
from math import floor
import random
import time


def init_window():
    pygame.init()
    pygame.display.set_mode((1024, 512))
    pygame.display.set_caption('Pacman')


def draw_backgfloor(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))

def draw_game_win(scr, img=None):
    if img:
        scr.blit(img,(0, 0))

def draw_game_lose(scr, img=None):
    if img:
        scr.blit(img,(0,0))


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
        if self.direction==1 or self.direction==0:
            scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))
        if self.direction==2:
            scr.blit(pygame.transform.rotate(self.image,-90), (self.screen_rect.x, self.screen_rect.y))
        if self.direction==3:
            scr.blit(pygame.transform.rotate(self.image,180), (self.screen_rect.x, self.screen_rect.y))
        if self.direction==4:
            scr.blit(pygame.transform.rotate(self.image,90), (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts = []
    num = 1
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 5.0/ 10.0

    def game_tick(self):
        super(Ghost, self).game_tick()

        if self.tick % 20 == 0 or self.direction == 0 and movingarrow.ghost!=1:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y) and not is_destructible_wall(floor(self.x + self.velocity),self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)) and not is_destructible_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
                self.direction = random.randint(1, 4)
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y) and not is_destructible_wall(floor(self.x - self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                    self.x = 0
                    self.direction = random.randint(1, 4)
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)) and not is_destructible_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
        self.set_coord(self.x, self.y)
class MovingArrow (GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self,'./resources/moving_arrow.png',x,y,tile_size, map_size)
        self.direction=0
        self.velocity = 4.0 / 10.0
        self.ghost=0
    def game_tick(self):
        super(MovingArrow, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y) and not is_destructible_wall(floor(self.x + self.velocity),self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)) and not is_destructible_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y) and not is_destructible_wall(floor(self.x - self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)) and not is_destructible_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        if pacman.movingarrow==1 and pacman.crossbow==1 and pacman.arrow==1:
            self.velocity=10.0 / 10.0
        self.set_coord(self.x, self.y)
        for g in Ghost.ghosts:
            if int(g.x)==int(self.x) and int(g.y)==int(self.y):
                g.direction=0
                self.ghost=1
class MovingBow (GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self,'./resources/crossbow.png',x,y,tile_size, map_size)
        self.direction=0
        self.velocity = 4.0 / 10.0
    def game_tick(self):
        super(MovingBow, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y) and not is_destructible_wall(floor(self.x + self.velocity),self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)) and not is_destructible_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y) and not is_destructible_wall(floor(self.x - self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)) and not is_destructible_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        self.set_coord(self.x, self.y)
class MovingSword (GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self,'./resources/sword.png',x,y,tile_size, map_size)
        self.direction=0
        self.velocity = 4.0 / 10.0
    def game_tick(self):
        super(MovingSword, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y) and not is_destructible_wall(floor(self.x + self.velocity),self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)) and not is_destructible_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y) and not is_destructible_wall(floor(self.x - self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)) and not is_destructible_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        self.set_coord(self.x, self.y)
def init_music():
   pygame.init()
   pygame.mixer.music.load('./resources/music.mp3')
   pygame.mixer.music.play()

def draw_ghosts(screen):
    for g in Ghost.ghosts:
        g.draw(screen)
def create_ghosts(ts, ms):
    Ghost.ghosts = [Ghost(1, 1, ts, ms) for i in range(Ghost.num)]
def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()
class Point(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/point.png', x, y, tile_size, map_size)
        self.direction=0
    def game_tick(self):
        super(Point, self).game_tick()
class Sword(GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self, './resources/sword.png',x,y,tile_size, map_size)
        self.direction=0
class CrossBow(GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self,'./resources/crossbow.png',x,y,tile_size, map_size)
        self.direction=0
class Arrow (GameObject):
    def __init__(self,x,y,tile_size,map_size):
        GameObject.__init__(self,'./resources/arrow.png',x,y,tile_size, map_size)
        self.direction=0


class Map:
    def __init__(self, filename, tile_size, map_size):
        self.map = []
        f=open(filename, 'r')
        txt = f.readlines()
        f.close()
        self.k=0
        for y in range(len(txt)):
            self.map.append([])
            for x in range(len(txt[y])):
                if txt[y][x] == "#":
                    self.map[-1].append(Wall(x, y, tile_size, map_size))
                elif txt[y][x]=='.':
                    self.map[-1].append(Point(x,y,tile_size, map_size))
                    self.k+=1
                elif txt[y][x]=='S':
                    self.map[-1].append(Sword(x,y,tile_size, map_size))
                elif txt[y][x]=='$':
                    self.map[-1].append(Destructible_Wall(x,y,tile_size,map_size))
                elif txt[y][x]=='C':
                    self.map[-1].append(CrossBow(x,y,tile_size,map_size))
                elif txt[y][x]=='A':
                    self.map[-1].append(Arrow(x,y,tile_size,map_size))
                else:
                    self.map[-1].append(None)
        self.tile_size = tile_size
        self.map_size = map_size
        if self.k==0:
            sys.exit(0)
    def draw(self,screen):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x]:
                    self.map[y][x].draw(screen)
a=open('map.txt', 'r')
l=a.readlines()
a.close()
pts=0
for i in range(len(l)):
    for v in range(len(l[i])):
        if l[i][v]=='.':
            pts+=1
print(pts)
class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 4.0 / 10.0
        self.points=pts
        self.gw=0
        self.death=0
        self.sword=0
        self.crossbow=0
        self.arrow=0
        self.movingarrow=0
    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y) and not is_destructible_wall(floor(self.x + self.velocity),self.y):
                self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
            if is_point(floor(self.x+self.velocity), self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x+self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x+self.velocity)),[])
                self.points-=1
            if is_sword(floor(self.x+self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x+self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x+self.velocity)),[])
                self.death-=5
                self.sword=1
            if is_arrow(floor(self.x+self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x+self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x+self.velocity)),[])
                self.arrow=1
            if is_crossbow(floor(self.x+self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x+self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x+self.velocity)),[])
                self.death-=3
                self.crossbow=1
            if self.sword==1:
                if is_destructible_wall(floor(self.x+self.velocity),self.y):
                    MAP.map[int(self.y)].pop(int(floor(self.x+self.velocity)))
                    MAP.map[int(self.y)].insert(int(floor(self.x+self.velocity)),[])
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)) and not is_destructible_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
            if is_point(self.x, floor(self.y+self.velocity)):
                MAP.map[int(floor(self.y+self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y+self.velocity))].insert(int(self.x),[])
                self.points-=1
            if is_sword(self.x, floor(self.y+self.velocity)):
                MAP.map[int(floor(self.y + self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y+self.velocity))].insert(int(self.x),[])
                self.death-=5
                self.sword=1
            if is_arrow(self.x, floor(self.y+self.velocity)):
                MAP.map[int(floor(self.y + self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y+self.velocity))].insert(int(self.x),[])
                self.arrow=1
            if is_crossbow(self.x, floor(self.y+self.velocity)):
                MAP.map[int(floor(self.y + self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y+self.velocity))].insert(int(self.x),[])
                self.death-=3
                self.crossbow=1
            if self.sword==1:
                if is_destructible_wall(self.x,floor(self.y+self.velocity)):
                    MAP.map[int(floor(self.y + self.velocity))].pop(int(self.x))
                    MAP.map[int(floor(self.y+self.velocity))].insert(int(self.x),[])
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y) and not is_destructible_wall(floor(self.x - self.velocity),self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
            if is_point(floor(self.x - self.velocity), self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x - self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x-self.velocity)),[])
                self.points-=1
            if is_sword(floor(self.x-self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x-self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x-self.velocity)),[])
                self.death-=5
                self.sword=1
            if is_arrow(floor(self.x-self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x-self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x-self.velocity)),[])
                self.arrow=1
            if is_crossbow(floor(self.x-self.velocity),self.y):
                MAP.map[int(self.y)].pop(int(floor(self.x-self.velocity)))
                MAP.map[int(self.y)].insert(int(floor(self.x-self.velocity)),[])
                self.death-=3
                self.crossbow=1
            if self.sword==1:
                if is_destructible_wall(floor(self.x-self.velocity),self.y):
                    MAP.map[int(self.y)].pop(int(floor(self.x-self.velocity)))
                    MAP.map[int(self.y)].insert(int(floor(self.x-self.velocity)),[])
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)) and not is_destructible_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
            if is_point(self.x, floor(self.y - self.velocity)):
                MAP.map[int(floor(self.y - self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y-self.velocity))].insert(int(self.x),[])
                self.points-=1
            if is_sword(self.x, floor(self.y-self.velocity)):
                MAP.map[int(floor(self.y - self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y-self.velocity))].insert(int(self.x),[])
                self.death-=5
                self.sword=1
            if is_arrow(self.x, floor(self.y-self.velocity)):
                MAP.map[int(floor(self.y - self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y-self.velocity))].insert(int(self.x),[])
                self.arrow=1
            if is_crossbow(self.x, floor(self.y-self.velocity)):
                MAP.map[int(floor(self.y - self.velocity))].pop(int(self.x))
                MAP.map[int(floor(self.y-self.velocity))].insert(int(self.x),[])
                self.death-=3
                self.crossbow=1
            if self.sword==1:
                if is_destructible_wall(self.x, floor(self.y-self.velocity)):
                    MAP.map[int(floor(self.y - self.velocity))].pop(int(self.x))
                    MAP.map[int(floor(self.y-self.velocity))].insert(int(self.x),[])
        self.set_coord(self.x, self.y)
        for g in Ghost.ghosts:
            if int(g.x)==int(self.x) and int(g.y)==int(self.y):
                self.death+=1
        for g in Ghost.ghosts:
            if int(g.y)==int(self.y) or int(g.x)==int(self.x):
                g.direction=self.direction
        if self.points==0:
            self.gw=1

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)
        self.direction=0
    def game_tick(self):
        super(Wall, self).game_tick()

class Destructible_Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/destructible_wall.png', x, y, tile_size, map_size)
        self.direction=0
    def game_tick(self):
        super(Destructible_Wall, self).game_tick()

def is_wall(x, y):
    return isinstance(MAP.map[int(y)][int(x)], Wall)
def create_walls(coords, ts, ms):
    Wall.walls = [Wall(2, 4, ts, ms)]

def is_destructible_wall(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Destructible_Wall)
def create_destructible_walls(coords, ts, ms):
    Destructible_Wall.destructible_walls = [Destructible_Wall(2, 4, ts, ms)]
def is_point(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Point)

def is_sword(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Sword)
def is_crossbow(x,y):
    return isinstance(MAP.map[int(y)][int(x)], CrossBow)
def is_arrow(x,y):
    return isinstance(MAP.map[int(y)][int(x)],Arrow)

def create_points(coords, ts, ms):
    Point.points = [Point(2, 4, ts, ms)]

def is_ghost(x,y):
    return isinstance(MAP.map[int(y)][int(x)], Ghost)

def process_events(events, packman, movingarrow, bow, sword):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
                if pacman.movingarrow!=1:
                    movingarrow.direction=3
                bow.direction=3
                sword.direction=3
            elif event.key == K_RIGHT:
                packman.direction = 1
                if pacman.movingarrow!=1:
                    movingarrow.direction=1
                bow.direction=1
                sword.direction=1
            elif event.key == K_UP:
                packman.direction = 4
                if pacman.movingarrow!=1:
                    movingarrow.direction=4
                bow.direction=4
                sword.direction=4
            elif event.key == K_DOWN:
                packman.direction = 2
                if pacman.movingarrow!=1:
                    movingarrow.direction=2
                bow.direction=2
                sword.direction=2
            elif event.key == K_SPACE:
                packman.direction = 0
                if pacman.movingarrow!=1:
                    movingarrow.direction=0
                bow.direction=0
                sword.direction=0
            elif event.key == K_LCTRL:
                if packman.arrow==1 and packman.crossbow==1:
                    packman.movingarrow=1


if __name__ == '__main__':
    init_window()
    tile_size = 32
    map_size = 32
    create_ghosts(tile_size, map_size)
    pacman = Pacman(5, 5, tile_size, map_size)
    movingarrow=MovingArrow(5,5,tile_size, map_size)
    bow=MovingBow(5,5,tile_size,map_size)
    sword=MovingSword(5,5,tile_size,map_size)
    global MAP
    MAP = Map('./pacman/map.txt', tile_size, map_size)
    backgfloor = pygame.image.load("./resources/background.png")
    game_win=pygame.image.load("./resources/game_win.png")
    game_lose=pygame.image.load("./resources/game_lose.png")
    screen = pygame.display.get_surface()
    init_music()

    while 1:
        process_events(pygame.event.get(), pacman, movingarrow, bow, sword)
        pygame.time.delay(100)
        if movingarrow.ghost!=1:
            tick_ghosts()
        pacman.game_tick()
        movingarrow.game_tick()
        bow.game_tick()
        sword.game_tick()
        draw_backgfloor(screen, backgfloor)
        if pacman.gw==1:
            draw_game_win(screen, game_win)
        if pacman.death>0:
            draw_game_lose(screen,game_lose)
        pacman.draw(screen)
        if pacman.arrow==1 and movingarrow.direction!=0:
            movingarrow.draw(screen)
        if pacman.crossbow==1:
            bow.draw(screen)
        if pacman.sword==1:
            sword.draw(screen)
        draw_ghosts(screen)
        MAP.draw(screen)
        pygame.display.update()
        if pacman.points==0:
            time.sleep(5)
            sys.exit(0)
        if pacman.death>0:
            time.sleep(5)
            sys.exit(0)
