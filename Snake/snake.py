import pygame
from direction import Direction
from segment import Segment
import copy

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        self.head_image = pygame.image.load("Snake/head.png")
        self.image = pygame.transform.rotate(self.head_image, 0)
        self.rect = self.image.get_rect(center = (12 * 32 +16, 9 * 32 +16))

        self.direction = Direction.UP
        self.new_direction = Direction.UP

        self.last_position = self.rect
        self.add_segment = False
        self.segmenty = []
        

    def change_direction(self, direction):
        change_on = True
        if direction == Direction.UP and self.direction == Direction.DOWN:
            change_on = False
        if direction == Direction.DOWN and self.direction == Direction.UP:
            change_on = False
        if direction == Direction.LEFT and self.direction == Direction.RIGHT:
            change_on = False
        if direction == Direction.RIGHT and self.direction == Direction.LEFT:
            change_on = False
        if change_on:
            self.new_direction = direction

    def update(self):
        self.direction = self.new_direction
        self.image = pygame.transform.rotate(self.head_image, (self.direction.value*-90))

        self.last_position = copy.deepcopy(self.rect)

        if self.direction == Direction.UP:
            self.rect.move_ip(0, -32)
        if self.direction == Direction.DOWN:
            self.rect.move_ip(0, 32)
        if self.direction == Direction.LEFT:
            self.rect.move_ip(-32, 0)
        if self.direction == Direction.RIGHT:
            self.rect.move_ip(32, 0)

        for i in range(len(self.segmenty)):
            if i == 0:
                self.segmenty[i].move(self.last_position)
            else:
                self.segmenty[i].move(self.segmenty[i-1].last_position)

        if self.add_segment:
            new_segment = Segment()

            new_position = None
            if len(self.segmenty) > 0:
                new_position = copy.deepcopy(self.segmenty[-1].pozycja)
            else:
                new_position = copy.deepcopy(self.last_position)
            new_segment.pozycja = new_position
            self.segmenty.append(new_segment)
            self.add_segment = False

    def draw_segments(self, display):
        for segment in self.segmenty:
            display.blit(segment.image, segment.position)

    def eat_apple(self):
        self.add_segment = True

    def check_collision(self):
        for segment in self.segmenty:
            if self.rect.topleft == segment.position.topleft:
                return True
            
        if self.rect.top < 0 or self.rect.top >= 608:
            return True
        if self.rect.left < 0 or self.rect.left >= 800:
            return True
        
        return False