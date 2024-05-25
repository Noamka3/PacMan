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
color = 'brown'
PI = math.pi
player_image =[]
for i in range(1,5):
    player_image.append(pygame.transform.scale(pygame.image.load(f'Player_image/{i}.png'),(38,38)))

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
        pygame.draw.circle(screen,'Red',(150,740),15)
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
    draw_player()
    draw_score()
    center_x = player_x +28
    center_y = player_y +24
    turns_allowed = check_position(center_x,center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
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
        player_x = 701



    pygame.display.flip()
pygame.quit()

