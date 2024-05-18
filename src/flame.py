import pygame

def animate_flame(screen):
    flame_images = [pygame.image.load(f"assets/images/flame_{i}.png").convert_alpha() for i in range(1, 6)]
    clock = pygame.time.Clock()
    frame = 0

    while frame < len(flame_images) * 10:
        screen.fill((0, 0, 0))
        screen.blit(flame_images[frame // 10], (400, 300))
        pygame.display.flip()
        clock.tick(15)
        frame += 1
