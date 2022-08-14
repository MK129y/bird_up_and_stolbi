import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
GPS = 60

windows = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

py, sy, ay = HEIGHT // 2, 0, 0
players = pygame.Rect(WIDTH // 3, py, 50, 50) #позиция  и ширина и высота пряоугольника

stat1 = 'start'
timer = 10
pipes = []


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
# Движение труб
    for i in range(len(pipes) -1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3

        if pipe.right < 100:
            pipes.remove(pipe)


    if stat1 == 'start':
        if click and timer == 0 and len(pipes) == 0:
            stat1 = 'play'

        py += (HEIGHT// 2 - py) * 0.1
        players.y = py
    elif stat1 == 'play':
        # если нажатие
        if click:
            ay = -2
        else:
            ay = 0

        # вниз типа падение
        py += sy
        sy = (sy + ay + 1) * 0.98  # скорость
        players.y = py
        #if len(pipes) == 0 or pipes[len(pipes)-1)].x < WIDTH - 200:
        if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, 200))
            pipes.append(pygame.Rect(WIDTH, 400, 50, 200))
            #pipes.append()
        ###
        #проверка птичка в границах экрана
        if players.top < 0 or players.bottom > HEIGHT:
            stat1 = 'fall'
        for pipe in pipes:
            if players.colliderect(pipe):
                stat1 = 'fall'
    elif stat1 == 'fall':
        sy, ay = 0, 0
        stat1 = 'start'
        timer = 60
    else:
        pass


    # #если нажатие
    # if click:
    #     ay = -2
    # else:
    #     ay = 0
    #
    # #вниз типа падение
    # py += sy
    # sy = (sy +ay + 1) * 0.98 #скорость
    # players.y = py
    ###

    windows.fill(pygame.Color('black'))
    for pipe in pipes:
        pygame.draw.rect(windows, pygame.Color('orange'), pipe)

    pygame.draw.rect(windows, pygame.Color('yellow'), players)
    #windows.blit(imgBird,(100,300),(34*int(frame)))


    pygame.display.update()
    clock.tick(GPS)

pygame.quit()
