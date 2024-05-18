import sys
import os
import pygame
from src.player import Player
from src.obstacle import Obstacle
from src.tower import Tower
from src.torch import Torch

pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

background_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'background.png')
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (1200, 750))

menu_background_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'background_menu.png')
menu_background = pygame.image.load(menu_background_path).convert()
menu_background = pygame.transform.scale(menu_background, (1200, 750))

footstep_sound_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds', 'footstep.wav')
jump_sound_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds', 'jump.wav')
background_music_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds', 'background_music.mp3')

footstep_sound = pygame.mixer.Sound(footstep_sound_path)
jump_sound = pygame.mixer.Sound(jump_sound_path)

pygame.mixer.music.load(background_music_path)
background_music_volume = 0.2
pygame.mixer.music.set_volume(background_music_volume)
pygame.mixer.music.play(-1)

player = Player((100, 300), footstep_sound, jump_sound)
all_sprites = pygame.sprite.Group(player)
obstacles = pygame.sprite.Group()
tower = Tower((900, 290))
tower_group = pygame.sprite.GroupSingle()
torch = Torch((600, 335))
torch_group = pygame.sprite.GroupSingle()

menu_mode = True
game_over = False
running = True
loose_screen = False
win_screen = False

def spawn_obstacle():
    if not game_over and not menu_mode and obstacles_crossed < target_obstacles:
        obstacle = Obstacle((1200, 500))
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        print("Obstacle spawned")

def reset_game():
    global player, all_sprites, obstacles, tower, tower_group, torch, torch_group
    global menu_mode, game_over, running, loose_screen, win_screen
    global obstacles_crossed, torch_collected, background_x, show_message

    player = Player((100, 300), footstep_sound, jump_sound)
    all_sprites = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()
    tower = Tower((900, 290))
    tower_group = pygame.sprite.GroupSingle()
    torch = Torch((600, 335))
    torch_group = pygame.sprite.GroupSingle()

    menu_mode = False
    game_over = False
    loose_screen = False
    win_screen = False

    obstacles_crossed = 0
    torch_collected = False
    background_x = 0
    show_message = False

pygame.time.set_timer(pygame.USEREVENT, 2000)

obstacles_crossed = 0
target_obstacles = 3
torch_collected = False
background_x = 0
show_message = False

def show_win_screen():
    screen.fill((0, 0, 0))
    win_text = font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 2 - win_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_loose_screen():
    screen.fill((0, 0, 0))
    loose_text = font.render("YOU LOSE!", True, (255, 0, 0))
    screen.blit(loose_text, (screen.get_width() // 2 - loose_text.get_width() // 2, screen.get_height() // 2 - loose_text.get_height() // 2))
    restart_button_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), restart_button_rect)
    restart_text = small_font.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2, restart_button_rect.centery - restart_text.get_height() // 2))
    pygame.display.flip()
    return restart_button_rect

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, rect, color, shadow_color, text_color):
    shadow_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width, rect.height)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    button_text = font.render(text, True, text_color)
    screen.blit(button_text, (rect.centerx - button_text.get_width() // 2, rect.centery - button_text.get_height() // 2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_mode:
                if play_button_rect.collidepoint(event.pos):
                    menu_mode = False
                elif help_button_rect.collidepoint(event.pos):
                    print("You're Jul and you've got to light the Olympic flame, but unfortunately there are a few obstacles in your way, so make sure you get to the tower to light the flame!")
            elif loose_screen:
                if restart_button_rect.collidepoint(event.pos):
                    reset_game()
        elif event.type == pygame.USEREVENT and not game_over and not win_screen and not loose_screen:
            spawn_obstacle()

    if menu_mode:
        screen.blit(menu_background, (0, 0))
        play_button_rect = pygame.Rect(400, 200, 400, 100)
        help_button_rect = pygame.Rect(400, 350, 400, 100)
        draw_button("Play", play_button_rect, (0, 255, 0), (0, 200, 0), (255, 255, 255))
        draw_button("Help", help_button_rect, (0, 0, 255), (0, 0, 200), (255, 255, 255))
    elif loose_screen:
        restart_button_rect = show_loose_screen()
    else:
        keys = pygame.key.get_pressed()

        if not game_over:
            player.update(keys)
            obstacles.update()
            torch_group.update()

            if pygame.sprite.spritecollide(player, obstacles, False):
                print("Game Over")
                game_over = True
                loose_screen = True

            for obstacle in obstacles:
                if obstacle.rect.right < player.rect.left and not obstacle.passed_by_player:
                    if player.rect.bottom >= 450 and player.rect.top < 450:
                        obstacles_crossed += 1
                        obstacle.passed_by_player = True
                        obstacle.kill()
                        print(f"Obstacle removed, total obstacles crossed: {obstacles_crossed}")

            if obstacles_crossed >= target_obstacles and torch not in torch_group:
                for obstacle in obstacles:
                    obstacle.kill()
                tower_group.add(tower)
                torch_group.add(torch)
                obstacles.empty()
                print("Tower and torch added")

            if pygame.sprite.spritecollide(player, torch_group, True):
                torch_collected = True
                show_message = True
                print("Torche ramassée!")
                torch.rect.center = player.rect.center

            if torch_collected:
                torch.rect.centerx = player.rect.centerx
                torch.rect.top = player.rect.top - torch.rect.height

            if torch_collected and pygame.sprite.spritecollide(player, tower_group, False):
                torch_collected = False
                torch.rect.topleft = (tower.rect.centerx - 25, tower.rect.top - 50)
                torch_group.add(torch)
                show_win_screen()
                running = False

            else:
                if obstacles_crossed >= target_obstacles:
                    if keys[pygame.K_LEFT]:
                        player.rect.x -= 5
                        background_x += 5
                    if keys[pygame.K_RIGHT]:
                        player.rect.x += 5
                        background_x -= 5
                    if keys[pygame.K_SPACE] and player.rect.bottom >= 450:
                        player.jump()

        if obstacles_crossed < target_obstacles:
            background_x -= 5
            if background_x <= -1200:
                background_x = 0
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + 1200, 0))

        all_sprites.draw(screen)
        tower_group.draw(screen)

        if torch_collected:
            torch.rect.centerx = player.rect.centerx
            torch.rect.top = player.rect.top - torch.rect.height
            torch_group.add(torch)
        torch_group.draw(screen)

        score_text = small_font.render(f'Score: {obstacles_crossed}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if show_message:
            draw_text("Well done! You've picked up the Olympic flame!", small_font, (255, 255, 255), screen, 300, 50)
            pygame.display.flip()
            pygame.time.wait(2000)
            show_message = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

