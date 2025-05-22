import pygame
import random

# 기초 설정 
SCREEN_WIDTH = 1280 # 화면 x 크기
SCREEN_HEIGHT = 720 # 화면 y 크기
CELL_SIZE = 3 # 픽셀당 사이즈
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE # 픽셀 x 범위
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE # 픽셀 y 범위

# 토양 정보 지정정
AIR = 0
GRAVEL = 1
CLAY = 2
SAND = 3
RAIN_DROP = 5

# 색상
COLOR_MAP = {
    AIR: (135, 206, 235),     # 하늘색
    GRAVEL: (139, 69, 19),    # 자갈
    CLAY: (160, 82, 45),      # 점토
    SAND: (194, 178, 128),    # 모래
    RAIN_DROP: (100, 149, 237)  # 비
}

# 침식 저항력
EROSION_RESISTANCE = {
    GRAVEL: 3,
    CLAY: 2,
    SAND: 1
}

# 강수 설정
RAIN_INTENSITY = 0
MAX_RAIN_INTENSITY = 20
rain_enabled = False

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

# 격자 생성
grid = [[AIR for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
erosion_timers = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 경사진 지형 생성
def create_mountain():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            slope = (GRID_HEIGHT * 0.75) - (x * 0.2)
            if y > slope:
                if y < slope + 40:
                    grid[y][x] = SAND
                elif y < slope + 80:
                    grid[y][x] = CLAY
                else:
                    grid[y][x] = GRAVEL
    # 맨 좌우 열은 항상 AIR로 설정 (지형 없음)
    for y in range(GRID_HEIGHT):
        grid[y][0] = AIR
        grid[y][1] = AIR

create_mountain()

# 그리기 함수들
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

# 비 생성
def rain():
    if rain_enabled and RAIN_INTENSITY > 0:
        for _ in range(RAIN_INTENSITY):
            x = random.randint(0, GRID_WIDTH - 2)
            if grid[0][x] == AIR:
                grid[0][x] = RAIN_DROP

# 비 및 물 업데이트
def update_water():
    for y in reversed(range(GRID_HEIGHT)):
        for x in range(0, GRID_WIDTH - 1):
            if x == 0:
                grid[y][x] = AIR

            if grid[y][x] == RAIN_DROP:
                # 화면 아래 끝면에 닿으면 바로 사라짐
                if y == GRID_HEIGHT - 1:
                    grid[y][x] = AIR
                else:
                    below = grid[y + 1][x]
                    if below == AIR:
                        grid[y + 1][x] = RAIN_DROP
                        grid[y][x] = AIR
                    elif below == RAIN_DROP:
                        grid[y][x]=AIR
                    else:
                        # 좌우 먼저 시도
                        moved = False
                        for dx in [-1, 1]:
                            nx = x + dx
                            if 0 <= nx < GRID_WIDTH and grid[y][nx] == AIR:
                                if grid[y-1][nx]==AIR:
                                    grid[y-1][nx] = RAIN_DROP
                                    grid[y][x] = AIR
                                    moved = True
                                    break
                                else:
                                    grid[y][nx] = RAIN_DROP
                                    grid[y][x] = AIR
                                    moved = True
                                    break 
                            # 침식 시도
                        if below in EROSION_RESISTANCE:
                            erosion_timers[y + 1][x] += 1
                            resistance = EROSION_RESISTANCE[below]
                            if erosion_timers[y + 1][x] >= resistance:
                                erosion_timers[y + 1][x] = 0
                                if grid[y + 1][x] == GRAVEL:
                                    grid[y + 1][x] = CLAY
                                elif grid[y + 1][x] == CLAY:
                                    grid[y + 1][x] = SAND
                                elif grid[y + 1][x] == SAND:
                                    grid[y + 1][x] = AIR
                                grid[y][x] = AIR
                        else:
                            grid[y][x] = AIR
# 슬라이더 조작
def handle_slider(pos):
    global RAIN_INTENSITY
    if slider_rect.collidepoint(pos):
        new_x = max(slider_rect.x, min(pos[0], slider_rect.x + slider_rect.width))
        handle_rect.x = new_x
        ratio = (new_x - slider_rect.x) / slider_rect.width
        RAIN_INTENSITY = int(ratio * MAX_RAIN_INTENSITY)

# 비 스위치
def toggle_rain(pos):
    global rain_enabled
    if switch_rect.collidepoint(pos):
        rain_enabled = not rain_enabled

# === 메인 루프 ===
frame = 0
running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()
    draw_slider()
    draw_switch()
    rain()
    update_water()
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
