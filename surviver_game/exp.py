import pygame
from setting import *
from image import *
from Level import *


class Exp(pygame.sprite.Sprite):
    def __init__(self, groups, player, x, y, exp):
        super().__init__(groups)
        self.exp_value = exp
        self.player = player
        self.pop = pygame.Vector2(x, y)
        self.rect_move_y = 0
        self.camera_y = 0
        self.frame = 0

        # 画像の取得
        self.index = 0
        self.image_list = exp_image_list
        self.index_max = 3
        self.image_size = pygame.Vector2(16, 16)

        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.image_size)

        self.rect = self.image.get_rect(center=(x, y))

    def scroll(self):
        self.rect.centery = (self.pop.y) + \
            (map_h - screen_h) - self.camera_y + self.rect_move_y

    def self_kill(self):
        if self.rect.left < 0 or self.rect.right > screen_w + 200:
            self.kill()

    def image_update(self):
        self.index = self.frame // 10 % self.index_max
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.image_size)

    def move(self):
        # プレイヤーと敵の位置を取得
        player_pos = pygame.math.Vector2(self.player.rect.center)
        exp_pos = pygame.math.Vector2(self.rect.center)

        # プレイヤーへの方向を計算
        direction = player_pos - exp_pos
        self.distance = player_pos.distance_to(exp_pos)
        if self.distance <= self.player.catch_range:
            # 距離がゼロでなければ方向を正規化して移動
            if direction.length() != 0:
                direction = direction.normalize()  # ベクトルを正規化
                self.rect.centerx += direction.x * 5
                self.rect_move_y += direction.y * 5

    def collition(self):
        if self.distance <= 24:
            self.player.gain_experience(self.exp_value)
            self.kill()

    def update(self):
        self.camera_y = self.player.camera_y
        self.scroll()
        self.move()
        self.self_kill()
        self.image_update()
        self.collition()
        self.frame += 1
