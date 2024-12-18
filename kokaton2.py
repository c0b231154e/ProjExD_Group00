import pygame
import sys
import random
import heapq
import pygame as pg
import os

#画像ファイルの場所を取得
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Pygameの初期化
pygame.init()

# 画面の設定
WIDTH, HEIGHT = 1024, 768  # 画面の大きさ
CELL_SIZE = 32  # セルサイズを設定
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# フレームレート
FPS = 60
clock = pygame.time.Clock()

# 迷路生成関数（ゴールを最も遠い点に置く）
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages(cx, cy):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上下左右
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 0 < nx < cols - 1 and 0 < ny < rows - 1 and maze[ny][nx] == 1:
                maze[cy + dy][cx + dx] = 0
                maze[ny][nx] = 0
                carve_passages(nx, ny)

    # 最短距離検索でゴールを位置決定
    def find_furthest_point(start_x, start_y):
        distances = [[-1 for _ in range(cols)] for _ in range(rows)]
        pq = [(0, start_x, start_y)]  # ヒープの初期化
        distances[start_y][start_x] = 0
        furthest = (start_x, start_y, 0)

        while pq:
            dist, x, y = heapq.heappop(pq)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and distances[ny][nx] == -1:
                    new_dist = dist + 1
                    distances[ny][nx] = new_dist
                    heapq.heappush(pq, (new_dist, nx, ny))
                    if new_dist > furthest[2]:
                        furthest = (nx, ny, new_dist)
        return furthest

    maze[1][1] = 0  # プレイヤー初期位置
    carve_passages(1, 1)
    furthest_x, furthest_y, _ = find_furthest_point(1, 1)
    maze[furthest_y][furthest_x] = 2  # ゴール位置
    return maze

# 迷路の生成
maze = generate_maze(ROWS, COLS)

# 壁とゴールのリスト
walls = []
goal = None
for row_index, row in enumerate(maze):
    for col_index, cell in enumerate(row):
        if cell == 1:
            walls.append(pygame.Rect(col_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        elif cell == 2:  # ゴールの位置
            goal = pygame.Rect(col_index * CELL_SIZE, row_index * CELL_SIZE, CELL_SIZE, CELL_SIZE)

# プレイヤーの初期位置
player_size = CELL_SIZE // 2
player_x, player_y = CELL_SIZE + (CELL_SIZE // 4), CELL_SIZE + (CELL_SIZE // 4)
player_speed = 4

# プレイヤー画像の読み込み
player_image = pg.image.load(f"fig/3.png") #こうかとんの画像
player_image = pygame.transform.scale(player_image, (player_size, player_size))  # プレイヤーの大きさにリサイズ

# 描画関数（変更点）
def draw_player(x, y):
    SCREEN.blit(player_image, (x, y))  # 画像を描画

try:
    wall_image = pg.image.load(f"fig/zimen.jpg")  # 壁の画像ファイル
    wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))  # セルサイズにリサイズ
except FileNotFoundError:
    print("Error: 壁の画像ファイルが見つかりません。")
    pygame.quit()
    sys.exit()

# 迷路を描画する関数の修正
def draw_maze():
    for wall in walls:
        SCREEN.blit(wall_image, wall.topleft)  # 壁の位置に画像を描画
    pygame.draw.rect(SCREEN, GREEN, goal)  # ゴールはそのまま

def display_game_clear():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Clear!", True, RED)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


# 背景画像の読み込み
background_image = pg.image.load(f"fig/pg_bg.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # 画面サイズに合わせてリサイズ

# ゲームループ
running = True
while running:
    SCREEN.blit(background_image,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        new_y += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        new_x += player_speed

    player_rect = pygame.Rect(new_x, new_y, player_size, player_size)
    if not any(player_rect.colliderect(wall) for wall in walls):
        player_x, player_y = new_x, new_y

    if player_rect.colliderect(goal):
        display_game_clear()
        running = False

    draw_maze()
    draw_player(player_x, player_y)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
