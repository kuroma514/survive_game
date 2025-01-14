import pygame
from setting import *
from image import *
from enemy_bullet import Enemy_bullet
from enemy_bullet import To_plaeer
from exp import Exp
from weaponmaneger import WeaponManager


class Enemy(pygame.sprite.Sprite):  # 敵の親クラス
    def __init__(self, groups, HP, SP, enemy_num, player, enemy_group, x, y, exp):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        # グループ
        self.enemy_group = enemy_group
        self.bullet_group = pygame.sprite.Group()

        # ステータス
        self.HP = HP
        self.SP = SP
        self.enemy_num = enemy_num
        self.frame = 0
        self.x = x
        self.y = y
        self.rect_move_y = 0
        self.index_max = 0
        self.exp = exp

        # 画像読み込み
        self.enemy_pop = pygame.Vector2(self.x, self.y)
        self.enemy_size = pygame.Vector2(32, 32)
        self.index = 0
        if enemy_num == "suraimu":
            self.image_list = suraimu_image_list
            self.index_max = 4
        if enemy_num == "ScaryBat":
            self.image_list = bat_image_list
            self.index_max = 3

        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.enemy_size)

        self.rect = self.image.get_rect(
            x=self.enemy_pop.x * mapchip_size, y=self.enemy_pop.y * mapchip_size)

        # 他クラスを参照
        self.player = player
        self.camera_y = 0
        self.target_pos = pygame.Vector2(0, 0)

        # 当たった武器の記録用
        self.collided_weapon = []

    def enemy_image_update(self):  # アニメーション
        self.index = self.frame // 10 % self.index_max
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.enemy_size)

    def enemy_scroll(self):
        self.rect.centery = (self.enemy_pop.y * mapchip_size) + \
            (map_h - screen_h) - self.camera_y + self.rect_move_y

    def check_collision_with_others(self):  # 衝突判定
        # 他のエネミーと衝突をチェック
        for other_enemy in self.enemy_group:
            if other_enemy == self:
                continue

            if self.rect.colliderect(other_enemy.rect):
                # 衝突を回避する処理
                direction = pygame.math.Vector2(
                    self.rect.center) - pygame.math.Vector2(other_enemy.rect.center)
                if direction.length() != 0:
                    direction = direction.normalize()  # ベクトルを正規化
                    self.rect.x += direction.x * self.SP * 1.5
                    self.rect.y += direction.y * self.SP * 1.5

    # def collision_weapon(self):
    #     for weapon in self.player.weapon_group:
    #         if pygame.sprite.spritecollide(self, weapon, True):
    #             self.HP -= weapon.AT
    #         if self.HP <= 0:
    #             self.kill()

    # def damage(self):
    #     self.weapon_manager = WeaponManager(self)
    #     print(self.weapon_manager.weapon_group)
    #     for weapon in self.weapon_manager.weapon_group:
    #         if self.rect.colliderect(weapon.rect):
    #             # 初めて当たった弾の場合のみダメージを受ける
    #             if weapon not in self.collided_weapon:
    #                 self.HP -= weapon.AT
    #                 self.collided_weapon.append(weapon)  # 衝突済みとして記録
    #             if self.HP <= 0:
    #                 exp = Exp(exp_group, self.player,
    #                           self.rect.centerx, self.rect_move_y +
    #                           (self.enemy_pop.y*mapchip_size), self.exp)
    #                 exp_group.add(exp)
    #                 self.kill()

    def damage(self, AT):
        self.HP -= AT
        if self.HP <= 0:
            exp = Exp(exp_group, self.player,
                      self.rect.centerx, self.rect_move_y +
                      (self.enemy_pop.y*mapchip_size), self.exp)
            exp_group.add(exp)
            self.kill()

    def move(self, dx, dy):
        # 新しい位置に移動
        self.rect.x += dx
        self.rect_move_y += dy

    def update(self):
        self.frame += 1
        self.enemy_scroll()
        self.enemy_image_update()
        self.camera_y = self.player.camera_y


class Shortrange(Enemy):
    def __init__(self, groups, HP, SP, image, player, enemy_group, x, y, exp):
        super().__init__(groups, HP, SP, image, player, enemy_group, x, y, exp)

    def move_towards_player(self):
        # プレイヤーと敵の位置を取得
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        # プレイヤーへの方向を計算
        direction = player_pos - enemy_pos

        self.check_collision_with_others()
        # 距離がゼロでなければ方向を正規化して移動
        if direction.length() != 0:
            direction = direction.normalize()  # ベクトルを正規化
            self.move(direction.x * self.SP, direction.y * self.SP)

    def update(self):
        super().update()
        self.move_towards_player()


class Longrange(Enemy):
    def __init__(self, groups, HP, SP, image, player, enemy_group, x, y, exp, range):
        super().__init__(groups, HP, SP, image, player, enemy_group, x, y, exp)
        self.distance = 0
        self.range = range * 48
        self.timer = 0
        self.num = image

    def move_towards_player(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        direction = player_pos - enemy_pos
        self.distance = player_pos.distance_to(enemy_pos)

        self.check_collision_with_others()

        if self.range * 0.8 <= self.distance <= self.range * 1.2:
            return
        elif self.range * 0.8 >= self.distance:
            direction = direction.normalize()
            self.move(-direction.x * self.SP * 0.8, -
                      direction.y * self.SP * 0.8)
        elif direction.length() != 0:
            direction = direction.normalize()
            self.move(direction.x * self.SP, direction.y * self.SP)

    def shoot(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        if self.timer >= 180:
            direction = player_pos - pygame.math.Vector2(self.rect.center)
            if self.num == "ScaryBat":
                bullet_to_player = To_plaeer(
                    self.bullet_group, 1.5, "Fire Effect and Bullet",
                    self.rect.centerx, self.rect_move_y +
                    (self.enemy_pop.y*mapchip_size), self.player, direction
                )
                self.bullet_group.add(bullet_to_player)  # グループに追加
            self.timer = 0

    def update(self):
        super().update()
        self.move_towards_player()
        self.shoot()
        self.bullet_group.update()  # バレットの更新
        self.bullet_group.draw(self.screen)  # バレットの描画
        self.timer += 1
