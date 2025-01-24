import pygame
from setting import *
from game import Game


pygame.init()
pygame.display.set_caption('surviver game')
screen = pygame.display.set_mode((screen_w, screen_h))
screen.fill(pygame.Color("WHITE"))

run = True

game = Game()

background = pygame.Surface((map_w, map_h))
background.fill(GREEN)

# ループ-------------------------------------------------------------------------------------------------------
while run:
    # スクリーンの初期化
    # for x in range(0, screen_w, mapchip_size):
    #     pygame.draw.line(screen, grid_color, (x, 0), (x, screen_h))
    # for y in range(0, screen_h, mapchip_size):
    #     pygame.draw.line(screen, grid_color, (0, y), (screen_w, y))

    # イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # 更新
    game.update()
    pygame.display.update()
    clock.tick(FPS)
    frame += 1

# ループ終わり--------------------------------------------------------------------------------------------------

pygame.quit()
