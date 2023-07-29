import pygame
import random

pygame.init()

width = 800
height = 900
blockSize = 30

shape_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 97, 3), (255, 255, 0), (255, 20, 147), (147, 112, 219)]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]
I = [['.0...',
      '.0...',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '.....',
      '.0000',
      '.....']]
L = [['.0...',
      '.0...',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '.000.',
      '.0...',
      '.....',
      '.....'],
     ['.....',
      '00...',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '...0.',
      '.000.',
      '.....',
      '.....']]
J = [['.0...',
      '.0...',
      '00...',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.00..',
      '.0...',
      '.0...',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '000..',
      '..0..',
      '.....']]
S = [['.....',
      '.00..',
      '00...',
      '.....',
      '.....'],
     ['.....',
      '0....',
      '00...',
      '.0...',
      '.....']]
Z = [['.....',
      '.0...',
      '00...',
      '0....',
      '.....'],
     ['.....',
      '.....',
      '..00.',
      '...00',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# List of shapes
shapes = [S, I, Z, L, O, J, T]

def get_piece():
    return Piece(5, 0, random.choice(shapes))


def create_grid():
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    return grid


grid = create_grid()


def draw_grid(window, grid):

    for i in range(len(grid)):
        pygame.draw.line(window,
                         (128, 128, 128),
                         (200, 100 + i * blockSize),
                         (500, 100 + i * blockSize)
                         )

# homework: create lines for the columns
# hint: copy and paste above code and then change the number inside the for loop
def draw_shape(piece):
    print(piece)
    #TODO: get shape from piece
    shape = piece.shape
    print(shape)
    rotation = piece.rotation
    print(rotation)
    format = shape[rotation%len(shape)]

    positions = []
    for i in range(len(format)):
        row = list(format[i])
        print(row)
        for j in range(len(row)):
            if(row[j] == "0"):
                print("Hello")
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
        #compare if it equals "0" if it is print ("Hello")
        #['.', '0', '.', '.', '.']
    return positions

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid():
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    return grid


grid = create_grid()




def valid_space(shape, grid):
    accepted_pos = []
    for i in range(20):
        subList = []
        for j in range(10):
            if grid[i][j] == (0,0,0):
                subList.append((j,i))

        for sub in subList:
            accepted_pos.append(sub)

    formatted = draw_shape(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False

    return True

def draw_window(window, grid):
    window.fill((0, 0, 0))
    draw_grid(window, grid)
    font = pygame.font.SysFont("comicsans", 60, bold=True)
    label = font.render("Tetris", 1, (255, 255, 255))
    window.blit(label, (350, 50))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                window,
                grid[i][j],
                (200 + j * blockSize,
                 100 + i * blockSize,
                 blockSize,
                 blockSize),
                0)

    pygame.draw.rect(window,
                    (128, 128 ,128),
                    (200,100,300,600),
                    5)
    draw_grid(window, grid)


def main(window):
    locked_positions = {}
    grid = create_grid()
    current_shape = get_piece()
    next_shape = get_piece()


    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    run = True
    change_shape = False
    while (run):
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time/ 1000> 5 :
            level_time = 0

            if level_time > 0.12:
                level_time -= 0.005
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1
            if not(valid_space(current_shape, grid)) and current_shape.y > 0:
                current_shape.y -= 1
                change_shape = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if not(valid_space(current_shape,grid)):
                        current_shape.y -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                    if not (valid_space(current_shape,grid)):
                        current_shape.rotation -= 1
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not(valid_space(current_shape,grid)):
                        current_shape.x += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not(valid_space(current_shape.grid)):
                        current_shape.x -= 1
        current_piece_position = draw_shape(current_shape)
        if change_shape == True:
            for pos in current_piece_position:
                p = (pos[0],pos[1])
                locked_positions[p] = current_shape.color
                current_shape = next_shape
                next_shape = get_piece()
                change_shape = False

        draw_window(window, grid)
        draw_next_shape(window,next_shape)
        pygame.display.update()

    pygame.quit()









def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text_middle(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main(window)

    pygame.quit()

def draw_next_shape(window, piece):
    font = pygame.font.SysFont("comicsans", 30, bold=True)
    label = font.render("Next Shape", 1, (255, 255, 255))
    window.blit(label, (650, 50))

    shape = piece.shape
    rotation = piece.rotation
    format = shape[rotation % len(shape)]
    for i in range(len(format)):
        row = list(format[i])

        for j in range(len(row)):
            if(row[j] == "0"):
                pygame.draw.rect(window,
                    piece.color,
                    (530 + j * blockSize,
                     300 + i * blockSize,
                     blockSize,
                     blockSize),
                     0)

def draw_text_middle(window):
    font = pygame.font.SysFont("comicsans", 30, bold=True)
    label = font.render("Welcome to Tetris", 1, (255, 255, 255))
    window.blit(label, (width // 2 - label.get_width() // 2, 450))


window = pygame.display.set_mode((width, height))
pygame.display.set_caption("JS's Tetris")
main_menu(window)
