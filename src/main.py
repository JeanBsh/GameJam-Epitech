import sys
import os
import pygame
from src.player import Player
from src.obstacle import Obstacle

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
background_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'background.png')
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (1200, 600))
player = Player((100, 450))
all_sprites = pygame.sprite.Group(player)
obstacles = pygame.sprite.Group()

def spawn_obstacle():
    if not game_over:
        obstacle = Obstacle((1200, 500))
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        print("Obstacle spawned")

pygame.time.set_timer(pygame.USEREVENT, 2000)

obstacles_crossed = 0
target_obstacles = 3
game_over = False
win_screen = False
background_x = 0

def show_win_screen():
    win_text = font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (450, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    return True

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT and not game_over and not win_screen:
            spawn_obstacle()

    keys = pygame.key.get_pressed()
    
    if not game_over:
        if not win_screen:
            player.update(keys)
            obstacles.update()

            if pygame.sprite.spritecollide(player, obstacles, False):
                print("Game Over")
                game_over = True
                running = False

            for obstacle in obstacles:
                if obstacle.rect.right < player.rect.left and not obstacle.rect.colliderect(player.rect):
                    if player.rect.bottom >= 450 and player.rect.top < 450:
                        obstacles_crossed += 1
                        obstacle.kill()
                        print(f"Obstacle removed, total obstacles crossed: {obstacles_crossed}")

            if obstacles_crossed >= target_obstacles:
                win_screen = show_win_screen()
                obstacles.empty()

        else:
            if keys[pygame.K_LEFT]:
                player.rect.x -= 5
                background_x += 5
            if keys[pygame.K_RIGHT]:
                player.rect.x += 5
                background_x -= 5
            if keys[pygame.K_UP]:
                player.rect.y -= 5
                background_x += 5
            if keys[pygame.K_DOWN]:
                player.rect.y += 5
                background_x -= 5

    if not win_screen or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        background_x -= 5
        if background_x <= -1200:
            background_x = 0
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 1200, 0))
    
    all_sprites.draw(screen)
    score_text = small_font.render(f'Score: {obstacles_crossed}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
