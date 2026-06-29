import pygame
import sys
import time

# --- Constants & Initialization ---
pygame.init()
WIDTH, HEIGHT = 450, 450
SIDE_PANEL_WIDTH = 250
BUTTON_HEIGHT = 120
TOTAL_WIDTH = WIDTH + SIDE_PANEL_WIDTH
TOTAL_HEIGHT = HEIGHT + BUTTON_HEIGHT

LINE_WIDTH = 6
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 12
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 28, 28)
LINE_COLOR = (45, 45, 45)
CIRCLE_COLOR = (240, 240, 240)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (0, 230, 118)
BTN_COLOR = (40, 40, 40)
BTN_HOVER_COLOR = (60, 60, 60)
BTN_ACTIVE_COLOR = (0, 150, 136)
PANEL_BG = (20, 20, 20)
METRIC_COLOR = (30, 136, 229)

screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')

# --- Game Logic Setup ---
player = "x"
ai = "o"
board = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]]

game_over = False
current_turn = player
active_algorithm = "minimax"

states_checked = 0
last_duration = 0.0

def is_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    if is_full(board):
        return "tie"
    return None

def minimax(board, depth, isMaximizing):
    global states_checked
    states_checked += 1

    winner = check_winner(board)
    if winner != None:
        if winner == player: return -10
        elif winner == ai: return 10
        elif winner == "tie": return 0
    
    if isMaximizing:
        best_score = float("-inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(best_score, score)
        return best_score

def alpha_beta(board, depth, isMaximizing, alpha, beta):
    global states_checked
    states_checked += 1

    winner = check_winner(board)
    if winner != None:
        if winner == player:
            return -10
        elif winner == ai:
            return 10
        elif winner == "tie":
            return 0
    
    if isMaximizing:
        best_score = float("-inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai
                    score = alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player
                    score = alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

def expectimax(board, depth, isMaximizing):
    global states_checked
    states_checked += 1

    winner = check_winner(board)
    if winner != None:
        if winner == player:
            return -10
        elif winner == ai:
            return 10
        elif winner == "tie":
            return 0
    
    if isMaximizing:
        best_score = float("-inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = ai
                    score = expectimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        total_score = 0
        available_moves = 0
        
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = player
                    score = expectimax(board, depth + 1, True)
                    board[row][col] = " "
                    
                    total_score += score
                    available_moves += 1
        
        if available_moves > 0:
            return total_score / available_moves
        return 0

def best_move(board):
    global states_checked, last_duration

    states_checked = 0
    start_time = time.perf_counter()

    best_score = float("-inf")
    move = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = ai
                
                if active_algorithm == "minimax":
                    score = minimax(board, 0, False)
                elif active_algorithm == "alpha_beta":
                    score = alpha_beta(board, 0, False, float("-inf"), float("inf"))
                elif active_algorithm == "expectimax":
                    score = expectimax(board, 0, False)
                    
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    move = (row, col)

    last_duration = (time.perf_counter() - start_time) * 1000
    
    if move != (-1, -1):
        board[move[0]][move[1]] = ai

def restart_game():
    global board, game_over, current_turn
    board = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]
    game_over = False
    current_turn = player

# --- Pygame Drawing Functions ---
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'o':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'x':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def display_winner(winner_text):
    font = pygame.font.SysFont("Arial", 40, bold=True)
    text = font.render(winner_text, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bg_rect = text_rect.inflate(20, 20)
    pygame.draw.rect(screen, BG_COLOR, bg_rect)
    pygame.draw.rect(screen, TEXT_COLOR, bg_rect, 3)
    screen.blit(text, text_rect)

def draw_ui_panel():
    # Restart Button
    restart_rect = pygame.Rect(0, HEIGHT, WIDTH, 50)
    mouse_pos = pygame.mouse.get_pos()
    
    if restart_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BTN_HOVER_COLOR, restart_rect)
    else:
        pygame.draw.rect(screen, BTN_COLOR, restart_rect)
        
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT), (WIDTH, HEIGHT), 3)
    
    font = pygame.font.SysFont("Arial", 20, bold=True)
    text = font.render("RESTART GAME", True, CIRCLE_COLOR)
    screen.blit(text, text.get_rect(center=restart_rect.center))
    
    # Algorithm Selection Buttons
    algo_y = HEIGHT + 50
    algo_h = BUTTON_HEIGHT - 50
    col_w = WIDTH // 3
    
    algos = [("minimax", "Minimax"), ("alpha_beta", "Alpha-Beta"), ("expectimax", "Expectimax")]
    algo_rects = {}
    
    for i, (key, label) in enumerate(algos):
        rect = pygame.Rect(i * col_w, algo_y, col_w, algo_h)
        algo_rects[key] = rect
        
        if active_algorithm == key:
            pygame.draw.rect(screen, BTN_ACTIVE_COLOR, rect)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BTN_HOVER_COLOR, rect)
        else:
            pygame.draw.rect(screen, BTN_COLOR, rect)
            
        pygame.draw.rect(screen, LINE_COLOR, rect, 1)
        
        lbl_font = pygame.font.SysFont("Arial", 14, bold=True)
        lbl_text = lbl_font.render(label, True, CIRCLE_COLOR)
        screen.blit(lbl_text, lbl_text.get_rect(center=rect.center))
        
    return restart_rect, algo_rects

def draw_side_panel():
    # Base layout background box
    panel_rect = pygame.Rect(WIDTH, 0, SIDE_PANEL_WIDTH, TOTAL_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG, panel_rect)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH, 0), (WIDTH, TOTAL_HEIGHT), 2)
    
    # Header Font
    header_font = pygame.font.SysFont("Arial", 22, bold=True)
    body_font = pygame.font.SysFont("Arial", 16)
    stat_font = pygame.font.SysFont("Arial", 16, bold=True)
    
    # Render Panel Titles
    title = header_font.render("AI METRICS LOG", True, TEXT_COLOR)
    screen.blit(title, (WIDTH + 20, 20))
    pygame.draw.line(screen, LINE_COLOR, (WIDTH + 20, 50), (TOTAL_WIDTH - 20, 50), 1)
    
    # Selected Algortihm Stat
    algo_lbl = body_font.render("Current Algorithm:", True, CIRCLE_COLOR)
    screen.blit(algo_lbl, (WIDTH + 20, 70))
    algo_val = stat_font.render(active_algorithm.upper().replace("_", " "), True, METRIC_COLOR)
    screen.blit(algo_val, (WIDTH + 20, 95))
    
    # States Checked Stat
    states_lbl = body_font.render("States Explored:", True, CIRCLE_COLOR)
    screen.blit(states_lbl, (WIDTH + 20, 140))
    states_val = stat_font.render(f"{states_checked:,} branches", True, METRIC_COLOR)
    screen.blit(states_val, (WIDTH + 20, 165))
    
    # Calculation Speed Stat
    time_lbl = body_font.render("Calculation Time:", True, CIRCLE_COLOR)
    screen.blit(time_lbl, (WIDTH + 20, 210))
    time_val = stat_font.render(f"{last_duration:.2f} ms", True, METRIC_COLOR)
    screen.blit(time_val, (WIDTH + 20, 235))

# --- Main Game Loop ---
while True:
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    
    # Draw UI Button
    restart_btn_rect, algo_rects = draw_ui_panel()
    draw_side_panel()

    if game_over:
        res = check_winner(board)
        if res == "tie":
            display_winner("It's a Tie!")
        else:
            display_winner(f"{res.upper()} Wins!")

    # AI Turn Execution
    if current_turn == ai and not game_over:
        best_move(board)
        current_turn = player
        if check_winner(board):
            game_over = True

    # Event Polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            
            # Click registered on Restart Button
            if restart_btn_rect.collidepoint((mouseX, mouseY)):
                restart_game()
                
            # Click registered on Algorithm Selection Panel
            elif mouseY > HEIGHT + 50:
                for key, rect in algo_rects.items():
                    if rect.collidepoint((mouseX, mouseY)):
                        active_algorithm = key

            # Click registered on Tic Tac Toe Board
            elif mouseY < HEIGHT and not game_over and current_turn == player:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if board[clicked_row][clicked_col] == " ":
                    board[clicked_row][clicked_col] = player
                    current_turn = ai
                    if check_winner(board):
                        game_over = True

    pygame.display.update()