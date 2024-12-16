import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), HP : int = 3, alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.HP = HP
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self, blocks : list, balls : list):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        self.HP -= 1
        if self.HP == 2: 
            self.color = (255, 165, 0) # 주황색
        elif self.HP == 1: 
            self.color = (255, 255, 0) # 노란색
        
        if self.HP <= 0:
            self.alive = False
            blocks.remove(self) # block 삭제
            self.new_block(balls)
        
    def new_block(self, balls: list): # 블록이 깨지면 랜덤확률로 공 생성
        # 1부터 10까지 난수 생성하여 2 이하인 경우 새로운 공 생성 -> 20% 확률
        if random.randint(1, 10) <= 2:
            # 공의 색깔 : 빨간색 또는 파란색으로 랜덤 설정
            new_ball_color = random.choice([(255, 0, 0), (0, 0, 255)])
            # 공의 위치 지정
            new_ball_pos = (self.rect.centerx, self.rect.centery)
            # 새로운 공 객체 생성 후 리스트에 추가
            new_ball = Ball(pos = new_ball_pos)
            new_ball.color = new_ball_color
            balls.append(new_ball)


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list, balls : list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        for block in blocks:
            if self.rect.colliderect(block.rect) and block.alive: # 충돌 여부 확인
                block.collide(blocks, balls)      # block 없애기
                self.dir = 360 - self.dir  # 공을 반사

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir
        # 상단 벽 충돌
        if self.rect.top <= 0:
            self.dir = 360 - self.dir
            #-self.dir
    
    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        return self.rect.bottom <= config.display_dimension[1] # 공이 아래쪽으로 빠진다면 False 반환
