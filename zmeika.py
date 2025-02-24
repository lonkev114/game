import pygame
import random
import time
import csv
import App

# Инициализация Pygame
pygame.init()
# Размер окна фиксированный
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
back1 = pygame.image.load("Kartinki_muzyka/silach.png")
back1 = pygame.transform.scale(back1, (WIDTH, HEIGHT))
sila = pygame.image.load("Kartinki_muzyka/dota4.jpg")
sila = pygame.transform.scale(sila, (WIDTH, HEIGHT))
back = pygame.image.load("Kartinki_muzyka/back.png")
back = pygame.transform.scale(back, (WIDTH, HEIGHT))
music_files = ["Kartinki_muzyka/Дон Омар feat Tego Calderon - Los Bandoleros.mp3", "Kartinki_muzyka/skrillex-damian-jr_-gong-marley-make-it-bun-dem.mp3", "Kartinki_muzyka/betsy-marija-jankovskaja-sigma-bojj.mp3"]

music_buttons = [
    {"label": "Главное - семья", "rect": pygame.Rect(10, 500, 210, 30), "file": music_files[0]},
    {"label": "Make it bun dem", "rect": pygame.Rect(10, 550, 215, 30), "file": music_files[1]},
    {"label": "Сигма", "rect": pygame.Rect(230, 500, 90, 30), "file": music_files[2]},
]

# Кнопка выключения музыки
sound_off_button_w, sound_off_button_h = 50, 50
sound_off_button  = pygame.image.load("Kartinki_muzyka/inamik.png")
sound_off_button = pygame.transform.scale(sound_off_button, (sound_off_button_w, sound_off_button_h))
sound_toggle_button = pygame.Rect(WIDTH - 70, 20, 50, 50)


# Цвета
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
amamam = pygame.mixer.Sound("Kartinki_muzyka/am-am-am.mp3")
pobeda = pygame.mixer.Sound("Kartinki_muzyka/aplodismentyi-nebolshoy-gruppyi-lyudey-s-radostnyimi-krikami.mp3")
taimer = pygame.mixer.Sound("Kartinki_muzyka/cursed-crown.mp3")
# Определяем размеры уровней (кол-во клеток)
LEVELS = {
    1: (7, 7),
    2: (10, 10),
    3: (12, 12),
}
# Экран ввода имени
def get_player_name():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    active = False
    text = ""
    while True:
        screen.fill(WHITE)
        label = font.render("Введите имя:", True, (0, 0, 0))
        screen.blit(label, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    main()
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text.strip():
                        return text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
# Функция для вычисления размера клетки
def get_cell_size(level):
    cols, rows = LEVELS[level]
    return min(WIDTH // cols, HEIGHT // rows)

# Загружаем спрайты (меняются по размеру под клетку)
def load_sprites(cell_size):
    head = pygame.image.load("Kartinki_muzyka/jeskiflow.jfif")
    body = pygame.image.load("Kartinki_muzyka/vodichka.jfif")
    apple = pygame.image.load("Kartinki_muzyka/bounty.png")
    wall = pygame.image.load("Kartinki_muzyka/wall.png")

    return {
        "head": pygame.transform.scale(head, (cell_size, cell_size)),
        "body": pygame.transform.scale(body, (cell_size, cell_size)),
        "apple": pygame.transform.scale(apple, (cell_size, cell_size)),
        "wall": pygame.transform.scale(wall, (cell_size, cell_size))
    }
# Функция для проверки, можно ли спавнить яблоко в данной позиции
def is_valid_apple_position(pos, walls, snake_body):
    return pos not in walls and pos not in snake_body

# Спавн яблока
def spawn_apple(columns, rows, walls, snake_body):
    while True:
        apple = (random.randint(0, columns - 1), random.randint(0, rows - 1))
        if is_valid_apple_position(apple, walls, snake_body):
            return apple
# Выбор уровня
def select_level():
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    pygame.display.set_caption("Змейка")
    buttons = [
        {"text": "Уровень 1", "rect": pygame.Rect(50, 30, 200, 50), "level": 1},
        {"text": "Уровень 2", "rect": pygame.Rect(50, 100, 200, 50), "level": 2},
        {"text": "Уровень 3", "rect": pygame.Rect(50, 170, 200, 50), "level": 3},
        {"text": "Back to main menu", "rect": pygame.Rect(440, 540, 350, 50), "level": 4},
        {"text": "Результаты", "rect": pygame.Rect(440, 480, 350, 50), "level": 5}  # Новая кнопка
    ]

    while True:
        screen.blit(sila, (0, 0))
        for btn in buttons:
            pygame.draw.rect(screen, GREEN, btn["rect"])
            text = font.render(btn["text"], True, BLACK)
            screen.blit(text, (btn["rect"].x + 20, btn["rect"].y + 10))
        for button in music_buttons:
            pygame.draw.rect(screen, (200, 200, 200), button["rect"])
            label = button_font.render(button["label"], True, (0, 0, 0))
            screen.blit(label, (button["rect"].x + 10, button["rect"].y + 5))

        screen.blit(sound_off_button, (WIDTH - 60, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    App.app()
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos) and btn["level"] != 4 and btn["level"] != 5:
                        return btn["level"]
                    elif btn["rect"].collidepoint(pos) and btn["level"] == 4:
                        App.app()
                        pygame.quit()
                        exit()
                    elif btn["rect"].collidepoint(pos) and btn["level"] == 5:
                        display_results()  # Переход к окну результатов
                for button in music_buttons:
                    if button["rect"].collidepoint(pos):
                        pygame.mixer.music.load(button["file"])
                        pygame.mixer.music.play(-1)
                        last = pygame.mixer.music.play(-1)
                if sound_toggle_button.collidepoint(pos):
                    pygame.mixer.music.stop()
# Класс змейки
class Snake:
    def __init__(self, cell_size):
        self.body = [(3, 3)]
        self.direction = (1, 0)  # Начинаем движение вправо
        self.cell_size = cell_size

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        self.body.insert(0, new_head)
        self.body.pop()  # Удаляем хвост

    def grow(self):
        self.body.append(self.body[-1])  # Увеличиваем змейку

    def draw(self, sprites):
        # Отрисовка головы
        head_x, head_y = self.body[0]
        screen.blit(sprites["head"], (head_x * self.cell_size, head_y * self.cell_size))

        # Отрисовка тела
        for segment in self.body[1:]:
            x, y = segment
            screen.blit(sprites["body"], (x * self.cell_size, y * self.cell_size))

def display_victory_screen(score, elapsed_time, player_name, level):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    # Тексты
    victory_text = font.render("Победа!", True, (0, 250, 0))
    score_text = small_font.render(f"Счет: {score}", True, (0, 250, 0))
    time_text = small_font.render(f"Время: {elapsed_time} сек.", True, (0, 250, 0))

    # Кнопки
    restart_button = small_font.render("Начать заново", True, (0, 250, 0))
    exit_button = small_font.render("Выход", True, (0, 250, 0))

    # Позиции текста и кнопок
    text_x = WIDTH // 2 - victory_text.get_width() // 2
    score_x = WIDTH // 2 - score_text.get_width() // 2
    time_x = WIDTH // 2 - time_text.get_width() // 2
    restart_x = WIDTH // 2 - restart_button.get_width() // 2
    exit_x = WIDTH // 2 - exit_button.get_width() // 2

    # Воспроизведение звука победы
    pobeda.play()

    # Основной цикл экрана победы
    running = True
    while running:
        screen.blit(back1, (0, 0))  # Отрисовка фона
        screen.blit(victory_text, (text_x, 150))
        screen.blit(score_text, (score_x, 250))
        screen.blit(time_text, (time_x, 300))

        # Отрисовка кнопок
        screen.blit(restart_button, (restart_x, 350))
        screen.blit(exit_button, (exit_x, 400))

        # Обновление экрана
        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    running = False
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Проверка нажатия на кнопку "Начать заново"
                if (restart_x <= mouse_pos[0] <= restart_x + restart_button.get_width() and
                    350 <= mouse_pos[1] <= 350 + restart_button.get_height()):
                    save_score(player_name, level, score, elapsed_time)  # Сохранение результата
                    main()  # Возврат в main()

                # Проверка нажатия на кнопку "Выход"
                if (exit_x <= mouse_pos[0] <= exit_x + exit_button.get_width() and
                    400 <= mouse_pos[1] <= 400 + exit_button.get_height()):
                    save_score(player_name, level, score, elapsed_time)  # Сохранение результата
                    running = False
                    pygame.quit()
                    exit()

# Сохранение счета в CSV
def save_score(player_name, level, score, elapsed_time):
    with open("game_scores_zmeika.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player_name, level, score, elapsed_time])

# Загрузка счета из CSV
def load_scores(level):
    scores = []
    with open("game_scores_zmeika.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[1]) == level:  # Проверяем уровень
                # Добавляем имя, счет и время
                scores.append((row[0], int(row[2]), float(row[3])))  # Имя, счет, время
    # Сортируем сначала по очкам (по убыванию), затем по времени (по возрастанию)
    scores.sort(key=lambda x: (-x[1], x[2]))
    return scores[:5]  # Возвращаем топ-5

# Результаты
def display_results():
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    result_font = pygame.font.Font(None, 28)

    level_buttons = [
        {"rect": pygame.Rect(40, 100, 200, 50), "label": "Уровень 1", "level": 1},
        {"rect": pygame.Rect(40, 200, 200, 50), "label": "Уровень 2", "level": 2},
        {"rect": pygame.Rect(40, 300, 200, 50), "label": "Уровень 3", "level": 3},
    ]
    back_button = pygame.Rect(WIDTH - 150, HEIGHT - 70, 120, 50)

    selected_level = None

    while True:
        screen.blit(back, (0, 0))  # Используем фон из основной игры
        title = font.render("Результаты", True, (255, 255, 255))
        screen.blit(title, (40, 10))

        for button in level_buttons:
            pygame.draw.rect(screen, (0, 255, 0), button["rect"])
            label = button_font.render(button["label"], True, (0, 0, 0))
            screen.blit(label, (button["rect"].x + 10, button["rect"].y + 10))

        pygame.draw.rect(screen, (255, 0, 0), back_button)
        label = button_font.render("Назад", True, (0, 0, 0))
        screen.blit(label, (back_button.x + 10, back_button.y + 10))

        if selected_level:
            scores = load_scores(selected_level)
            y_offset = 400
            for i, (name, score, time) in enumerate(scores):
                result_text = f"{i + 1}место: {name}: {score} очков, {time:.2f} сек"
                result_label = result_font.render(result_text, True, (255, 255, 255))
                screen.blit(result_label, (40, y_offset))
                y_offset += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    main()
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in level_buttons:
                    if button["rect"].collidepoint(pos):
                        selected_level = button["level"]
                if back_button.collidepoint(pos):
                    return  # Возврат в главное меню
# Основная игра
def main():

    level = select_level()
    columns, rows = LEVELS[level]
    cell_size = get_cell_size(level)
    sprites = load_sprites(cell_size)
    score = 0
    # Скорость змейки в зависимости от уровня
    FPS = {1: 4, 2: 6, 3: 9}[level]
    clock = pygame.time.Clock()
    start_time = time.time()
    # Создаем змейку
    snake = Snake(cell_size)

    # Стены на 3 уровне
    walls = []
    # Спавн яблока при начале игры
    apple = spawn_apple(columns, rows, walls, snake.body)


    if level == 3:
        for y in range(2, rows - 2):
            walls.append((2, y))
            walls.append((columns, y))  # Смещение стен правее

    player_name = get_player_name()
    running = True
    taime=True
    while running:
        screen.blit(back, (0, 0))
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != (0, -1):
                    snake.direction = (0, 1)

        # Движение змейки
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.body[0] == apple:
            amamam.play()
            snake.grow()
            score += 1
            apple = spawn_apple(columns, rows, walls, snake.body)

        # Проверка столкновения со стенами
        if level == 3 and snake.body[0] in walls:
            running = False
            elapsed_time = int(time.time() - start_time)
            display_victory_screen(score, elapsed_time, player_name, level)
        # Проверка на выход за границы
        head_x, head_y = snake.body[0]
        if head_x < 0 or head_x > columns or head_y < 0 or head_y >= rows:
            running = False
            elapsed_time = int(time.time() - start_time)
            display_victory_screen(score, elapsed_time, player_name, level)
        # Проверка на столкновение с собой
        if snake.body[0] in snake.body[2:]:
            running = False
            elapsed_time = int(time.time() - start_time)
            display_victory_screen(score, elapsed_time, player_name, level)
        # Отрисовка змейки
        snake.draw(sprites)

        # Отрисовка яблока
        apple_x, apple_y = apple
        screen.blit(sprites["apple"], (apple_x * cell_size, apple_y * cell_size))

        # Отрисовка стен
        for wall_x, wall_y in walls:
            screen.blit(sprites["wall"], (wall_x * cell_size, wall_y * cell_size))
        pygame.display.flip()
        clock.tick(5)

        while taime:
            taimer.play()
            pygame.time.delay(4100)
            taime = False
