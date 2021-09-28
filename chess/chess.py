import pygame
import pygame.freetype

pygame.init()
clock = pygame.time.Clock()
screen_size = 720
tile_size = 90
screen = pygame.display.set_mode((screen_size, screen_size))
screen.fill((60, 60, 60))
dragging = False
chess_piece_id_creator = 1
pygame.display.set_caption("Chess")
all_tiles = []
all_pieces = []
all_sprites = pygame.sprite.Group()
white_king_in_check = False
black_king_in_check = False
captured_a_piece = False
total_moves = 0
white_pawn = pygame.image.load("chess_images/wp.png")
white_rook = pygame.image.load("chess_images/wr.png")
white_bishop = pygame.image.load("chess_images/wb.png")
white_knight = pygame.image.load("chess_images/wn.png")
white_queen = pygame.image.load("chess_images/wq.png")
white_king = pygame.image.load("chess_images/wk.png")
black_pawn = pygame.image.load("chess_images/bp.png")
black_rook = pygame.image.load("chess_images/br.png")
black_bishop = pygame.image.load("chess_images/bb.png")
black_knight = pygame.image.load("chess_images/bn.png")
black_queen = pygame.image.load("chess_images/bq.png")
black_king = pygame.image.load("chess_images/bk.png")
white_turn = True
wq_rook = None
wk_rook = None
bq_rook = None
bk_rook = None


class ChessTile:
    def __init__(self, row, column, x_pos, y_pos, size):
        self.row = row
        self.column = column
        self.size = size
        self.hitbox = pygame.Rect(x_pos, y_pos, size, size)
        all_tiles.append(self)
        if (self.row + self.column) % 2 == 0:
            self.color = "white"
        else:
            self.color = "black"

    def draw(self):
        if self.color == "white":
            pygame.draw.rect(screen, (200, 200, 200), self.hitbox)
        else:
            pygame.draw.rect(screen, (120, 120, 120), self.hitbox)

    def on_left_click(self):
        print(f"row: {self.row}")
        print(f"column: {self.column}")

    def signal_available(self):
        pygame.draw.circle(screen, (120, 200, 120), self.hitbox.center, 20)

    def check_occupied(self):
        to_return = ""
        for piece in all_pieces:
            if piece.row == self.row and piece.column == self.column:
                to_return = to_return + piece.color
        return to_return

    def check_en_passant(self):
        for piece in all_pieces:
            if piece.row == self.row and piece.column == self.column and isinstance(piece,
                                                                                    Pawn) and piece.move_number == 1 and total_moves == piece.m_n_when_double_moved + 1:
                return True
        return False


class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, row, column, image, color):
        global chess_piece_id_creator
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (tile_size - 10, tile_size - 10))
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.temp_row = self.row
        self.temp_column = self.column
        all_pieces.append(self)
        self.moveable_squares = []
        self.moved_up_two_last_turn = False
        for tile in all_tiles:
            if tile.row == self.row and tile.column == self.column:
                self.matched_tile = tile
        self.rect.center = self.matched_tile.hitbox.center
        self.color = color
        self.id = chess_piece_id_creator
        self.move_number = 0
        self.m_n_when_double_moved = 0
        self.moveable_squares2 = []
        chess_piece_id_creator += 1

    def snap_to_tile(self, mpos3):
        global total_moves
        global white_turn
        temp_matched_tile = False
        global captured_a_piece
        captured_a_piece = False
        for tile in self.moveable_squares:
            if tile.hitbox.collidepoint(mpos3):
                temp_matched_tile = tile
        if not temp_matched_tile == False:
            for piece in all_pieces:
                if piece.matched_tile == temp_matched_tile:
                    captured_a_piece = True
                    piece.captured()
            self.matched_tile = temp_matched_tile
            if isinstance(self, Pawn) and (
                    self.row == self.matched_tile.row + 2 or self.row == self.matched_tile.row - 2):
                self.m_n_when_double_moved = total_moves
            if isinstance(self, Pawn) and self.column != self.matched_tile.column and captured_a_piece == False:
                for piece in all_pieces:
                    if piece.matched_tile.row == self.matched_tile.row + 1 and piece.matched_tile.column == self.matched_tile.column and self.color == "white":
                        piece.captured()
                    if piece.matched_tile.row == self.matched_tile.row - 1 and piece.matched_tile.column == self.matched_tile.column and self.color == "black":
                        piece.captured()
            if isinstance(self, Pawn) and (self.matched_tile.row == 8 or self.matched_tile.row == 1):
                self.replace_with_queen()
            if isinstance(self, King) and (abs(self.column - self.matched_tile.column)) > 1:
                if self.matched_tile.column == 3:
                    if self.color == "black":
                        for tile in all_tiles:
                            if tile.row == self.row and tile.column == 4:
                                bq_rook.matched_tile = tile
                                bq_rook.rect.center = bq_rook.matched_tile.hitbox.center
                                bq_rook.row = bq_rook.matched_tile.row
                                bq_rook.column = bq_rook.matched_tile.column
                    if self.color == "white":
                        for tile in all_tiles:
                            if tile.row == self.row and tile.column == 4:
                                wq_rook.matched_tile = tile
                                wq_rook.rect.center = wq_rook.matched_tile.hitbox.center
                                wq_rook.row = wq_rook.matched_tile.row
                                wq_rook.column = wq_rook.matched_tile.column
                if self.matched_tile.column == 7:
                    if self.color == "black":
                        for tile in all_tiles:
                            if tile.row == self.row and tile.column == 6:
                                bk_rook.matched_tile = tile
                                bk_rook.rect.center = bk_rook.matched_tile.hitbox.center
                                bk_rook.row = bk_rook.matched_tile.row
                                bk_rook.column = bk_rook.matched_tile.column
                    if self.color == "white":
                        for tile in all_tiles:
                            if tile.row == self.row and tile.column == 6:
                                wk_rook.matched_tile = tile
                                wk_rook.rect.center = wk_rook.matched_tile.hitbox.center
                                wk_rook.row = wk_rook.matched_tile.row
                                wk_rook.column = wk_rook.matched_tile.column
            self.rect.center = self.matched_tile.hitbox.center
            self.row = self.matched_tile.row
            self.column = self.matched_tile.column
            self.move_number += 1
            white_turn = not white_turn
            total_moves += 1

        else:
            self.rect.center = self.matched_tile.hitbox.center
            self.row = self.matched_tile.row
            self.column = self.matched_tile.column
        for piece in all_pieces:
            piece.available_moves()
        king_in_check()

    def show_available_moves(self):
        for tile in self.moveable_squares:
            tile.signal_available()

    def captured(self):
        all_pieces.remove(self)
        all_sprites.remove(self)

    def on_left_click(self):
        pass

    def is_next_move_check(self):
        w_king_check_flag = False
        b_king_check_flag = False
        temp_moveable_squares = []
        for square in self.moveable_squares:
            self.row = square.row
            self.column = square.column
            for piece in all_pieces:
                if piece.color != self.color:
                    piece.moveable_squares.clear()
                    if self.row == piece.row and self.column == piece.column:
                        pass
                    else:
                        piece.available_moves()
            king_in_check()
            if white_king_in_check:
                w_king_check_flag = True
            if black_king_in_check:
                b_king_check_flag = True
            if not w_king_check_flag and self.color == "white":
                temp_moveable_squares.append(square)
            if not b_king_check_flag and self.color == "black":
                temp_moveable_squares.append(square)
            w_king_check_flag = False
            b_king_check_flag = False
        self.row = self.temp_row
        self.column = self.temp_column
        self.moveable_squares = temp_moveable_squares
        self.moveable_squares2 = temp_moveable_squares


class Pawn(ChessPiece):

    def available_moves(self):
        self.moveable_squares.clear()
        not_blocked = False
        if self.color == "white":
            for tile in all_tiles:
                if tile.row == self.row - 1 and tile.column == self.column and tile.check_occupied() == "":
                    self.moveable_squares.append(tile)
                    not_blocked = True
            for tile in all_tiles:
                if tile.row == self.row - 1 and (
                        tile.column == self.column + 1 or tile.column == self.column - 1) and tile.check_occupied() == "black":
                    self.moveable_squares.append(tile)
            if self.move_number == 0:
                for tile in all_tiles:
                    if tile.row == self.row - 2 and tile.column == self.column and tile.check_occupied() == "" and not_blocked:
                        self.moveable_squares.append(tile)
            if self.row == 4:
                for tile in all_tiles:
                    if tile.row == self.row and (
                            tile.column == self.column - 1 or tile.column == self.column + 1) and tile.check_en_passant():
                        for tile2 in all_tiles:
                            if tile2.row == tile.row - 1 and tile2.column == tile.column and tile2.check_occupied() == "":
                                self.moveable_squares.append(tile2)

        else:
            for tile in all_tiles:
                if tile.row == self.row + 1 and tile.column == self.column and tile.check_occupied() == "":
                    self.moveable_squares.append(tile)
                    not_blocked = True
            for tile in all_tiles:
                if tile.row == self.row + 1 and (
                        tile.column == self.column + 1 or tile.column == self.column - 1) and tile.check_occupied() == "white":
                    self.moveable_squares.append(tile)
            if self.move_number == 0:
                for tile in all_tiles:
                    if tile.row == self.row + 2 and tile.column == self.column and tile.check_occupied() == "" and not_blocked:
                        self.moveable_squares.append(tile)
            if self.row == 5:
                for tile in all_tiles:
                    if tile.row == self.row and (
                            tile.column == self.column - 1 or tile.column == self.column + 1) and tile.check_en_passant():
                        for tile2 in all_tiles:
                            if tile2.row == tile.row + 1 and tile2.column == tile.column and tile2.check_occupied() == "":
                                self.moveable_squares.append(tile2)

    def replace_with_queen(self):
        if self.color == "white":
            new_queen = Queen(1, self.matched_tile.column, white_queen, self.color)
            self.captured()
        else:
            new_queen = Queen(8, self.matched_tile.column, black_queen, self.color)
            self.captured()
        all_pieces.append(new_queen)
        all_sprites.add(new_queen)


class Rook(ChessPiece):

    def available_moves(self):
        self.moveable_squares.clear()
        up_blocked = False
        left_blocked = False
        right_blocked = False
        down_blocked = False
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_row > 1 and not up_blocked:
            self.temp_row -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_row < 8 and not down_blocked:
            self.temp_row += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_column > 0 and not left_blocked:
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_column < 8 and not right_blocked:
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break


class Bishop(ChessPiece):
    def __init__(self, row, column, image, color):
        super().__init__(row, column, image, color)
        self.temp_row = self.row
        self.temp_column = self.column

    def available_moves(self):
        self.moveable_squares.clear()
        up_left_blocked = False
        up_right_blocked = False
        down_left_blocked = False
        down_right_blocked = False
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_row > 1 and not up_left_blocked and self.temp_column > 1:
            self.temp_row -= 1
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row > 1 and not up_right_blocked and self.temp_column < 8:
            self.temp_row -= 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row < 8 and not down_left_blocked and self.temp_column > 1:
            self.temp_row += 1
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row > 1 and not up_right_blocked and self.temp_column < 8:
            self.temp_row -= 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row < 8 and not down_right_blocked and self.temp_column < 8:
            self.temp_row += 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break


class Knight(ChessPiece):
    def available_moves(self):
        self.moveable_squares.clear()
        for tile in all_tiles:
            if tile.row == self.row - 2 and tile.column == self.column - 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row - 2 and tile.column == self.column + 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row - 1 and tile.column == self.column - 2 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row - 1 and tile.column == self.column + 2 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row + 1 and tile.column == self.column - 2 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row + 1 and tile.column == self.column + 2 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row + 2 and tile.column == self.column - 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break
        for tile in all_tiles:
            if tile.row == self.row + 2 and tile.column == self.column + 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
                break


class Queen(ChessPiece):

    def available_moves(self):
        self.moveable_squares.clear()
        up_blocked = False
        left_blocked = False
        right_blocked = False
        down_blocked = False
        up_left_blocked = False
        up_right_blocked = False
        down_left_blocked = False
        down_right_blocked = False

        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row > 1 and not up_blocked:
            self.temp_row -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_row < 8 and not down_blocked:
            self.temp_row += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_column > 0 and not left_blocked:
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_column < 8 and not right_blocked:
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column
        while self.temp_row > 1 and not up_left_blocked and self.temp_column > 1:
            self.temp_row -= 1
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row > 1 and not up_right_blocked and self.temp_column < 8:
            self.temp_row -= 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row < 8 and not down_left_blocked and self.temp_column > 1:
            self.temp_row += 1
            self.temp_column -= 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_left_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_left_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row > 1 and not up_right_blocked and self.temp_column < 8:
            self.temp_row -= 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        up_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        up_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break
        self.temp_row = self.row
        self.temp_column = self.column

        while self.temp_row < 8 and not down_right_blocked and self.temp_column < 8:
            self.temp_row += 1
            self.temp_column += 1
            for tile in all_tiles:
                if tile.row == self.temp_row and tile.column == self.temp_column:
                    if tile.check_occupied() != "" and tile.check_occupied() != self.color:
                        self.moveable_squares.append(tile)
                        down_right_blocked = True
                        break
                    if tile.check_occupied() != "" and tile.check_occupied() == self.color:
                        down_right_blocked = True
                        break
                    else:
                        self.moveable_squares.append(tile)
                        break


class King(ChessPiece):
    def available_moves(self):
        self.moveable_squares.clear()
        for tile in all_tiles:
            if self.row - 1 == tile.row and tile.column == self.column - 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row - 1 == tile.row and tile.column == self.column and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row - 1 == tile.row and tile.column == self.column + 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row == tile.row and tile.column == self.column - 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row == tile.row and tile.column == self.column + 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row + 1 == tile.row and tile.column == self.column - 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row + 1 == tile.row and tile.column == self.column and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)
            if self.row + 1 == tile.row and tile.column == self.column + 1 and tile.check_occupied() != self.color:
                self.moveable_squares.append(tile)

        if self.castle_left():
            for tile in all_tiles:
                if tile.row == self.row and tile.column == self.column - 2:
                    self.moveable_squares.append(tile)

        if self.castle_right():
            for tile in all_tiles:
                if tile.row == self.row and tile.column == self.column + 2:
                    self.moveable_squares.append(tile)

    def castle_left(self):
        to_return = True
        if self.move_number == 0:
            if self.color == "white" and wq_rook.move_number == 0:
                i = 2
                while i < 5:
                    for tile in all_tiles:
                        if tile.row == self.row:
                            if tile.column == i and tile.check_occupied() != "":
                                to_return = False
                        if i > 2:
                            for piece in all_pieces:
                                if piece.color != self.color:
                                    for move in piece.moveable_squares:
                                        if move.row == self.row and move.column == i:
                                            to_return = False
                    i += 1
                return to_return
            if self.color == "black" and bq_rook.move_number == 0:
                i = 2
                while i < 5:
                    for tile in all_tiles:
                        if tile.row == self.row:
                            if tile.column == i and tile.check_occupied() != "":
                                to_return = False
                        if i > 2:
                            for piece in all_pieces:
                                if piece.color != self.color:
                                    for move in piece.moveable_squares:
                                        if move.row == self.row and move.column == i:
                                            to_return = False
                    i += 1
                return to_return

    def castle_right(self):
        to_return = True
        if self.move_number == 0:
            if self.color == "white" and wk_rook.move_number == 0:
                i = 6
                while i < 8:
                    for tile in all_tiles:
                        if tile.row == self.row:
                            if tile.column == i and tile.check_occupied() != "":
                                to_return = False
                    for piece in all_pieces:
                        if piece.color != self.color:
                            for move in piece.moveable_squares:
                                if move.row == self.row and move.column == i:
                                    to_return = False
                    i += 1
                return to_return
            if self.color == "black" and bq_rook.move_number == 0:
                i = 6
                while i < 8:
                    for tile in all_tiles:
                        if tile.row == self.row:
                            if tile.column == i and tile.check_occupied() != "":
                                to_return = False
                    for piece in all_pieces:
                        if piece.color != self.color:
                            for move in piece.moveable_squares:
                                if move.row == self.row and move.column == i:
                                    to_return = False
                    i += 1
                return to_return


def create_tiles():
    x_pos = 0
    y_pos = 0
    row = 1
    column = 1
    while row <= 8:
        while column <= 8:
            da_tile = ChessTile(row, column, x_pos, y_pos, tile_size)
            column += 1
            x_pos += tile_size
        row += 1
        y_pos += tile_size
        x_pos = 0
        column = 1


def draw_tiles():
    for tile in all_tiles:
        tile.draw()


def set_up_board():
    i = 1
    global b_king
    global w_king
    global wk_rook
    global bk_rook
    global wq_rook
    global bq_rook
    while i < 9:
        w_pawn = Pawn(7, i, white_pawn, "white")
        i += 1
        all_sprites.add(w_pawn)
    i = 1
    while i < 9:
        b_pawn = Pawn(2, i, black_pawn, "black")
        i += 1
        all_sprites.add(b_pawn)
    wq_rook = Rook(8, 1, white_rook, "white")
    all_sprites.add(wq_rook)
    wk_rook = Rook(8, 8, white_rook, "white")
    all_sprites.add(wk_rook)
    wq_bishop = Bishop(8, 3, white_bishop, "white")
    all_sprites.add(wq_bishop)
    wk_bishop = Bishop(8, 6, white_bishop, "white")
    all_sprites.add(wk_bishop)
    wq_knight = Knight(8, 2, white_knight, "white")
    all_sprites.add(wq_knight)
    wk_knight = Knight(8, 7, white_knight, "white")
    all_sprites.add(wk_knight)
    w_queen = Queen(8, 4, white_queen, "white")
    all_sprites.add(w_queen)
    w_king = King(8, 5, white_king, "white")
    all_sprites.add(w_king)
    bq_rook = Rook(1, 1, black_rook, "black")
    all_sprites.add(bq_rook)
    bk_rook = Rook(1, 8, black_rook, "black")
    all_sprites.add(bk_rook)
    bq_bishop = Bishop(1, 3, black_bishop, "black")
    all_sprites.add(bq_bishop)
    bk_bishop = Bishop(1, 6, black_bishop, "black")
    all_sprites.add(bk_bishop)
    bq_knight = Knight(1, 2, black_knight, "black")
    all_sprites.add(bq_knight)
    bk_knight = Knight(1, 7, black_knight, "black")
    all_sprites.add(bk_knight)
    b_queen = Queen(1, 4, black_queen, "black")
    all_sprites.add(b_queen)
    b_king = King(1, 5, black_king, "black")
    all_sprites.add(b_king)


create_tiles()
draw_tiles()
set_up_board()
dragged_piece = None


def king_in_check():
    global black_king_in_check
    global white_king_in_check
    white_king_in_check = False
    black_king_in_check = False
    for piece in all_pieces:
        if not isinstance(piece, King):
            for tile in piece.moveable_squares:
                if tile.row == b_king.row and tile.column == b_king.column and piece.color == "white":
                    black_king_in_check = True
                if tile.row == w_king.row and tile.column == w_king.column and piece.color == "black":
                    white_king_in_check = True


while True:
    clock.tick(60)
    draw_tiles()
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mpos = pygame.mouse.get_pos()
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(mpos):
                        if white_turn and sprite.color == "white" or not white_turn and sprite.color == "black":
                            dragging = True
                            dragged_piece = sprite
                if dragged_piece is not None:
                    dragged_piece.available_moves()
                    king_in_check()
                    dragged_piece.is_next_move_check()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragged_piece is not None:
                mpos3 = pygame.mouse.get_pos()
                dragged_piece.snap_to_tile(mpos3)
                dragging = False
                dragged_piece = None
    if dragging:
        dragged_piece.show_available_moves()
        mpos2 = pygame.mouse.get_pos()
        dragged_piece.rect.centerx = mpos2[0]
        dragged_piece.rect.centery = mpos2[1]
    pygame.display.flip()
