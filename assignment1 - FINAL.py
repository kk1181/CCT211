import math
import pygame
import random

pygame.init()

# Constants
screen_width = 600
screen_height = 400
obstacle_width = 30
obstacle_height = 10
font = pygame.font.SysFont("freesansbold.ttf", 48)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

pygame.display.set_caption("Catch the Ball")

# Colors
bgColour = (172, 201, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (216, 28, 166)


ballImage = pygame.image.load('ball.png')
ball_diameter = ballImage.get_width()
boardImage = pygame.image.load('board.png')
board_width = boardImage.get_width()
board_height = boardImage.get_height()

class Board:
    def __init__(self):
        self.x = screen_width // 2 - board_width // 2
        self.y = screen_height - 50
        self.dx = 0

    def move(self):
        self.x += self.dx
        # Ensure the board stays within the screen
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - board_width:
            self.x = screen_width - board_width

    def draw(self):
        screen.blit(boardImage, (self.x, self.y))

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(ball_diameter, screen_width - ball_diameter)
        self.y = random.randint(1, 10)
        self.dx = random.choice([-3, 3])
        self.dy = 3

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x < 0 or self.x > screen_width - ball_diameter:
            self.dx *= -1
        if self.y < 0:
            self.dy *= -1

    def draw(self):
        screen.blit(ballImage, (self.x, self.y))

    # Collision
    # Check if the ball collides with the surface of the board
    def collide_with_board(self, board):
        return (board.x < self.x < board.x + board_width) and (self.y + ball_diameter >= board.y) and (self.dy > 0)


class Obstacle:
    def __init__(self):
        self.x = random.randint(0, screen_width - obstacle_width)
        self.y = 0  # Start from the ceiling
        self.dy = 2  # Falling speed

    def move(self):
        self.y += self.dy

        # Reset obstacle when it goes off the screen
        if self.y > screen_height:
            self.x = random.randint(0, screen_width - obstacle_width)
            self.y = 0

    def draw(self):
        pygame.draw.rect(screen, PINK, (self.x, self.y, obstacle_width, obstacle_height))

    # Collision
    # Detect if the obstacle hits the board
    def collide_with_board(self, board):
        if (self.x < board.x + board_width and
                self.x + obstacle_width > board.x and
                self.y < board.y + board_height and
                self.y + obstacle_height > board.y):
            return True
        return False


# Blit text on screen
def show_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

# Game over screen
def game_over_screen():
    screen.fill(BLACK)
    show_text("Game Over!", screen_width // 2 - 80, screen_height // 2 - 20)
    pygame.display.flip()
    pygame.time.wait(3000)

# Win screen
def win_screen():
    screen.fill(BLACK)
    show_text("You Win!", screen_width // 2 - 80, screen_height // 2 - 20)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    board = Board()
    ball = Ball()
    obstacle = []

    # Create 4 obstacles all at once
    for i in range(4):
        obstacle.append(Obstacle())

    score = 0
    lives = 3
    close_game = False

    while not close_game:
        screen.fill(bgColour)
        board.move()
        ball.move()

        # Draw objects
        board.draw()
        ball.draw()

        # Check for collision between ball and board
        if ball.collide_with_board(board):
            # Bounce
            ball.dy *= -1
            score += 1

        # Deduct life and reset ball if it falls off the bottom of the screen
        if ball.y > screen_height:
            lives -= 1
            ball.reset()

        # Draw obstacles and check for collision
        for item in obstacle:
            item.move()
            item.draw()
            if item.collide_with_board(board):
                lives -= 1
                item.y = 0

        # Controls of the player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.dx = -5
                if event.key == pygame.K_RIGHT:
                    board.dx = 5
            if event.type == pygame.KEYUP:
                board.dx = 0

        # Show score
        show_text(f"Score: {score}", 10, 10)
        # Show life
        show_text(f"Lives: {lives}", screen_width - 150, 10)

        # Check for win condition:
        if score >= 5:
            win_screen()
            close_game = True

        # Check for game over:
        if lives <= 0:
            game_over_screen()
            close_game = True

        clock.tick(80)
        pygame.display.flip()



if __name__ == "__main__":
    main()

