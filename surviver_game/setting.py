import pygame


# FPSの設定
FPS = 60
frame = 0

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
mapchip_size = 48
mapchip_num = pygame.Vector2(16, 10)
map_size = pygame.Vector2(16, 450)
map_w, map_h = int(mapchip_size * map_size.x), int(mapchip_size * map_size.y)
font_path = "mono/font/JF-Dot-Shinonome16.ttf"

# DisplaySize(WindowSize)
screen_w, screen_h = int(
    mapchip_size * mapchip_num.x), int(mapchip_size * mapchip_num.y)

camera_y = 0
exp_group = pygame.sprite.Group()

background = pygame.Surface((map_w, map_h))
background.fill(WHITE)

grid_color = BLACK
