from typing import List

import pygame
from pygame import Rect
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
GPS = 60

windows = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
#шрифт текста на экране
font1 = pygame.font.Font(None, 35)
fon2 = pygame.font.Font(None, 85)

imgfon =pygame.image.load('image/fon.png') #картинка фона
imgBird = pygame.image.load('image/bird.png') #картинка птички
imgPipeupp = pygame.image.load('image/pipe_top.png')#труба верхняя
imgPipedown = pygame.image.load('image/pipe_bottom.png')

#музыка фон
pygame.mixer.music.load('music/shi_fon.mp3') #загрузка звукового файла
pygame.mixer.music.set_volume(0.1) #уменьшение громкости от 0 жо 1
pygame.mixer.music.play(-1) #постоянное воспроизведение (-1) повтор зациклена


#музыка звуковые эффекты
sndFall = pygame.mixer.Sound('music/mouse_ok_format.wav')

py, sy, ay = HEIGHT // 2, 0, 0
players = pygame.Rect(WIDTH // 3, py, 34, 24) #позиция  и ширина и высота пряоугольника

frame = 0
animatsiya = 0
stat = 'start'
timer = 10
pipes = []
fon = []
pipesScores = []
lives = 3
scores = 0

pipeSpeed = 3
pipeGateSize = 200
pipeGatePos = HEIGHT // 2


fon.append(pygame.Rect(0, 0, 288, 600))



play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    #управление
    press = pygame.mouse.get_pressed()# состояние всех кнопок мыши
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE] #переменная нажатие на кнопку мыши либо на пробел

    if timer > 0:
        timer -= 1
    animatsiya = (animatsiya + 0.2) % 4

    #frame = (frame + 0.2) % 4
    pipeSpeed = 3 + scores // 100
#фон
    for i in range(len(fon)-1, -1, -1):
        f = fon[i]
        f.x -= pipeSpeed // 2

        if f.right < 0:
            fon.remove(f)


        if fon[len(fon)-1].right <= WIDTH:
            fon.append(pygame.Rect(fon[len(fon)-1].right, 0, 288, 600))
            #fon.append(pygame.Rect(fon[len(fon)-1].right, 0, 288, 600))

        #Движение труб
    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        #pipe.x -= 3

        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipesScores:
                pipesScores.remove(pipe)

    if stat == 'start':
        if click and timer == 0 and len(pipes) == 0:
            stat = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        players.y = py

        # если нажатие
    elif stat == 'play':
        if click:
            ay = -2
        else:
            ay = 0

        # вниз типа падение
        py += sy
        sy = (sy + ay + 1) * 0.98  # скорость
        players.y = py



        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipeGatePos - pipeGateSize // 2))
            pipes.append(
                pygame.Rect(WIDTH, pipeGatePos + pipeGateSize // 2, 52, HEIGHT - pipeGatePos + pipeGateSize // 2))

            pipeGatePos += randint(-100, 100)
            if pipeGatePos < pipeGateSize:
                pipeGatePos = pipeGateSize
            elif pipeGatePos > HEIGHT - pipeGateSize:
                pipeGatePos = HEIGHT - pipeGateSize




        if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, 200))
            pipes.append(pygame.Rect(WIDTH, 400, 50, 200))

        if players.top < 0 or players.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if players.colliderect(pipe):
                state = 'fall'

            # if pipe.right < players.left and pipe not in pipesScores:
            #     pipesScores.append(pipe)
            #     scores += 5






        # if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
        #     pipes.append(pygame.Rect(WIDTH, 0, 50, 200))
        #     pipes.append(pygame.Rect(WIDTH, 400, 50, 200))
        # ###
        # #проверка птичка в границах экрана
        # if players.top < 0 or players.bottom > HEIGHT:
        #     stat = 'fall'
        # for pipe in pipes:
        #     if players.colliderect(pipe):
        #         stat = 'fall'
        #
#разобраться почему птичка не возвр на прежденее положение и препятсявие не задевает , что то удалила( посмотреть


    elif stat == 'fall':
        sndFall.play() #звук нажатие
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2
        stat = 'start'
        timer = 60

        lives -= 1 #уменьшение жизни при зароне
        if lives > 0:
            stat = 'start'
            timer = 60
        else:
            stat = 'game over'
            timer = 120

    else:
        py += sy
        sy = (sy + ay + 1) * 0.98  # скорость
        players.y = py

        if timer == 0:
            play = False

    windows.fill(pygame.Color('black'))
    for f in fon:
        windows.blit(imgfon, f)

    for pipe in pipes:
        if pipe.y == 0:
            rect = imgPipeupp.get_rect(bottomleft= pipe.bottomleft)
            windows.blit(imgPipeupp, rect)
        else:
                rect = imgPipedown.get_rect(topleft=pipe.topleft)
                windows.blit(imgPipedown, rect)

    imageBird = imgBird.subsurface(34 * int(animatsiya), 0, 34, 24)
    imageBird = pygame.transform.rotate(imageBird, -sy * 2)
    windows.blit(imageBird, players)# вывод птицы

    #print(animatsiya)
    text = font1.render('Очки: ' +str(scores), 1, pygame.Color('black'))
    windows.blit(text, (10,10))

    tex = font1.render('Жизни ' + str(lives), 1, pygame.Color('black'))
    windows.blit(tex, (10,HEIGHT- 30))

    pygame.display.update()
    clock.tick(GPS)

pygame.quit()
