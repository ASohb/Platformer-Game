import pgzrun
from random import randint

# Configurações básicas da tela
WIDTH = 800
HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Estado inicial do jogo
game_state = "menu"
victory_message = ""
game_over = False
music_on = False

# Carregar a música
music.set_volume(0.5)

# Classe para o jogador
class Hero:
    def __init__(self):
        first_platform = platforms[0]
        self.sprite = Actor('bunny1_walk1', (first_platform.rect.centerx, first_platform.rect.top - 50))
        self.vx = 0
        self.vy = 0
        self.is_jumping = False
        self.sprites_walk = ['bunny1_walk1', 'bunny1_walk2']
        self.sprites_jump = ['bunny1_jump1', 'bunny1_jump2']
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_delay = 0.1

    def draw(self):
        self.sprite.draw()

    def update(self, dt, platforms, enemies):
        global game_over
        if game_over or victory_message:
            return
        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            if self.is_jumping:
                self.animation_index = (self.animation_index + 1) % len(self.sprites_jump)
                self.sprite.image = self.sprites_jump[self.animation_index]
            else:
                self.animation_index = (self.animation_index + 1) % len(self.sprites_walk)
                self.sprite.image = self.sprites_walk[self.animation_index]
            self.animation_timer = 0

        self.sprite.x += self.vx
        if self.sprite.x < 0:
            self.sprite.x = 0
        elif self.sprite.x > WIDTH:
            self.sprite.x = WIDTH

        self.sprite.y += self.vy
        self.vy += 0.5

        on_platform = False
        for platform in platforms:
            if self.sprite.colliderect(platform.rect) and self.vy >= 0:
                self.vy = 0
                self.is_jumping = False
                self.sprite.y = platform.rect.top - self.sprite.height // 2
                on_platform = True
                break

        if not on_platform and self.sprite.y >= HEIGHT:
            self.sprite.y = HEIGHT - 100
            self.is_jumping = False
            self.vy = 0

        for enemy in enemies:
            if self.sprite.colliderect(enemy.rect):
                self.vx = 0
                self.vy = 0
                game_over = True
                return False
        return True

    def jump(self):
        if not self.is_jumping:
            self.vy = -10
            self.is_jumping = True

# Classe para as plataformas
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = Rect((x, y), (width, height))
        self.color = GREEN

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)

# Classe para os inimigos
class Enemy:
    def __init__(self, platform):
        self.platform = platform
        self.rect = Rect((platform.rect.x, platform.rect.y - 50), (50, 50))
        self.images = ['spikeman', 'spikeman2']
        self.image_index = 0
        self.image = Actor(self.images[self.image_index])
        self.image.pos = (self.rect.x, self.rect.y + 25)
        self.direction = 1
        self.speed = 2
        self.animation_timer = 0
        self.animation_delay = 0.1

    def draw(self):
        self.image.draw()

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image.image = self.images[self.image_index]
            self.animation_timer = 0

        self.rect.x += self.direction * self.speed
        if self.rect.left < self.platform.rect.left or self.rect.right > self.platform.rect.right:
            self.direction *= -1

        self.image.pos = (self.rect.x, self.rect.y + 25)

platforms = [
    Platform(100, 500, 200, 20),
    Platform(300, 400, 200, 20),
    Platform(500, 300, 200, 20),
    Platform(700, 200, 200, 20),
    Platform(100, 100, 200, 20),
    Platform(500, 100, 200, 20),
]

hero = Hero()

enemies = [
    Enemy(platforms[1]),
    Enemy(platforms[2]),
]

def draw_menu():
    screen.fill(WHITE)
    screen.draw.text("Menu Principal", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color=BLACK)
    screen.draw.text("Start Game", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color=BLACK)
    screen.draw.text("Toggle Music", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=40, color=BLACK)
    screen.draw.text("Exit", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=40, color=BLACK)

def on_mouse_down(pos):
    global game_state, music_on
    if 300 < pos[0] < 500 and 270 < pos[1] < 310:
        game_state = "game"
    elif 300 < pos[0] < 500 and 320 < pos[1] < 360:
        if music_on:
            music.stop()
        else:
            music.play('background_music')
        music_on = not music_on
    elif 300 < pos[0] < 500 and 370 < pos[1] < 410:
        exit()

def draw_game():
    screen.clear()
    hero.draw()
    for platform in platforms:
        platform.draw()
    for enemy in enemies:
        enemy.draw()
    if victory_message:
        screen.draw.text(victory_message, center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color=YELLOW)
    if game_over:
        screen.draw.text("You lost!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color=RED)

def update_game(dt):
    global victory_message, game_over
    if keyboard.left:
        hero.vx = -5
    elif keyboard.right:
        hero.vx = 5
    else:
        hero.vx = 0
    if keyboard.space:
        hero.jump()
    if not game_over and hero.update(dt, platforms, enemies):
        for enemy in enemies:
            enemy.update(dt)
        if hero.sprite.colliderect(platforms[-1].rect):
            victory_message = "You won!"
            hero.vx = 0
            hero.vy = 0

def update(dt):
    if game_state == "menu":
        pass
    elif game_state == "game":
        update_game(dt)

def draw():
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()

pgzrun.go()
