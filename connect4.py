import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # 80% of the screen
CELL_SIZE = 80
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create the game grid
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Initialize Pygame screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Connect Four")

# Function to draw the game grid
def draw_grid():
    screen.fill(BLACK)  # Fill the background with black
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if grid[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif grid[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

# Function to check for a win
def check_win(player):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if col + 3 < GRID_WIDTH and grid[row][col] == player and grid[row][col + 1] == player and grid[row][col + 2] == player and grid[row][col + 3] == player:
                return True
            if row + 3 < GRID_HEIGHT and grid[row][col] == player and grid[row + 1][col] == player and grid[row + 2][col] == player and grid[row + 3][col] == player:
                return True
            if col + 3 < GRID_WIDTH and row + 3 < GRID_HEIGHT and grid[row][col] == player and grid[row + 1][col + 1] == player and grid[row + 2][col + 2] == player and grid[row + 3][col + 3] == player:
                return True
            if col - 3 >= 0 and row + 3 < GRID_HEIGHT and grid[row][col] == player and grid[row + 1][col - 1] == player and grid[row + 2][col - 2] == player and grid[row + 3][col - 3] == player:
                return True
    return False

# Main game loop
running = True
current_player = 1
simulated_game = True

while running:
    if simulated_game:
        # Simulate the game with random moves for both players
        for _ in range(GRID_WIDTH * GRID_HEIGHT):
            draw_grid()
            pygame.display.update()

            # Simulate Player 1's move (Random column selection)
            available_columns = [col for col in range(GRID_WIDTH) if grid[0][col] == 0]
            if not available_columns:
                print("It's a draw!")
                grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Reset the grid
                current_player = 1  # Reset the player
                time.sleep(2)  # Pause for 2 seconds before restarting
                break
            move_col = random.choice(available_columns)

            # Initialize the animation row at the top with the correct player's color
            anim_row = 0
            while anim_row < GRID_HEIGHT and grid[anim_row][move_col] == 0:
                draw_grid()
                pygame.draw.circle(screen, RED if current_player == 1 else YELLOW, (move_col * CELL_SIZE + CELL_SIZE // 2, anim_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                pygame.display.update()
                time.sleep(0.2)  # Add a delay for animation
                anim_row += 1

            row = anim_row - 1  # Set the final row where the disc lands
            grid[row][move_col] = current_player

            if check_win(current_player):
                print(f"PC{current_player} wins!")
                time.sleep(2)  # Pause for 2 seconds before restarting
                grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Reset the grid
                current_player = 1  # Reset the player
                break
            else:
                current_player = 3 - current_player  # Toggle between 1 and 2

            time.sleep(1)  # Add a delay for visualization

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
