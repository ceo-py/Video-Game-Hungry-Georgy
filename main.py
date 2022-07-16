import pygame
import os
import random
from pygame import mixer
import time

pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Georgy")
WHITE = (255, 255, 255)
FPS = 60
G_HEAD_LEFT = pygame.image.load(os.path.join("g_head_left.png"))
G_HEAD_RIGHT = pygame.image.load(os.path.join("g_head_right.png"))
G_HEAD_EATING_RIGHT = pygame.image.load(os.path.join("g_head_eating_right.png"))
G_HEAD_EATING_LEFT = pygame.image.load(os.path.join("g_head_eating_left.png"))

FLYING_BANNANA = pygame.image.load(os.path.join("bannana1.png"))
LEGS_STILL = pygame.image.load(os.path.join("leg_still1.png"))
LEGS_LEFT = pygame.image.load(os.path.join("leg_walk1.png"))
LEGS_RIGHT = pygame.image.load(os.path.join("leg_walk2.png"))
LEGS_JUMP = pygame.image.load(os.path.join("leg_jump1.png"))
LEGS_FLY = pygame.image.load(os.path.join("leg_jump1.png"))
BACK_GROUND = pygame.transform.scale(pygame.image.load(os.path.join("bg.png")), (WIDTH, HEIGHT))
MAIN_FONT = pygame.font.SysFont("comicsans", 50)
mixer.init()
mixer.music.load("hapvane.wav")
mixer.music.set_volume(0.1)

score = 0
lives_ = 3
level = 0

wave_length = 0
Start_pos = 300


class Character:
    def __init__(self, x, y, lives=3):
        self.x = x
        self.y = y
        self.lives = lives
        self.georgy_move_speed = 7.5
        self.head_position = G_HEAD_LEFT
        self.mask = pygame.mask.from_surface(self.head_position)
        self.legs = LEGS_STILL

    def character_georgy(self):
        pass

    def draw(self, window):
        window.blit(self.legs, (self.x + 8, self.y + 50))
        window.blit(self.head_position, (self.x, self.y))

    def check_catch(self, obj_1):
        return moving(obj_1, self)


bannans = []

georgy = Character(430, 410)


class ObjDroping:
    def __init__(self, x, y, lives=1):
        self.x = x
        self.y = y
        self.lives = lives
        self.moving = 1
        self.pic = FLYING_BANNANA
        self.mask = pygame.mask.from_surface(self.pic)

    def move(self):
        pass

    def draw(self, window):
        window.blit(self.pic, (self.x, self.y))


def crate_bannanas(range_):
    for _ in range(range_):
        bannans.append(ObjDroping(random.randrange(50, WIDTH - 100, 50), random.randrange(-1500, -100)))


def draw_window():
    WIN.blit(BACK_GROUND, (0, 0))
    for bannan in bannans:
        bannan.draw(WIN)
    # draw test
    score_text = MAIN_FONT.render(f"Score : {score}", 1, (255, 0, 0))
    lives_text = MAIN_FONT.render(f"Lives : {lives_}", 1, (255, 0, 0))
    level_text = MAIN_FONT.render(f"Level : {level}", 1, (255, 0, 0))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 50, 1))
    WIN.blit(lives_text, (10, 1))
    WIN.blit(level_text, (340, 1))

    georgy.draw(WIN)

    pygame.display.update()


def moving(obj1, obj2):
    offset_x = obj1.x - obj2.x
    offset_y = obj1.y - obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    angle = 0
    clock = pygame.time.Clock()
    run = True
    global score, lives_, level, wave_length
    while run:
        clock.tick(FPS)
        if not bannans:
            level += 1
            wave_length += 10
            crate_bannanas(wave_length)
            draw_window()
            next_level = MAIN_FONT.render(f"Congratulation you reach level {level}", 1, (255, 0, 0))
            WIN.blit(next_level, (80, 150))
            pygame.display.update()
            time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and georgy.x >= 1:
            georgy.head_position = G_HEAD_LEFT
            georgy.legs = LEGS_LEFT
            georgy.x -= georgy.georgy_move_speed
        if keys[pygame.K_RIGHT] and georgy.x <= 830:
            georgy.head_position = G_HEAD_RIGHT
            georgy.legs = LEGS_RIGHT
            georgy.x += georgy.georgy_move_speed
        if keys[pygame.K_UP] and georgy.y == 410:
            georgy.legs = LEGS_JUMP
            georgy.y -= 100

        if not any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP]]):
            georgy.legs = LEGS_STILL

        if georgy.y != 410:
            georgy.y += 5
        angle += 1

        for obj_ in bannans:
            obj_.y += 1
            obj_.pic = pygame.transform.rotate(FLYING_BANNANA, angle)
            if georgy.check_catch(obj_):
                score += 1
                if georgy.head_position == G_HEAD_RIGHT:
                    georgy.head_position = G_HEAD_EATING_RIGHT
                else:
                    georgy.head_position = G_HEAD_EATING_LEFT
                bannans.remove(obj_)
                mixer.music.play()
            if obj_.y == 410:
                lives_ -= 1
                bannans.remove(obj_)

        if lives_ == 0:
            game_over = MAIN_FONT.render(f"Game Over HUNGRY GEORGY!!!", 1, (255, 0, 0))
            WIN.blit(game_over, (80, 150))
            pygame.display.update()
            time.sleep(3)
            lives_ = 3
            score = 0
            lives_ = 3
            level = 0
            wave_length = 0
            bannans.clear()

    exit()
    pygame.quit()


if __name__ == "__main__":
    main()

main()
