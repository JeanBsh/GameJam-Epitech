import pygame
import os

class Torch(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.frames = []
        for i in range(1, 4):
            image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', f'flame{i}.png')
            frame = pygame.image.load(image_path).convert_alpha()
            frame = pygame.transform.scale(frame, (400, 400))
            self.frames.append(frame)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=position)
        self.animation_speed = 0.1
        self.animation_counter = 0

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
