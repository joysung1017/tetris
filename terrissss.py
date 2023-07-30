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
                         (250, 100 + i * blockSize),
                         (550, 100 + i * blockSize)
                         )


    for j in range(len(grid[0])):
        pygame.draw.line(window,
                        (128, 128, 128),
                        (250 + j * blockSize, 100),
                        (250 + j * blockSize, 700)
                        )

# homework: create lines for the columns
# hint: copy and paste above code and then change the number inside the for loop
def draw_shape(piece):

    #TODO: get the shape from piece
    shape = piece.shape

    #TODO: get the rotation from piece
    rotation = piece.rotation

    format = shape[rotation % len(shape)]

    positions = []
    #['.....', '.....', '..00.', '.00..', '.....']
    for i in range(len(format)):
        row = list(format[i])

        for j in range(len(row)):
            if( row[j] == "0"):
                positions.append((piece.x + j, piece.y + i))
            #TODO: compare if it equals "0" if it is print("HELLO)
            # ['.', '0', '.', '.', '.']
    for i , pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions
# In the main function, change the offsets for the grid and "Next
# In the main function, change the offsets for the grid and "Next Shape" text
def draw_window(window, grid):
    window.fill((0, 0, 0))
    draw_grid(window, grid)
    font = pygame.font.SysFont("comicsans", 30, bold=True)
    label = font.render("Tetris", 1, (255, 255, 255))
    window.blit(label, (width // 2 - label.get_width() // 2, 50))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                window,
                grid[i][j],
                (width // 2 - 5 * blockSize + j * blockSize,
                 100 + i * blockSize,
                 blockSize,
                 blockSize),
                0)

    pygame.draw.rect(window,
                    (128, 128 ,128),
                    (width // 2 - 5 * blockSize, 100, 10 * blockSize, 20 * blockSize),
                    5)
    draw_grid(window, grid)


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

grid = create_grid()


def clear_rows(grid, locked_positions):
    completed_rows = []
    for i in range(len(grid)):
        row_completed = True
        for j in range(len(grid[i])):
            if grid[i][j] == (0,0,0):
                row_completed = False
                break
            if row_completed:
                completed_rows.append(i)
    for row in completed_rows:
        del grid[row]
        grid.insert(0,[(0,0,0) for i in range(10)])
        for pos in list(locked_positions):
            x,y = pos
            if y == row:
                del locked_positions[pos]
    return grid



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

def main(window):
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_shape = get_piece()
    next_shape = get_piece()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1

            if not valid_space(current_shape, grid) and current_shape.y > 0:
                current_shape.y -= 1
                for pos in draw_shape(current_shape):
                    x, y = pos
                    if y > -1:
                        locked_positions[pos] = current_shape.color
                current_shape = next_shape
                next_shape = get_piece()
        grid = clear_rows(grid, locked_positions)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if not valid_space(current_shape, grid):
                        current_shape.y -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                    if not valid_space(current_shape, grid):
                        current_shape.rotation -= 1
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not valid_space(current_shape, grid):
                        current_shape.x += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not valid_space(current_shape, grid):
                        current_shape.x -= 1

        current_piece_position = draw_shape(current_shape)
        for i in range(len(current_piece_position)):
            x, y = current_piece_position[i]
            if 0 <= y <= 19:
                grid[y][x] = current_shape.color

        draw_window(window, grid)
        draw_next_shape(window, next_shape)
        pygame.display.update()








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
    window.blit(label, (580, 50))

    shape = piece.shape
    rotation = piece.rotation
    format = shape[rotation % len(shape)]
    for i in range(len(format)):
        row = list(format[i])

        for j in range(len(row)):
            if(row[j] == "0"):
                pygame.draw.rect(window,
                    piece.color,
                    (600 + j * blockSize,
                     250 + i * blockSize,
                     blockSize,
                     blockSize),
                     0)

        window.blit(label, (570,350))

def draw_text_middle(window):
    font = pygame.font.SysFont("comicsans", 30, bold=True)
    label = font.render("Welcome to Tetris", 1, (255, 255, 255))
    window.blit(label, (width // 2 - label.get_width() // 2, 450))


window = pygame.display.set_mode((width, height))
pygame.display.set_caption("JS's Tetris")
main_menu(window)
