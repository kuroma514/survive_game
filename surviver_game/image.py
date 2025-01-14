import pygame

# スライム画像切り取り
suraimu_image_date = pygame.image.load(
    f'mono/image/enemy/suraimu.png')

suraimu_image_list = []
for i in range(4):
    suraimu_image_pose = pygame.Vector2(64, 64 * i)
    suraimu_image_cut_size = pygame.Vector2(64, 64)
    suraimu_cut_image = suraimu_image_date.subsurface(
        pygame.Rect(suraimu_image_pose, suraimu_image_cut_size))
    suraimu_image_list.append(suraimu_cut_image)

# コウモリ画像切り取り
bat_image_date = pygame.image.load(
    f'mono/image/enemy/ScaryBat.png')
bat_image_list = []
for i in range(3):
    bat_image_pose = pygame.Vector2(i * 64, 0)
    bat_image_cut_size = pygame.Vector2(64, 64)
    bat_cut_image = bat_image_date.subsurface(
        pygame.Rect(bat_image_pose, bat_image_cut_size))
    bat_image_list.append(bat_cut_image)


# 赤の弾画像切り取り
image_date = pygame.image.load(
    f'mono/image/bullet/Fire Effect and Bullet.png')
red_bullet_image_list = []
for i in range(4):
    image_pose = pygame.Vector2(19*16 + i*16, 9 * 16)
    image_cut_size = pygame.Vector2(16, 16)
    cut_image = image_date.subsurface(
        pygame.Rect(image_pose, image_cut_size))
    red_bullet_image_list.append(cut_image)

# waterball画像切り取り
image_date = pygame.image.load(
    f'mono/image/bullet/Water Effect and Bullet.png')
water_bullet_image_list = []
for i in range(4):
    image_pose = pygame.Vector2(19*16 + i*16, 9*16)
    image_cut_size = pygame.Vector2(16, 16)
    cut_image = image_date.subsurface(
        pygame.Rect(image_pose, image_cut_size))
    water_bullet_image_list.append(cut_image)

# 手裏剣画像切り取り
image_date = pygame.image.load(
    f'mono/image/bullet/Water Effect and Bullet.png')
syuriken_image_list = []
for i in range(4):
    image_pose = pygame.Vector2(19*16 + i*16, 7*16)
    image_cut_size = pygame.Vector2(16, 16)
    cut_image = image_date.subsurface(
        pygame.Rect(image_pose, image_cut_size))
    syuriken_image_list.append(cut_image)

# 経験値画像切り取り
image_date = pygame.image.load(
    f'mono/image/efect/exp.png')
exp_image_list = []
for i in range(3):
    image_pose = pygame.Vector2(i*32, 0)
    image_cut_size = pygame.Vector2(32, 32)
    cut_image = image_date.subsurface(
        pygame.Rect(image_pose, image_cut_size))
    exp_image_list.append(cut_image)
