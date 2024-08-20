import pygame
import time
import sys
import logger

pygame.font.init()

constant = {
    "TILE_SIZE": 32,
    "WIDTH": 1280,
    "HEIGHT": 720,
    "FPS": 60
}
color = {
    "floor": (200, 200, 200),
    "wall": (0, 0, 0),
    "player": (0, 0, 255),
    "monster": (255, 0, 0),
    "treasure": (0, 255, 0),

    "WHITE":(255, 255, 255),
    "GRAY": (150, 150, 150),
    "BLACK": (0, 0, 0),
}
font = {
    "big":    pygame.font.Font(None, 74),
    "small":  pygame.font.Font(None, 36),
    "tiny":   pygame.font.Font(None, 24),
    "main":   pygame.font.Font("core/fonts/JetBrainsMono-Regular.ttf", 13),
}
images = {
    "background": pygame.transform.scale(pygame.image.load("core/textures/background.png"), (constant["WIDTH"], constant["HEIGHT"]))
}


def main_menu(screen: pygame.Surface, clock: pygame.time.Clock = pygame.time.Clock()) -> str:
    """
    Displays the main menu of the game, handling user input and rendering the menu buttons and text.
    Args:
        screen (pygame.Surface): The surface to render the menu on.
        clock (pygame.time.Clock): The clock to manage the game's framerate. Defaults to pygame.time.Clock().
    Returns:
        str: The user's selected action, either "new_game", "load_game", or None if the game is quit.
    """

    last_update_time = time.time()
    while True:
        clock.tick(constant["FPS"])
        screen.blit(images["background"], (0, 0))

        last_update_time = logger.set_caption(clock, last_update_time, 0.25)

        # Créer des boutons sous forme de rectangles
        new_game_button = pygame.Rect(constant["WIDTH"] // 2 - 150,  constant["HEIGHT"] // 2.5 - 50, 300, 50)
        load_game_button = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 + 20, 300, 50)
        quit_game_button = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 + 100, 300, 50)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    return "new_game"
                if load_game_button.collidepoint(event.pos):
                    return "load_game"
                if quit_game_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Dessiner les boutons
        pygame.draw.rect(screen, color["GRAY"], new_game_button)
        pygame.draw.rect(screen, color["GRAY"], load_game_button)
        pygame.draw.rect(screen, color["GRAY"], quit_game_button)

        # Dessiner le texte sur les boutons
        draw_text(
            screen,
            "Nouvelle Partie",
            new_game_button.x + 50,
            new_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )
        draw_text(
            screen,
            "Charger Partie",
            load_game_button.x + 50,
            load_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )
        draw_text(
            screen,
            "Quitter",
            quit_game_button.x + 50,
            quit_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )

        # Actualiser l'affichage
        pygame.display.flip()


def option_menu(screen: pygame.Surface, clock: pygame.time.Clock = pygame.time.Clock()) -> str:
    """
    Displays an option menu with buttons to continue the game, save and quit, return home, or quit the game.
    Parameters:
        screen (pygame.Surface): The surface on which the menu is displayed.
        clock (pygame.time.Clock): The clock used to control the frame rate. Defaults to pygame.time.Clock().
    Returns:
        str: A string indicating the user's choice, or None if the user quits the game.
    """

    last_update_time = time.time()
    while True:
        clock.tick(constant["FPS"])
        screen.blit(images["background"], (0, 0))
        last_update_time = logger.set_caption(clock, last_update_time, 0.25)

        # Créer des boutons sous forme de rectangles
        continue_game_button = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 - 50, 350, 50)
        save_game_button     = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 + 20, 350, 50)
        return_home_button   = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 + 80, 350, 50)
        quit_game_button     = pygame.Rect(constant["WIDTH"] // 2 - 150, constant["HEIGHT"] // 2.5 + 140, 350, 50)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_game_button.collidepoint(event.pos):
                    return "continue_game"
                if save_game_button.collidepoint(event.pos):
                    return "save_game"
                if return_home_button.collidepoint(event.pos):
                    return "return_home"
                if quit_game_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Dessiner les boutons
        pygame.draw.rect(screen, color["GRAY"], continue_game_button)
        pygame.draw.rect(screen, color["GRAY"], save_game_button)
        pygame.draw.rect(screen, color["GRAY"], return_home_button)
        pygame.draw.rect(screen, color["GRAY"], quit_game_button)

        # Dessiner le texte sur les boutons
        draw_text(
            screen,
            "Continuer",
            continue_game_button.x + 50,
            continue_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )
        draw_text(
            screen,
            "Sauvegarder et Quitter",
            save_game_button.x + 50,
            save_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )
        draw_text(
            screen,
            "Retour au menu",
            return_home_button.x + 50,
            return_home_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )
        draw_text(
            screen,
            "Quitter",
            quit_game_button.x + 50,
            quit_game_button.y + 10,
            color["BLACK"],
            font["small"],
            color["GRAY"],
        )

        # Actualiser l'affichage
        pygame.display.flip()


def loading_animation(screen: pygame.Surface, message: str, duration: int = 5, clock: pygame.time.Clock = pygame.time.Clock()) -> None:
    """
    Displays a loading animation on the screen with a given message and duration.
    Args:
        screen (pygame.Surface): The surface to render the animation on.
        message (str): The message to display during the animation.
        duration (int): The duration of the animation in seconds. Defaults to 5.
        clock (pygame.time.Clock): The clock to manage the game's framerate. Defaults to pygame.time.Clock().
    Returns:
        None
    """

    start_time = time.time()
    spinner = "|/-\\"
    spinner_index = 0
    last_update_time = time.time()

    while time.time() - start_time < duration:
        clock.tick(constant["FPS"])
        screen.blit(images["background"], (0, 0))
        last_update_time = logger.set_caption(clock, last_update_time, 0.25)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

        # Dessiner l'animation (texte de chargement avec spinner)
        draw_text(
            screen,
            spinner[spinner_index] + " " + message,
            constant["WIDTH"] // 2 - 100,
            constant["HEIGHT"] // 2 - 50,
            color["WHITE"],
            font["small"],
            None,
        )

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Passer au prochain caractère du spinner
        spinner_index = (spinner_index + 1) % len(spinner)
        time.sleep(0.1)  # Pause pour contrôler la vitesse du spinner


def draw_text(screen: pygame.Surface, text: str, x: int, y: int, color: tuple = (255, 255, 255), font: pygame.font.Font = font["main"], bg_color: tuple = (0, 0, 0)) -> None:
    """
    Draws text on the screen with a given color, font, and background color.
    Args:
        screen (pygame.Surface): The surface to render the text on.
        text (str): The text to draw.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        color (tuple, optional): The color of the text. Defaults to (255, 255, 255).
        font (pygame.font.Font, optional): The font of the text. Defaults to font["main"].
        bg_color (tuple, optional): The background color of the text. Defaults to (0, 0, 0).
    Returns:
        None
    """

    if bg_color is None:
        text_surface = font.render(text, True, color)
    else :
        text_surface = font.render(text, True, color, bg_color)
    screen.blit(text_surface, (x, y))


def draw_map(screen: pygame.Surface, dungeon_map: list[list[str]]) -> None:
    """
    Draws the map on the screen.
    Args:
        screen (pygame.Surface): The surface to render the map on.
        dungeon_map (list[list[str]]): The map to draw.
    Returns:
        None
    """

    COLOR_WALL = color["wall"]
    COLOR_FLOOR = color["floor"]
    COLOR_PLAYER = color["player"]
    COLOR_MONSTER = color["monster"]
    COLOR_TREASURE = color["treasure"]

    # Effacer l'écran
    screen.fill((0, 0, 0))

    for y, row in enumerate(dungeon_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * constant["TILE_SIZE"], y * constant["TILE_SIZE"], constant["TILE_SIZE"], constant["TILE_SIZE"])
            if tile == "#":
                pygame.draw.rect(screen, COLOR_WALL, rect)
            elif tile == ".":
                pygame.draw.rect(screen, COLOR_FLOOR, rect)
            elif tile == "@":
                pygame.draw.rect(screen, COLOR_PLAYER, rect)
            elif tile == "M":
                pygame.draw.rect(screen, COLOR_MONSTER, rect)
            elif tile == "T":
                pygame.draw.rect(screen, COLOR_TREASURE, rect)

    pygame.display.flip()