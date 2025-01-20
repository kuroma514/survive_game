import pygame
import pygame_gui
import math
import random
from setting import *
from enemy import Enemy
from enemy import Shortrange
from enemy import Longrange
from weapons import Weapon
from weapons import Waterball
from weapons import Syuriken
from Level import LevelSystem
from weaponmaneger import WeaponManager


class Player(pygame.sprite.Sprite):

    def __init__(self, groups, HP, SP, AT, bullet_size, bullet_speed, catch_range, cooltime, image):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface((map_w, map_h))
        self.enemy_group = pygame.sprite.Group()
        self.game_pose = False
        self.enemy_test = Enemy(self.enemy_group, 100, 1,
                                'suraimu', self, self.enemy_group, 4, 4, 15)
        self.enemy_kotei = Enemy(self.enemy_group, 100, 1,
                                 'suraimu', self, self.enemy_group, 8, -400, 100)

        # ステータス
        self.HP = HP
        self.initial_HP = HP
        self.AT_level = 1
        self.SP_level = 1
        self.bullet_size_level = 1
        self.bullet_speed_level = 1
        self.cooltime_level = 1
        self.catch_range_level = 1
        self.Far = 0
        self.SpawnTimer = 0

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
        self.EnemyKillTime = 0
        self.level_system = LevelSystem(self)

        self.weapon_manager = WeaponManager(self, self.enemy_group)
        self.weapon_manager.add_weapon("Syuriken", 2000, 35, 3.5, 1)
        self.level_system.SyurikenLevel += 1
        self.SpawnPopX = 0
        self.SpawnPopY = 0

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

        self.game_timer = 0
        self.game_time = 0

    def GameOver(self):
        if self.HP == 0:
            rect = pygame.Rect((100, 100, 600, 200))
            pygame.draw.rect(self.screen, BLACK, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 2)

            font_size = 32
            font = pygame.font.Font(None, font_size)  # デフォルトフォントを使用
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=rect.center)

            self.screen.blit(text, text_rect)
            self.game_pose = True

    def GameClear(self):
        if self.Far >= 450:
            rect = pygame.Rect((100, 100, 600, 200))
            pygame.draw.rect(self.screen, BLACK, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 2)

            font_size = 32
            font = pygame.font.Font(None, font_size)  # デフォルトフォントを使用
            text = font.render("Game Clear", True, WHITE)
            text_rect = text.get_rect(center=rect.center)

            self.screen.blit(text, text_rect)
            self.game_pose = True

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

    def DrawFar(self):
        font_size = 16
        font = pygame.font.Font(font_path, font_size)
        self.Far = int(-(self.camera_y - map_h) / mapchip_size)
        text_surface = font.render(f"{self.Far}/450 m", True, (255, 255, 255))
        self.screen.blit(text_surface, (690, 10))
        self.game_time = self.game_timer // 60
        time_surface = font.render(
            f"{self.game_time}", True, (255, 255, 255))
        self.screen.blit(time_surface, (720, 30))

    def SpawnPopSet(self):
        self.SpawnPopX = round(random.uniform(0.5, 15.5), 1)
        pop_y = round(random.uniform(0.5, 3), 1)
        self.SpawnPopY = pop_y + \
            (((map_h - screen_h) - self.camera_y) / 2 / mapchip_size)

    def SpawnEnemy(self):
        if self.game_pose == False:
            if self.Far <= 30 and self.SpawnTimer == 180:
                SpawnNum = self.Far // 10
                self.SpawnTimer = 0
                for i in range(SpawnNum):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 100, 1,
                                            'suraimu', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 20)
            elif self.Far <= 70 and self.SpawnTimer == 180:
                SpawnNum1 = self.Far//10
                SpawnNum2 = self.Far//20
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 100, 1,
                                            'suraimu', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 20)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 200, 0.7,
                                           "ScaryBat", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 40, 5)

            elif self.Far <= 120 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 50) // 10
                SpawnNum2 = (self.Far - 60) // 15 + 1
                SpawnNum3 = self.Far // 20
                self.SpawnTimer = 0
                for i in range(SpawnNum3):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 100, 1,
                                            'suraimu', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 20)
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.5,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 70)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 200, 0.7,
                                           "ScaryBat", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 40, 5)
            elif self.Far <= 170 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 100) // 10 + 3
                SpawnNum2 = (self.Far - 100) // 20
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.5,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 70)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 400, 2,
                                           "mush", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100, 4)
            elif self.Far <= 220 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 160) // 10
                SpawnNum2 = (self.Far - 160) // 20
                SpawnNum3 = 1
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.5,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 70)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 400, 2,
                                           "mush", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100, 4)
                for i in range(SpawnNum3):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 600, 2.5,
                                            'reaper', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 250)
            elif self.Far <= 280 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 180) // 10
                SpawnNum2 = (self.Far - 180) // 15
                SpawnNum3 = 1
                SpawnNum4 = 1
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.7,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 50)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 400, 2,
                                           "mush", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 60, 4)
                for i in range(SpawnNum3):
                    random_number = random.randint(0, 1)
                    if random_number == 1:
                        self.SpawnPopSet()
                        self.enemy = Shortrange(self.enemy_group, 600, 2.5,
                                                'reaper', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100)
                for i in range(SpawnNum4):
                    random_number = random.randint(0, 1)
                    if random_number == 1:
                        self.SpawnPopSet()
                        self.enemy = Shortrange(self.enemy_group, 1000, 1,
                                                'Golem', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 200)
            elif self.Far <= 360 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 220) // 10
                SpawnNum2 = (self.Far - 260) // 15
                SpawnNum3 = 1
                SpawnNum4 = 2
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.7,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 50)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 400, 2,
                                           "mush", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 60, 4)
                for i in range(SpawnNum3):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 600, 2.5,
                                            'reaper', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100)
                for i in range(SpawnNum4):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 1000, 1,
                                            'Golem', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 200)
            elif self.Far <= 400 and self.SpawnTimer == 180:
                SpawnNum1 = (self.Far - 300) // 15
                SpawnNum2 = (self.Far - 300) // 20
                SpawnNum3 = 2
                SpawnNum4 = (self.Far - 300) // 20
                self.SpawnTimer = 0
                for i in range(SpawnNum1):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 300, 1.7,
                                            'frog', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 50)
                for i in range(SpawnNum2):
                    self.SpawnPopSet()
                    self.enemy = Longrange(self.enemy_group, 400, 2,
                                           "mush", self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 60, 4)
                for i in range(SpawnNum3):
                    random_number = random.randint(0, 1)
                    if random_number == 1:
                        self.SpawnPopSet()
                        self.enemy = Shortrange(self.enemy_group, 600, 2.5,
                                                'reaper', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100)
                for i in range(SpawnNum4):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 1000, 1,
                                            'Golem', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 200)
            elif self.Far <= 450 and self.SpawnTimer == 180:
                SpawnNum3 = 2
                SpawnNum4 = (self.Far - 300) // 10 + 2
                self.SpawnTimer = 0
                for i in range(SpawnNum3):
                    random_number = random.randint(0, 1)
                    if random_number == 1:
                        self.SpawnPopSet()
                        self.enemy = Shortrange(self.enemy_group, 600, 2.5,
                                                'reaper', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 100)
                for i in range(SpawnNum4):
                    self.SpawnPopSet()
                    self.enemy = Shortrange(self.enemy_group, 1000, 1,
                                            'Golem', self, self.enemy_group, self.SpawnPopX, -self.SpawnPopY, 200)
            self.SpawnTimer += 1

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
        self.DrawFar()
        self.SpawnEnemy()
        self.frame += 1
        self.timer += 1
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.GameOver()
        self.GameClear()
        if self.game_pose == False:
            self.game_timer += 1
