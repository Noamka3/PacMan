#Build Pac-Man :
from board import boards
#check Pip for pygame
import pygame
import math

pygame.init()

WIDTH = 750
HEIGHT = 780
screen = pygame.display.set_mode([WIDTH,HEIGHT])
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = '#007FFF'
PI = math.pi
player_image =[]
for i in range(1,5):
    player_image.append(pygame.transform.scale(pygame.image.load(f'Player_image/{i}.png'),(38,38)))
Red_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/red.png'),(50,50))
Green_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/Green.png'),(50,50))
Pink_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/Pink.png'),(50,50))
brown_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/brown.png'),(50,50))
Power_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/PowerAngle.png'),(50,50))
dead_img = pygame.transform.scale(pygame.image.load(f'Ghost_image/dead.png'),(50,50))


player_x = 375
player_y = 520
direction = 0
counter = 0
flicker = False
#R,L,U,D
turns_allowed = [False,False,False,False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_count = 0
eaten_ghost = [False,False,False,False]
moving = False
startup_counter = 0
Lives = 3

#Ghost
Red_x = 40
Red_y = 56
Red_direction = 0

Green_x = 375
Green_y = 360
Green_direction = 2

Pink_x = 375
Pink_y = 300
Pink_direction = 2

brown_x = 341
brown_y = 360
brown_direction = 0

targets = [(player_x,player_y),(player_x,player_y),(player_x,player_y),(player_x,player_y)]

Red_dead = False
Green_dead = False
Pink_dead = False
brown_dead = False

Red_box = False
Green_box = False
Pink_box = False
brown_box = False

ghost_speed = 2




class Gohst:
    def __init__(self,x_coord,y_coord,target,speed,img,direct,dead,box,id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos +22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.in_box = box
        self.direction = direct
        self.dead = dead
        self.img = img
        self.id = id
        self.turns,self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img,(self.x_pos,self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(Power_img,(self.x_pos,self.y_pos))
        else:
            screen.blit(dead_img,(self.x_pos,self.y_pos))
            ghost_rect = pygame.rect.Rect((self.center_x - 18,self.center_y - 18),(36,36))
            return ghost_rect



    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3)//num1][self.center_x//num2] == 9:
                self.turns[2] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_Red(self):
       #Right,Left,Up,Down
       # r, l, u, d
       # blinky is going to turn whenever colliding with walls, otherwise continue straight
       if self.direction == 0:
           if self.target[0] > self.x_pos and self.turns[0]:
               self.x_pos += self.speed
           elif not self.turns[0]:
               if self.target[1] > self.y_pos and self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.target[1] < self.y_pos and self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.target[0] < self.x_pos and self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
               elif self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
           elif self.turns[0]:
               self.x_pos += self.speed
       elif self.direction == 1:
           if self.target[0] < self.x_pos and self.turns[1]:
               self.x_pos -= self.speed
           elif not self.turns[1]:
               if self.target[1] > self.y_pos and self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.target[1] < self.y_pos and self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.target[0] > self.x_pos and self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
               elif self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
           elif self.turns[1]:
               self.x_pos -= self.speed
       elif self.direction == 2:
           if self.target[1] < self.y_pos and self.turns[2]:
               self.direction = 2
               self.y_pos -= self.speed
           elif not self.turns[2]:
               if self.target[0] > self.x_pos and self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
               elif self.target[0] < self.x_pos and self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
               elif self.target[1] > self.y_pos and self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.turns[3]:
                   self.direction = 3
                   self.y_pos += self.speed
               elif self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
               elif self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
           elif self.turns[2]:
               self.y_pos -= self.speed
       elif self.direction == 3:
           if self.target[1] > self.y_pos and self.turns[3]:
               self.y_pos += self.speed
           elif not self.turns[3]:
               if self.target[0] > self.x_pos and self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
               elif self.target[0] < self.x_pos and self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
               elif self.target[1] < self.y_pos and self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.turns[2]:
                   self.direction = 2
                   self.y_pos -= self.speed
               elif self.turns[0]:
                   self.direction = 0
                   self.x_pos += self.speed
               elif self.turns[1]:
                   self.direction = 1
                   self.x_pos -= self.speed
           elif self.turns[3]:
               self.y_pos += self.speed
       if self.x_pos < -10:
           self.x_pos = 750
       elif self.x_pos > 750:
           self.x_pos - 10
       return self.x_pos, self.y_pos, self.direction

    def  move_Pink(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 750
        elif self.x_pos > 750:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
    def move_brown(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 750
        elif self.x_pos > 750:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
    def move_Green(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 750
        elif self.x_pos > 750:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction





#Building a display
def draw_board():
    num1 = ((HEIGHT - 60) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    # player  => 0-Right,1-Left,2-Up,3-Down
    if direction == 0:
        screen.blit(player_image[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_image[counter // 5],True,False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_image[counter // 5],90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_image[counter // 5],270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 8
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 30:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 14 <= centery % num1 <= 30:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 30:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 30:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(RedX,RedY,GreenX,GreenY,PinkX,PinkY,brownX,brownY):
  if player_x < 375:
      runaway_x = 750
  else:
      runaway_x = 0
  if player_y < 375:
     runaway_y = 750
  else:
      runaway_y = 0
  return_target = (375,400)
  if powerup:
      if not Red.dead:
          Red_target = (runaway_x,runaway_y)
      else:
          Red_target = return_target

      if not Green.dead:
          Green_target = (runaway_x,player_y)
      else:
          Green_target = return_target

      if not Pink.dead:
          Pink_target = (player_x,runaway_y)
      else:
          Pink_target = return_target

      if not brown.dead:
          brown_target = (375,375)
      else:
          brown_target = return_target
  else:
      if not Red.dead:
          if 340 < RedX < 560 and 340 < RedY < 500:
            Red_target = (400,100)
          else:
            Red_target = (player_x,player_y)
      else:
            Red_target = return_target

      if not Green.dead:
          if 340 < GreenX < 560 and 340 < GreenY < 500:
            Green_target = (400,100)
          else:
           Green_target = (player_x,player_y)
      else:
           Green_target = return_target

      if not Pink.dead:
              if 340 < PinkX < 560 and 340 < PinkY < 500:
                  Pink_target = (400, 100)
              else:
                  Pink_target = (player_x, player_y)
      else:
                  Pink_target = return_target

      if not brown.dead:
          if 340 < brownX < 560 and 340 < brownY < 500:
              brown_target = (400, 100)
          else:
              brown_target = (player_x, player_y)
      else:
              brown_target = return_target


  return [Red_target,Green_target,Pink_target,brown_target]








#Game Score
def check_collisions(score,power,power_count,eaten_ghosts):
    num1 = (HEIGHT-50)//32
    num2=WIDTH//30
    if 0 < player_x < 800:
        if level[center_y//num1][center_x//num2] == 1:
            level[center_y//num1][center_x//num2] = 0
            score +=10
#Big Point
        if level[center_y//num1][center_x//num2] == 2:
            level[center_y//num1][center_x//num2] = 0
            score +=50
            power = True
            power_count = 0
            eaten_ghosts = [False,False,False,False]

    return score,power,power_count,eaten_ghosts

def draw_score():
    num1 = (HEIGHT-50)//32
    num2 = WIDTH//30
    score_text = font.render('Score:', True, 'white')
    score_value_text = font.render(str(score), True, 'Gold')
    screen.blit(  score_text, (10, 730))
    screen.blit(score_value_text, (80, 730))
    if powerup:
        pygame.draw.circle(screen,'#007FFF',(150,740),15)
    for i in range(Lives):
        screen.blit(pygame.transform.scale(player_image[0],(30,30)),(620+i*40,730))

#screen game run
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter +=1
        if counter > 3:
           flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_count < 600:
        power_count +=1
    elif powerup and power_count >=600:
        powerup = False
        power_count = 0
        eaten_ghost = [False,False,False,False]
    if startup_counter < 10:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x +20
    center_y = player_y +20
    player_circle =  pygame.draw.circle(screen,'Black',(center_x,center_y),20,1)
    draw_player()
    #Ghost
    Red = Gohst(Red_x,Red_y,targets[0],ghost_speed,Red_img,Red_direction,Red_dead,Red_box,0)
    Green = Gohst(Green_x,Green_y,targets[1],ghost_speed,Green_img,Green_direction,Green_dead,Green_box,1)
    Pink = Gohst(Pink_x,Pink_y,targets[2],ghost_speed,Pink_img,Pink_direction,Pink_dead,Pink_box,2)
    brown = Gohst(brown_x,brown_y,targets[3],ghost_speed,brown_img,brown_direction,brown_dead,brown_box,3)
    draw_score()
    targets = get_targets(Red_x,Red_y,Green_x,Green_y,Pink_x,Pink_y,brown_x,brown_y)

    turns_allowed = check_position(center_x,center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        Red_x,Red_y,Red_direction = Red.move_Red()
        Green_x, Green_y, Green_direction = Green.move_Red()
        Pink_x, Pink_y, Pink_direction = Pink.move_Red()
        brown_x, brown_y, brown_direction = brown.move_Red()

    score,powerup,power_count,eaten_ghost = check_collisions(score,powerup,power_count,eaten_ghost)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 750:
        player_x = -47
    elif player_x < -50:
        player_x = 700

    if player_x > 700:
        player_x = -47
    elif player_x < -50:
        player_x = 750


    pygame.display.flip()
pygame.quit()

