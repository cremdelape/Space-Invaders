import pygame
from pygame import mixer
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

bullet = None
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('SPACE INVADERS')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')
mixer.music.load('background.mp3')
mixer.music.play(-1)
health_font = pygame.font.SysFont('comicsans', 30, True)
game_font = pygame.font.SysFont('comicsans', 100, True)
clock = pygame.time.Clock()
running = True


class Player:
    def __init__(self):
        self.x = 370
        self.y = 532
        self.image = pygame.image.load('player.png')
        self.speed = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def display(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def boundary(self):
        if self.x < 0:
            self.x = 0
        if self.x > 732:
            self.x = 732

    def input(self):
        global bullet_state
        global bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.speed = player_speed
            if event.key == pygame.K_LEFT:
                self.speed = -player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    mixer.Sound('laser.wav').play()
                    bullet = Bullet()
                    bullet_state = 'fire'
        if event.type == pygame.KEYUP:
            self.speed = 0

    def move(self):
        self.x += self.speed
        self.boundary()


class Bullet:
    def __init__(self):
        self.x = player.x
        self.y = 526
        self.image = pygame.image.load('bullet.png')
        self.rect = pygame.Rect(self.x + 26, self.y, 10, 30)

    def display(self):
        screen.blit(self.image, (self.x + 16, self.y))
        self.rect = pygame.Rect(self.x + 26, self.y, 10, 30)

    def reload(self):
        global bullet_state
        if self.y < 0:
            bullet_state = 'ready'
            del self

    def flight(self):
        self.y -= bullet_speed

    def is_collided(self):
        global score
        global bullet_state
        global enemy
        if self.rect.colliderect(enemy.rect):
            mixer.Sound('explosion.wav').play()
            bullet_state = 'ready'
            score += 1
            enemies.pop(enemies.index(enemy))
            del self


class Enemy:
    def __init__(self):
        self.x = random.randint(0, 731)
        self.y = 0
        self.image = pygame.image.load('enemy.png')
        self.direction = 'right'
        self.x_speed = enemy_speed
        self.y_speed = 40
        self.bombs = []
        self.max_bombs = 10
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def display(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def speed_change(self):
        global enemy_speed
        if self.y > 450:
            self.x_speed = enemy_speed * 2
        elif self.y > 300:
            self.x_speed = round(enemy_speed * 1.5)

    def move(self):
        if self.direction == 'right':
            self.x += self.x_speed
        if self.direction == 'left':
            self.x -= self.x_speed

    def dir_change(self):
        if self.x <= 0:
            self.direction = 'right'
            self.y += self.y_speed
        if self.x >= 732:
            self.direction = 'left'
            self.y += self.y_speed

    def kamikaze(self):
        global health
        if self.rect.colliderect(player.rect):
            health = 0


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = bomb_speed
        self.image = pygame.image.load('bomb.png')
        self.rect = pygame.Rect(self.x + 10, self.y, 11, 30)

    def display(self):
        screen.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x + 10, self.y, 11, 30)

    def flight(self):
        self.y += self.speed

    def hit(self):
        global health
        if self.rect.colliderect(player.rect):
            mixer.Sound('damage.wav').play()
            health -= 10
            enemy.bombs.pop(enemy.bombs.index(self))


def health_bar():
    global screen
    outline = pygame.Rect(688, 555, 102, 20)
    pygame.draw.rect(screen, (255, 0, 0), outline, 2)
    inside = pygame.Rect(689, 557, health, 18)
    pygame.draw.rect(screen, (0, 255, 0), inside)


def game_over():
    global max_enemies
    if health <= 0:
        max_enemies = 0
        return True
    else:
        return False


health = 100
score = 0
max_enemies = 5
bullet_state = 'ready'
enemy_speed = 1
bomb_speed = enemy_speed + 5
bullet_speed = 10
player_speed = 5
player = Player()
enemies = []
count = 0
while running:
    screen.blit(background, (0, 0))
    score_text = health_font.render(f'SCORE  {score}', 1, (255, 255, 255))
    screen.blit(score_text, (680, 505))
    if not game_over():
        health_text = health_font.render('HEALTH', 1, (255, 0, 0))
        screen.blit(health_text, (690, 525))
        health_bar()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.input()
    if not game_over():
        max_enemies = score + 5
    if game_over():
        max_enemies = 0
        for enemy in enemies:
            enemies.pop(enemies.index(enemy))

    while len(enemies) <= max_enemies:
        enemies.append(Enemy())
    if not game_over():
        for enemy in enemies:
            chance = random.randint(1, 500)
            if chance == 1:
                if len(enemy.bombs) <= enemy.max_bombs:
                    enemy.bombs.append(Bomb(enemy.x, enemy.y))
            if enemy.bombs:
                for bomb in enemy.bombs:
                    bomb.flight()
                    bomb.display()
                    bomb.hit()
                    if bomb.y > 600:
                        enemy.bombs.pop(enemy.bombs.index(bomb))

            enemy.kamikaze()
            enemy.dir_change()
            enemy.speed_change()
            enemy.move()
            enemy.display()
            if bullet_state == 'fire':
                bullet.is_collided()
    player.move()
    player.display()
    if bullet_state == 'fire':
        bullet.reload()
        bullet.flight()
        bullet.display()
    if game_over():
        text = game_font.render('GAME OVER', 1, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 300))
        screen.blit(text, text_rect)
        mixer.music.stop()
        count = 1
    while count == 1:
        mixer.Sound('game over.wav').play()
        count += 1
    clock.tick(60)
    pygame.display.update()
