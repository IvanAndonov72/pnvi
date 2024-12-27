import pygame
import random
import sys
import os

# Set working directory to the script's location
os.chdir(os.path.dirname(__file__))

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Debugging: Check working directory
print(f"Current working directory: {os.getcwd()}")

# Spaceship logic
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("spaceship.png").convert_alpha()
            print("Spaceship image loaded successfully!")
        except pygame.error as e:
            print(f"Error loading spaceship image: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # Red placeholder
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Asteroid logic
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("asteroid.png").convert_alpha()
            print("Asteroid image loaded successfully!")
        except pygame.error as e:
            print(f"Error loading asteroid image: {e}")
            self.image = pygame.Surface((40, 40))
            self.image.fill((128, 128, 128))  # Gray placeholder
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - 40)

# Crystal logic
class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("energy_crystal.png").convert_alpha()
            print("Crystal image loaded successfully!")
        except pygame.error as e:
            print(f"Error loading crystal image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 255))  # Cyan placeholder
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -30)
            self.rect.x = random.randint(0, WIDTH - 30)

# Sprite groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
crystals = pygame.sprite.Group()

spaceship = Spaceship()
all_sprites.add(spaceship)

for _ in range(5):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

for _ in range(3):
    crystal = Crystal()
    all_sprites.add(crystal)
    crystals.add(crystal)

# Score
score = 0
font = pygame.font.SysFont("Arial", 24)

# Game loop
clock = pygame.time.Clock()
run = True
try:
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Game logic
        all_sprites.update()

        # Collision with asteroid
        if pygame.sprite.spritecollideany(spaceship, asteroids):
            run = False

        # Collect crystals
        collected = pygame.sprite.spritecollide(spaceship, crystals, True)
        for crystal in collected:
            score += 10
            new_crystal = Crystal()
            all_sprites.add(new_crystal)
            crystals.add(new_crystal)

        # Render screen
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    pygame.quit()
    sys.exit()
