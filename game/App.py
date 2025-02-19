import zmeika
import PeregaSirat
import pygame


# Параметры окна
w, h = 800, 600
back = pygame.image.load("razryvnaya.png")
back = pygame.transform.scale(back, (w, h))
screen = pygame.display.set_mode((w, h))
buttons = [
    {"label": "Уточка", "rect": pygame.Rect(60, 230, 150, 70), "level": 1},
    {"label": "Змейка", "rect": pygame.Rect(550, 230, 150, 70), "level": 2},
]
# Главный экран
def main_menu1():
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 36)
    pygame.display.set_caption("Приложение")

    while True:
        screen.blit(back, (0, 0))
        title = font.render("Выберите уровень", True, (255, 255, 255))
        screen.blit(title, (w // 2 - title.get_width() // 2, 50))

        for button in buttons:
            pygame.draw.rect(screen, (0, 255, 0), button["rect"])
            label = button_font.render(button["label"], True, (0, 0, 0))
            screen.blit(label, (button["rect"].x + 10, button["rect"].y + 10))

        text = font.render("Управление:", True, (0, 255, 0))
        screen.blit(text, (280 , 310))

        text1 = font.render("Стрелочки", True, (0, 255, 0))
        screen.blit(text1, (30 , 350))
        text1 = font.render("для передвижения", True, (0, 255, 0))
        screen.blit(text1, (30 , 380))
        text1 = font.render("Enter", True, (0, 255, 0))
        screen.blit(text1, (30, 410))
        text1 = font.render("для стрельбы", True, (0, 255, 0))
        screen.blit(text1, (30, 440))
        text2 = font.render("Стрелочки", True, (0, 255, 0))
        screen.blit(text2, (465, 350))
        text2 = font.render("для передвижения", True, (0, 255, 0))
        screen.blit(text2, (465, 380))
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
                    if button["rect"].collidepoint(pos):
                        return button["level"]

def main_menu(level):
    if level == 1:
        PeregaSirat.f()
        return
        # Запуск игры "Утки"
    elif level == 2:
        zmeika.main()
        return
        # Запуск игры "Змейка"

def app():
    main_menu(main_menu1())


if __name__ == "__main__":
    app()