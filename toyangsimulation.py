import pygame
import sys
import random
# === Pygame 초기화 ===
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("토양 침식 시뮬레이터 설정")
font = pygame.font.SysFont(None, 28)
    
# === 입력창 클래스 ===
class InputBox:
    def __init__(self, x, y, w, h, label, default=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue2')
        self.text = default
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('gray')
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = pygame.Color('gray')
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(font.render(self.label, True, (255, 255, 255)), (self.rect.x - 180, self.rect.y + 5))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        try:
            return float(self.text)
        except ValueError:
            return 0

# === 설정 입력창 생성 ===
input_boxes = [
    InputBox(250, 50, 140, 30, "inclination:", "0.2"),
    InputBox(250, 100, 140, 30, "gravel:", "3"),
    InputBox(250, 150, 140, 30, "clay:", "2"),
    InputBox(250, 200, 140, 30, "sand:", "1"),
]

# 시작 버튼
start_button = pygame.Rect(320, 450, 160, 50)

def settings_screen():
    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                return [box.get_value() for box in input_boxes]

        for box in input_boxes:
            box.draw(screen)

        pygame.draw.rect(screen, (0, 200, 0), start_button)
        start_label = font.render("start", True, (255, 255, 255))
        screen.blit(start_label, (start_button.x + 50, start_button.y + 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# 설정 입력 받기
slope_value, gravel_er, clay_er, sand_er = settings_screen()

# 이제 설정을 반영한 시뮬레이터 실행
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
RAIN_DROP = 5

# 색상
COLOR_MAP = {
    AIR: (135, 206, 235),     # 하늘색
    GRAVEL: (139, 69, 19),    # 자갈
    CLAY: (160, 82, 45),      # 점토
    SAND: (194, 178, 128),    # 모래
    WATER: (0, 0, 255),       # 물
    RAIN_DROP: (100, 149, 237)  # 비
}

EROSION_RESISTANCE = {
    GRAVEL: gravel_er,
    CLAY: clay_er,
    SAND:sand_er
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
def create_mountain(slope_value):
    # 흙 층의 총 두께를 slope_value에 따라 조절 (기본 두께: 60, 범위: 20~80)
    base_thickness = int(max(20, min(80, 80 - slope_value * 60)))

    sand_thickness = base_thickness // 3
    clay_thickness = base_thickness // 3
    gravel_thickness = base_thickness - sand_thickness - clay_thickness

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            slope = (GRID_HEIGHT * 0.75) - (x * slope_value)
            if y > slope:
                if y < slope + sand_thickness:
                    grid[y][x] = SAND
                elif y < slope + sand_thickness + clay_thickness:
                    grid[y][x] = CLAY
                else:
                    grid[y][x] = GRAVEL

    # 맨 좌우 열은 항상 AIR로 설정 (지형 없음)
    for y in range(GRID_HEIGHT):
        grid[y][0] = AIR
        grid[y][1] = AIR

create_mountain(slope_value)

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

def draw_time(frame):
    seconds = frame // 30
    time_text = font.render(f"Time: {seconds}s", True, (255, 255, 255))
    screen.blit(time_text, (450, SCREEN_HEIGHT - 45))

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
            if grid[y][x] == RAIN_DROP:
                # 화면 아래 끝면에 닿으면 바로 사라짐
                if x == 0:
                    grid[y][x] = AIR
                elif y == GRID_HEIGHT - 1:
                    grid[y][x] = AIR
                else:
                    below = grid[y + 1][x]
                    if below == AIR:
                        grid[y + 1][x] = RAIN_DROP
                        grid[y][x] = AIR
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

            elif grid[y][x] == WATER:
                moved = False
                # 좌우 먼저 우선적으로 확산하되, 이미 물이 있는 곳으로는 가지 않음
                for dx in [-1, 1, 0]:
                    ny, nx = y, x + dx
                    if 0 <= nx < GRID_WIDTH:
                        if grid[ny][nx] == AIR:
                            grid[ny][nx] = WATER
                            grid[y][x] = AIR
                            moved = True
                            break
                        elif grid[ny][nx] == WATER:
                            continue  # 물 있는 곳은 건너뜀
                        elif grid[ny][nx] in EROSION_RESISTANCE:
                            resistance = EROSION_RESISTANCE[grid[ny][nx]]
                            if random.random() < 1 / (resistance * 10):
                                grid[ny][nx] = WATER
                                grid[y][x] = AIR
                                moved = True
                                break
                # 아래로 이동은 마지막에 시도
                if not moved and y + 1 < GRID_HEIGHT and grid[y + 1][x] == AIR:
                    grid[y + 1][x] = WATER
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
    draw_time(frame)
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
