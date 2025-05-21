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
RAIN_AREA_WIDTH = 315
RAIN_INTENSITY = 0  # 초기에는 비가 오지 않음
MAX_RAIN_INTENSITY = 100
rain_enabled = False  # 비 ON/OFF 상태

# === 초기화 ===
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# 슬라이더 위치
slider_rect = pygame.Rect(50, SCREEN_HEIGHT - 40, 200, 10)
handle_rect = pygame.Rect(slider_rect.x, slider_rect.y - 5, 10, 20)

# 스위치 버튼
switch_rect = pygame.Rect(300, SCREEN_HEIGHT - 50, 100, 30)

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

def draw_slider():
    pygame.draw.rect(screen, (200, 200, 200), slider_rect)
    pygame.draw.rect(screen, (100, 100, 255), handle_rect)
    intensity_text = font.render(f"Rain Intensity: {RAIN_INTENSITY}", True, (255, 255, 255))
    screen.blit(intensity_text, (slider_rect.x, slider_rect.y - 25))

def draw_switch():
    pygame.draw.rect(screen, (0, 200, 0) if rain_enabled else (200, 0, 0), switch_rect)
    label = font.render("Rain ON" if rain_enabled else "Rain OFF", True, (255, 255, 255))
    screen.blit(label, (switch_rect.x + 10, switch_rect.y + 5))

def rain(frame):
    if rain_enabled and RAIN_INTENSITY > 0:
        for _ in range(RAIN_INTENSITY):
            x = GRID_WIDTH // 2 - RAIN_AREA_WIDTH // 2 + random.randint(0, RAIN_AREA_WIDTH)
            if grid[0][x] == AIR:
                grid[0][x] = WATER

def update_water():
    for y in reversed(range(GRID_HEIGHT - 1)):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y][x] == WATER:
                if grid[y + 1][x] == AIR:
                    grid[y + 1][x] = WATER
                    grid[y][x] = AIR
                elif grid[y + 1][x] in EROSION_RESISTANCE:
                    resistance = EROSION_RESISTANCE[grid[y + 1][x]]
                    if random.random() < 1 / (resistance * 10):
                        grid[y + 1][x] = WATER
                        grid[y][x] = AIR
                    else:
                        grid[y][x] = AIR
                else:
                    grid[y][x] = AIR

def mouse_rain():
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // CELL_SIZE
        grid_y = my // CELL_SIZE
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = grid_x + dx, grid_y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if grid[ny][nx] == AIR:
                        grid[ny][nx] = WATER

def handle_slider(pos):
    global RAIN_INTENSITY
    if slider_rect.collidepoint(pos):
        new_x = max(slider_rect.x, min(pos[0], slider_rect.x + slider_rect.width))
        handle_rect.x = new_x
        ratio = (new_x - slider_rect.x) / slider_rect.width
        RAIN_INTENSITY = int(ratio * MAX_RAIN_INTENSITY)

def toggle_rain(pos):
    global rain_enabled
    if switch_rect.collidepoint(pos):
        rain_enabled = not rain_enabled

def draw_time(frame):
    seconds = frame // 30  # 30 FPS 기준 초 단위 변환
    time_text = font.render(f"Time: {seconds}s", True, (255, 255, 255))
    screen.blit(time_text, (450, SCREEN_HEIGHT - 45))

frame = 0
running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()
    draw_slider()
    draw_switch()
    rain(frame)
    mouse_rain()
    update_water()
    draw_time(frame)
    pygame.display.flip()
    clock.tick(30)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_slider(event.pos)
            toggle_rain(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                handle_slider(event.pos)

pygame.quit()
