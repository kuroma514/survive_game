import pygame
from setting import *
from image import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, image, AT, SP, size, cooltime, player, x, y):
        super().__init__(groups)
        self.player = player
        self.SP = SP * self.player.bullet_speed
        self.AT = AT * self.player.AT
        self.size = size * self.player.bullet_size
        self.cooltime = cooltime
        self.image_num = image
        self.enemy_group = self.player.enemy_group
        self.camera_y = self.player.camera_y
        self.rect_move_y = 0
        self.frame = 0
        self.pop = pygame.Vector2(
            x, y - ((map_h - screen_h) - self.camera_y))

        # 画像の取得
        self.index = 0
        if self.image_num == "Water Effect and Bullet":
            self.image_list = water_bullet_image_list
            self.index_max = 4
            self.image_size = pygame.Vector2(32, 32) * self.size
        if self.image_num == "syuriken":
            self.image_list = syuriken_image_list
            self.index_max = 4
            self.image_size = pygame.Vector2(24, 24) * self.size
        if self.image_num == "bom":
            self.image_list = boom_image_list
            self.index_max = 9
            self.image_size = pygame.Vector2(160, 160) * self.size
        if self.image_num == "beam":
            self.image_list = beam_image_list
            self.index_max = 8
            self.image_size = pygame.Vector2(120, 600) * self.size

        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.image_size)

        self.rect = self.image.get_rect(center=(x, y))

    def scroll(self):
        self.rect.centery = (self.pop.y) + \
            (map_h - screen_h) - self.camera_y + self.rect_move_y

    def self_kill(self):
        if self.rect.left < 0 or self.rect.right > screen_w or self.rect.top < 0 or self.rect.bottom > screen_h:
            self.kill()

    def image_update(self):
        if self.player.game_pose == False:
            self.index = self.frame // 10 % self.index_max
            self.pre_image = self.image_list[self.index]
            self.image = pygame.transform.scale(
                self.pre_image, self.image_size)

    def update(self):
        self.camera_y = self.player.camera_y
        self.frame += 1
        self.self_kill()
        self.scroll()
        self.image_update()


class Waterball(Weapon):
    def __init__(self, groups, image, AT, SP, size, cooltime, player, x, y):
        super().__init__(groups, image, AT, SP, size, cooltime, player, x, y)
        self.direction = self.player.direction

        #  0  1  2  3 (1) ↓
        #  4  5  6  7 (5) ←
        #  8  9  10 11(9) →
        #  12 13 14 15(13) ↑

    def move(self):
        if self.player.game_pose == False:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            elif 0 <= self.player.index <= 3:
                self.direction = pygame.Vector2(0, 1)
            elif 4 <= self.player.index <= 7:
                self.direction = pygame.Vector2(-1, 0)
            elif 8 <= self.player.index <= 11:
                self.direction = pygame.Vector2(1, 0)
            else:
                self.direction = pygame.Vector2(0, -1)

            self.rect.x += self.direction.x * self.SP
            self.rect_move_y += self.direction.y * self.SP

    def update(self):
        super().update()
        self.move()


class Syuriken(Weapon):
    def __init__(self, groups, image, AT, SP, size, cooltime, player, x, y):
        super().__init__(groups, image, AT, SP, size, cooltime, player, x, y)
        player_pos = pygame.math.Vector2(self.player.rect.center)
        self.direction = -(player_pos - self.player.nearest_enemy_now)
        self.timer = 0

    def move(self):
        if self.player.game_pose == False:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.rect.centerx += self.direction.x * self.SP
            self.rect_move_y += self.direction.y * self.SP

    def self_kill(self):
        if pygame.sprite.spritecollide(self, self.enemy_group, False):
            self.timer += 1
            if self.timer >= 5:
                self.kill()
                self.timer = 0

    def update(self):
        super().update()
        self.move()
        self.self_kill()


class Bom(Weapon):
    def __init__(self, groups, image, AT, SP, size, cooltime, player, x, y):
        super().__init__(groups, image, AT, SP, size, cooltime, player, x, y)
        self.direction = self.player.direction
        self.BomTimer = 0
        #  0  1  2  3 (1) ↓
        #  4  5  6  7 (5) ←
        #  8  9  10 11(9) →
        #  12 13 14 15(13) ↑
        if 0 <= self.player.index <= 3:
            self.rect_move_y += int(self.image_size.x * 0.8)
        elif 4 <= self.player.index <= 7:
            self.rect.centerx -= int(self.image_size.x * 0.8)
        elif 8 <= self.player.index <= 11:
            self.rect.centerx += int(self.image_size.x*0.8)
        else:
            self.rect_move_y -= int(self.image_size.x*0.8)

    def boom(self):
        if self.BomTimer == 90:
            self.kill()

    def update(self):
        super().update()
        self.BomTimer += 1
        self.boom()


class Beam(Weapon):
    def __init__(self, groups, image, AT, SP, size, cooltime, player, x, y):
        super().__init__(groups, image, AT, SP, size, cooltime, player, x, y)
        self.beamtimer = 0
        self.move()

    def self_kill(self):
        if self.beamtimer == 80:
            self.kill()

    def move(self):
        self.rect_move_y -= 3 * mapchip_size

    def update(self):
        super().update()
        self.beamtimer += 1
        self.self_kill()
