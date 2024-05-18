import pygame
import os

class Tower(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'tower.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect(topleft=position)
