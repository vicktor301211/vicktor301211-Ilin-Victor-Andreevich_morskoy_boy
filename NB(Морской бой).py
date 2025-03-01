from all_colors import *
import pygame
pygame.init()

import pygame.mixer
pygame.mixer.init()

shot_sound = pygame.mixer.Sound('resourse/shot.mp3')
explosion_sound = pygame.mixer.Sound('resourse/explosion.mp3')
fail_sound = pygame.mixer.Sound('resourse/fail.mp3')

pygame.mixer.music.load('resourse/sonar.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

shot_sound.set_volume(0.6)

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Моя игра")
BACKGROUND = CYAN
screen.fill(BACKGROUND)

screen_rect = screen.get_rect()

ship = pygame.Rect(300, 200, 50, 100)
ship.right = screen_rect.right
ship.centery = screen_rect.centery

missiles_counter = 10
missiles = []

for i in range(missiles_counter):
    missile = pygame.Rect(50, screen_rect.centery, 10, 10)  # Снаряд появляется по центру экрана
    missiles.append({'rect': missile, 'launched': False, 'speed_x': 0, 'speed_y': 0})

ship_speeed_y = 1
ship_alive = True
hp_ship = 10

FPS = 60
clock = pygame.time.Clock()
running = True

# Индекс текущего снаряда, который регулируется
current_missile_index = 0

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Запуск текущего снаряда
                if not missiles[current_missile_index]['launched']:
                    missiles[current_missile_index]['launched'] = True
                    missiles[current_missile_index]['speed_x'] = 3
                    shot_sound.play()
                    print(f'Снаряды: {missiles_counter-1}, Здоровье корабля: {hp_ship}')
                    # Переход к следующему снаряду
                    current_missile_index = (current_missile_index + 1) // missiles_counter

            # Регулировка положения снаряда
            elif event.key == pygame.K_w:
                if not missiles[current_missile_index]['launched']:
                    missiles[current_missile_index]['rect'].y -= 10  # Двигаем снаряд вверх
            elif event.key == pygame.K_s:
                if not missiles[current_missile_index]['launched']:
                    missiles[current_missile_index]['rect'].y += 10  # Двигаем снаряд вниз

    # Основная логика
    for missile in missiles[:]:  # Используем срез [:] для итерации по копии списка
        if missile['launched']:
            missile['rect'].move_ip(missile['speed_x'], missile['speed_y'])
            if not missile['rect'].colliderect(screen_rect):
                missiles.remove(missile)
                missiles_counter -= 1
                missile['launched'] = False
                fail_sound.play()

            if ship_alive and missile['rect'].colliderect(ship):
                hp_ship -= 1
                missiles.remove(missile)
                missiles_counter -= 1       # Уничтожаем снаряд после попадания
                explosion_sound.play()
                print(f'Снаряды: {missiles_counter}, Здоровье корабля: {hp_ship}')
                if hp_ship <= 0:
                    ship_alive = False
                    pygame.mixer.music.stop()
                    BACKGROUND = RED
                    screen.fill(BACKGROUND)
                elif missiles_counter <= 0:
                    BACKGROUND = BLACK
                    screen.fill(BACKGROUND)
                    pygame.mixer.music.stop()

    # Отрисовка объектов
    screen.fill(BACKGROUND)
    if ship_alive:
        pygame.draw.rect(screen, BLUE, ship)
        ship.move_ip(0, ship_speeed_y)
        if ship.bottom > screen_rect.bottom or ship.top < screen_rect.top:
            ship_speeed_y = -ship_speeed_y

    # Отрисовка всех снарядов
    for missile in missiles:
        pygame.draw.rect(screen, RED, missile['rect'])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()