# Pose-Estimation Flappy (Flappy) Bird

***Welcome to Flappy Flappy Bird, where you can roleplay Flappy Bird!***



Literal flappy bird. Uses your webcam to detect flapping arm motion using pose estimation. Built in 1 day for no particular reason (I was bored). Currently still a protoype, maybe create a webapp later.

### Design

The flappy bird portion is very simple, it's a reimplementation of the standard flappy bird game in Python using the `pygame` library. For pose estimation, we'll use OpenCV to do the video processing and interface with the webcam, while the actual pose estimation is handled using Google's [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) library. To control the bird in-game, we'll track the markers for the person's left and right wrist/forearm and each time we detect sufficient vertical motion, we'll consider it "flapping" and move the bird accordingly. 

**Additional Considerations:**

- Ideally we would trigger the in-game "flap" every time our player's arm move downwards, so we don't need to consider upwards movement in either of the player's arms to trigger "flapping"
- We don't want to continuously trigger "flapping" when the player moves their arms down either though, so we'll set a minimum velocity that the player has to flap for us to consider it "flapping"
- To make things easier, we'll assume that our minimum flapping velocity is fast enough that it's impossible for a person to trigger "flapping" multiple times with a single downwards arm movement



### Changelog
- Aug 17 Add docstrings and documentation
- Aug 4 2024 Add changelog
- Aug 3 2024 Initial commit

## Usage
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
