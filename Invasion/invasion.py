import pygame, random, math
from pygame import mixer

WHITE = (255, 255, 255)
GREY = (30,30,30)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Invasion extraterrestre")

score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_controls():
    controls_text = font.render("CONTROLES DEL JUEGO:", True, WHITE)
    screen.blit(controls_text, (250, 150))
    controls_text = font.render("Moverse a la Izquierda: Flecha Izquierda", True, WHITE)
    screen.blit(controls_text, (250, 200))
    controls_text = font.render("Moverse a la Derecha: Flecha Derecha", True, WHITE)
    screen.blit(controls_text, (250, 250))
    controls_text = font.render("Disparar: Barra Espaciadora", True, WHITE)
    screen.blit(controls_text, (250, 300))
    controls_text = font.render("Pausar juego: P", True, WHITE)
    screen.blit(controls_text, (250, 350))
    controls_text = font.render("Presiona una tecla para empezar", True, WHITE)
    screen.blit(controls_text, (250, 420))

game_paused = False

def pause_game():
    paused_font = pygame.font.Font('freesansbold.ttf', 64)
    paused_text = paused_font.render("JUEGO EN PAUSA", True, WHITE)
    screen.blit(paused_text, (110, 250))
    pygame.display.update()
    pygame.time.delay(2000)

def show_score(x, y):
    score = font.render("Puntos: " + str(score_val), True, WHITE)
    screen.blit(score, (x, y))

def game_over():
    global running
    game_over_text = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (190, 250))
    pygame.display.update()
    pygame.time.delay(2000)
    running = False  

player_image = pygame.image.load('data/spaceship.png')
player_X = 370
player_Y = WINDOW_HEIGHT - 70
player_X_change = 0

ovni_images = []
ovni_X = []
ovni_Y = []
ovni_X_change = []
ovni_Y_change = []
num_ovnis = 8

alien_image = pygame.image.load('data/alien.png')
alien_X = []
alien_Y = []
alien_X_change = []
alien_Y_change = 20
alien_count = 5  
aliens_enabled = False  

alien_bullet_image = pygame.image.load('data/alien_bullet.png')
alien_bullet_X = []
alien_bullet_Y = []
alien_bullet_Y_change = 5
alien_bullet_state = "ready"

for _ in range(alien_count):
    alien_X.append(random.randint(64, 737))
    alien_Y.append(random.randint(30, 180))
    alien_X_change.append(2)

for _ in range(num_ovnis):
    ovni_images.append(pygame.image.load('data/ovni.png'))
    ovni_X.append(random.randint(64, 737))
    ovni_Y.append(random.randint(30, 180))
    ovni_X_change.append(2)
    ovni_Y_change.append(50)

bullet_image = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_X_change = 0
bullet_Y_change = 7
bullet_state = "rest"

size_collision = 35
def is_collision(x1, x2, y1, y2):
    if isinstance(x1, list):
        for i in range(len(x1)):
            distance = math.sqrt((x1[i] - x2) ** 2 + (y1[i] - y2) ** 2)
            if distance <= size_collision:  
                return True
        return False
    else:
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance <= size_collision  
    
explosion_sound = mixer.Sound('data/explosion.wav')

def player(x, y):
    screen.blit(player_image, (x - 16, WINDOW_HEIGHT - 70))

def ovni(x, y, i):
    screen.blit(ovni_images[i], (x, y))

def alien(x, y, i):
    screen.blit(alien_image, (x, y))

def bullet(x, y):
    global bullet_state
    screen.blit(bullet_image, (x, y))
    bullet_state = "fire"

def alien_bullet(x, y):
    screen.blit(alien_bullet_image, (x, y))

mixer.music.load('data/background.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

show_controls()
pygame.display.update()

waiting_for_key = True
while waiting_for_key:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting_for_key = False
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(GREY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_paused = not game_paused
                if game_paused:
                    pause_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_X_change = -3
    if keys[pygame.K_RIGHT]:
        player_X_change = 3
    if keys[pygame.K_SPACE]:
        if bullet_state == "rest":
            bullet_X = player_X
            bullet_Y = player_Y
            bullet_state = "fire"
            bullet_sound = mixer.Sound('data/bullet.wav')
            bullet_sound.play()

    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change
        if bullet_Y <= 0:
            bullet_state = "rest"

    player_X += player_X_change

    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    for i in range(num_ovnis):
        ovni_X[i] += ovni_X_change[i]

        if ovni_Y[i] >= 450:
            if abs(player_X - ovni_X[i]) < 80:
                for j in range(num_ovnis):
                    ovni_Y[j] = 2000
                    explosion_sound.play()
                game_over()
                break

        if ovni_X[i] >= 735 or ovni_X[i] <= 0:
            ovni_X_change[i] *= -1
            ovni_Y[i] += ovni_Y_change[i]

        if is_collision(bullet_X, ovni_X[i], bullet_Y, ovni_Y[i]):
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            ovni_X[i] = random.randint(64, 736)
            ovni_Y[i] = random.randint(30, 200)
            ovni_X_change[i] *= -1

            if score_val >= 10 and not aliens_enabled:
                aliens_enabled = True
                num_ovnis = 0 

                for _ in range(alien_count):
                    alien_X.append(random.randint(64, 737))
                    alien_Y.append(random.randint(30, 180))
                    alien_X_change.append(2)
            
        ovni(ovni_X[i], ovni_Y[i], i)

    if aliens_enabled:
        for i in range(alien_count):
            alien_X[i] += alien_X_change[i]

            if alien_X[i] >= 735 or alien_X[i] <= 0:
                alien_X_change[i] *= -1
                alien_Y[i] += alien_Y_change

            if is_collision(bullet_X, alien_X[i], bullet_Y, alien_Y[i]):
                score_val += 2
                bullet_Y = 600
                bullet_state = "rest"
                alien_X[i] = random.randint(64, 736)
                alien_Y[i] = random.randint(30, 200)
            
            if random.randint(0, 100) < 10 and alien_bullet_state == "ready":
                alien_bullet_state = "fire"
                alien_bullet_X.append(alien_X[i])
                alien_bullet_Y.append(alien_Y[i])

            alien(alien_X[i], alien_Y[i], i)

    if alien_bullet_state == "fire":
        for i in range(len(alien_bullet_X)):
            alien_bullet(alien_bullet_X[i], alien_bullet_Y[i])
            alien_bullet_Y[i] += alien_bullet_Y_change

            if is_collision(player_X, alien_bullet_X[i], player_Y, alien_bullet_Y[i]):
                explosion_sound.play()
                game_over()
                break

            if alien_bullet_Y[i] >= WINDOW_HEIGHT:
                alien_bullet_state = "ready"
                alien_bullet_X.pop(i)
                alien_bullet_Y.pop(i)

    if player_X <= 16:
        player_X = 16
    elif player_X >= 750:
        player_X = 750

    show_score(scoreX, scoreY)
    player(player_X, player_Y)
    pygame.display.update()
    clock.tick(70)

pygame.quit()
