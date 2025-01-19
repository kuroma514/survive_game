import pygame
import pygame_gui
import math
from setting import *
from enemy import Enemy
from weapons import Weapon
from weapons import Waterball
from weapons import Syuriken
from Level import LevelSystem
from weaponmaneger import WeaponManager


class Player(pygame.sprite.Sprite):

    def __init__(self, groups, HP, SP, AT, bullet_size, bullet_speed, catch_range, cooltime, image, enemy_group):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface((map_w, map_h))
        self.enemy_group = enemy_group
        self.game_pose = False

        # ステータス
        self.HP = HP
        self.initial_HP = HP
        self.AT_level = 1
        self.SP_level = 1
        self.bullet_size_level = 1
        self.bullet_speed_level = 1
        self.cooltime_level = 1
        self.catch_range_level = 1

        self.initial_AT = AT
        self.initial_bullet_size = bullet_size
        self.initial_bullet_speed = bullet_speed
        self.initial_SP = SP
        self.initial_cooltime = cooltime
        self.initial_catch_range = catch_range

        self.AT = self.initial_AT * self.AT_level
        self.bullet_size = self.initial_bullet_size * self.bullet_size_level
        self.bullet_speed = self.initial_bullet_speed * self.bullet_speed_level
        self.SP = self.initial_SP * self.SP_level
        self.cooltime = self.initial_cooltime * self.cooltime_level
        self.catch_range = self.initial_catch_range * \
            self.catch_range_level * mapchip_size

        self.image = image
        self.frame = 0
        self.timer = 0
        self.level_system = LevelSystem(self)

        self.weapon_manager = WeaponManager(self, enemy_group)
        self.weapon_manager.add_weapon("Syuriken", 2000, 35, 3.5)
        self.level_system.SyurikenLevel += 1

        # 仮
        self.HP -= 2

        # 移動
        self.direction = pygame.math.Vector2(0, 0)
        # self.SP = SP

        # プレイヤー画像読み込み
        self.Player_pop = pygame.Vector2(7, 7)
        self.Player_size = pygame.Vector2(48, 48)
        self.Player_image_date = pygame.image.load(
            f'mono/image/players/{image}.png')

        # プレイヤー画像切り取り
        self.image_list = []
        for i in range(4):
            for j in range(3):
                self.Player_image_pose = pygame.Vector2(32 * j, 32 * i)
                self.Player_image_cut_size = pygame.Vector2(32, 32)
                cut_image = self.Player_image_date.subsurface(
                    pygame.Rect(self.Player_image_pose, self.Player_image_cut_size))
                self.image_list.append(cut_image)
            self.Player_image_pose = pygame.Vector2(32, 32 * i)
            self.Player_image_cut_size = pygame.Vector2(32, 32)
            cut_image = self.Player_image_date.subsurface(
                pygame.Rect(self.Player_image_pose, self.Player_image_cut_size))
            self.image_list.append(cut_image)

        self.index = 11
        #  0  1  2  3 (1) ↓
        #  4  5  6  7 (5) ←
        #  8  9  10 11(9) →
        #  12 13 14 15(13) ↑
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(
            self.pre_image, self.Player_size)

        # 画像をRectオブジェクトとして取得
        self.rect = self.image.get_rect(
            x=self.Player_pop.x * mapchip_size, y=self.Player_pop.y * mapchip_size)
        self.camera_y = map_h - screen_h

        self.heart_image_set()

        self.last_damage_time = 0
        self.muteki_time = 1000
        self.Alive = True

        # マップチップ
        self.mapchip_iamge_list = []

        self.YellowGreen_grass_image_date = pygame.image.load(
            f'mono/image/map/YellowGreen_grass.png')
        grass_cut_image = self.YellowGreen_grass_image_date.subsurface(
            pygame.Rect((0, 128), (32, 32)))
        self.mapchip_iamge_list.append(grass_cut_image)

        self.Flower_image_date = pygame.image.load(
            f'mono/image/map/Flower.png')
        Flower_cut_image = self.Flower_image_date.subsurface(
            pygame.Rect((0, 0), (32, 32)))
        self.mapchip_iamge_list.append(Flower_cut_image)

        self.mapchip_iamge_list_index = 0
        self.mapchip_pre_image = self.mapchip_iamge_list[self.mapchip_iamge_list_index]
        self.mapchip_image = pygame.transform.scale(
            self.mapchip_pre_image, (mapchip_size, mapchip_size))

    def status_update(self):
        self.AT = self.initial_AT * self.AT_level
        self.bullet_size = self.initial_bullet_size * self.bullet_size_level
        self.bullet_speed = self.initial_bullet_speed * self.bullet_speed_level
        self.SP = self.initial_SP * self.SP_level
        self.cooltime = self.initial_cooltime * self.cooltime_level
        self.catch_range = self.initial_catch_range * \
            self.catch_range_level * mapchip_size

    def screen_byouga(self):
        self.screen.blit(background, (0, -self.camera_y))
        for i in range(16):
            for j in range(10):
                background.blit(self.mapchip_image,
                                (i*48, self.camera_y + j*48))

    def gain_experience(self, amount):
        """経験値を獲得"""
        self.level_system.add_experience(amount)

    def input(self):
        if self.game_pose == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] or key[pygame.K_w]:
                self.direction.y = -1
                self.index = self.frame//12 % 4 + 12
            elif key[pygame.K_DOWN] or key[pygame.K_s]:
                self.direction.y = 1
                self.index = self.frame//12 % 4
            else:
                self.direction.y = 0

            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.direction.x = -1
                self.index = (self.frame//12 % 4)+4
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.direction.x = 1
                self.index = (self.frame//12 % 4)+8
            else:
                self.direction.x = 0

    def move(self):
        if self.game_pose == False:
            # ベクトルの向きを固定して大きさを1にする(斜め移動の速度調整)
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.rect.x += self.direction.x * self.SP
            self.check_screen_line()
            self.camera_y += self.direction.y * self.SP
            self.check_screen_line()

    def check_screen_line(self):
        # スクリーンからキャラが出ないようにする
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_w:
            self.rect.right = screen_w
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > screen_h:
        #     self.rect.bottom = screen_h

    def image_update(self):
        if self.game_pose == False:
            # キーを話したときに両足をつくアニメーションにする
            if self.direction.x == 0 and self.direction.y == 0 and 0 <= self.index <= 3:
                self.index = 1
            elif self.direction.x == 0 and self.direction.y == 0 and 4 <= self.index <= 7:
                self.index = 5
            elif self.direction.x == 0 and self.direction.y == 0 and 8 <= self.index <= 11:
                self.index = 9
            elif self.direction.x == 0 and self.direction.y == 0 and 12 <= self.index <= 15:
                self.index = 13

            self.pre_image = self.image_list[self.index]
            self.image = pygame.transform.scale(
                self.pre_image, self.Player_size)

    def heart_image_set(self):
        self.heart_image_list = []
        self.heart_pop = pygame.Vector2(1, 1)
        self.heart_size = pygame.Vector2(32, 32)

        # 画像の読み込み
        self.red_heart_image_date = pygame.image.load(
            f'mono/image/other/red_heart.png')
        self.black_heart_image_date = pygame.image.load(
            f'mono/image/other/black_heart.png')

        self.red_heart_image = pygame.transform.scale(
            self.red_heart_image_date, (32, 32))
        self.black_heart_image = pygame.transform.scale(
            self.black_heart_image_date, (32, 32))
        for i in range(self.HP):
            self.screen.blit(self.red_heart_image, (i*32, 0))
        for i in range(self.initial_HP - self.HP):
            self.screen.blit(self.black_heart_image, (self.HP*32 + i*32, 0))

    def collision(self):
        if self.game_pose == False:
            self.current_time = pygame.time.get_ticks()  # 現在の時刻を取得
            if pygame.sprite.spritecollide(self, self.enemy_group, False):
                if self.current_time - self.last_damage_time > self.muteki_time:  # 1秒間は無敵
                    self.HP -= 1
                    self.last_damage_time = self.current_time
                if self.HP <= 0:
                    self.Alive = False
            # Trueで弾を削除
            for enemy in self.enemy_group:
                if pygame.sprite.spritecollide(self, enemy.bullet_group, True):
                    if self.current_time - self.last_damage_time > self.muteki_time:  # 無敵時間チェック
                        self.HP -= 1
                        self.last_damage_time = self.current_time
                    if self.HP <= 0:
                        self.Alive = False

    def find_nearest_enemy(self):
        """最も近いエネミーを返す"""
        self.nearest_enemy = None
        min_distance = float('inf')  # 初期値を無限大に設定

        for enemy in self.enemy_group:
            # プレイヤーとエネミーの距離を計算
            distance = math.sqrt((self.rect.centerx - enemy.rect.centerx)**2 +
                                 (self.rect.centery - enemy.rect.centery)**2)
            if distance < min_distance:
                min_distance = distance
                self.nearest_enemy = enemy
        self.nearest_enemy_now = pygame.Vector2(
            self.nearest_enemy.rect.centerx, self.nearest_enemy.rect.centery)

    def update(self):
        self.input()
        self.move()
        self.image_update()
        self.screen_byouga()
        self.heart_image_set()
        self.collision()
        self.find_nearest_enemy()
        self.weapon_manager.update()
        self.level_system.update()
        self.status_update()
        self.frame += 1
        self.timer += 1
