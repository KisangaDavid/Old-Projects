import pygame
import random
import time
import pygame.freetype

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
screen.fill((230, 230, 230))
pygame.display.set_caption("Loop Puzzle")

mah_font = pygame.freetype.SysFont("arial", 30)
mah_font2 = pygame.freetype.SysFont("arial", 20)
success_font = pygame.freetype.SysFont("arial", 22)


rows = 5
columns = 5
current_x_pos = 150
current_y_pos = 150
line_id_creator = 1
box_id_creator = 1
allLines = []
allBoxes = []
top_line_info = []
left_line_info = []
right_line_info = []
bottom_line_info = []
awkward_placement = False
error = False
secret_line_error = False


class GridBox:
    def __init__(self, x1, y1, size, row, column):
        global box_id_creator
        self.id = box_id_creator
        box_id_creator += 1
        self.hitbox = pygame.Rect(x1, y1, size, size)
        allBoxes.append(self)
        self.adjacent = []
        self.adjacent2 = []
        self.row = row
        self.column = column
        self.user_adjacent = 0
        self.secret_adjacent = 0
        self.is_shown = False

    # user lines
    def find_adjacent(self):
        for thing in allLines:
            if thing.hitbox.colliderect(self.hitbox):
                self.adjacent.append(thing)
    # secret lines

    def find_adjacent2(self):
        for thing in allLines:
            if thing.hitbox.colliderect(self.hitbox):
                self.adjacent2.append(thing)

    def check_user_lines(self):
        i = 0
        self.find_adjacent()
        for thing in self.adjacent:
            if thing.line_state == 1:
                i += 1
        self.user_adjacent = i
        return i

    def check_secret_lines(self):
        i = 0
        self.find_adjacent2()
        for thing in self.adjacent2:
            if thing.secret_line:
                i += 1
        self.secret_adjacent = i
        return i

    def show_number(self):
        mah_font.render_to(screen, (self.hitbox.centerx - 8, self.hitbox.centery - 10), str(self.secret_adjacent), (40, 40, 40))

    def draw_da_box(self):
        pygame.draw.rect(screen, (20, 20, 240), self.hitbox)

    def clear_box(self):
        screen.fill((230, 230, 230), (self.hitbox.left + 5, self.hitbox.top + 5, 50, 50))


class GridLine:
    def __init__(self, xpos1, ypos1, direction, thickness):
        global line_id_creator
        self.line_state = 0
        self.id = line_id_creator
        line_id_creator += 1
        self.xpos1 = xpos1
        self.ypos1 = ypos1
        self.thickness = thickness
        self.direction = direction
        self.secret_line = False
        if direction == "right":
            self.xpos2 = xpos1 + 60
            self.ypos2 = ypos1
            self.hitbox = pygame.Rect(self.xpos1 + 1, self.ypos1-7, 60, 14)
        if direction == "down":
            self.xpos2 = xpos1
            self.ypos2 = ypos1 + 60
            self.hitbox = pygame.Rect(self.xpos1 - 7, self.ypos1 + 1, 14, 60)
        allLines.append(self)

    def create_line(self):
        pygame.draw.line(screen, (230, 230, 230), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)

    def on_left_click(self):
        if self.line_state == 0 or self.line_state == 2:
            pygame.draw.line(screen, (50, 50, 50), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)
            self.line_state = 1
        elif self.line_state == 1:
            pygame.draw.line(screen, (230, 230, 230), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)
            self.line_state = 0

    def on_right_click(self):
        if self.line_state == 0 or self.line_state == 1:
            self.line_state = 2
            pygame.draw.line(screen, (250, 0, 0), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)
        elif self.line_state == 2:
            self.line_state = 0
            pygame.draw.line(screen, (230, 230, 230), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)

    def show_lines(self):
        pygame.draw.line(screen, (60, 200, 60), (self.xpos1, self.ypos1), (self.xpos2, self.ypos2), self.thickness)
        self.line_state = 0

    def on_secret_click(self):
        self.secret_line = True



def make_row_of_boxes(length, row):
    global current_x_pos
    i = 0
    while i < length:
        i += 1
        da_box = GridBox(current_x_pos + 2, current_y_pos + 2, 59, row, i)
        current_x_pos += 60
    current_x_pos = 150


def make_all_boxes(r, c):
    global current_y_pos
    j = 0
    for row in range(0, r):
        j += 1
        make_row_of_boxes(c, j)
        current_y_pos += 60
    current_y_pos = 150


def draw_whole_line(direction, length):
    global current_x_pos
    global current_y_pos
    i = 0
    if direction == "right":
        while i < length:
            da_line = GridLine(current_x_pos, current_y_pos, "right", 8)
            da_line.create_line()
            current_x_pos += 60
            i += 1
        current_x_pos = 150
    if direction == "down":
        while i < length:
            da_line = GridLine(current_x_pos, current_y_pos, "down", 8)
            da_line.create_line()
            current_y_pos += 60
            i += 1
        current_y_pos = 150


def draw_grid(r, c):
    global current_x_pos
    global current_y_pos
    for row in range(0, r + 1):
        draw_whole_line("right", c)
        current_y_pos += 60
    current_y_pos = 150
    for column in range(0, c + 1):
        draw_whole_line("down", r)
        current_x_pos += 60
    current_x_pos = 150


def draw_row_of_circles(ypos):
    current_xpos = 150
    i = 0
    while i < columns + 1:
        pygame.draw.circle(screen, (50, 50, 50), (current_xpos, ypos), 7)
        current_xpos += 60
        i += 1


def redraw_all_circles():
    current_ypos = 150
    i = 0
    while i < rows + 1:
        draw_row_of_circles(current_ypos)
        current_ypos += 60
        i += 1


def four_start_lines():
    global top_line_info
    global left_line_info
    global right_line_info
    global bottom_line_info
    global awkward_placement
    top_line_info.append(random.randrange(5) * 60 + 150)
    top_line_info.append(random.randrange(2)*60 + 150)
    top_line_info.append("right")
    top_line_info.append("first")
    left_line_info.append(random.randrange(2)*60 + 150)
    left_line_info.append(random.randrange(1, 4) * 60 + 150)
    left_line_info.append("down")
    left_line_info.append("second")
    bottom_line_info.append(random.randrange(5) * 60 + 150)
    bottom_line_info.append(random.randrange(4, 6) * 60 + 150)
    bottom_line_info.append("right")
    bottom_line_info.append("third")
    right_line_info.append(random.randrange(4, 6) * 60 + 150)
    right_line_info.append(random.randrange(1, 4) * 60 + 150)
    right_line_info.append("down")
    right_line_info.append("fourth")

    for thing in allLines:
        if top_line_info[0] == thing.xpos1 and top_line_info[1] == thing.ypos1 and top_line_info[2] == thing.direction:
            thing.on_secret_click()
        if right_line_info[0] == thing.xpos1 and right_line_info[1] == thing.ypos1 and right_line_info[2] == thing.direction:
            thing.on_secret_click()
        if left_line_info[0] == thing.xpos1 and left_line_info[1] == thing.ypos1 and left_line_info[2] == thing.direction:
            thing.on_secret_click()
        if bottom_line_info[0] == thing.xpos1 and bottom_line_info[1] == thing.ypos1 and bottom_line_info[2] == thing.direction:
            thing.on_secret_click()
    if left_line_info[0] == 210 and left_line_info[1] == 330 and bottom_line_info[0] == 150 and bottom_line_info[1] == 390:
        awkward_placement = True


def connect_two_start_lines(start_line, end_line):
    global awkward_placement
    if start_line[3] == "first":
        x_position = start_line[0]
        y_position = start_line[1]
    elif start_line[3] == "second":
        x_position = start_line[0]
        y_position = start_line[1] + 60
    elif start_line[3] == "third":
        x_position = start_line[0] + 60
        y_position = start_line[1]
    elif start_line[3] == "fourth":
        x_position = start_line[0]
        y_position = start_line[1]
    if end_line[3] == "fourth":
        x_destination = end_line[0]
        y_destination = end_line[1] + 60
    elif end_line[3] == "first":
        x_destination = end_line[0] + 60
        y_destination = end_line[1]
    else:
        x_destination = end_line[0]
        y_destination = end_line[1]

    if start_line[3] == "first":
        while x_position != x_destination or y_position != y_destination:
            pygame.display.flip()
            if x_position <= 270:
                if y_position < y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position += 60
                if y_position > y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position -= 60
                if x_position < x_destination:

                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                    x_position += 60
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
            else:
                if x_position < x_destination:
                    x_position += 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                if y_position < y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position += 60
                if y_position > y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position -= 60

    elif start_line[3] == "second":
        if awkward_placement:
            return
        while x_position != x_destination or y_position != y_destination:
            pygame.display.flip()
            if y_position >= 330:
                if x_position < x_destination:
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                    x_position += 60
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                if y_position < y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position += 60
                if y_position > y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position -= 60
            else:
                if y_position < y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position += 60
                if y_position > y_destination:
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                    y_position -= 60
                if x_position < x_destination:
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                    x_position += 60
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()

    elif start_line[3] == "third":
        if awkward_placement:
            x_position = 150
            y_position = 390
            for thing in allLines:
                if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                    thing.on_secret_click()
            y_position += 60
            for thing in allLines:
                if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                    thing.on_secret_click()
            x_position += 60
        while x_position != x_destination or y_position != y_destination:
            pygame.display.flip()
            if x_position >= 330:
                if y_position < y_destination:
                    y_position += 60
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                if y_position > y_destination:
                    y_position -= 60
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                if x_position < x_destination:
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                    x_position += 60
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
            else:
                if x_position < x_destination:
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                    x_position += 60
                if x_position > x_destination:
                    x_position -= 60
                    for thing in allLines:
                        if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                            thing.on_secret_click()
                if y_position < y_destination:
                    y_position += 60
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()
                if y_position > y_destination:
                    y_position -= 60
                    for thing in allLines:
                        if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                            thing.on_secret_click()

    elif start_line[3] == "fourth":
        while x_position != x_destination or y_position != y_destination:
            pygame.display.flip()
            if x_position < x_destination:

                for thing in allLines:
                    if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                        thing.on_secret_click()
                x_position += 60
            if x_position > x_destination:
                x_position -= 60
                for thing in allLines:
                    if thing.ypos1 == y_position and thing.direction == "right" and thing.xpos1 == x_position:
                        thing.on_secret_click()

            if y_position < y_destination:
                y_position += 60
                for thing in allLines:
                    if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                        thing.on_secret_click()
            if y_position > y_destination:
                y_position -= 60
                for thing in allLines:
                    if thing.xpos1 == x_position and thing.direction == "down" and thing.ypos1 == y_position:
                        thing.on_secret_click()


def make_full_loop():
    global top_line_info
    global left_line_info
    global right_line_info
    global bottom_line_info
    global awkward_placement
    awkward_placement = False
    top_line_info.clear()
    left_line_info.clear()
    bottom_line_info.clear()
    right_line_info.clear()
    for line in allLines:
        line.secret_line = False
    four_start_lines()
    connect_two_start_lines(top_line_info, left_line_info)
    connect_two_start_lines(left_line_info, bottom_line_info)
    connect_two_start_lines(bottom_line_info, right_line_info)
    connect_two_start_lines(right_line_info, top_line_info)
    if not check_secret_loop_completion():
        make_full_loop()


def show_numbers():
    for box in allBoxes:
        box.clear_box()
    for box in allBoxes:
        if random.randrange(4) >= 2:
            box.is_shown = True
            box.check_secret_lines()
            box.show_number()



def check_solution():
    global error
    error = False
    check_loop()
    for box in allBoxes:
        if box.is_shown:
            box.check_user_lines()
            if str(box.user_adjacent) != str(box.secret_adjacent):
                error = True
            box.adjacent.clear()
    if error:
        on_fail()
    else:
        on_success()


def on_success():
    time_taken = time.time() - start_time
    screen.fill((230, 230, 230), (0, 0, 600, 100))
    success_font.render_to(screen, (35, 60), f"Success! You have finished this puzzle in {round(time_taken, 2)} seconds!", (80, 220, 80))


def on_fail():
    screen.fill((230, 230, 230), (0, 0, 600, 100))
    mah_font.render_to(screen, (80, 50), "You missed something, try again!", (240, 40, 40))


def check_loop():
    for thing in allLines:
        if thing.line_state == 1:
            only_two_connections(thing, 1)


def only_two_connections(my_line, line_state):
    connect_counter = 0
    global error
    if my_line.direction == "right":
        connecting_x_pos1 = my_line.xpos1
        connecting_y_pos1 = my_line.ypos1
        connecting_x_pos2 = my_line.xpos1 + 60
        connecting_y_pos2 = my_line.ypos1
        for thing in allLines:
            if thing.line_state == line_state:
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 - 60 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos2 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
    if my_line.direction == "down":
        connecting_x_pos1 = my_line.xpos1
        connecting_y_pos1 = my_line.ypos1
        connecting_x_pos2 = my_line.xpos1
        connecting_y_pos2 = my_line.ypos1 + 60
        for thing in allLines:
            if thing.line_state == line_state:
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 - 60 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 and thing.ypos2 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 - 60 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
    if connect_counter != 2:
        error = True

def secret_line_only_two_connections(my_line):
    connect_counter = 0
    global secret_line_error
    if my_line.direction == "right":
        connecting_x_pos1 = my_line.xpos1
        connecting_y_pos1 = my_line.ypos1
        connecting_x_pos2 = my_line.xpos1 + 60
        connecting_y_pos2 = my_line.ypos1
        for thing in allLines:
            if thing.secret_line:
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 - 60 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos2 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos2 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
    if my_line.direction == "down":
        connecting_x_pos1 = my_line.xpos1
        connecting_y_pos1 = my_line.ypos1
        connecting_x_pos2 = my_line.xpos1
        connecting_y_pos2 = my_line.ypos1 + 60
        for thing in allLines:
            if thing.secret_line:
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 and thing.ypos1 == connecting_y_pos2 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos2 - 60 and thing.ypos1 == connecting_y_pos2 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 and thing.ypos2 == connecting_y_pos1 and thing.direction == "down":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 - 60 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
                if thing.xpos1 == connecting_x_pos1 and thing.ypos1 == connecting_y_pos1 and thing.direction == "right":
                    connect_counter += 1
    if connect_counter != 2:
        secret_line_error = True

def check_secret_loop():
    for thing in allLines:
        if thing.secret_line:
            secret_line_only_two_connections(thing)

def check_secret_loop_completion():
    global secret_line_error
    secret_line_error = False
    check_secret_loop()
    if secret_line_error:
        return False
    else:
        return True

def create_new_puzzle():
    global start_time
    allLines.clear()
    allBoxes.clear()
    draw_grid(5, 5)
    make_all_boxes(5, 5)
    make_full_loop()
    show_numbers()
    start_time = time.time()

create_new_puzzle()
mah_font2.render_to(screen, (170, 530), "Press enter to solve the puzzle", (40, 40, 40))
mah_font2.render_to(screen, (135, 560), "Press space to see a possible solution", (40, 40, 40))
mah_font2.render_to(screen, (195, 500), "Press S for a new puzzle", (40, 40, 40))


while True:
    clock.tick(60)
    redraw_all_circles()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if event.button == 1:
                for line in allLines:
                    if line.hitbox.collidepoint(mpos):
                        line.on_left_click()
            elif event.button == 3:
                for line in allLines:
                    if line.hitbox.collidepoint(mpos):
                        line.on_right_click()
        elif event.type == pygame.KEYDOWN and event.key == 13:
            check_solution()
        elif event.type == pygame.KEYDOWN and event.key == 32:
            for thing in allLines:
                if thing.secret_line:
                    thing.show_lines()
        elif event.type == pygame.KEYDOWN and event.key == 115:
            create_new_puzzle()
