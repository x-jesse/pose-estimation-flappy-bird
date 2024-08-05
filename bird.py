import pygame

# Bird class
class Bird:
    def __init__(self, bird_frames, screen_heigt):
        self.frames = bird_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.x = 50
        self.y = screen_heigt // 2
        self.y_speed = 0
        self.animation_counter = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.y_speed * 3)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

    def update(self):
        self.y_speed += GRAVITY
        self.y += self.y_speed
        self.rect.y = self.y

        # Handle animation
        self.animation_counter += 1
        if self.animation_counter % 5 == 0:  # Change frame every 5 ticks
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def jump(self):
        self.y_speed = BIRD_JUMP