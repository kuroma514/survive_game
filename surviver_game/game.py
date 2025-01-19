import pygame
from setting import *
from image import *
from player import Player
from enemy import Enemy
from enemy import Shortrange
from enemy import Longrange
from weapons import Waterball


class Game:

    def __init__(self):
        self.screen = pygame.display.get_surface()

        # スプライト
        self.create_group()
        self.player_num = 'boukensya'
        self.enemy_test_num = 'suraimu'
        self.Player = Player(self.player_group, 5, 3, 1, 1, 1, 1.5,
                             1, self.player_num, self.enemy_group)
        self.enemy_test = Enemy(self.enemy_group, 100, 1,
                                self.enemy_test_num, self.Player, self.enemy_group, 4, 4, 2)
        self.enemy_kotei = Enemy(self.enemy_group, 100, 1,
                                 self.enemy_test_num, self.Player, self.enemy_group, 8, -400, 100)

        for i in range(1):
            self.shortrange_enemy_test = Shortrange(self.enemy_group, 1, 1,
                                                    self.enemy_test_num, self.Player, self.enemy_group, i + 10, 4, 2)
        # self.longrange_enemy_test = Longrange(self.enemy_group, 100, 0.7,
        #                                       "ScaryBat", self.Player, self.enemy_group, 10, 4, 3 ,4)

    def create_group(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()

    def update(self):
        self.player_group.update()
        self.player_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        exp_group.update()
        exp_group.draw(self.screen)
