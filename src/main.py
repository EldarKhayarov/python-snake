import curses
import random


INITIAL_DELAY = 100
DIRECTIONS = (
    curses.KEY_UP,
    curses.KEY_DOWN,
    curses.KEY_LEFT,
    curses.KEY_RIGHT,
)

window: curses.window
delay: int

snake: dict
food: list


def make_snake(x, y, length=3):
    result = [(x, y + i) for i in range(length)]

    return result


def make_food(max_x, max_y, random_position=False):
    global snake
    if not random_position:
        return max_x // 2, max_y // 2

    while True:
        result = (random.randint(0, max_x + 1), random.randint(0, max_y + 1))
        if result not in snake:
            return result


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

    # make a snake
    my, mx = window.getmaxyx()
    snk_x, snk_y = mx // 2, my // 2
    snake = make_snake(snk_x, snk_y)


def loop():
    global window
    global snake
    global food
    snake_direction = curses.KEY_UP
    max_y, max_x = window.getmaxyx()

    while True:
        new_snake_direction = window.getch()
        if new_snake_direction == curses.KEY_BREAK:
            break

        if new_snake_direction in DIRECTIONS:
            snake_direction = new_snake_direction

        # check new snake vector
        if snake_direction == curses.KEY_UP:
            new_snake_head = (snake[0][0], snake[0][1] - 1)
        elif snake_direction == curses.KEY_DOWN:
            new_snake_head = (snake[0][0], snake[0][1] + 1)
        elif snake_direction == curses.KEY_LEFT:
            new_snake_head = (snake[0][0] - 1, snake[0][1])
        elif snake_direction == curses.KEY_RIGHT:
            new_snake_head = (snake[0][0] + 1, snake[0][1])
        else:
            raise ValueError("Key value isn't in the available keys list.")

        # create a new snake
        snake = [new_snake_head, *snake[1:]]
        head = snake[0]

        # Go out of bounds
        if not (0 <= head[0] <= max_x and 0 <= head[1] <= max_y):
            end_game("You're lose.")

        # TODO: If snake eats itself

        # TODO: If snake eats food

        # TODO: If snake takes whole window


def end_game(message):
    # TODO: make endpoint
    print(message)


if __name__ == '__main__':
    init_window()
    init_game()
    loop()
