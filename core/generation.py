import random
import func
import logger

console = logger.Logger("out.log", "Map generator")

def generate_random_map(width: int, height: int, nb_monster: int, nb_tresor: int, difficulty: int) -> list[list[str]]:
    """
    Function to generate a random map
    Args:
        width (int): width of the map
        height (int): height of the map
        nb_monster (int): number of monsters
        nb_tresor (int): number of tresors
        difficulty (int): difficulty level
    Returns:
        list[list[str]]: dungeon map
    """

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


def find_open_areas(dungeon_map: list[list[str]]) -> list[tuple[int, int]]:
    """
    Function to find the open areas
    Args:
        dungeon_map (list[list[str]]): dungeon map
    Returns:
        list[tuple[int, int]]: list of open areas
    """

    open_areas = []
    for y, row in enumerate(dungeon_map):
        for x, tile in enumerate(row):
            if tile == ".":
                open_areas.append((x, y))
    return open_areas


def connect_points(dungeon_map: list[list[str]], points: list[tuple[int, int]]) -> list[list[str]]:
    """
    Connect the points in the dungeon map
    Args:
        dungeon_map (list[list[str]]): dungeon map
        points (list[tuple[int, int]]): list of points
    Returns:
        list[list[str]]: dungeon map
    """

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


def add_monster(dungeon_map: list[list[str]], nb_monster: int, difficulty: int) -> list[list[str]]:
    """
    Add the monster on the dungeon map
    Args:
        dungeon_map (list[list[str]]): dungeon map
        nb_monster (int): number of monsters
        difficulty (int): difficulty level
    Returns:
        list[list[str]]: dungeon map
    """

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


def add_tresor(dungeon_map: list[list[str]], nb_tresor: int) -> list[list[str]]:
    """
    Add the tresor on the dungeon map
    Args:
        dungeon_map (list[list[str]]): dungeon map
        nb_tresor (int): number of tresor
    Returns:
        list[list[str]]: dungeon map
    """

    while count_tresor(dungeon_map) < nb_tresor:
        x = random.randint(0, len(dungeon_map[0]) - 1)
        y = random.randint(0, len(dungeon_map) - 1)

        if dungeon_map[y][x] == ".":
            dungeon_map[y][x] = "T"
    return dungeon_map


def count_tresor(dungeon_map: list[list[str]]) -> int:
    """
    Count the number of tresor
    Args:
        dungeon_map (list[list[str]]): the map to count
    Returns:
        int: number of tresor
    """
    count = 0
    for row in dungeon_map:
        count += row.count("T")
    return count


def count_monsters(dungeon_map: list[list[str]]) -> int:
    """
    Count the number of monsters
    Args:
        dungeon_map (list[list[str]]): the map to count
    Returns:
        int: number of monsters
    """

    count = 0
    for row in dungeon_map:
        count += row.count("M")
    return count
