import pygame
import random
import textwrap
from setting import *
from image import *


class LevelSystem:
    def __init__(self, player):
        self.player = player
        self.screen = self.player.screen
        self.level = 1
        self.timer = 0
        self.current_experience = 0
        self.experience_to_next_level = 1  # 次のレベルまでに必要な経験値
        self.selection = False
        self.font_title_size = 24
        self.font_desc_size = 16
        self.font_title = pygame.font.Font(font_path, self.font_title_size)
        self.font_desc = pygame.font.Font(font_path, self.font_desc_size)
        self.image_size = 0
        self.cursor_index = 0
        self.PressAmout = 0
        self.WaterballLevel = 0
        self.SyurikenLevel = 0
        self.BomLevel = 0
        self.BeamLevel = 0
        self.skills = [
            {"type": "weapon", "name": "手裏剣",
                "description": "敵に向かって手裏剣を投げる"},
            {"type": "weapon", "name": "水魔法",
                "description": "前方に水の魔法弾を放つ"},
            {"type": "weapon", "name": "手榴弾",
                "description": "前方に爆発を放つ"},
            {"type": "weapon", "name": "ビーム",
             "description": "上方向に巨大なビームを放つ"},
            {"type": "weapon", "name": "ケチになる",
                "description": "経験値の獲得範囲が30%上がる"},
            {"type": "skill", "name": "筋トレ",
                "description": "攻撃力が10%上昇する"},
            {"type": "skill", "name": "速度アップ",
                "description": "足が10%速くなる"},
            {"type": "skill", "name": "きようになる",
                "description": "攻撃頻度が10%短くなる"},
            {"type": "skill", "name": "おおきくする",
                "description": "発射物が15%大きくなる"},
            {"type": "skill", "name": "肩力アップ",
                "description": "発射物の速度が20%速くなる"},
            {"type": "skill", "name": "ヒール",
                "description": "HPを2回復する"},
        ]
        self.status = [
            {"name": "体力    ", "value": f"{int(self.player.initial_HP)}"},
            {"name": "攻撃    ", "value": f"{int(self.player.AT * 100)}%"},
            {"name": "速度    ", "value": f"{int(self.player.SP / 3 * 100)}%"},
            {"name": "攻撃範囲",
                "value": f"{int(self.player.bullet_size * 100)}%"},
            {"name": "回収範囲",
                "value": f"{int(self.player.catch_range / 1.5 / (mapchip_size) * 100)}%"},
            {"name": "発射速度",
                "value": f"{int(self.player.bullet_speed * 100)}%"},
            {"name": "攻撃速度", "value": f"{int(self.player.cooltime * 100)}%"},
        ]
        self.selected_skills = []

    def status_update(self):
        self.status = [
            {"name": "体力    ", "value": f"{int(self.player.initial_HP)}"},
            {"name": "攻撃    ", "value": f"{int(self.player.AT * 100)}%"},
            {"name": "速度    ", "value": f"{int(self.player.SP / 3 * 100)}%"},
            {"name": "攻撃範囲",
                "value": f"{int(self.player.bullet_size * 100)}%"},
            {"name": "回収範囲",
                "value": f"{int(self.player.catch_range / 1.5 / (mapchip_size) * 100)}%"},
            {"name": "発射速度",
                "value": f"{int(self.player.bullet_speed * 100)}%"},
            {"name": "攻撃速度", "value": f"{int(self.player.cooltime * 100)}%"},
        ]

    def effect_levelup(self):
        if self.PressAmout == 0:
            self.PressAmout = 1
            for i, skill in enumerate(self.selected_skills):
                if i == self.cursor_index:
                    if skill["name"] == "ケチになる":
                        self.player.catch_range_level += 0.3
                    elif skill["name"] == "筋トレ":
                        self.player.AT_level += 0.1
                    elif skill["name"] == "速度アップ":
                        self.player.SP_level += 0.1
                    elif skill["name"] == "きようになる":
                        self.player.cooltime_level *= 0.9
                    elif skill["name"] == "おおきくする":
                        self.player.bullet_size_level += 0.15
                    elif skill["name"] == "肩力アップ":
                        self.player.bullet_speed_level += 0.2
                    elif skill["name"] == "ヒール":
                        self.player.HP = self.player.initial_HP
                    elif skill["name"] == "水魔法":
                        if self.WaterballLevel == 0:
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 3000, 60, 2, 1)
                            skill["description"] = "水魔法のレベルが上昇し、与えるダメージの基礎値が30増加"
                        elif self.WaterballLevel == 1:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 3000, 90, 2, 1)
                            skill["description"] = "水魔法のレベルが上昇し、クールタイムの基礎値が0.6秒減少"
                        elif self.WaterballLevel == 2:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 2400, 90, 2, 1)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃範囲の基礎値が40%上昇"
                        elif self.WaterballLevel == 3:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 2400, 90, 2, 1.4)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃の基礎値が30上昇"
                        elif self.WaterballLevel == 4:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 2400, 120, 2, 1.4)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃速度の基礎値が0.6秒減少"
                        elif self.WaterballLevel == 5:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 1800, 120, 2, 1.4)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃範囲の基礎値が40%上昇し、さらに発射速度の基礎値が50%上昇"
                        elif self.WaterballLevel == 6:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 1800, 120, 3, 1.8)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃の基礎値が30上昇"
                        elif self.WaterballLevel == 7:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 1800, 150, 2, 1.8)
                            skill["description"] = "水魔法のレベルが上昇し、クールタイムの基礎値が0.4秒減少"
                        elif self.WaterballLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 1400, 150, 2, 1.8)
                            skill["description"] = "水魔法のレベルが上昇し、攻撃範囲の基礎値が120%上昇"
                        elif self.WaterballLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Waterball")
                            self.player.weapon_manager.add_weapon(
                                "Waterball", 1400, 150, 3, 3)
                            skill["description"] = "これ以上レベルは上がらない"

                        self.WaterballLevel += 1
                    elif skill["name"] == "手裏剣":
                        if self.SyurikenLevel == 0:
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 2000, 35, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、与えるダメージの基礎値が15増加"
                        elif self.SyurikenLevel == 1:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 2000, 50, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、クールタイムの基礎値が0.4秒減少"
                        elif self.SyurikenLevel == 2:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 1600, 50, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、クールタイムの基礎値が0.3秒減少"
                        elif self.SyurikenLevel == 3:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 1300, 50, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、攻撃の基礎値が15上昇"
                        elif self.SyurikenLevel == 4:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 1300, 65, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、クールタイムの基礎値が0.4秒減少"
                        elif self.SyurikenLevel == 5:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 900, 65, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、攻撃の基礎値が10上昇"
                        elif self.SyurikenLevel == 6:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 900, 75, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、攻撃の基礎値が15上昇"
                        elif self.SyurikenLevel == 7:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 900, 90, 3.5, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、クールタイムの基礎値が0.2秒減少"
                        elif self.SyurikenLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 700, 90, 5.3, 1)
                            skill["description"] = "手裏剣のレベルが上昇し、攻撃が20上昇し、さらにクールタイムの基礎値が0.3秒減少し、さらに発射速度の基礎値が50%上昇"
                        elif self.SyurikenLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Syuriken")
                            self.player.weapon_manager.add_weapon(
                                "Syuriken", 400, 110, 5.3, 1)
                            skill["description"] = "これ以上レベルは上がらない"

                        self.SyurikenLevel += 1

                    elif skill["name"] == "手榴弾":
                        if self.BomLevel == 0:
                            self.player.weapon_manager.add_weapon(
                                "Bom", 3500, 80, 3, 1)
                            skill["description"] = "手榴弾のレベルが上昇し、与えるダメージの基礎値が30増加"
                        elif self.BomLevel == 1:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 3500, 110, 3, 1)
                            skill["description"] = "手榴弾のレベルが上昇し、クールタイムの基礎値が0.7秒減少"
                        elif self.BomLevel == 2:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2800, 110, 3, 1)
                            skill["description"] = "手榴弾のレベルが上昇し、攻撃範囲の基礎値が20%上昇"
                        elif self.BomLevel == 3:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2800, 110, 3, 1.2)
                            skill["description"] = "手榴弾のレベルが上昇し、攻撃の基礎値が30上昇"
                        elif self.BomLevel == 4:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2800, 140, 3, 1.2)
                            skill["description"] = "手榴弾のレベルが上昇し、クールタイムの基礎値が0.5秒減少"
                        elif self.BomLevel == 5:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2300, 140, 3, 1.2)
                            skill["description"] = "手榴弾のレベルが上昇し、攻撃範囲が20%上昇"
                        elif self.BomLevel == 6:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2300, 140, 3, 1.4)
                            skill["description"] = "手榴弾のレベルが上昇し、攻撃が30上昇"
                        elif self.BomLevel == 7:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 2300, 170, 3, 1.4)
                            skill["description"] = "手榴弾のレベルが上昇し、クールタイムが0.5秒減少"
                        elif self.BomLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 1800, 170, 3, 1.4)
                            skill["description"] = "手榴弾のレベルが上昇し、攻撃が20上昇し、さらにクールタイムが0.4秒減少し、さらに攻撃範囲が30%上昇"
                        elif self.BomLevel == 9:
                            self.player.weapon_manager.remove_weapon(
                                "Bom")
                            self.player.weapon_manager.add_weapon(
                                "Bom", 1400, 190, 3, 1.7)
                            skill["description"] = "これ以上レベルは上がらない"
                        self.BomLevel += 1
                    elif skill["name"] == "ビーム":
                        if self.BeamLevel == 0:
                            self.player.weapon_manager.add_weapon(
                                "Beam", 4000, 40, 3, 1)
                            skill["description"] = "ビームのレベルが上昇し、与えるダメージの基礎値が25増加"
                        elif self.BeamLevel == 1:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 4000, 65, 3, 1)
                            skill["description"] = "ビームのレベルが上昇し、クールタイムの基礎値が0.8秒減少"
                        elif self.BeamLevel == 2:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 3200, 65, 2, 1)
                            skill["description"] = "ビームのレベルが上昇し、攻撃範囲の基礎値が30%上昇"
                        elif self.BeamLevel == 3:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 3200, 65, 2, 1.3)
                            skill["description"] = "ビームのレベルが上昇し、攻撃の基礎値が20上昇"
                        elif self.BeamLevel == 4:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 3200, 85, 2, 1.3)
                            skill["description"] = "ビームのレベルが上昇し、クールタイムの基礎値が0.6秒減少"
                        elif self.BeamLevel == 5:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 2600, 85, 2, 1.3)
                            skill["description"] = "ビームのレベルが上昇し、攻撃範囲の基礎値が30%上昇"
                        elif self.BeamLevel == 6:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 2600, 85, 2, 1.6)
                            skill["description"] = "ビームのレベルが上昇し、攻撃の基礎値が20上昇"
                        elif self.BeamLevel == 7:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 2600, 105, 2, 1.6)
                            skill["description"] = "ビームのレベルが上昇し、クールタイムの基礎値が0.5秒減少"
                        elif self.BeamLevel == 8:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 2100, 105, 2, 1.6)
                            skill["description"] = "ビームのレベルが上昇し、攻撃範囲の基礎値が40%上昇し、さらに攻撃が25上昇"
                        elif self.BeamLevel == 9:
                            self.player.weapon_manager.remove_weapon(
                                "Beam")
                            self.player.weapon_manager.add_weapon(
                                "Beam", 2100, 110, 2, 2)
                            skill["description"] = "これ以上レベルは上がらない"

                        self.BeamLevel += 1

    def WeaponUpdate(self):
        if self.WaterballLevel == 1:
            self.skills[1]["description"] = "水魔法のレベルが上昇し、与えるダメージの基礎値が20増加"
        if self.SyurikenLevel == 1:
            self.skills[0]["description"] = "手裏剣のレベルが上昇し、与えるダメージの基礎値が10増加"

    def add_experience(self, amount):
        self.current_experience += amount
        while self.current_experience >= self.experience_to_next_level:
            self.current_experience -= self.experience_to_next_level
            self.level_up()

    def draw_description(self, text, rect, max_width):
        """指定した幅で改行してテキストを描画"""
        # 最大文字数で改行
        wrapped_lines = textwrap.wrap(text, width=max_width)

        # テキストの描画
        line_height = self.font_desc_size  # 1行の高さ
        for i, line in enumerate(wrapped_lines):
            text_surface = self.font_desc.render(
                line, True, WHITE)  # 白色で描画
            text_rect = text_surface.get_rect(
                topleft=(rect.left + 5, (rect.top + 10 + 30 + self.image_size) + 5 + i * line_height))
            self.screen.blit(text_surface, text_rect)

    def cursor(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and self.cursor_index < 2 and self.timer > FPS/4:
            self.cursor_index += 1
            self.timer = 0
        if key[pygame.K_a] and 0 < self.cursor_index and self.timer > FPS/4:
            self.cursor_index -= 1
            self.timer = 0

    def draw_status(self):
        if self.selection == True:
            rect = pygame.Rect((200, 40, 400, 100))
            pygame.draw.rect(self.screen, BLACK, rect)
            for i in range(4):
                for j in range(2):
                    index = i * 2 + j  # 総合インデックスを計算
                    if index < len(self.status):
                        status = self.status[index]  # 辞書型の要素を取得
                        text = self.font_desc.render(
                            status["name"] + "：" + status["value"], True, WHITE)
                        text_rect = text.get_rect(topleft=(
                            rect.left + 5 + j*200, (rect.top + 10) + i*self.font_desc_size))
                        self.screen.blit(text, text_rect)

    def draw_skils(self):
        if self.selection == True:
            self.cursor()
            self.draw_status()
            for i, skill in enumerate(self.selected_skills):
                # スキル表示用のボックスを描画
                rect = pygame.Rect((100+i*200, 150, 150, 200))
                if self.cursor_index == i:
                    pygame.draw.rect(self.screen, BLUE, rect)
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)
                # スキル名を表示
                text = self.font_title.render(
                    skill["name"], True, WHITE)
                text_rect = text.get_rect(midtop=(rect.centerx, rect.top + 10))
                self.screen.blit(text, text_rect)
                # スキルのイメージを表示
                self.image_size = 80
                image_rect = pygame.Rect(
                    (rect.centerx - self.image_size / 2), (rect.top + 10 + 30), self.image_size, self.image_size)
                pygame.draw.rect(self.screen, (128, 128, 128), image_rect)
                # スキルの説明を表示
                self.draw_description(
                    skill["description"], rect, max_width=150 // self.font_desc_size)

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.effect_levelup()
            self.selection = False
            self.player.game_pose = False

    def level_up(self):
        self.level += 1
        self.PressAmout = 0
        self.experience_to_next_level = (self.level * self.level) + 20
        self.selection = True
        self.selected_skills = random.sample(self.skills, 3)
        self.player.game_pose = True

    def update(self):
        self.WeaponUpdate()
        self.status_update()
        self.draw_skils()
        self.timer += 1
