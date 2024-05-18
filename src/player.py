import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, position, jump_sound):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'player_jul.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 160))

        self.full_rect = self.image.get_rect(topleft=position)

        hitbox_width = self.full_rect.width // 2
        hitbox_height = self.full_rect.height // 2

        self.rect = pygame.Rect(
            self.full_rect.left + (self.full_rect.width - hitbox_width) // 2,
            self.full_rect.top + (self.full_rect.height - hitbox_height) // 2,
            hitbox_width,
            hitbox_height
        )

        self.velocity_y = 0
        self.on_ground = True
        self.is_jumping = False

        self.jump_sound = jump_sound

    def jump(self):
        if self.on_ground:
            self.velocity_y = -20
            self.on_ground = False
            self.is_jumping = True
            self.jump_sound.play()

    def update(self, keys):
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

        self.rect.y += self.velocity_y
        if self.rect.bottom >= 535:
            self.rect.bottom = 535
            self.on_ground = True
            self.velocity_y = 0
            self.is_jumping = False
        else:
            self.velocity_y += 1

        self.full_rect.center = self.rect.center

    def draw(self, surface):
        surface.blit(self.image, self.full_rect)
        name_surface = pygame.font.Font(None, 36).render("JUL", True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(self.full_rect.centerx, self.full_rect.top - 10))
        surface.blit(name_surface, name_rect)
