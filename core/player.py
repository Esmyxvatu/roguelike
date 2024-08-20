import func
import logger
import time
import sys
import random
import pygame as pg
import gui

console = logger.Logger("out.log", "Player processus")

def move(dungeon_map: list[list[str]], direction: int, screen: pg.Surface) -> None:
    """
    Function to move the player on the dungeon map
    Args:
        dungeon_map (list[list[str]]): dungeon map
        direction (int): direction
        screen (pg.Surface): screen surface
    Returns:
        None
    """

    x, y = func.find_player_position(dungeon_map)
    new_x, new_y = x, y

    if direction == pg.K_UP or direction == pg.K_z:  # Haut
        new_y = y - 1
    elif direction == pg.K_DOWN or direction == pg.K_s:  # Bas
        new_y = y + 1
    elif direction == pg.K_LEFT or direction == pg.K_q:  # Gauche
        new_x = x - 1
    elif direction == pg.K_RIGHT or direction == pg.K_d:  # Droite
        new_x = x + 1

    if dungeon_map[new_y][new_x] == ".":
        dungeon_map[y][x] = "."
        dungeon_map[new_y][new_x] = "@"
        console.info("Player moved to " + str(new_x) + "," + str(new_y))

    if dungeon_map[new_y][new_x] == "M":
        func.monster_health[f"{new_x},{new_y}"]["health"] -= 3
        gui.draw_text(screen, f"You attacked the monster! Its health is now: {str(func.monster_health[f"{new_x},{new_y}"].get("health"))}", 0, 15)
        pg.display.flip()
        time.sleep(0.5)
        if int(func.monster_health[f"{new_x},{new_y}"].get("health")) <= 0:
            dungeon_map[new_y][new_x] = "."
            func.monster_health.pop(f"{new_x},{new_y}")
            gui.draw_text(screen, "You killed the monster!", 0, 15)
            pg.display.flip()
            console.info("Player killed a monster!")
            time.sleep(0.5)
        else:
            func.player_health -= int(func.monster_health[f"{new_x},{new_y}"].get("attack"))

            if func.player_health <= 0:
                gui.draw_text(screen, "You died!", 0, 15, (255, 0, 0))
                pg.display.flip()
                console.info("Player died!")
                time.sleep(0.5)
                sys.exit()

            gui.draw_text(screen, f"You were attacked by the monster! Your health is now: {str(func.player_health)}", 0, 15)
            pg.display.flip()
            time.sleep(0.5)

    if dungeon_map[new_y][new_x] == "T":
        dungeon_map[y][x] = "."
        item = random.choice(func.items)

        if item == "Potion":
            func.nb_potion += 1

        dungeon_map[new_y][new_x] = "@"
        gui.draw_text(screen, f"You found a {item}!", 0, 15, (0, 255, 0))
        pg.display.flip()
        console.info("Player found a " + item)
        time.sleep(0.5)
