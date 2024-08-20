import random
import func

def move(dungeon_map: list[list[str]]) -> list[list[str]]:
    """
    Function to move the monsters on the dungeon map
    Args:
        dungeon_map (list[list[str]]): dungeon map
    Returns:
        list[list[str]]: dungeon map
    """

    directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

    # Crée une liste des positions des monstres
    monsters_to_move = list(func.monster_health.keys())

    for monster_pos in monsters_to_move:
        # Récupère les coordonnées du monstre
        x, y = map(int, monster_pos.split(","))

        # Choisis une direction aléatoire
        direction = random.choice(list(directions.keys()))
        dx, dy = directions[direction]

        new_x, new_y = x + dx, y + dy

        # Vérifie les limites de la carte et si la nouvelle position est un espace vide
        if (0 <= new_x < len(dungeon_map[0]) and 0 <= new_y < len(dungeon_map) and dungeon_map[new_y][new_x] == "."):
            # Déplace le monstre
            dungeon_map[new_y][new_x] = "M"
            dungeon_map[y][x] = "."

            # Met à jour la position du monstre dans monster_health
            func.monster_health[f"{new_x},{new_y}"] = func.monster_health.pop(f"{x},{y}")

    return dungeon_map
