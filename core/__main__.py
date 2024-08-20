import func
import logger as log
import gui

import pygame as pg


# Initialisation de Pygame et des variables globales
pg.init()

screen = pg.display.set_mode((gui.constant["WIDTH"], gui.constant["HEIGHT"]))
pg.display.set_caption("Roguelike")


# Créer un logger
console = log.Logger("out.log", "Start processus")
open("out.log", "a").write("\n")


# Lancer le menu principal
menu_choice = gui.main_menu(screen)

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
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            else:
                dungeon_map = func.choose_action(dungeon_map, event.key, screen)
    pg.display.flip()

pg.quit()
