import pygame
import random
import cv2
import mediapipe as mp

# Initialize Pygame
pygame.init()

# Load assets
try:
    BIRD_FRAMES = [
        pygame.image.load('bird1.png'),
        pygame.image.load('bird2.png'),
        pygame.image.load('bird3.png')
    ]
    BACKGROUND_IMAGE = pygame.image.load('background.png')
    PIPE_IMAGE = pygame.image.load('pipe.png')
    BACKGROUND_SIZE = BACKGROUND_IMAGE.get_size()
    SCREEN_WIDTH, SCREEN_HEIGHT = BACKGROUND_SIZE
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
FPS = 30  # Reduced to 30 for better performance
GRAVITY = 0.25
BIRD_JUMP = -6.5
PIPE_GAP = 200  # Increased to give more room

# Bird class
class Bird:
    def __init__(self):
        self.frames = BIRD_FRAMES
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
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

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = PIPE_IMAGE
        self.image_top = pygame.transform.flip(self.image, False, True)
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.rect_top = self.image_top.get_rect(topleft=(self.x, self.height - self.image_top.get_height()))
        self.rect_bottom = self.image.get_rect(topleft=(self.x, self.height + PIPE_GAP))

    def draw(self, screen):
        screen.blit(self.image_top, self.rect_top.topleft)
        screen.blit(self.image, self.rect_bottom.topleft)

    def update(self):
        self.rect_top.x -= 3
        self.rect_bottom.x -= 3

    def off_screen(self):
        return self.rect_top.right < 0

    def collides_with(self, bird):
        return self.rect_top.colliderect(bird.rect) or self.rect_bottom.colliderect(bird.rect)


# Game class
class FlappyBirdGame:
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    def __init__(self, invincible=False):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = pygame.sprite.Group()
        self.invincible = invincible
        for i in range(3):
            pipe = Pipe(SCREEN_WIDTH + i * 200)
            self.pipes.add(pipe)
        self.score = 0

        # Initialize wrist positions outside the loop
        self.prev_left_wrist_y = None
        self.prev_right_wrist_y = None
        self.flap_threshold = 20

    def run(self):
        running = True
        cap = cv2.VideoCapture(0)
        while running and cap.isOpened():
            self.clock.tick(FPS)

            success, image = cap.read()
            if not success:
                break
            
            # Resize the image for faster processing
            image = cv2.resize(image, (320, 240))
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and detect the pose every 2 frames
            if self.clock.get_time() % 2 == 0:
                results = self.pose.process(image_rgb)

                if results.pose_landmarks:
                    # Draw the pose landmarks on the original image
                    self.mp_drawing.draw_landmarks(
                        image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                    # Get the positions of the left and right wrists
                    left_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

                    # Convert normalized landmark positions to pixel positions
                    left_wrist_y = left_wrist.y * image.shape[0]
                    right_wrist_y = right_wrist.y * image.shape[0]

                    # Check for downward flapping motion
                    if self.prev_left_wrist_y is not None and self.prev_right_wrist_y is not None:
                        left_wrist_movement = left_wrist_y - self.prev_left_wrist_y
                        right_wrist_movement = right_wrist_y - self.prev_right_wrist_y

                        if left_wrist_movement > self.flap_threshold and right_wrist_movement > self.flap_threshold:
                            self.bird.jump()
                            cv2.putText(image, 'Flapping Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    # Update previous wrist positions
                    self.prev_left_wrist_y = left_wrist_y
                    self.prev_right_wrist_y = right_wrist_y

            # Display the image with the pose landmarks
            cv2.imshow('MediaPipe Pose', image)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            self.bird.update()
            self.pipes.update()

            if not self.invincible:
                for pipe in self.pipes:
                    if pipe.collides_with(self.bird):
                        running = False

                if self.bird.y > SCREEN_HEIGHT or self.bird.y < 0:
                    running = False

            if self.pipes.sprites()[0].off_screen():
                self.pipes.remove(self.pipes.sprites()[0])
                new_pipe = Pipe(SCREEN_WIDTH + 200)
                self.pipes.add(new_pipe)
                self.score += 1

            self.draw()
            pygame.display.update()

        print(f"Game over! Your score was: {self.score}")
        cap.release()
        cv2.destroyAllWindows()

    def draw(self):
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_score()

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.score), True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2, 50))

if __name__ == '__main__':
    FlappyBirdGame(invincible=False).run()
    pygame.quit()
