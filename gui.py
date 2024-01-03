import pygame
import sys
import random

pygame.init()

# Variables
SCREEN_WIDTH = 810
SCREEN_HEIGHT = 810

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")
selected_cell = (0, 0)
sudoku_puzzle = []

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def sudoku_solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if sudoku_solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]

    while not sudoku_solve(grid):
        grid = [[0 for _ in range(9)] for _ in range(9)]

    holes_to_remove = random.randint(30, 40)
    for _ in range(holes_to_remove):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    return grid

sudoku_puzzle = generate_sudoku()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Functions
def draw_grid():
    for i in range(1, GRID_SIZE):
        if i % 3 == 0:
            pygame.draw.line(screen, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, SCREEN_HEIGHT), 7)
            pygame.draw.line(screen, WHITE, (0, CELL_SIZE * i), (SCREEN_WIDTH, CELL_SIZE * i), 7)
        else:
            pygame.draw.line(screen, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, SCREEN_HEIGHT), 2)
            pygame.draw.line(screen, WHITE, (0, CELL_SIZE * i), (SCREEN_WIDTH, CELL_SIZE * i), 2)

def draw_numbers(grid):
    font = pygame.font.SysFont(("arialblack"), 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != 0:
                number_text = font.render(str(sudoku_puzzle[i][j]), True, WHITE)
                screen.blit(number_text, (j * CELL_SIZE +  30, i * CELL_SIZE + 15))

def draw_board(grid, selected):
    draw_grid()
    draw_numbers(grid)

    transparent_color = (255, 0, 0, 128)
     
    transparent_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(transparent_surface, transparent_color, (CELL_SIZE // 2, CELL_SIZE // 2), 30)

    screen.blit(transparent_surface, (selected[1] * CELL_SIZE, selected[0] * CELL_SIZE))

solve = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_cell = (mouse_y // CELL_SIZE, mouse_x // CELL_SIZE)
        elif event.type == pygame.KEYDOWN and selected_cell:
            if pygame.K_1 <= event.key <= pygame.K_9 and sudoku_puzzle[selected_cell[0]][selected_cell[1]] == 0:
                sudoku_puzzle[selected_cell[0]][selected_cell[1]] = int(event.unicode)
            elif event.key == pygame.K_KP_ENTER:
                if sudoku_solve(sudoku_puzzle):
                    solve = True
                    print("Solved!")
                else:
                    solve = False
                    print("Could not solve :(")

    screen.fill((52, 78, 91))
    draw_board(sudoku_puzzle, selected_cell)

    pygame.display.update()