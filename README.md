# Catfish Car Tetris

Catfish Car Tetris is a quirky and fun game where you stack catfish in various car types. Fill the car with catfish without overflowing and earn points!

## Table of Contents

1. [Installation](#installation)
2. [How to Play](#how-to-play)
3. [Game Features](#game-features)
4. [Dependencies](#dependencies)
5. [File Structure](#file-structure)
6. [Troubleshooting](#troubleshooting)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/catfish-car-tetris.git cd catfish-car-tetris
```

2. Set up a virtual environment (recommended):

```
python3 -m venv venv
```

3. Activate the virtual environment:

- On macOS and Linux:

  ```
  source venv/bin/activate
  ```

- On Windows:

  ```
  venv\Scripts\activate
  ```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

## How to Play

1. Run the game:

```
python catfish_car_tetris.py
```

2. At the start screen, choose your car type using the up and down arrow keys, then press Enter to start.

3. Controls:
- Left Arrow: Move catfish left
- Right Arrow: Move catfish right
- Space: Drop catfish quickly
- P: Pause/Resume game
- H: View tutorial (on start screen)

4. Stack the catfish in the car without overflowing. The game ends when:
- The car's wetness reaches 100%
- You stack 10 catfish
- A catfish touches the top of the screen

5. Try to achieve the highest score possible!

## Game Features

- Three car types to choose from: sedan, minivan, and SUV
- Three catfish sizes: small, medium, and large
- Increasing difficulty as you level up
- High score tracking
- Background music and sound effects

## Dependencies

- Python 3.x
- Pygame

All dependencies are listed in the `requirements.txt` file.

## File Structure

catfish-car-tetris/
│
├── catfish_car_tetris.py
├── requirements.txt
├── README.md
├── high_scores.json
│
└── assets/
├── sedan.png
├── minivan.png
├── suv.png
├── sedan_interior.png
├── minivan_interior.png
├── suv_interior.png
├── small_catfish.png
├── medium_catfish.png
├── large_catfish.png
├── background_music.mp3
├── place.wav
└── splash.wav

Ensure all image and sound files are present in the `assets/` directory.

## Troubleshooting

- If you encounter any issues with loading images or sounds, make sure all files are present in the `assets/` directory.
- If you're having trouble with Pygame installation, refer to the official Pygame documentation for your specific operating system.
- For any other issues, please open an issue on the GitHub repository.

Enjoy playing Catfish Car Tetris!