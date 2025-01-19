import pygame
from setting import *
import pygame_gui
import pygame_gui.ui_manager


class UpgradeManager:
    def __init__(self, player):
        self.screen = pygame.display.get_surface()
        self.ui_manager = pygame_gui.UIManager(screen_w, screen_h)
        self.player = player
        self.upgrade_choices = []
        self.choice_buttons = []
        self.upgrade_window = None

        # スキルや武器のデータ
        self.available_upgrades = [
            {"type": "weapon", "name": "Waterball",
                "description": "強力な水の弾丸を発射", "damage": 50},
            {"type": "weapon", "name": "Syuriken",
                "description": "素早く飛ぶ手裏剣", "damage": 30},
            {"type": "skill", "name": "HP Boost",
                "description": "最大HPを20増加", "effect": {"hp": 20}},
            {"type": "skill", "name": "Speed Boost",
                "description": "移動速度を10%増加", "effect": {"speed": 0.1}},
            {"type": "skill", "name": "Attack Boost",
                "description": "攻撃力を10%増加", "effect": {"attack": 0.1}},
        ]

    def generate_choices(self):
        """ランダムで3つの選択肢を生成"""
        import random
        self.upgrade_choices = random.sample(self.available_upgrades, 3)

    def create_upgrade_window(self):
        """スキル選択画面を作成"""
        self.upgrade_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((200, 100), (400, 300)),
            manager=self.ui_manager,
            window_display_title="Upgrade Selection",
            object_id="#upgrade_window"
        )

        for i, choice in enumerate(self.upgrade_choices):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50, 50 + i * 60), (300, 50)),
                text=f"{choice['name']} - {choice['description']}",
                manager=self.ui_manager,
                container=self.upgrade_window
            )
            self.choice_buttons.append((button, choice))

    def handle_event(self, event):
        """選択肢ボタンのクリックイベントを処理"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for button, choice in self.choice_buttons:
                if event.ui_element == button:
                    self.apply_upgrade(choice)
                    self.upgrade_window.kill()
                    self.choice_buttons = []
                    break

    def apply_upgrade(self, choice):
        """選んだ武器やスキルをプレイヤーに適用"""
        if choice["type"] == "weapon":
            self.player.weapon_manager.add_weapon(
                choice["name"], cooltime=3000)
        elif choice["type"] == "skill":
            for key, value in choice["effect"].items():
                setattr(self.player, key, getattr(self.player, key) + value)

    def level_up(self):
        """レベルアップ時の処理"""
        self.generate_choices()
        self.create_upgrade_window()
