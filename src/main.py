import sys
import os
import pygame
from src.player import Player
from src.obstacle import Obstacle

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)

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

def show_win_screen():
    win_text = font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (450, 250))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_game_over_screen():
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (450, 250))
    pygame.display.flip()
    pygame.time.wait(2000)

running = True
background_x = 0
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT and not game_over:
            spawn_obstacle()

    keys = pygame.key.get_pressed()
    player.update(keys)
    obstacles.update()

    if pygame.sprite.spritecollide(player, obstacles, False):
        print("Game Over")
        game_over = True
        show_game_over_screen()
        running = False

    for obstacle in obstacles:
        if not obstacle.passed_by_player and obstacle.rect.right < player.rect.left:
            if player.rect.bottom < obstacle.rect.top:
                obstacle.passed_by_player = True
                score += 1
                print(f"Score updated: {score}")

        if obstacle.rect.right < 0:
            if not game_over:
                obstacles_crossed += 1
                obstacle.kill()
                print(f"Obstacle removed, total obstacles crossed: {obstacles_crossed}")

    if obstacles_crossed >= target_obstacles and not game_over:
        game_over = True
        print("Victory Condition Met")
        show_win_screen()
        running = False

    background_x -= 5
    if background_x <= -1200:
        background_x = 0

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 1200, 0))

    all_sprites.draw(screen)

    score_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
