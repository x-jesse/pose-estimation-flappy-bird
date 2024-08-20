# Pose-Estimation Flappy (Flappy) Bird 

***Welcome to Flappy Flappy Bird, where you can roleplay Flappy Bird!***

>*Warning: flashing lights in demo video*

https://github.com/user-attachments/assets/7b23e03b-f5a9-4e3f-aa84-a6fbda904167

Literal flappy bird. Uses your webcam to detect flapping arm motion using pose estimation. Currently still a protoype, maybe create a webapp later.

## Usage
Developed on Mac OS Sonoma (14.3.1) running Python version 3.11.4. If there's issues installing dependencies consider checking Python version or running on Linux.

Setup virtualenv and install dependencies:
```
python -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
```
Run the game:
```
python game.py
```

## Design

The flappy bird portion is very simple, it's a reimplementation of the standard flappy bird game in Python using the `pygame` library. For pose estimation, we'll use OpenCV to do the video processing and interface with the webcam, while the actual pose estimation is handled using Google's [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) library. To control the bird in-game, we'll track the markers for the person's left and right wrist/forearm and each time we detect sufficient vertical motion, we'll consider it "flapping" and move the bird accordingly. 

<p align="center">
  <img width="400" alt="diagram" src="https://github.com/user-attachments/assets/a427498e-bbc5-41ca-b5a4-04d24c3da2ad">
</p>

**Additional Considerations:**

- Ideally we would trigger the in-game "flap" every time our player's arm move downwards, so we don't need to consider upwards movement in either of the player's arms to trigger "flapping"
- We don't want to continuously trigger "flapping" when the player moves their arms down either though, so we'll set a minimum velocity that the player has to flap for us to consider it "flapping"
- To make things easier, we'll assume that our minimum flapping velocity is fast enough that it's impossible for a person to trigger "flapping" multiple times with a single downwards arm movement

![flappy_bird](https://github.com/user-attachments/assets/fbf43740-b781-47e5-8577-3b28a40f5992)

### Changelog
- Aug 19 2024 Add documentation and demo vid to readme
- Aug 17 2024 Add docstrings and documentation
- Aug 4 2024 Add changelog
- Aug 3 2024 Initial commit


