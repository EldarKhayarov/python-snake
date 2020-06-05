import curses
import random


INITIAL_DELAY = 80
DIRECTIONS = (
    curses.KEY_UP,
    curses.KEY_DOWN,
    curses.KEY_LEFT,
    curses.KEY_RIGHT,
)
CHAR_SNAKE_HEAD = '0'
CHAR_SNAKE_BODY = 'o'
CHAR_FOOD = '*'
CHAR_SPACE = ' '
CHAR_WALL = '#'

window: curses.window
delay: int

snake: list
ate_food: list
food: tuple
score: int


def make_snake(x: int, y: int, length: int = 3) -> list:
    return [make_snake_chain(x, y + i) for i in range(length)]


def make_snake_chain(x: int, y: int) -> tuple:
    return x, y


def make_food(max_x: int, max_y: int) -> tuple:
    global snake

    while True:
        result = (random.randint(1, max_x), random.randint(1, max_y))
        if result not in snake:
            return result


def head_on_snake(snake: list) -> bool:
    if len(snake) > 2 and snake[0] in [(s[0], s[1]) for s in snake[1:]]:
        return True
    return False


def head_on_food(snake: list, food: tuple) -> bool:
    if snake[0][0] == food[0] and snake[0][1] == food[1]:
        return True
    return False


def init_window():
    global window
    global delay
    delay = INITIAL_DELAY
    screen = curses.initscr()
    curses.curs_set(0)
    screen_height, screen_width = screen.getmaxyx()
    window = curses.newwin(screen_height, screen_width, 0, 0)
    window.keypad(True)
    window.timeout(delay)


def init_game():
    global snake
    global window
    global food
    global score
    global ate_food

    # Ate food
    ate_food = []

    # Make a snake
    max_y, max_x = window.getmaxyx()
    snk_x, snk_y = max_x // 2, max_y // 2
    snake = make_snake(snk_x, snk_y)

    # Show snake
    window.addch(snake[0][1], snake[0][0], CHAR_SNAKE_HEAD)
    for x, y in snake[1:]:
        window.addch(y, x, CHAR_SNAKE_BODY)

    # Make food
    food = make_food(max_x, max_y)
    # Show food
    window.addch(food[1], food[0], CHAR_FOOD)
    # Init score
    score = 0


def loop():
    # init global variables
    global window
    global snake
    global food
    global score
    global ate_food

    # Set UP direction by default
    snake_direction = curses.KEY_UP
    max_y, max_x = window.getmaxyx()

    while True:
        new_snake_direction = window.getch()
        if new_snake_direction == curses.KEY_BREAK:
            break

        if new_snake_direction in DIRECTIONS:
            snake_direction = new_snake_direction

        # Check new snake direction
        if snake_direction == curses.KEY_UP:
            new_snake_head = make_snake_chain(snake[0][0], snake[0][1] - 1)
        elif snake_direction == curses.KEY_DOWN:
            new_snake_head = make_snake_chain(snake[0][0], snake[0][1] + 1)
        elif snake_direction == curses.KEY_LEFT:
            new_snake_head = make_snake_chain(snake[0][0] - 1, snake[0][1])
        elif snake_direction == curses.KEY_RIGHT:
            new_snake_head = make_snake_chain(snake[0][0] + 1, snake[0][1])
        else:
            raise ValueError("Key value isn't in the available keys list.")

        # Create a new snake
        if snake[-1] in ate_food:
            body = snake
            ate_food.remove(snake[-1])
        else:
            body = snake[:-1]
            # Delete tail char
            # y then x
            window.addch(snake[-1][1], snake[-1][0], CHAR_SPACE)

        snake = [new_snake_head, *body]
        head = snake[0]
        # Show head at the new position
        window.addch(snake[1][1], snake[1][0], CHAR_SNAKE_BODY)
        window.addch(snake[0][1], snake[0][0], CHAR_SNAKE_HEAD)

        # Go out of bounds
        if not (0 < head[0] < max_x and 0 < head[1] < max_y):
            end_game(f"You're lose. Your score is {score}.")
            break

        # Snake eats itself
        if head_on_snake(snake):
            end_game(f"You're lose. Your score is {score}.")
            break

        # Snake eats food
        if head_on_food(snake, food):
            ate_food.append(food)
            score += 1
            # Generate new food position
            food = make_food(max_x, max_y)
            # Show food at the new position
            window.addch(food[1], food[0], CHAR_FOOD)

        # Snake takes whole window
        if len(snake) == (max_y + 1) * (max_x + 1):
            end_game(f"You're won with score: {score}.")
            break


def end_game(message):
    print(message)


if __name__ == '__main__':
    init_window()
    init_game()
    loop()
