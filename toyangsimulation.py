import pygame
import random

# 화면 설정
WIDTH, HEIGHT = 1280, 720
ROWS, COLS = 720, 1280
CELL_SIZE = WIDTH // COLS

# 색상
COLORS = {
    'sand': (194, 178, 128),
    'clay': (210, 105, 30),
    'gravel': (120, 120, 120),
    'eroded': (100, 100, 255)
}

# 침식 저항 (값이 낮을수록 쉽게 침식됨)
EROSION_RESISTANCE = {
    'sand': 0.01,
    'clay': 0.005,
    'gravel': 0.002
}

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("오름 침식 시뮬레이터")

# 격자 생성
grid = [[random.choice(['sand', 'clay', 'gravel']) for _ in range(COLS)] for _ in range(ROWS)]
eroded = [[False for _ in range(COLS)] for _ in range(ROWS)]

# 침식 시뮬레이션 함수
def erode():
    for row in range(ROWS):
        for col in range(COLS):
            if not eroded[row][col]:
                soil = grid[row][col]
                if random.random() < EROSION_RESISTANCE[soil]:
                    eroded[row][col] = True

# 그리기 함수
def draw():
    for row in range(ROWS):
        for col in range(COLS):
            color = COLORS['eroded'] if eroded[row][col] else COLORS[grid[row][col]]
            pygame.draw.rect(win, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

# 메인 루프
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(10)  # FPS 설정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    erode()
    draw()

pygame.quit()