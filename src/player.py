import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'player_jul.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=position)
        self.velocity_y = 0
        self.on_ground = True
        self.is_jumping = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = -20
            self.on_ground = False
            self.is_jumping = True

    def update(self, keys):
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

        self.rect.y += self.velocity_y
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
            self.on_ground = True
            self.velocity_y = 0
            self.is_jumping = False
        else:
            self.velocity_y += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        name_surface = pygame.font.Font(None, 36).render("JUL", True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        surface.blit(name_surface, name_rect)
