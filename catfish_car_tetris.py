import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (200, 230, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catfish Car Tetris")

# Car types
CAR_TYPES = {
    "sedan": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT, "capacity": 500, "image": "sedan.png", "interior": "sedan_interior.png"},
    "minivan": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT, "capacity": 800, "image": "minivan.png", "interior": "minivan_interior.png"},
    "suv": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT, "capacity": 700, "image": "suv.png", "interior": "suv_interior.png"}
}

# Catfish types
CATFISH_TYPES = {
    "small": {"min_size": 2, "max_size": 4, "score": 10, "image": "small_catfish.png"},
    "medium": {"min_size": 4, "max_size": 6, "score": 20, "image": "medium_catfish.png"},
    "large": {"min_size": 6, "max_size": 8, "score": 30, "image": "large_catfish.png"}
}

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(os.path.join("assets", name)).convert_alpha()
        size = image.get_size()
        return pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    except pygame.error:
        print(f"Unable to load image: {name}")
        return pygame.Surface((50, 50))  # Return a dummy surface if image loading fails

car_images = {car_type: load_image(info["image"], 1) for car_type, info in CAR_TYPES.items()}
car_interiors = {car_type: load_image(info["interior"], 1) for car_type, info in CAR_TYPES.items()}
catfish_images = {catfish_type: load_image(info["image"], 0.3) for catfish_type, info in CATFISH_TYPES.items()}

# Load sounds
try:
    pygame.mixer.music.load(os.path.join("assets", "background_music.mp3"))
    place_sound = pygame.mixer.Sound(os.path.join("assets", "place.wav"))
    splash_sound = pygame.mixer.Sound(os.path.join("assets", "splash.wav"))
except pygame.error:
    print("Unable to load one or more sound files. Continuing without sound.")

class Car:
    def __init__(self, car_type):
        self.type = car_type
        self.width = CAR_TYPES[car_type]["width"]
        self.height = CAR_TYPES[car_type]["height"]
        self.capacity = CAR_TYPES[car_type]["capacity"]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.wetness = 0
        self.image = car_images[car_type]
        self.interior = car_interiors[car_type]

    def draw(self, surface):
        # Draw interior
        surface.blit(self.interior, self.rect)
        
        # Draw exterior with transparency
        exterior = pygame.transform.scale(self.image, (self.width, self.height))
        exterior.set_alpha(128)  # Set transparency (0 is fully transparent, 255 is fully opaque)
        surface.blit(exterior, self.rect)
        
        # Draw wetness meter
        wetness_height = int(self.height * (self.wetness / 100))
        pygame.draw.rect(surface, BLUE, (self.rect.right - 30, self.rect.bottom - wetness_height, 20, wetness_height))

class Catfish:
    def __init__(self, x, catfish_type):
        self.type = catfish_type
        self.size = random.randint(CATFISH_TYPES[catfish_type]["min_size"], CATFISH_TYPES[catfish_type]["max_size"])
        self.rect = pygame.Rect(x, 0, self.size * 20, self.size * 10)  # Increased size
        self.score = CATFISH_TYPES[catfish_type]["score"]
        self.image = catfish_images[catfish_type]

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def draw(self, surface):
        scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        surface.blit(scaled_image, self.rect)

class Game:
    def __init__(self, car_type):
        self.car = Car(car_type)
        self.catfish = None
        self.placed_catfish = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.fall_speed = 1
        self.spawn_initial_catfish()
        self.adjust_initial_catfish_position()

    def adjust_initial_catfish_position(self):
        while self.check_collision(self.catfish):
            self.catfish.rect.y -= 1
        self.catfish.rect.y += 1  # Move it down one pixel to ensure it's just touching

    def spawn_catfish(self):
        catfish_type = random.choice(list(CATFISH_TYPES.keys()))
        x = random.randint(0, SCREEN_WIDTH - CATFISH_TYPES[catfish_type]["max_size"] * 20)
        return Catfish(x, catfish_type)

    def spawn_initial_catfish(self):
        self.catfish = self.spawn_catfish()
        self.catfish.rect.bottom = 0

    def move_catfish(self, dx):
        self.catfish.move(dx, 0)
        if self.check_collision(self.catfish):
            self.catfish.move(-dx, 0)

    def check_collision(self, obj):
        if obj.rect.bottom > self.car.rect.bottom:
            return True
        for placed_catfish in self.placed_catfish:
            if obj.rect.colliderect(placed_catfish.rect):
                return True
        return False

    def update(self):
        if not self.game_over and not self.paused:
            self.catfish.move(0, self.fall_speed)
            if self.check_collision(self.catfish):
                self.catfish.move(0, -self.fall_speed)
                self.place_catfish()
                if not self.game_over:
                    self.spawn_initial_catfish()

    def place_catfish(self):
        self.placed_catfish.append(self.catfish)
        self.score += self.catfish.score
        self.car.wetness += self.catfish.size
        try:
            place_sound.play()
        except NameError:
            pass
        if self.car.wetness >= 100 or len(self.placed_catfish) >= 10 or self.catfish.rect.top <= 0:
            self.game_over = True
            try:
                splash_sound.play()
            except NameError:
                pass
        else:
            self.level_up()
            self.spawn_initial_catfish()
            self.adjust_initial_catfish_position()

    def level_up(self):
        if self.score >= self.level * 100:
            self.level += 1
            self.fall_speed += 0.5

    def draw(self, surface):
        surface.fill(LIGHT_BLUE)
        self.car.draw(surface)
        for catfish in self.placed_catfish:
            catfish.draw(surface)
        if self.catfish:
            self.catfish.draw(surface)
        self.draw_score(surface)
        self.draw_level(surface)

    def draw_score(self, surface):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (10, 10))

    def draw_level(self, surface):
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.level}", True, BLACK)
        surface.blit(level_text, (10, 50))

class HighScores:
    def __init__(self):
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open("high_scores.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_scores(self):
        with open("high_scores.json", "w") as f:
            json.dump(self.scores, f)

    def add_score(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()

    def draw(self, surface):
        font = pygame.font.Font(None, 36)
        title = font.render("High Scores", True, BLACK)
        surface.blit(title, (SCREEN_WIDTH // 2 - 75, 50))
        for i, score in enumerate(self.scores):
            text = font.render(f"{i+1}. {score}", True, BLACK)
            surface.blit(text, (SCREEN_WIDTH // 2 - 50, 100 + i * 40))

def start_screen():
    font = pygame.font.Font(None, 48)
    title = font.render("Catfish Car Tetris", True, BLACK)
    instruction = font.render("Choose your car:", True, BLACK)
    car_options = list(CAR_TYPES.keys())

    selected = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(car_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(car_options)
                elif event.key == pygame.K_RETURN:
                    return car_options[selected]
                elif event.key == pygame.K_h:
                    show_tutorial()

        screen.fill(LIGHT_BLUE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 150, 50))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - 125, 150))
        for i, option in enumerate(car_options):
            color = RED if i == selected else BLACK
            text = font.render(option.capitalize(), True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, 250 + i * 50))
        help_text = font.render("Press H for Help", True, BLACK)
        screen.blit(help_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))
        pygame.display.flip()
        clock.tick(30)

def pause_menu():
    font = pygame.font.Font(None, 48)
    pause_text = font.render("PAUSED", True, RED)
    resume_text = font.render("Press P to Resume", True, BLACK)
    quit_text = font.render("Press Q to Quit", True, BLACK)

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((200, 200, 200))

    screen.blit(overlay, (0, 0))
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50))
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 20))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70))
    pygame.display.flip()

def show_tutorial():
    font = pygame.font.Font(None, 36)
    title = font.render("How to Play", True, BLACK)
    instructions = [
        "Left/Right Arrow: Move catfish",
        "Space: Drop catfish",
        "P: Pause game",
        "",
        "Fill the car with catfish without overflowing!",
        "",
        "Press any key to return to menu"
    ]

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(LIGHT_BLUE)
        screen.blit(title, (SCREEN_WIDTH // 2 - 70, 50))
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            screen.blit(text, (50, 120 + i * 40))
        pygame.display.flip()
        clock.tick(30)

def game_loop():
    clock = pygame.time.Clock()
    high_scores = HighScores()

    while True:
        car_type = start_screen()
        if car_type is None:
            break

        game = Game(car_type)
        try:
            pygame.mixer.music.play(-1)
        except NameError:
            pass

        while not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.move_catfish(-10)
                    elif event.key == pygame.K_RIGHT:
                        game.move_catfish(10)
                    elif event.key == pygame.K_SPACE:
                        while not game.check_collision(game.catfish):
                            game.catfish.move(0, 1)
                        game.catfish.move(0, -1)
                        game.place_catfish()
                        if not game.game_over:
                            game.spawn_initial_catfish()
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused
                        if game.paused:
                            try:
                                pygame.mixer.music.pause()
                            except NameError:
                                pass
                            pause_menu()
                        else:
                            try:
                                pygame.mixer.music.unpause()
                            except NameError:
                                pass

            if not game.paused:
                game.update()
                game.draw(screen)
                pygame.display.flip()

            clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 36))
        pygame.display.flip()
        pygame.time.wait(2000)
        high_scores.add_score(game.score)
        try:
            pygame.mixer.music.stop()
        except NameError:
            pass
        
        # Show high scores
        showing_scores = True
        while showing_scores:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    showing_scores = False

            screen.fill(LIGHT_BLUE)
            high_scores.draw(screen)
            pygame.display.flip()
            clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    game_loop()