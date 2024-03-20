import pygame
import random
import time 
from apple import Apple
from direction import Direction
from snake import Snake

display_width = 800
display_height = 608

Points = 0

background = pygame.Surface((display_width, display_height))

#generate the field with dif colours in random pos

for i in range(25):
    for j in range(19):
        image = pygame.image.load("Snake/background.png")
        mask = (random.randrange(0, 20), random.randrange(0, 20), random.randrange(0, 20))

        image.fill(mask, special_flags=pygame.BLEND_ADD)
        background.blit(image, (i*32, j*32))

pygame.init()

display = pygame.display.set_mode([display_width, display_height])
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('Comic Sans MS', 24)

snake = Snake()
move_snake = pygame.USEREVENT + 1
pygame.time.set_timer(move_snake, 200)

apple = Apple()
apples = pygame.sprite.Group()
apples.add(apple)

#game loop

game_on = True

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False

            if event.key == pygame.K_w:
                snake.change_direction(Direction.UP)
            if event.key == pygame.K_s:
                snake.change_direction(Direction.DOWN)
            if event.key == pygame.K_d:
                snake.change_direction(Direction.RIGHT)
            if event.key == pygame.K_a:
                snake.change_direction(Direction.LEFT)

        elif event.type == move_snake:
                snake.update()

        elif event.type == pygame.QUIT:
            game_on = False

    collision_apple = pygame.sprite.spritecollideany(snake, apples)
    if collision_apple != None:
        collision_apple.kill()
        snake.eat_apple()
        Points += 1
        apple = Apple()
        apples.add(apple)

    display.blit(background, (0, 0))

    snake.draw_segments(display)

    display.blit(snake.image, snake.rect)

    for apple in apples:
        display.blit(apple.image, apple.rect)

    results = font1.render(f'Score: {Points}', False, (0, 0, 0))
    display.blit(results, (16, 16))

    if snake.check_collision():
        text_fail = font1.render('Game over', False, (200, 0, 0))
        display.blit(text_fail, (display_width/2-50, display_height/2))
        game_on = False

    pygame.display.flip()
    clock.tick(30)

time.sleep(1)
pygame.quit()

