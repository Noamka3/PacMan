#Build Pac-Man :
from board import boards
#check Pip for pygame
import pygame
import math

pygame.init()

WIDTH = 700
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH,HEIGHT])
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'brown'
PI = math.pi
player_image =[]
for i in range(1,5):
    player_image.append(pygame.transform.scale(pygame.image.load(f'Player_image/{i}.png'),(35,35)))

player_x = 450
player_y = 655
direction = 0
counter = 0
flicker = False
#R,L,U,D
turns_allowed = [False,False,False,False]


#Building a display
def draw_board(lvl):
    num1 = ((HEIGHT-20)//32)
    num2 = (WIDTH//30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen,'white',(j*num2+(0.5*num2),i*num1+(0.5*num1)),4)
            if level[i][j] == 2 and not flicker :
                pygame.draw.circle(screen,'white',(j*num2+(0.5*num2),i*num1+(0.5*num1)),10)
            if level[i][j] == 3:
                pygame.draw.line(screen,color,(j*num2 + (0.5*num2),i*num1),
                                 (j* num2 + (0.5*num2),i*num1 + num1),3)
            if level[i][j] == 4:
                pygame.draw.line(screen,color,(j*num2,+ i*num1 + (0.5*num1)),
                                 (j* num2 + num2,i*num1 + (0.5*num1)),3)
            if level[i][j] == 5:
                pygame.draw.arc(screen,color,[(j*num2 - (num2*0.4)) - 2 , (i*num1 + (0.5*num1)),num2,num1],0,PI/2 ,3)

            if level[i][j] == 6:
                pygame.draw.arc(screen,color,[(j*num2 + (num2*0.5)) , (i*num1 + (0.5*num1)),num2,num1],PI/2 ,PI,3)

            if level[i][j] == 7:
                pygame.draw.arc(screen,color,[(j*num2 + (num2*0.5)) , (i*num1 - (0.4*num1)),num2,num1],PI ,3*PI/2,3)

            if level[i][j] == 8:
                pygame.draw.arc(screen,color,[(j*num2 - (num2*0.4)) , (i*num1 - (0.4*num1)),num2,num1],3*PI / 2 ,2*PI,3)

            if level[i][j] == 9:
                pygame.draw.line(screen,'white',(j*num2,+ i*num1 + (0.5*num1)),
                                 (j* num2 + num2,i*num1 + (0.5*num1)),3)


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


def check_position(centerX,centerY):
    turns = [False,False,False,False]
    num1 = (HEIGHT-20)//32
    num2 = (WIDTH//30)
    num3 = 15
    #Check collisions based on center x and center y of player +/- fudge number
    if centerX //30 <29:
        if direction == 0:
            if level[centerY//num1][(centerX- num3)//num2] <3:
                turns[1]=True
        if level[centerY // num1][(centerX - num3) // num2] < 3:
            turns[1] = True

        if level[centerY // num1][(centerX - num3) // num2] < 3:
            turns[1] = True

        if level[centerY // num1][(centerX - num3) // num2] < 3:
            turns[1] = True



    else:
        turns[0] =True
        turns[1] = True
    return  turns

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
    screen.fill('black')
    draw_board(level)
    draw_player()
    center_x = player_x +20
    center_y = player_y +18
    turns_allowed = check_position(center_x,center_y)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3



    pygame.display.flip()
pygame.quit()