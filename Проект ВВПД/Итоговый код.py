import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра: Крестики-нолики и преодоление препятствий")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (160, 32, 240)  
BLUE = (0, 0, 255)      
LIGHT_BLUE = (173, 216, 230) 

CELL_SIZE = 200
font = pygame.font.Font(None, 72)

player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (40, 40))

obstacle_image = pygame.image.load('obstacle.png')
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

background_image_tic_tac_toe = pygame.image.load('background_tic_tac_toe.png')
background_image_tic_tac_toe = pygame.transform.scale(background_image_tic_tac_toe, (WIDTH, HEIGHT))

background_image_obstacles = pygame.image.load('background_obstacles.png')
background_image_obstacles = pygame.transform.scale(background_image_obstacles, (WIDTH, HEIGHT))

background_image_menu = pygame.image.load('background_menu.png') 
background_image_menu = pygame.transform.scale(background_image_menu, (WIDTH, HEIGHT))

def show_message(message, font_size=36, duration=None):
    text_font = pygame.font.Font(None, font_size)
    text = text_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    if duration:
        pygame.time.wait(duration)

def check_winner(board):
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != ' ':
            return True
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            return True
    if board[0] == board[4] == board[8] != ' ':
        return True
    if board[2] == board[4] == board[6] != ' ':
        return True
    return False

def draw_board(board, player_score, bot_score):
    screen.blit(background_image_tic_tac_toe, (0, 0))
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, WHITE, (j * CELL_SIZE + (WIDTH - 3 * CELL_SIZE) // 2, i * CELL_SIZE + (HEIGHT - 3 * CELL_SIZE) // 2, CELL_SIZE, CELL_SIZE), 2)
            if board[i * 3 + j] == 'X':
                text = font.render('X', True, PURPLE)  # Сделал крестики фиолетовыми
                screen.blit(text, (j * CELL_SIZE + (WIDTH - 3 * CELL_SIZE) // 2 + CELL_SIZE // 2 - text.get_width() // 2, i * CELL_SIZE + (HEIGHT - 3 * CELL_SIZE) // 2 + CELL_SIZE // 2 - text.get_height() // 2))
            elif board[i * 3 + j] == 'O':
                text = font.render('O', True, BLUE)  # Сделал нолики синими
                screen.blit(text, (j * CELL_SIZE + (WIDTH - 3 * CELL_SIZE) // 2 + CELL_SIZE // 2 - text.get_width() // 2, i * CELL_SIZE + (HEIGHT - 3 * CELL_SIZE) // 2 + CELL_SIZE // 2 - text.get_height() // 2))
    score_text = font.render(f"Счёт - Вы: {player_score} | Бот: {bot_score}", True, LIGHT_BLUE)
    screen.blit(score_text, (10, 10))
    menu_text = font.render("Нажмите ESC для выхода в меню", True, LIGHT_BLUE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT - 50))
    pygame.display.flip()

def tic_tac_toe(player_score=0, bot_score=0):
    board = [' '] * 9
    player_turn = True
    
    while True:
        draw_board(board, player_score, bot_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mouseX, mouseY = event.pos
                column = (mouseX - (WIDTH - 3 * CELL_SIZE) // 2) // CELL_SIZE
                row = (mouseY - (HEIGHT - 3 * CELL_SIZE) // 2) // CELL_SIZE
                index = row * 3 + column
                if 0 <= index < 9 and board[index] == ' ':
                    board[index] = 'X'
                    if check_winner(board):
                        draw_board(board, player_score, bot_score)
                        show_message("Вы выиграли!", font_size=48)
                        player_score += 1
                        board = [' '] * 9
                        player_turn = True
                    elif ' ' not in board:
                        draw_board(board, player_score, bot_score)
                        show_message("Ничья!", font_size=48)
                        board = [' '] * 9
                        player_turn = True
                    else:
                        player_turn = False
        
        if not player_turn:
            empty_cells = [i for i, x in enumerate(board) if x == ' ']
            if empty_cells:
                index = random.choice(empty_cells)
                board[index] = 'O'
                if check_winner(board):
                    draw_board(board, player_score, bot_score)
                    show_message("Бот выиграл!", font_size=48)
                    bot_score += 1
                    board = [' '] * 9
                elif ' ' not in board:
                    draw_board(board, player_score, bot_score)
                    show_message("Ничья!", font_size=48)
                    board = [' '] * 9
                player_turn = True

class PlayerObstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - 40)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - 40)

def run_obstacle_game():
    player = PlayerObstacle()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    obstacles_group = pygame.sprite.Group()
    for _ in range(6):
        obstacle = Obstacle()
        obstacles_group.add(obstacle)

    running = True
    clock = pygame.time.Clock()
    score = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player_group.update()
        obstacles_group.update()

        if pygame.sprite.spritecollideany(player, obstacles_group):
            show_message("Вы проиграли в игре с препятствиями!")
            running = False

        score += 1 / 60
        screen.blit(background_image_obstacles, (0, 0))
        player_group.draw(screen)
        obstacles_group.draw(screen)

        score_text = font.render(f"Счёт: {int(score)}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

running = True
show_message("Нажмите любую клавишу, чтобы начать игру!")
player_score = 0
bot_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            mode_font = pygame.font.Font(None, 48)
            screen.blit(background_image_menu, (0, 0))  
            text = mode_font.render("Выберите режим: (1) Крестики-нолики, (2) Препятствия", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            tic_tac_toe(player_score, bot_score)
                            waiting = False
                        elif event.key == pygame.K_2:
                            run_obstacle_game()
                            waiting = False

pygame.quit()
