import func
import logger as log
import gui

import pygame as pg
import time


# Initialisation de Pygame et des variables globales
pg.init()

screen = pg.display.set_mode((gui.constant["WIDTH"], gui.constant["HEIGHT"]))
clock = pg.time.Clock()
pg.display.set_caption("Roguelike")


# Créer un logger
console = log.Logger("out.log", "Start processus")
open("out.log", "w").write("")


# Lancer le menu principal
menu_choice = gui.main_menu(screen, clock)

if menu_choice == "new_game":
    dungeon_map = func.create_new_game(screen)
elif menu_choice == "load_game":
    file_path = input("Enter the save file path: ")
    dungeon_map = func.load_game(file_path)

console.info("Starting game...")

# Effacer l'écran
screen.fill(gui.color["WHITE"])

# Dessiner la carte
gui.draw_map(screen, dungeon_map)

# Mettre à jour l'affichage
pg.display.flip()

# Boucle de jeu principale
last_update_time = time.time()
running = True
while running:
    last_update_time = log.set_caption(clock, last_update_time, 0.25)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            dungeon_map = func.choose_action(dungeon_map, event.key, screen)

    clock.tick(gui.constant["FPS"])
    pg.display.flip()

pg.quit()
