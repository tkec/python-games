import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置游戏标题
pygame.display.set_caption("打飞机游戏")

# 加载图片并缩放
player_image = pygame.image.load('images/player.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # 缩小玩家图片

enemy_image = pygame.image.load('images/enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (200, 200))  # 缩小敌人图片

bullet_image = pygame.image.load('images/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (60, 80)) # 缩小子弹图片

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 5)

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# 初始化玩家、敌人、子弹精灵组
player = Player()
player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group([Enemy() for _ in range(5)])
bullet_group = pygame.sprite.Group()

# 设置时钟
clock = pygame.time.Clock()


# 定义一个变量来跟踪按键状态
key_pressed = False

# 游戏主循环
running = True
while running:

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                key_pressed = False

    if key_pressed:
        print("key pressed")
        bullet = Bullet(player.rect.centerx, player.rect.top)
        bullet_group.add(bullet)

    # 更新游戏对象
    keys = pygame.key.get_pressed()
    player_group.update(keys)
    enemy_group.update()
    bullet_group.update()

    # 检测碰撞
    collisions = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
    for enemy in collisions.values():
        enemy_group.add(Enemy())

    # 渲染图形
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    enemy_group.draw(screen)
    bullet_group.draw(screen)
    pygame.display.flip()

    # 设置帧率
    clock.tick(60)

# 退出Pygame
pygame.quit()
