import pygame
import os

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'obstacle.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=position)
        self.passed_by_player = False

    def update(self):
        self.rect.x -= 10
        if self.rect.right < 0:
            self.kill()
            print("Obstacle removed")
