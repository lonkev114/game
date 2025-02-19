import pygame
import random
import time
import csv
import App
# Инициализация Pygame
pygame.init()

pygame.display.set_caption("Тир")
LEVELS = {
    1: (5, 1),  # 5 линий по 1 утке
    2: (7, 2),  # 7 линий по 2 утки
    3: (9, 3), # 9 линии по 3 утки
}
# Параметры окна
w, h = 800, 600
FPS = 60
duck_w, duck_h = 60, 40
duck_speed = 5
crosshair_speed = 10
WHITE = (255, 255, 255)

# Настройка окна
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Тир по уточкам")

# Загрузка изображений
win_image = pygame.image.load("perage.jpg")
win_image = pygame.transform.scale(win_image, (w, h))
duck_image = pygame.image.load("duck.png")
duck_image = pygame.transform.scale(duck_image, (duck_w, duck_h))
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (w, h))
game_screen_bg = pygame.image.load("perega.jpg")
game_screen_bg = pygame.transform.scale(game_screen_bg, (w, h))
# Загрузка звуков
impact = pygame.mixer.Sound("Meat_Hook_impact.mp3.mpeg")
pobeda = pygame.mixer.Sound("aplodismentyi-nebolshoy-gruppyi-lyudey-s-radostnyimi-krikami.mp3")
shoot_sound = pygame.mixer.Sound("Meat_Hook.mp3")
music_files = ["Mikhail_SHufutinskijj_-_YA_kalendar_ya_kalendar_ya_kalendar_ya_kalendar_70894577.mp3", "Лепс, Алегрова vs Bring Me The Horizon -- Я тебе не Sleepwalking (online-audio-converter.com).mp3", "g3ox-em-gigachad-theme-phonk-house-version-mp3.mp3"]


# Кнопки треков
music_buttons = [
    {"label": "Я календарь", "rect": pygame.Rect(15, 500, 175, 30), "file": music_files[0]},
    {"label": "Лепс", "rect": pygame.Rect(200, 500, 90, 30), "file": music_files[1]},
    {"label": "Гигачад", "rect": pygame.Rect(310, 500, 120, 30), "file": music_files[2]},
]
# Кнопки остальные
buttons = [
    {"label": "Уровень 1", "rect": pygame.Rect(50, 150, 150, 50), "level": 1},
    {"label": "Уровень 2", "rect": pygame.Rect(50, 220, 150, 50), "level": 2},
    {"label": "Уровень 3", "rect": pygame.Rect(50, 290, 150, 50), "level": 3},
    {"label": "Back to main menu", "rect": pygame.Rect(10, 5, 250, 50), "level": 4}
]
# Кнопка выключения музыки
sound_off_button_w, sound_off_button_h = 50, 50
sound_off_button  = pygame.image.load("inamik.png")
sound_off_button = pygame.transform.scale(sound_off_button, (sound_off_button_w, sound_off_button_h))

sound_on_button  = pygame.image.load("inamikOn.png")
sound_on_button = pygame.transform.scale(sound_off_button, (sound_off_button_w, sound_off_button_h))
sound_toggle_button = pygame.Rect(w - 70, 20, 50, 50)
# Переменная для отслеживания состояния звука
sound_on = False
# Класс утки
class Duck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([-1, 1])

    def move(self):
        self.x += duck_speed * self.direction
        if self.x <= 0 or self.x >= w - duck_w:
            self.direction *= -1

    def draw(self):
        screen.blit(duck_image, (self.x, self.y))


# Экран ввода имени
def get_player_name():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(w // 2 - 150, h // 2, 300, 50)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    active = False
    text = ""
    while True:
        screen.fill(WHITE)
        label = font.render("Введите имя:", True, (0, 0, 0))
        screen.blit(label, (w // 2 - 100, h // 2 - 50))
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
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


# Главное меню
def display_main_menu():
    global sound_on
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    last = None
    # Кнопка для просмотра результатов
    results_button = {"rect": pygame.Rect(10, 75, 270, 50), "label": "Прошлые результаты", "level": 5}
    pygame.display.set_caption("Тир")
    while True:
        screen.blit(background_image, (0, 0))
        title = font.render("Тир по уточкам", True, (255, 255, 255))
        screen.blit(title, (w // 2 - 100, 10))
        # Кнопки
        for button in buttons:
            pygame.draw.rect(screen, (0, 255, 0), button["rect"])
            label = button_font.render(button["label"], True, (0, 0, 0))
            screen.blit(label, (button["rect"].x + 10, button["rect"].y + 10))
        # Кнопка "Результаты"
        pygame.draw.rect(screen, (0, 255, 0), results_button["rect"])
        label = button_font.render(results_button["label"], True, (0, 0, 0))
        screen.blit(label, (results_button["rect"].x + 10, results_button["rect"].y + 10))
        # Кнопки с музыкой
        for button in music_buttons:
            pygame.draw.rect(screen, (200, 200, 200), button["rect"])
            label = button_font.render(button["label"], True, (0, 0, 0))
            screen.blit(label, (button["rect"].x + 10, button["rect"].y + 5))
        # Картинка кнопки для выключения/включения музыки
        if sound_on:
            screen.blit(sound_on_button, (w - 60, 10))
        else:
            screen.blit(sound_off_button, (w - 60, 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    pygame.quit()
                    exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button["rect"].collidepoint(pos) and button["level"] != 4:
                        return button["level"]
                    elif button["rect"].collidepoint(pos) and button["level"] == 4:
                        App.app()
                        pygame.quit()
                        exit()
                for button in music_buttons:
                    if button["rect"].collidepoint(pos):
                        pygame.mixer.music.load(button["file"])
                        pygame.mixer.music.play(-1)
                        last = pygame.mixer.music.play(-1)
                if sound_toggle_button.collidepoint(pos):
                    sound_on = not sound_on
                    if sound_on:
                        if last is not None:
                            pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                if results_button["rect"].collidepoint(pos):
                    display_results()  # Переход к окну результатов

# Экран с лучшими результатами
def display_results():
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    result_font = pygame.font.Font(None, 28)

    level_buttons = [
        {"rect": pygame.Rect(w // 2 - 100, 100, 200, 50), "label": "Уровень 1", "level": 1},
        {"rect": pygame.Rect(w // 2 - 100, 200, 200, 50), "label": "Уровень 2", "level": 2},
        {"rect": pygame.Rect(w // 2 - 100, 300, 200, 50), "label": "Уровень 3", "level": 3},
    ]
    back_button = pygame.Rect(w - 150, h - 70, 120, 50)

    selected_level = None

    while True:
        screen.blit(background_image, (0, 0))
        title = font.render("Результаты", True, (255, 255, 255))
        screen.blit(title, (w // 2 - 100, 10))

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
                result_text = f"{i + 1}. {name}: {score} очков, {time:.2f} сек"
                result_label = result_font.render(result_text, True, (255, 255, 255))
                screen.blit(result_label, (w // 2 - 150, y_offset))
                y_offset += 30

        pygame.display.flip()

        for event in pygame.event.get():
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
# Экран победы
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
    text_x = w // 2 - victory_text.get_width() // 2
    score_x = w // 2 - score_text.get_width() // 2
    time_x = w // 2 - time_text.get_width() // 2
    restart_x = w // 2 - restart_button.get_width() // 2
    exit_x = w // 2 - exit_button.get_width() // 2

    # Воспроизведение звука победы
    pobeda.play()

    # Основной цикл экрана победы
    running = True
    while running:
        screen.blit(win_image, (0, 0))  # Отрисовка фона
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
                    f()

                # Проверка нажатия на кнопку "Выход"
                if (exit_x <= mouse_pos[0] <= exit_x + exit_button.get_width() and
                    400 <= mouse_pos[1] <= 400 + exit_button.get_height()):
                    save_score(player_name, level, score, elapsed_time)  # Сохранение результата
                    running = False
                    pygame.quit()
                    exit()


# Сохранение счета в CSV
def save_score(player_name, level, score, elapsed_time):
    with open("game_scores_duck.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player_name, level, score, elapsed_time])

# Загрузка счета из CSV
def load_scores(level):
    scores = []
    with open("game_scores_duck.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[1]) == level:  # Проверяем уровень
                scores.append((row[0], int(row[2]), float(row[3])))  # Имя, счет, время
    # Сортируем по времени (чем меньше время, тем лучше)
    scores.sort(key=lambda x: x[2])
    return scores[:5]  # Возвращаем топ-5

# Основная игра
def main(level, player_name):
    lines, ducks_per_line = LEVELS[level]
    spacing = h // (lines + 1)
    ducks = [Duck(random.randint(0, w - duck_w), i * spacing) for i in range(1, lines + 1) for _ in
             range(ducks_per_line)]

    crosshair_x, crosshair_y = w // 2, h // 2
    crosshair_size = 40
    score = 0
    start_time = time.time()

    running = True
    while running:
        screen.blit(game_screen_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Выход по нажатию ESC
                    running = False
                if event.key == pygame.K_RETURN:
                    shoot_sound.play()
                    for duck in ducks:
                        if duck.x <= crosshair_x <= duck.x + duck_w and duck.y <= crosshair_y <= duck.y + duck_h:
                            impact.play()
                            ducks.remove(duck)
                            score += 1
                            break
        # Логика прицела
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and crosshair_x > 0:
            crosshair_x -= crosshair_speed
        if keys[pygame.K_RIGHT] and crosshair_x < w:
            crosshair_x += crosshair_speed
        if keys[pygame.K_UP] and crosshair_y > 0:
            crosshair_y -= crosshair_speed
        if keys[pygame.K_DOWN] and crosshair_y < h:
            crosshair_y += crosshair_speed

        for duck in ducks:
            duck.move()
            duck.draw()
        #Отрисовка прицела
        pygame.draw.line(screen, (255, 0, 0), (crosshair_x - crosshair_size // 2, crosshair_y),
                         (crosshair_x + crosshair_size // 2, crosshair_y), 2)
        pygame.draw.line(screen, (255, 0, 0), (crosshair_x, crosshair_y - crosshair_size // 2),
                         (crosshair_x, crosshair_y + crosshair_size // 2), 2)
        # Условие для победы
        if len(ducks) == 0:
            elapsed_time = int(time.time() - start_time)
            display_victory_screen(score, elapsed_time, player_name, level)
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def f():
    selected_level = display_main_menu()
    if selected_level:
        player_name = get_player_name()
        if player_name:
            main(selected_level, player_name)
