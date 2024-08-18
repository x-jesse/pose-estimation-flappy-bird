import pygame
import cv2
import mediapipe as mp
from classes.player import Player
from classes.obstacle import Obstacle
from classes.button import Button

class FlappyBirdGame:
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    def __init__(self, invincible=False):
        """
        
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Flappy Bird')
        self.clock = pygame.time.Clock()
        self.bird = Player(sprites=BIRD_SPRITES, screen_height=SCREEN_HEIGHT, gravity=GRAVITY, jump_speed=BIRD_JUMP)
        self.pipes = pygame.sprite.Group()
        self.invincible = invincible
        self.score = 0

        for i in range(3):
            pipe = Obstacle(x=SCREEN_WIDTH + i * PIPE_GAP, sprites=PIPE_SPRITES, screen_height=SCREEN_HEIGHT, gap=PIPE_GAP)
            self.pipes.add(pipe)

        # pose detection params
        self.prev_left_wrist_y = None
        self.prev_right_wrist_y = None
        self.flap_threshold = 20

        self.font = pygame.font.SysFont(None, 36)
        self.retry_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50, "Retry", self.font, (255, 0, 0), (200, 0, 0))

    def run(self):
        """
        
        """
        running = True
        cap = cv2.VideoCapture(0)
        while running and cap.isOpened():
            self.clock.tick(FPS)

            success, image = cap.read()
            if not success:
                print("Error reading video frame")
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
                            print("Flap")

                    # Update previous wrist positions
                    self.prev_left_wrist_y = left_wrist_y
                    self.prev_right_wrist_y = right_wrist_y

            # Display the image with the pose landmarks
            cv2.imshow('MediaPipe Pose', image)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # spacebar as backup control
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
                new_pipe = Obstacle(x=SCREEN_WIDTH + 200, sprites=PIPE_SPRITES, screen_height=SCREEN_HEIGHT, gap=PIPE_GAP)
                self.pipes.add(new_pipe)
                self.score += 1

            self.draw()
            pygame.display.update()

            if not running:
                self.show_game_over()

        print(f"Game over! Your score was: {self.score}")
        cap.release()
        cv2.destroyAllWindows()

    def draw(self):
        """
        
        """
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_score()

    def draw_score(self):
        """

        """
        font = pygame.font.SysFont(None, 36)
        text = font.render(str(self.score), True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH // 2, 50))

    def show_game_over(self):
        """Handles the game over screen and retry button.
        
        """
        while True:
            self.screen.fill(WHITE)
            self.draw_score()
            self.retry_button.draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.retry_button.is_clicked():
                        self.__init__(invincible=self.invincible)  # Reset the game
                        self.run()

if __name__ == '__main__':
    pygame.init()

    try:
        BIRD_SPRITES = [
            pygame.image.load('assets/bird1.png'),
            pygame.image.load('assets/bird2.png'),
            pygame.image.load('assets/bird3.png')
        ]
        BACKGROUND_IMAGE = pygame.image.load('assets/background.png')
        PIPE_SPRITES = [pygame.image.load('assets/pipe.png')]
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
    FPS = 30
    GRAVITY = 0.25
    BIRD_JUMP = -6.5
    PIPE_GAP = 200

    FlappyBirdGame().run()
    pygame.quit()
