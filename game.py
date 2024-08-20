import pygame
import cv2
import random
import mediapipe as mp
import numpy as np
from classes.player import Player
from classes.obstacle import Obstacle
from classes.button import Button

class FlappyBirdGame:
    """A Flappy Bird game with pose detection controls.

    This class handles the game loop, player controls, pose detection using
    MediaPipe, and the overall game state. The player can control the bird
    by performing a downward flapping motion detected by the webcam.

    Attributes:
        mp_pose (mp.solutions.pose.Pose): MediaPipe Pose instance for pose detection.
        pose (mp.solutions.pose.Pose): Instance of MediaPipe Pose.
        mp_drawing (mp.solutions.drawing_utils): MediaPipe Drawing Utilities for drawing landmarks.
        screen (pygame.Surface): The Pygame display surface.
        clock (pygame.time.Clock): The game clock to control the frame rate.
        bird (Player): The player-controlled bird character.
        pipes (pygame.sprite.Group): A group of obstacles (pipes) in the game.
        invincible (bool): If True, the bird is invincible and cannot die.
        score (int): The player's current score.
        prev_left_wrist_y (float): The y-coordinate of the left wrist in the previous frame.
        prev_right_wrist_y (float): The y-coordinate of the right wrist in the previous frame.
        flap_threshold (int): The movement threshold to trigger a flap.
        font (pygame.font.Font): The font used for displaying the score and retry button.
        retry_button (Button): A button to retry the game after game over.
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    def __init__(self, invincible: bool = False):
        """
        Initializes the FlappyBirdGame with the given settings.

        Args:
            invincible (bool): Whether the bird should be invincible. Defaults to False.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Flappy Bird')
        self.clock = pygame.time.Clock()
        self.bird = Player(
            sprites=BIRD_SPRITES, 
            screen_height=SCREEN_HEIGHT, 
            gravity=GRAVITY, 
            jump_speed=BIRD_JUMP
        )
        self.pipes = pygame.sprite.Group()
        self.invincible = invincible
        self.score = 0

        # spawns 4 pipes to start
        for i in range(4):
            pos = SCREEN_WIDTH + i * PIPE_X_OFFSET
            pipe = Obstacle(
                x=pos, 
                sprites=PIPE_SPRITES, 
                screen_height=SCREEN_HEIGHT, 
                gap=PIPE_Y_GAP, 
                speed=GAME_SPEED
            )
            self.pipes.add(pipe)

        # pose detection params
        self.prev_left_wrist_y = None
        self.prev_right_wrist_y = None
        self.flap_threshold = 20

        self.font = pygame.font.Font("assets/ThaleahFat.ttf", 36)
        self.retry_button = Button(
            x=SCREEN_WIDTH // 2 - 50, 
            y=SCREEN_HEIGHT // 2, 
            width=100, 
            height=50, 
            text="Retry", 
            font=self.font, 
            color=(120, 0, 0), 
            hover_color=(177, 0, 0)
        )

    def run(self) -> None:
        """Starts the main game loop and processes input and game logic."""
        running = True
        cap = cv2.VideoCapture(0)
        while running and cap.isOpened():
            self.clock.tick(FPS)

            success, frame = cap.read()
            if not success:
                print("Error reading video frame")
                break
            
            # Resize the image for faster processing
            frame = cv2.resize(frame, (320, 240))
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = np.zeros(frame.shape, dtype=np.uint8) # comment this line if you want to overlay the pose markers on live webcam feed instead of black frame

            # Process the image and detect the pose every 2 frames
            if self.clock.get_time() % 2 == 0:
                results = self.pose.process(image_rgb)

                if results.pose_landmarks:
                    # Draw the pose landmarks on the original image
                    self.mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                    # Get the positions of the left and right wrists
                    left_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

                    # Convert normalized landmark positions to pixel positions
                    left_wrist_y = left_wrist.y * frame.shape[0]
                    right_wrist_y = right_wrist.y * frame.shape[0]

                    # Check for downward flapping motion
                    if self.prev_left_wrist_y is not None and self.prev_right_wrist_y is not None:
                        left_wrist_movement = left_wrist_y - self.prev_left_wrist_y
                        right_wrist_movement = right_wrist_y - self.prev_right_wrist_y

                        if left_wrist_movement > self.flap_threshold and right_wrist_movement > self.flap_threshold:
                            self.bird.jump()

                    # Update previous wrist positions
                    self.prev_left_wrist_y = left_wrist_y
                    self.prev_right_wrist_y = right_wrist_y

            # Display the image with the pose landmarks
            cv2.imshow('MediaPipe Pose', frame)
            
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
                
            if self.invincible and self.bird.y > SCREEN_HEIGHT:
                self.bird.y = SCREEN_HEIGHT

            if self.pipes.sprites()[0].off_screen():
                self.pipes.remove(self.pipes.sprites()[0])
                self.score += 1

                new_pipe = Obstacle(
                    x=SCREEN_WIDTH + PIPE_X_OFFSET, 
                    sprites=PIPE_SPRITES, 
                    screen_height=SCREEN_HEIGHT, 
                    gap=PIPE_Y_GAP, 
                    speed=GAME_SPEED
                )
                self.pipes.add(new_pipe)

            self.draw()
            pygame.display.update()

            if not running:
                self.show_game_over()

        cap.release()
        cv2.destroyAllWindows()

    def draw(self) -> None:
        """Draws the game elements on the screen."""
        self.screen.blit(BACKGROUND_IMAGE, (0, 0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_score()

    def draw_score(self) -> None:
        """Draws the current score on the screen."""
        text = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2, 50))

    def show_game_over(self) -> None:
        """Handles the game over screen and retry button.

        Displays the final score and a button to retry the game.
        """
        while True:
            self.draw_score()
            self.retry_button.draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.retry_button.is_clicked():
                        self.__init__(invincible=self.invincible)
                        self.run()


if __name__ == '__main__':
    pygame.init()

    try:
        BIRD_SPRITES = [
            pygame.image.load('assets/bird1.png'),
            pygame.image.load('assets/bird2.png'),
            pygame.image.load('assets/bird3.png')
        ]
        SCREEN_WIDTH, SCREEN_HEIGHT = (1024, 548)
        BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('assets/background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        PIPE_SPRITES = [pygame.image.load('assets/pipe.png')]

    except pygame.error as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        exit()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Game settings
    FPS = 45
    GRAVITY = .4
    BIRD_JUMP = -8
    PIPE_Y_GAP = 300
    PIPE_X_OFFSET = 250
    GAME_SPEED = 6

    FlappyBirdGame(invincible=False).run()
    pygame.quit()
