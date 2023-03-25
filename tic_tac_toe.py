import pygame

# Definição de constantes
WIDTH, HEIGHT = 300, 360
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192,192,192)

# Classe para o jogo da velha
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jogo da Velha")
        self.board = [['', '', ''] for _ in range(ROWS)]
        self.ia_mode = False
        self.current_player = 'X'
        self.score_x = 0
        self.score_o = 0
        self.font = pygame.font.Font(None, 24)
        self.score_font = pygame.font.Font(None, 24)
        # self.neural = my_own_ai.perceptron(ROWS, COLS, 1, [9,18,18,18,18,18,18,18,18,18,9])
        # self.translate_ia = lambda number: (number//3, number- 3*(number//3))

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.screen, WHITE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
                text = self.font.render(self.board[row][col], 1, BLACK)
                self.screen.blit(text, (col*SQUARE_SIZE+SQUARE_SIZE//3, row*SQUARE_SIZE+SQUARE_SIZE//3))

    def draw_scores(self):
        score_x_text = self.score_font.render("X: " + str(self.score_x), 1, BLACK)
        self.screen.blit(score_x_text, (10, 310))
        score_o_text = self.score_font.render("O: " + str(self.score_o), 1, BLACK)
        self.screen.blit(score_o_text, (240, 310))

    def switch_player(self):
            if self.current_player == 'O':
                self.current_player = 'X'

            else:
                self.current_player = 'O'


    def mark_square(self, row, col):
        try:
            if self.board[row][col] == '':
                self.board[row][col] = self.current_player
                self.switch_player()
        except:
            pass

    def check_win(self):
        # Checagem de linhas
        for row in self.board:
            if len(set(row)) == 1 and row[0] != '':
                return row[0]

        # Checagem de colunas
        for col in range(COLS):
            if len(set([self.board[row][col] for row in range(ROWS)])) == 1 and self.board[0][col] != '':
                return self.board[0][col]

        # Checagem de diagonais
        if len(set([self.board[i][i] for i in range(ROWS)])) == 1 and self.board[0][0] != '':
            return self.board[0][0]
        if len(set([self.board[i][2-i] for i in range(ROWS)])) == 1 and self.board[0][2] != '':
            return self.board[0][2]

        # Empate
        if all([col.count('') == 0 for col in self.board]):
            return 'tie'

        # Ninguém ganhou
        return None

    def reset_board(self):
        self.board = [['', '', ''] for _ in range(ROWS)]
        self.current_player = 'X'

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not self.check_win():
                    x, y = pygame.mouse.get_pos()
                    row = y // SQUARE_SIZE
                    col = x // SQUARE_SIZE
                    self.mark_square(row, col)

            self.screen.fill(GREY)
            self.draw_board()
            self.draw_scores()

            if self.check_win():
                winner = self.check_win()
                if winner == 'tie':
                    message = "Empate!"
                else:
                    message = f"O jogador {winner} ganhou!"
                    if winner == 'X':
                        self.score_x += 1
                    else:
                        self.score_o += 1
                text = self.font.render(message, 1, BLACK)
                self.screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2))
                pygame.display.update()
                pygame.time.wait(2000)

                self.reset_board()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
