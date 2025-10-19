#!/usr/bin/env python3

import os
import sys
import time
import pygame as pg
from pygame.locals import *
from minMaxAgent import MinMaxAgent

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR_X = (233, 65, 65)
LINE_COLOR_O = (0, 134, 244)
FPS = 30

def find_assets_path():
    """Determines the correct path to the assets folder."""
    # Path when running as a Flatpak
    flatpak_path = '/app/share/game/assets'
    if os.path.isdir(flatpak_path):
        return flatpak_path
    # Path when running directly from source
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'assets')

ASSETS_PATH = find_assets_path()

class Game:
    def __init__(self):
        """Initializes the game, Pygame, and all game assets."""
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100), 0, 32)
        pg.display.set_caption("Tic Tac Toe")
        self.clock = pg.time.Clock()

        self.bot = MinMaxAgent()
        self.mapping = {'x': 1, None: 0, 'o': -1}
        
        # Game state variables
        self.game_state = "MENU"  # Can be "MENU" or "PLAYING"
        self.game_mode = None  # Can be "vs_bot" or "vs_human"
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.turn = 'x'
        self.winner = None
        self.draw = False
        self.scores = {'x': 0, 'o': 0, 'draws': 0}
        self.last_match_result = "Select a mode to start!"

        self.load_assets()

    def load_assets(self):
        """Loads all images and fonts."""
        try:
            self.cover_img = pg.image.load(os.path.join(ASSETS_PATH, 'cover.png'))
            self.x_img = pg.image.load(os.path.join(ASSETS_PATH, 'x.png'))
            self.o_img = pg.image.load(os.path.join(ASSETS_PATH, 'o.png'))
            self.one_player_img = pg.image.load(os.path.join(ASSETS_PATH, 'one_player.png'))
            self.two_players_img = pg.image.load(os.path.join(ASSETS_PATH, 'two_players.png'))

            # Scale images
            self.cover_img = pg.transform.scale(self.cover_img, (SCREEN_WIDTH, SCREEN_HEIGHT + 100))
            self.x_img = pg.transform.scale(self.x_img, (80, 80))
            self.o_img = pg.transform.scale(self.o_img, (80, 80))
            self.one_player_img = pg.transform.scale(self.one_player_img, (200, 102))
            self.two_players_img = pg.transform.scale(self.two_players_img, (200, 102))
            
            # Button rectangles for menu
            self.one_player_rect = self.one_player_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
            self.two_players_rect = self.two_players_img.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))
            
            # Fonts
            self.font = pg.font.Font(None, 30)

        except pg.error as e:
            print(f"Error loading assets: {e}")
            sys.exit()

    def draw_menu(self):
        """Draws the initial game mode selection menu."""
        self.screen.fill(WHITE)
        self.screen.blit(self.one_player_img, self.one_player_rect)
        self.screen.blit(self.two_players_img, self.two_players_rect)
        pg.display.update()

    def draw_board(self):
        """Draws the game board grid and status bar."""
        self.screen.fill(WHITE)
        # Vertical lines
        pg.draw.line(self.screen, BLACK, (SCREEN_WIDTH / 3, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGHT), 7)
        pg.draw.line(self.screen, BLACK, (SCREEN_WIDTH / 3 * 2, 0), (SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT), 7)
        # Horizontal lines
        pg.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT / 3), (SCREEN_WIDTH, SCREEN_HEIGHT / 3), 7)
        pg.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT / 3 * 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 3 * 2), 7)
        self.draw_status()
    
    def draw_status(self):
        """Draws the score and status information on the bottom bar."""
        total_games = self.scores['x'] + self.scores['o'] + self.scores['draws']
        
        score_text = (f"Win X: {self.scores['x']}/{total_games} | "
                      f"Win O: {self.scores['o']}/{total_games} | "
                      f"Draws: {self.scores['draws']}/{total_games}")

        if self.winner:
            message = f"Last Match: {self.winner.upper()} won!"
        elif self.draw:
            message = "Last Match: Game Draw!"
        else:
            message = f"{self.turn.upper()}'s Turn"

        # Render text
        font = pg.font.Font(None, 24)
        score_surface = font.render(score_text, True, WHITE)
        message_surface = font.render(message, True, WHITE)
        
        # Position and draw
        self.screen.fill(BLACK, (0, 400, 500, 100))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 425))
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH / 2, 465))
        
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(message_surface, message_rect)
        pg.display.update()

    def check_win(self):
        """Checks for a win or draw condition and updates scores."""
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winner = self.board[row][0]
                line_color = LINE_COLOR_X if self.winner == 'x' else LINE_COLOR_O
                pg.draw.line(self.screen, line_color, (0, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6),
                             (SCREEN_WIDTH, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6), 4)
                break
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winner = self.board[0][col]
                line_color = LINE_COLOR_X if self.winner == 'x' else LINE_COLOR_O
                pg.draw.line(self.screen, line_color, ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, 0),
                             ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, SCREEN_HEIGHT), 4)
                break
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winner = self.board[0][0]
            line_color = LINE_COLOR_X if self.winner == 'x' else LINE_COLOR_O
            pg.draw.line(self.screen, line_color, (50, 50), (350, 350), 4)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winner = self.board[0][2]
            line_color = LINE_COLOR_X if self.winner == 'x' else LINE_COLOR_O
            pg.draw.line(self.screen, line_color, (350, 50), (50, 350), 4)
        
        # Check for draw
        if all(all(row) for row in self.board) and self.winner is None:
            self.draw = True
        
        # Update scores if game is over
        if self.winner:
            self.scores[self.winner] += 1
        elif self.draw:
            self.scores['draws'] += 1
        
        self.draw_status()

    def draw_xo(self, row, col):
        """Draws an X or O on the board at the specified row and column."""
        self.board[row-1][col-1] = self.turn
        
        posx = (col - 1) * (SCREEN_WIDTH / 3) + 30
        posy = (row - 1) * (SCREEN_HEIGHT / 3) + 30

        if self.turn == 'x':
            self.screen.blit(self.x_img, (posx, posy))
            self.turn = 'o'
        else:
            self.screen.blit(self.o_img, (posx, posy))
            self.turn = 'x'
        pg.display.update()

    def handle_click(self):
        """Handles user mouse clicks on the board."""
        x, y = pg.mouse.get_pos()
        
        if y > SCREEN_HEIGHT: return  # Click was on the status bar

        col = int(x // (SCREEN_WIDTH / 3)) + 1
        row = int(y // (SCREEN_HEIGHT / 3)) + 1

        if row and col and self.board[row-1][col-1] is None:
            self.draw_xo(row, col)
            self.check_win()

            # Bot's turn if in vs_bot mode and game is not over
            if self.game_mode == 'vs_bot' and not (self.winner or self.draw):
                agent_board = [[self.mapping[cell] for cell in row] for row in self.board]
                r, c, _ = self.bot.chooseAction(agent_board, self.mapping[self.turn])
                time.sleep(0.25) # Add a small delay for bot's move
                self.draw_xo(r + 1, c + 1)
                self.check_win()

    def reset_game(self):
        """Resets the game board for the next match."""
        time.sleep(.1)
        self.turn = 'x'
        self.draw = False
        self.winner = None
        self.board = [[None] * 3, [None] * 3, [None] * 3]
        self.draw_board()

    def run(self):
        """The main game loop."""
        self.screen.blit(self.cover_img, (0, 0))
        pg.display.update()
        time.sleep(.1)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                if self.game_state == "MENU":
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.one_player_rect.collidepoint(event.pos):
                            self.game_mode = "vs_bot"
                            self.game_state = "PLAYING"
                            self.draw_board()
                        elif self.two_players_rect.collidepoint(event.pos):
                            self.game_mode = "vs_human"
                            self.game_state = "PLAYING"
                            self.draw_board()
                
                elif self.game_state == "PLAYING":
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.winner or self.draw:
                            self.reset_game()
                        else:
                            self.handle_click()
            
            if self.game_state == "MENU":
                self.draw_menu()

            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
