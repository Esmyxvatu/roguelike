import time
import json
import pygame as pg
import random

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


def getInfo(dungeon_map):
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


def find_player_position(dungeon_map):
    for y, row in enumerate(dungeon_map):
        for x, tile in enumerate(row):
            if tile == "@":
                return x, y


def choose_action(dungeon_map, key, screen) :
    global player_health, nb_potion

    console.info("Moving monsters...")
    dungeon_map = m.move(dungeon_map)

    # Dessiner la carte
    g.draw_map(screen, dungeon_map)

    g.draw_text(screen, "Health : " + str(player_health) + ", Potion(s) : " + str(nb_potion) + getInfo(dungeon_map), 0, 0)
    pg.display.flip()

    if key == pg.K_ESCAPE :
        console.info("Quitting game...")
        exit(0)
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
    elif key == pg.K_RETURN :
        save(dungeon_map, screen)
    else :
        console.warning("Invalid action : " + str(key))
        g.draw_text(screen, "Invalid action", 0, 15, (255, 0, 0))
        pg.display.flip()

    # Dessiner la carte
    g.draw_map(screen, dungeon_map)

    g.draw_text(screen, "Health : " + str(player_health) + ", Potion(s) : " + str(nb_potion) + getInfo(dungeon_map), 0, 0)

    return dungeon_map


def create_new_game(screen, difficulty=level):
    width = g.constant["WIDTH"] // 32
    height = g.constant["HEIGHT"] // 32
    nb_monster = random.randint(2, difficulty * 2)
    nb_tresor = max(3, int(nb_monster / 2))

    # Lancer l'animation dans un thread séparé
    g.loading_animation(screen, "Generating dungeon...")

    console.info("Generating random map with width={}, height={}, nb_monster={}, nb_tresor={}".format(width, height, nb_monster, nb_tresor))
    dungeon_map = k.generate_random_map(int(width), int(height), int(nb_monster), int(nb_tresor), difficulty)

    return dungeon_map


def load_game(file_path):
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


def save(dungeon_map, screen):
    with open("save.json", "w") as f:
        console.info("Saving game...")
        f.write(json.dumps({"map": dungeon_map, "player": {"health": player_health, "potions": nb_potion}, "ennemies": monster_health, "level": level}))
        console.info("Game saved to save.json")
        g.draw_text(screen, "Game saved", 0, 15, (0, 255, 0))
        pg.display.flip()
        time.sleep(0.5)
        exit()
