import pygame
from setting import *
from image import *


class LevelSystem:
    def __init__(self, player):
        self.player = player
        self.level = 1
        self.current_experience = 0
        self.experience_to_next_level = 1  # 次のレベルまでに必要な経験値

    def add_experience(self, amount):
        self.current_experience += amount
        while self.current_experience >= self.experience_to_next_level:
            self.current_experience -= self.experience_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience_to_next_level = (self.level * self.level)
        print(f"Level UP!：残り{self.experience_to_next_level}")
