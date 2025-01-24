import pygame
from setting import *
from image import *


class Enemy_bullet(pygame.sprite.Sprite):  # 敵弾の親クラス
    def __init__(self, groups, SP, image, x, y, player):
        super().__init__(groups)  # 可変長引数でグループを展開

        # ステータス
        self.SP = SP
        self.image_name = image
        self.bullet_pop = pygame.Vector2(x, y)  # エネミーの位置を取得
        self.rect_move_y = 0
        self.frame = 0

        # プレイヤーくらすを参照
        self.player = player
        self.camera_y = 0

        # 画像の取得
        self.index = 0
        if self.image_name == "Fire Effect and Bullet":
            self.image_list = red_bullet_image_list
            self.index_max = 4
            self.enemy_size = pygame.Vector2(16, 16)

        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.enemy_size)

        self.rect = self.image.get_rect(center=(x, y))

    def scroll(self):
        self.rect.centery = (self.bullet_pop.y) + \
            (map_h - screen_h) - self.camera_y + self.rect_move_y

    def image_update(self):
        if self.player.game_pose == False:
            self.index = self.frame // 5 % self.index_max
            self.pre_image = self.image_list[self.index]
            self.image = pygame.transform.scale(
                self.pre_image, self.enemy_size)

    def self_kill(self):
        if self.rect.left < 0 or self.rect.right > screen_w:
            self.kill()

    def update(self):
        self.camera_y = self.player.camera_y
        # カメラオフセットを適用
        self.scroll()
        self.image_update()
        self.self_kill()
        self.frame += 1


class To_plaeer(Enemy_bullet):
    def __init__(self, groups, SP, image, x, y, player, direction):
        super().__init__(groups, SP, image, x, y, player)

        # プレイヤーへの方向を計算
        self.direction = direction

    def move_towards_player(self):
        if self.player.game_pose == False:
            if self.direction.length() != 0:
                self.direction = self.direction.normalize()  # ベクトルを正規化
                self.rect.centerx += self.direction.x * self.SP
                self.rect_move_y += self.direction.y * self.SP

    def update(self):
        super().update()
        self.move_towards_player()
