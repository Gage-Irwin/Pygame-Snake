import pygame
import random
from enum import Enum, auto
pygame.font.init()


BOARD_WIDTH = 17
BOARD_HEIGHT = 15
SNAKE_SPEED = 200


NODE_SIZE = 50
WIDTH = BOARD_WIDTH*NODE_SIZE
HEIGHT = BOARD_HEIGHT*NODE_SIZE
pygame.display.set_caption("snake")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
TEXT_FONT = pygame.font.SysFont('comicsans', 60)
TEXT_FONT_2 = pygame.font.SysFont('comicsans', 30)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
DARK_GREEN = (2, 191, 2)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREY = (169, 169, 169)
DARK_BLUE = (50, 84, 207)
LIGHT_BLUE = (113, 134, 209)

END_SCREEN_WIDTH = WIDTH//1.5
END_SCREEN_HEIGHT = HEIGHT//2
END_SCREEN = pygame.Rect((WIDTH - END_SCREEN_WIDTH)//2, (HEIGHT - END_SCREEN_HEIGHT)//2, END_SCREEN_WIDTH, END_SCREEN_HEIGHT)

class GameState(Enum):
    WIN = auto()
    LOSS = auto()
    CONTINUE = auto()

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Node():

    def __init__(self, x, y, food = False, head = False):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE)
        self.food = food
        self.head = head

    def move(self, x, y):
        self.x, self.y = x, y
        self.rect.x, self.rect.y = self.x*NODE_SIZE, self.y*NODE_SIZE

    def draw(self):
        pygame.draw.rect(screen, DARK_GREEN, self.rect)
        if self.head:
            pygame.draw.rect(screen, GREEN, self.rect)
        if self.food:
            pygame.draw.rect(screen, RED, self.rect)

class Snake():

    def __init__(self):
        self.reset_snake()

    def reset_snake(self):
        self.game_state = GameState.CONTINUE
        self.body = []
        self.body.append(Node((BOARD_WIDTH//4)-1, (BOARD_HEIGHT//2), head=True))
        self.food = Node(BOARD_WIDTH-BOARD_WIDTH//4, BOARD_HEIGHT//2, food=True)
        self.show_ending_screen = True

    def add_snake_body(self, x, y):
        self.body.append(Node(x, y))

    def move_snake(self, direction:Direction):
        if self.game_state != GameState.CONTINUE:
            return False

        head = self.body[0]
        previous_head_pos = (head.x, head.y)
        previous_tail_pos = (self.body[-1].x, self.body[-1].y)

        if direction == Direction.UP:
            if not self.can_move(head.x,head.y-1):
                return False
            head.move(head.x,head.y-1)

        if direction == Direction.DOWN:
            if not self.can_move(head.x,head.y+1):
                return False
            head.move(head.x,head.y+1)

        if direction == Direction.LEFT:
            if not self.can_move(head.x-1,head.y):
                return False
            head.move(head.x-1,head.y)

        if direction == Direction.RIGHT:
            if not self.can_move(head.x+1,head.y):
                return False
            head.move(head.x+1,head.y)

        last_x, last_y = previous_head_pos
        for snake_piece in self.body[1:]:
            temp_x, temp_y = snake_piece.x, snake_piece.y
            snake_piece.move(last_x, last_y)
            last_x, last_y = temp_x, temp_y

        if (head.x, head.y) == (self.food.x, self.food.y):
            self.add_snake_body(previous_tail_pos[0], previous_tail_pos[1])
            self.new_food()

        self.check_game_state()
        return True

    def can_move(self, x, y):
        if len(self.body) < 2:
            return True
        if (x, y) == (self.body[1].x, self.body[1].y):
            return False
        return True

    def new_food(self):
        positions = [(snake_piece.x, snake_piece.y) for snake_piece in self.body]
        rand_x, rand_y = random.randint(0,BOARD_WIDTH-1), random.randint(0,BOARD_HEIGHT-1)
        while (rand_x, rand_y) in positions:
            rand_x, rand_y = random.randint(0,BOARD_WIDTH-1), random.randint(0,BOARD_HEIGHT-1)
        self.food = Node(rand_x, rand_y, food=True)

    def check_game_state(self):
        head = self.body[0]
        if self.is_collision():
            self.game_state = GameState.LOSS

        if head.y > BOARD_HEIGHT-1 or head.y < 0 or head.x > BOARD_WIDTH-1 or head.x < 0:
            self.game_state = GameState.LOSS

        if BOARD_HEIGHT*BOARD_WIDTH == len(self.body):
            self.game_state = GameState.WIN

    def is_collision(self):
        positions = [(snake_piece.x, snake_piece.y) for snake_piece in self.body]
        if len(positions) == len(set(positions)):
            return False
        return True

    def toggle_ending_screen(self):
        if self.game_state != GameState.CONTINUE:
            self.show_ending_screen = not self.show_ending_screen

    def draw(self):
        # draw board background
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if (x+y)%2 == 0:
                    pygame.draw.rect(screen, LIGHT_BLUE, (x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE))
                else:
                    pygame.draw.rect(screen, DARK_BLUE, (x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE))

        # draw food
        self.food.draw()

        # draw snake
        for snake_piece in self.body:
            snake_piece.draw()

        # winner screen
        if self.game_state != GameState.CONTINUE and self.show_ending_screen:
            end_text = TEXT_FONT.render(f"WINNER! {len(self.body)}/{BOARD_HEIGHT*BOARD_WIDTH}", 1, BLACK)
            if self.game_state == GameState.LOSS:
                end_text = TEXT_FONT.render(f"LOSS! {len(self.body)}/{BOARD_HEIGHT*BOARD_WIDTH}", 1, BLACK)
            pygame.draw.rect(screen, WHITE, END_SCREEN)
            pygame.draw.rect(screen, BLACK, END_SCREEN, 5)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//10))
            end_text = TEXT_FONT_2.render("Press 'r' to reset game.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//2))
            end_text = TEXT_FONT_2.render("Press 'h' to show board.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height/1.4))

def main():
    snake = Snake()
    clock = pygame.time.Clock()
    auto_move_snake = pygame.USEREVENT+1
    pygame.time.set_timer(auto_move_snake, SNAKE_SPEED)
    running = True
    last_direction = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    snake.reset_snake()
                    last_direction = None
                if event.key == pygame.K_h:
                    snake.toggle_ending_screen()
                if event.key == pygame.K_w:
                    if snake.move_snake(Direction.UP):
                        last_direction = Direction.UP
                if event.key == pygame.K_s:
                    if snake.move_snake(Direction.DOWN):
                        last_direction = Direction.DOWN
                if event.key == pygame.K_a:
                    if snake.move_snake(Direction.LEFT):
                        last_direction = Direction.LEFT
                if event.key == pygame.K_d:
                    if snake.move_snake(Direction.RIGHT):
                        last_direction = Direction.RIGHT
            if event.type == auto_move_snake:
                if last_direction != None:
                    snake.move_snake(last_direction)

        snake.draw()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()