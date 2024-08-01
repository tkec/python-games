import pygame
import sys
import random
from copy import deepcopy

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸和标题
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("数独")

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 字体设置
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# 数独初始局面
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# 创建一个副本，用于用户输入
board = [row[:] for row in initial_board]


# 校验数独是否合法
def is_valid(board, num, pos):
    # 检查行
    for i in range(9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    # 检查列
    for i in range(9):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    # 检查子网格
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True



# 生成一个完整的数独解
# def solve(board):
#     empty = find_empty(board)
#     if not empty:
#         return True
#     row, col = empty
#
#     for num in range(1, 10):
#         if is_valid(board, num, (row, col)):
#             board[row][col] = num
#             if solve(board):
#                 return True
#             board[row][col] = 0
#     return False

def solve(board, rows, cols, boxes):
    """使用递归和回溯算法求解数独，使用剪枝优化。"""
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if not rows[row][num] and not cols[col][num] and not boxes[(row // 3) * 3 + col // 3][num]:
            board[row][col] = num
            rows[row][num] = True
            cols[col][num] = True
            boxes[(row // 3) * 3 + col // 3][num] = True

            if solve(board, rows, cols, boxes):
                return True

            board[row][col] = 0
            rows[row][num] = False
            cols[col][num] = False
            boxes[(row // 3) * 3 + col // 3][num] = False

    return False


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


# def generate_complete_board():
#     board = [[0] * 9 for _ in range(9)]
#     solve(board)
#     return board

def generate_complete_board():
    """生成一个完整的数独解。"""
    board = [[0] * 9 for _ in range(9)]
    rows = [[False] * 10 for _ in range(9)]
    cols = [[False] * 10 for _ in range(9)]
    boxes = [[False] * 10 for _ in range(9)]
    solve(board, rows, cols, boxes)
    return board


# def has_unique_solution(board):
#     solutions = []
#
#     def backtrack(board):
#         if len(solutions) > 1:
#             return
#         empty = find_empty(board)
#         if not empty:
#             solutions.append(deepcopy(board))
#             return
#         row, col = empty
#         for num in range(1, 10):
#             if is_valid(board, num, (row, col)):
#                 board[row][col] = num
#                 backtrack(board)
#                 board[row][col] = 0
#
#     backtrack(board)
#     return len(solutions) == 1


def has_unique_solution(board):
    """检查一个数独棋盘是否有唯一解。"""
    solutions = []

    def backtrack(board, rows, cols, boxes):
        if len(solutions) > 1:
            return
        empty = find_empty(board)
        if not empty:
            solutions.append(deepcopy(board))
            return
        row, col = empty
        for num in range(1, 10):
            if not rows[row][num] and not cols[col][num] and not boxes[(row // 3) * 3 + col // 3][num]:
                board[row][col] = num
                rows[row][num] = True
                cols[col][num] = True
                boxes[(row // 3) * 3 + col // 3][num] = True

                backtrack(board, rows, cols, boxes)

                board[row][col] = 0
                rows[row][num] = False
                cols[col][num] = False
                boxes[(row // 3) * 3 + col // 3][num] = False

    rows = [[False] * 10 for _ in range(9)]
    cols = [[False] * 10 for _ in range(9)]
    boxes = [[False] * 10 for _ in range(9)]

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                rows[i][board[i][j]] = True
                cols[j][board[i][j]] = True
                boxes[(i // 3) * 3 + j // 3][board[i][j]] = True

    backtrack(board, rows, cols, boxes)
    return len(solutions) == 1

# def generate_new_board():
#     board = generate_complete_board()
#     solve(board)
#     cells = [(i, j) for i in range(9) for j in range(9)]
#     random.shuffle(cells)
#     for row, col in cells:
#         backup = board[row][col]
#         board[row][col] = 0
#         if not has_unique_solution(board):
#             board[row][col] = backup
#     return board

def generate_new_board():
    """生成一个新的数独局面，保证唯一解。"""
    board = generate_complete_board()
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for row, col in cells:
        backup = board[row][col]
        board[row][col] = 0
        if not has_unique_solution(board):
            board[row][col] = backup
    return board


# 画网格
def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(screen, BLACK, (i * 60, 0), (i * 60, 540), thickness)
        pygame.draw.line(screen, BLACK, (0, i * 60), (540, i * 60), thickness)


# 画数独棋盘
def draw_board(selected_cell=None):
    screen.fill(WHITE)
    draw_grid()
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                if initial_board[i][j] != 0:
                    value = font.render(str(board[i][j]), True, BLACK)
                else:
                    value = font.render(str(board[i][j]), True, BLUE)
                screen.blit(value, (j * 60 + 20, i * 60 + 15))
    if selected_cell:
        pygame.draw.rect(screen, YELLOW, (selected_cell[1] * 60, selected_cell[0] * 60, 60, 60), 3)


# 按钮类
class Button:
    def __init__(self, text, pos, size, font, bg_color=GRAY, fg_color=BLACK, disabled_color=GRAY):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.disabled_color = disabled_color
        self.rect = pygame.Rect(pos, size)
        self.disabled = False

    def draw(self, screen):
        if self.disabled:
            pygame.draw.rect(screen, self.disabled_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.fg_color)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.disabled

    def set_disabled(self, disabled):
        self.disabled = disabled


# 检查是否成功
def check_win():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0 or not is_valid(board, board[i][j], (i, j)):
                return False
    return True


# 显示非法输入提示
def show_invalid_input():
    message = small_font.render("wrong", True, RED)
    # screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 50))
    screen.blit(message, ((WIDTH // 2) + message.get_width(), HEIGHT - 40))


# 显示成功提示框
def show_success_dialog():
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100))
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100), 2)
    message = small_font.render("success！", True, BLACK)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 40))
    confirm_button.draw(screen)


# 主循环
running = True
selected_cell = None
show_invalid = False
invalid_time = 0
clock = pygame.time.Clock()
win = False

# 新游戏按钮
new_game_button = Button("New", (WIDTH // 2 - 50, HEIGHT - 45), (100, 40), small_font)
confirm_button = Button("Confirm", (WIDTH // 2 - 40, HEIGHT // 2 + 20), (80, 40), small_font)

while running:
    screen.fill(WHITE)
    draw_board(selected_cell)

    if show_invalid:
        show_invalid_input()
        if pygame.time.get_ticks() - invalid_time > 2000:
            show_invalid = False

    if win:
        show_success_dialog()
    else:
        new_game_button.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if new_game_button.is_clicked(event.pos):
                new_game_button.set_disabled(True)
                board = generate_new_board()
                initial_board = [row[:] for row in board]
                selected_cell = None
                win = False
                new_game_button.set_disabled(False)  # 生成完成后重新启用按钮
            elif confirm_button.is_clicked(event.pos):
                win = False
                new_game_button.set_disabled(False)
            elif not win:
                if x < 540 and y < 540:
                    selected_cell = (y // 60, x // 60)
                else:
                    selected_cell = None
        elif event.type == pygame.KEYDOWN and selected_cell:
            row, col = selected_cell
            if initial_board[row][col] == 0:  # 确保不能修改初始的数字
                key = event.key
                num = None
                if key == pygame.K_0 or key == pygame.K_DELETE:  # 检查按下的是0或者DELETE
                    num = 0
                    board[row][col] = 0
                elif pygame.K_1 <= key <= pygame.K_9:
                    num = key - pygame.K_0
                    board[row][col] = num

                    if not is_valid(board, num, selected_cell):
                        show_invalid = True
                        invalid_time = pygame.time.get_ticks()
                        board[selected_cell[0]][selected_cell[1]] = 0
                    if check_win():
                        win = True

    clock.tick(30)

pygame.quit()
sys.exit()
