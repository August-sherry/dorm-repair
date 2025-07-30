import pygame
import sys

# 模块初始化
pygame.init()

# 定义基本内容
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 0, 0)

BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 50
WIDTH = HEIGHT = MARGIN * 2 + (BOARD_SIZE - 1) * CELL_SIZE
VALID_RADIUS = 15

FONT_PATH = "C:/Windows/Fonts/simhei.ttf"

# 游戏初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('五子棋游戏')
board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]  # 创建棋盘
record = []                     # 记录已下的棋子编号
current_player = 'black'        # 先手玩家
game_over = False               # 游戏结束标志
last_move = None                # 记录最后一步棋


def get_chinese_player(player):
    return "黑方" if player == "black" else "白方"


def get_position_number(row, col):
    return row * BOARD_SIZE + col + 1


def get_row_col_from_number(number):
    number -= 1
    return number // BOARD_SIZE, number % BOARD_SIZE


def check_win(row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]          #赢的方向
    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 5:
            return True
    return False


def draw_board():
    screen.fill(BOARD_COLOR)
    for i in range(BOARD_SIZE):
        start = MARGIN + i * CELL_SIZE
        pygame.draw.line(screen, BLACK, (MARGIN, start), (WIDTH - MARGIN, start))
        pygame.draw.line(screen, BLACK, (start, MARGIN), (start, WIDTH - MARGIN))

    # 绘制所有棋子
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col]:
                color = BLACK if board[row][col] == 'black' else WHITE
                pos = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                pygame.draw.circle(screen, color, pos, CELL_SIZE // 2 - 2)

    # 标记最后一步棋
    if last_move:
        row, col = last_move
        pos = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
        pygame.draw.circle(screen, (255, 0, 0) if board[row][col] == 'black' else (0, 0, 255), pos, 5, 1)


def show_status(text):
    font = pygame.font.Font(FONT_PATH, 30)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (MARGIN, 5))


def show_winner_popup(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    popup_width = 300
    popup_height = 150
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, WHITE, popup_rect)

    font = pygame.font.Font(FONT_PATH, 40)
    text = font.render(f"{winner}胜利！", True, (255, 0, 0))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15)))

    small_font = pygame.font.Font(FONT_PATH, 25)
    tip_text = small_font.render('按任意键重新开始', True, BLACK)
    screen.blit(tip_text, tip_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))


def handle_click(pos, player):
    global current_player, game_over, record, last_move

    if game_over:
        return False

    if (player == 'black' and current_player != 'black') or (player == 'white' and current_player != 'white'):
        return False

    x, y = pos
    col = round((x - MARGIN) / CELL_SIZE)
    row = round((y - MARGIN) / CELL_SIZE)

    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return False

    cross_x = (MARGIN + col * CELL_SIZE)
    cross_y = (MARGIN + row * CELL_SIZE)
    dx = x - cross_x
    dy = y - cross_y
    distance_sq = dx ** 2 + dy ** 2

    if distance_sq <= VALID_RADIUS ** 2:
        pos_number = get_position_number(row, col)
        if pos_number not in record:
            board[row][col] = player
            record.append(pos_number)
            last_move = (row, col)

            if check_win(row, col, player):
                game_over = True
                return True

            current_player = 'white' if player == 'black' else 'black'
            return True

    return False


# 游戏的主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键(黑方)
                handle_click(event.pos, 'black')
            elif event.button == 3:  # 右键(白方)
                handle_click(event.pos, 'white')
            elif event.button == 2 and game_over:  # 中键重新开始
                board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
                record = []
                current_player = 'black'
                game_over = False
                last_move = None

    draw_board()
    chinese_player = get_chinese_player(current_player)
    if game_over:
        show_status(f"游戏结束 - {chinese_player}获胜！")
        show_winner_popup(chinese_player)
    else:
        show_status(f'轮到: {chinese_player}下子')
    pygame.display.flip()