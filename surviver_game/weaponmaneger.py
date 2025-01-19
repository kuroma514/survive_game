import pygame
from weapons import *


class WeaponManager:
    def __init__(self, player, enemy_group):
        self.player = player
        self.weapon_cooldowns = {}
        self.enemy_group = enemy_group
        self.weapon_group = pygame.sprite.Group()

    def add_weapon(self, weapon_type, cooltime, AT, bullet_speed):
        """武器を登録し、クールタイムを設定"""
        self.weapon_cooldowns[weapon_type] = {
            "cooltime": cooltime,
            "last_shot_time": 0,
            "AT": AT,
            "bullet_speed": bullet_speed
        }

    def shoot(self):
        if self.player.game_pose == False:
            """武器ごとにクールタイムを考慮して自動発射"""
            current_time = pygame.time.get_ticks()

            for weapon_type, cooldown_info in self.weapon_cooldowns.items():
                if current_time - cooldown_info["last_shot_time"] >= cooldown_info["cooltime"] * self.player.cooltime:
                    # 武器の種類に応じて発射
                    if weapon_type == "Waterball":
                        new_weapon = Waterball(
                            self.weapon_group, "Water Effect and Bullet", cooldown_info[
                                "AT"], cooldown_info["bullet_speed"], 1, 3000, self.player,  # bullet_speed = 2
                            self.player.rect.centerx, self.player.rect.centery)
                    elif weapon_type == "Syuriken":
                        new_weapon = Syuriken(
                            self.weapon_group, "syuriken", cooldown_info[
                                "AT"], cooldown_info["bullet_speed"], 1, 2000, self.player,  # bullet_speed = 3.5
                            self.player.rect.centerx, self.player.rect.centery)

                    self.weapon_group.add(new_weapon)
                    cooldown_info["last_shot_time"] = current_time

    def handle_collisions(self):
        if self.player.game_pose == False:
            """武器と敵の衝突処理"""
            # 衝突した武器ごとに、当たった敵を記録して次に同じ敵にダメージを与えないようにする
            collisions = pygame.sprite.groupcollide(
                self.weapon_group, self.enemy_group, False, False)

            for weapon, enemies in collisions.items():
                for enemy in enemies:
                    if not hasattr(weapon, '_damaged_enemies'):
                        weapon._damaged_enemies = set()  # 追跡リストを初期化

                    # 衝突した敵がまだダメージを受けていなければ
                    if enemy not in weapon._damaged_enemies:
                        enemy.damage(weapon.AT)  # ダメージを与える
                        print(enemy.HP)
                        weapon._damaged_enemies.add(enemy)  # 追跡リストに追加

    def remove_weapon(self, weapon_type):
        """登録された武器を削除"""
        if weapon_type in self.weapon_cooldowns:
            del self.weapon_cooldowns[weapon_type]
            print(f"Weapon {weapon_type} has been removed.")
        else:
            print(f"Weapon {weapon_type} does not exist.")

    def update(self):
        self.shoot()
        self.handle_collisions()
        self.weapon_group.update()
        self.weapon_group.draw(self.player.screen)
