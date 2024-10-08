import time
import json
import pygame as pg
import random
import sys

import player     as p
import logger     as l
import monster    as m
import gui        as g
import generation as k

items = ["Potion", "Potion", "Potion"]

player_health = 20
monster_health = {} # { "x,y" : {"health": 5, "attack": 3} }
nb_potion = 0
level = 1
console = l.Logger("out.log", "Main processus")


def getInfo(dungeon_map: list[list[str]]) -> str:
    """
    Get the health of monster next to the player
    Args:
        dungeon_map (list[list[str]]): dungeon map
    Returns:
        str: text with monster(s) health
    """

    global monster_health
    text = ""

    x, y = find_player_position(dungeon_map)

    try:
        if dungeon_map[y][x+1] == "M":
            text += ", Health mob right : "+ str(monster_health[f"{x+1},{y}"].get("health"))
            return text
    except IndexError or KeyError:
        pass
    try:
        if dungeon_map[y][x-1] == "M":
            text += ", Health mob left : " + str(monster_health[f"{x-1},{y}"].get("health"))
    except IndexError or KeyError:
        pass
    try:
        if dungeon_map[y-1][x] == "M":
            text += ", Health mob up : " + str(monster_health[f"{x},{y-1}"].get("health"))
    except IndexError or KeyError:
        pass
    try:
        if dungeon_map[y+1][x] == "M":
            text += ", Health mob down : " + str(monster_health[f"{x},{y+1}"].get("health"))
    except IndexError or KeyError:
        pass

    return text


def find_player_position(dungeon_map: list[list[str]]) -> tuple[int, int]:
    """
    Get the position of the player
    Args:
        dungeon_map (list[list[str]]): dungeon map
    Returns:
        tuple[int, int]: position of the player
    """

    for y, row in enumerate(dungeon_map):
        for x, tile in enumerate(row):
            if tile == "@":
                return x, y


def run_game(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    Main function to run the game
    Args:
        screen (pg.Surface): screen surface
    Returns:
        bool: True if the game is running
    """

    # Initialisation ou réinitialisation des variables de jeu
    # dungeon_map = func.create_new_game(screen) ou autre fonction pour créer un nouveau jeu
    dungeon_map = create_new_game(screen)  # Exemple pour un nouveau jeu

    console.info("Starting game...")

    # Effacer l'écran
    screen.fill(g.color["WHITE"])

    # Dessiner la carte
    g.draw_map(screen, dungeon_map)

    # Mettre à jour l'affichage
    pg.display.flip()

    # Boucle de jeu principale
    last_update_time = time.time()
    running = True
    while running:
        last_update_time = l.set_caption(clock, last_update_time, 0.25)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                # Traiter les actions dans le jeu
                dungeon_map = choose_action(dungeon_map, event.key, screen, clock)

        clock.tick(g.constant["FPS"])
        pg.display.flip()

    return running


def main(screen: pg.Surface, clock: pg.time.Clock) -> None:
    """
    Function to start the game and manage the menu
    Args:
        screen (pg.Surface): screen surface
        clock (pg.time.Clock): clock
    Returns:
        None
    """

    while True:
        # Lancer le menu principal
        menu_choice = g.main_menu(screen, clock)

        if menu_choice == "new_game":
            if not run_game(screen, clock):
                break  # Sortir si l'utilisateur souhaite quitter

        elif menu_choice == "load_game":
            file_path = input("Enter the save file path: ")
            # Charger le jeu et lancer la boucle de jeu
            dungeon_map = load_game(file_path)
            console.info("Starting loaded game...")

            screen.fill(g.color["BLACK"])
            g.draw_map(screen, dungeon_map)
            pg.display.flip()

            if not run_game(screen, clock):
                break  # Sortir si l'utilisateur souhaite quitter

        elif menu_choice == "exit":
            pg.quit()
            sys.exit()


def choose_action(dungeon_map: list[list[str]], key:int, screen:pg.Surface, clock:pg.time.Clock) -> None:
    """
    Function to choose an action in the game
    Args:
        dungeon_map (list[list[str]]): dungeon map
        key (int): key pressed
        screen (pg.Surface): screen surface
        clock (pg.time.Clock): clock
    Returns:
        None
    """

    global player_health, nb_potion

    console.info("Moving monsters...")
    dungeon_map = m.move(dungeon_map)

    # Dessiner la carte
    g.draw_map(screen, dungeon_map)

    g.draw_text(screen, "Health : " + str(player_health) + ", Potion(s) : " + str(nb_potion) + getInfo(dungeon_map), 0, 0)
    pg.display.flip()

    if key == pg.K_ESCAPE :
        choice = g.option_menu(screen)
        if choice == "continue_game":
            pass
        elif choice == "save_game":
            save(dungeon_map, screen)
        elif choice == "return_home":
            main(screen, clock)
    elif key in [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_z, pg.K_q, pg.K_s, pg.K_d] :
        p.move(dungeon_map, key, screen)
    elif key == pg.K_u :
        console.info("Player using an item...")
        if nb_potion > 0 :
            player_health += 10
            nb_potion -= 1
            console.info("Potion used")
            g.draw_text(screen, "Potion used", 0, 15, (0, 255, 0))
            pg.display.flip()
        else :
            console.warning("No potion in inventory")
            g.draw_text(screen, "No potion in inventory", 0, 15, (255, 0, 0))
            pg.display.flip()
    else :
        console.warning("Invalid action : " + str(key))
        g.draw_text(screen, "Invalid action", 0, 15, (255, 0, 0))
        pg.display.flip()

    # Dessiner la carte
    g.draw_map(screen, dungeon_map)

    g.draw_text(screen, "Health : " + str(player_health) + ", Potion(s) : " + str(nb_potion) + getInfo(dungeon_map), 0, 0)

    return dungeon_map


def create_new_game(screen:pg.Surface, difficulty:int=level) -> list[list[str]]:
    """
    Function to create a new game
    Args:
        screen (pg.Surface): screen surface
        difficulty (int): difficulty level
    Returns:
        list[list[str]]: dungeon map
    """

    width = g.constant["WIDTH"] // g.constant["TILE_SIZE"]
    height = g.constant["HEIGHT"] // g.constant["TILE_SIZE"]
    nb_monster = random.randint(2, difficulty * 2)
    nb_tresor = max(3, int(nb_monster / 2))

    # Lancer l'animation dans un thread séparé
    g.loading_animation(screen, "Generating dungeon...")

    console.info("Generating random map with width={}, height={}, nb_monster={}, nb_tresor={}".format(width, height, nb_monster, nb_tresor))
    dungeon_map = k.generate_random_map(int(width), int(height), int(nb_monster), int(nb_tresor), difficulty)

    return dungeon_map


def load_game(file_path:str) -> list[list[str]]:
    """
    Load a game from a save file
    Args:
        file_path (str): save file path
    Returns:
        list[list[str]]: dungeon map
    """

    global dungeon_map, player_health, nb_potion, monster_health, level
    with open(file_path, "r") as f:
        json_map = f.read()
        json_list = json.loads(json_map)

        console.info("Loading game from save file...")

        dungeon_map = json_list["map"]
        nb_potion = json_list["player"]["potions"]
        player_health = json_list["player"]["health"]
        monster_health = json_list["ennemies"]
        level = json_list["level"]
        return dungeon_map


def save(dungeon_map: list[list[str]], screen:pg.Surface) -> None:
    """
    Save the game to a json file
    Args:
        dungeon_map (list[list[str]]): dungeon map
        screen (pg.Surface): screen surface
    Returns:
        None
    """

    with open("save.json", "w") as f:
        console.info("Saving game...")
        f.write(json.dumps({"map": dungeon_map, "player": {"health": player_health, "potions": nb_potion}, "ennemies": monster_health, "level": level}))
        console.info("Game saved to save.json")
        g.draw_text(screen, "Game saved", g.constant["WIDTH"] // 2 - 100, g.constant["HEIGHT"] // 2 - 20, (0, 255, 0), g.font["big"], None)
        pg.display.flip()
        time.sleep(0.5)
        exit()
