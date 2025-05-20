import pygame
import random

# === 설정 ===
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 4
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# 토양 종류
AIR = 0
GRAVEL = 1
CLAY = 2
SAND = 3
WATER = 4

# 색상
COLOR_MAP = {
    AIR: (135, 206, 235),     # 하늘색
    GRAVEL: (139, 69, 19),    # 자갈
    CLAY: (160, 82, 45),      # 점토
    SAND: (194, 178, 128),    # 모래
    WATER: (0, 0, 255)        # 물
}

# 침식 저항력
EROSION_RESISTANCE = {
    GRAVEL: 3,
    CLAY: 2,
    SAND: 1
}

# 강수 설정
RAIN_INTENSITY = 5
RAIN_DURATION = 300
RAIN_AREA_WIDTH = 40

# === 초기화 ===
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

grid = [[AIR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def create_mountain():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if y > GRID_HEIGHT * 0.75:
                grid[y][x] = GRAVEL
            elif y > GRID_HEIGHT * 0.5:
                grid[y][x] = CLAY
            elif y > GRID_HEIGHT * 0.4:
                grid[y][x] = SAND

create_mountain()

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLOR_MAP[grid[y][x]]
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def rain(frame):
    if frame < RAIN_DURATION:
        for _ in range(RAIN_INTENSITY):
            x = GRID_WIDTH // 2 - RAIN_AREA_WIDTH // 2 + random.randint(0, RAIN_AREA_WIDTH)
            if grid[0][x] == AIR:
                grid[0][x] = WATER

def update_water():
    for y in reversed(range(GRID_HEIGHT - 1)):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y][x] == WATER:
                # 아래가 비어 있으면 아래로 이동
                if grid[y + 1][x] == AIR:
                    grid[y + 1][x] = WATER
                    grid[y][x] = AIR
                # 침식 처리
                elif grid[y + 1][x] in EROSION_RESISTANCE:
                    resistance = EROSION_RESISTANCE[grid[y + 1][x]]
                    if random.random() < 1 / (resistance * 10):
                        grid[y + 1][x] = WATER
                        grid[y][x] = AIR
                    else:
                        # 침식되지 않으면 물은 사라짐
                        grid[y][x] = AIR
                else:
                    # 아래가 다른 물질이면 물은 사라짐
                    grid[y][x] = AIR

def mouse_rain():
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # 왼쪽 버튼 클릭 시
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // CELL_SIZE
        grid_y = my // CELL_SIZE
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = grid_x + dx, grid_y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if grid[ny][nx] == AIR:
                        grid[ny][nx] = WATER

frame = 0
running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()
    rain(frame)
    mouse_rain()
    update_water()
    pygame.display.flip()
    clock.tick(30)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
