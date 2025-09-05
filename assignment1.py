import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BOARD_WIDTH = 100
BOARD_HEIGHT = 10
BALL_RADIUS = 10
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 10
LIVES = 3
TARGET_SCORE = 5  # Set the target score to win
FONT = pygame.font.SysFont("freesansbold.ttf", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Ball")

# Game objects
class Board:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = 350
        self.dx = 5

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.dx
        if direction == "right" and self.x < SCREEN_WIDTH - BOARD_WIDTH:
            self.x += self.dx

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, BOARD_WIDTH, BOARD_HEIGHT))

class Ball:
    def __init__(self):
        self.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        self.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT // 2)
        self.dx = random.choice([-3, 3])
        self.dy = 3

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x <= BALL_RADIUS or self.x >= SCREEN_WIDTH - BALL_RADIUS:
            self.dx *= -1
        if self.y <= BALL_RADIUS:
            self.dy *= -1

    def bounce(self):
        self.dy *= -1

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)

    def collide_with_board(self, board):
        return (self.y + BALL_RADIUS >= board.y and
                board.x <= self.x <= board.x + BOARD_WIDTH)

class Obstacle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.y = 0  # Start from the ceiling
        self.speed = 2  # Falling speed

    def move(self):
        self.y += self.speed

        # Reset obstacle when it goes off the screen
        if self.y > SCREEN_HEIGHT:
            self.x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            self.y = 0

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    def collide_with_board(self, board):
        return (self.y + OBSTACLE_HEIGHT >= board.y and
                board.x <= self.x <= board.x + BOARD_WIDTH)

# Game functions
def show_text(text, x, y):
    label = FONT.render(text, True, WHITE)
    screen.blit(label, (x, y))

def game_over_screen():
    screen.fill(BLACK)
    show_text("Game Over!", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20)
    pygame.display.flip()
    pygame.time.wait(3000)

def win_screen():
    screen.fill(BLACK)
    show_text("You Win!", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20)
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
def main():
    board = Board()
    ball = Ball()
    obstacles = [Obstacle() for _ in range(3)]
    lives = LIVES
    score = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Board movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            board.move("left")
        if keys[pygame.K_RIGHT]:
            board.move("right")

        # Ball movement
        ball.move()

        # Check for ball-board collision
        if ball.collide_with_board(board):
            ball.bounce()
            score += 1  # Player gains a point each time the ball hits the board

        # Check for obstacle movement and collision with board
        for obstacle in obstacles:
            obstacle.move()
            if obstacle.collide_with_board(board):
                lives -= 1
                obstacle.y = 0  # Reset obstacle position after hit

        # Check for ball falling off the screen (touching the bottom)
        if ball.y > SCREEN_HEIGHT:
            lives -= 1
            ball = Ball()  # Reset ball after it touches the bottom

        # Draw objects
        board.draw()
        ball.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # Display score and lives
        show_text(f"Score: {score}", 10, 10)
        show_text(f"Lives: {lives}", SCREEN_WIDTH - 120, 10)

        # Check for win condition
        if score >= TARGET_SCORE:
            win_screen()
            running = False

        # Game over logic
        if lives <= 0:
            game_over_screen()
            running = False

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
