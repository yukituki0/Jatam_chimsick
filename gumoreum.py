import pygame
import random

CELL_SIZE = 1
ROWS = 180*4
COLS = 320*4
WIDTH = CELL_SIZE * COLS  
HEIGHT = CELL_SIZE * ROWS  

map_data = []

for row in range(ROWS):
    line = [0] * COLS  
    if 60 <= row < 90:
        width = (row - 60) * 2 
        start = COLS // 2 - width // 2
        end = COLS // 2 + width // 2
        for col in range(start, end):
            line[col] = 3  
    elif 90 <= row < 120:
        width = (row - 90) * 3 + 60
        start = COLS // 2 - width // 2
        end = COLS // 2 + width // 2
        for col in range(start, end):
            line[col] = 2  
    elif 120 <= row:
        width = (row - 120) * 4 + 150
        start = COLS // 2 - width // 2
        end = COLS // 2 + width // 2
        for col in range(start, end):
            if 0 <= col < COLS:
                line[col] = 1  
    map_data.append(line)

terrain_soil = {
    0: None,
    1: 'gravel',
    2: 'clay',
    3: 'sand'
}

COLORS = {
    'sand': (194, 178, 128),
    'clay': (210, 105, 30),
    'gravel': (120, 120, 120),
    #'eroded': (220, 220, 220),
    None: (100, 100, 255)
}

EROSION_RESISTANCE = {
    'sand': 0.0001,
    'clay': 0.00005,
    'gravel': 0.00002
}

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("오름 모양 침식 시뮬레이터")

grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

def erode():
    for row in range(ROWS):
        for col in range(COLS):
            tcode = map_data[row][col]
            soil = terrain_soil[tcode]
            if soil and not grid[row][col]:
                if random.random() < EROSION_RESISTANCE[soil]:
                    grid[row][col] = True

def draw():
    for row in range(ROWS):
        for col in range(COLS):
            tcode = map_data[row][col]
            soil = terrain_soil[tcode]
            color = COLORS[None]
            if soil:
                color = COLORS[None] if grid[row][col] else COLORS[soil]
            pygame.draw.rect(win, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    erode()
    draw()

pygame.quit()