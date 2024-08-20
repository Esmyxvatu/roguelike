import random
import func
import logger

console = logger.Logger("out.log", "Map generator")

def generate_random_map(width, height, nb_monster, nb_tresor, difficulty):
    console.info("Generating random map...")
    dungeon_map = [["#" for _ in range(width)] for _ in range(height)]
    for _ in range(5):  # Créer 5 pièces aléatoires
        room_width = random.randint(3, 6)
        room_height = random.randint(3, 6)
        x = random.randint(1, width - room_width - 1)
        y = random.randint(1, height - room_height - 1)

        for i in range(room_height):
            for j in range(room_width):
                dungeon_map[y + i][x + j] = "."

    # Placer le joueur dans la première pièce
    console.info("Placing player...")
    dungeon_map[y + 1][x + 1] = "@"

    console.info("Connecting points...")
    open_areas = find_open_areas(dungeon_map)
    connected = connect_points(dungeon_map, open_areas)

    console.info("Adding monsters and tresors...")
    connected = add_monster(connected, nb_monster, difficulty)
    connected = add_tresor(connected, nb_tresor)

    return connected


def find_open_areas(dungeon_map):
    open_areas = []
    for y, row in enumerate(dungeon_map):
        for x, tile in enumerate(row):
            if tile == ".":
                open_areas.append((x, y))
    return open_areas


def connect_points(dungeon_map, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        # Relier horizontalement
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if dungeon_map[y1][x] == "#":
                dungeon_map[y1][x] = "."

        # Relier verticalement
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if dungeon_map[y][x2] == "#":
                dungeon_map[y][x2] = "."

    return dungeon_map


def add_monster(dungeon_map, nb_monster, difficulty):
    while count_monsters(dungeon_map) < nb_monster:
        x = random.randint(0, len(dungeon_map[0]) - 1)
        y = random.randint(0, len(dungeon_map) - 1)

        if dungeon_map[y][x] == ".":
            dungeon_map[y][x] = "M"
            func.monster_health[f"{x},{y}"] = {
                "health": random.randint(5, difficulty*10+5),
                "attack": random.randint(2, difficulty*4),
            }

    return dungeon_map


def add_tresor(dungeon_map, nb_tresor):
    while count_tresor(dungeon_map) < nb_tresor:
        x = random.randint(0, len(dungeon_map[0]) - 1)
        y = random.randint(0, len(dungeon_map) - 1)

        if dungeon_map[y][x] == ".":
            dungeon_map[y][x] = "T"
    return dungeon_map


def count_tresor(dungeon_map):
    count = 0
    for row in dungeon_map:
        count += row.count("T")
    return count


def count_monsters(dungeon_map):
    count = 0
    for row in dungeon_map:
        count += row.count("M")
    return count
