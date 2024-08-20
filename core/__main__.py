import pygame as pg

import logger as log
import func
import gui


# Initialisation de Pygame et des variables globales
pg.init()


screen = pg.display.set_mode((gui.constant["WIDTH"], gui.constant["HEIGHT"]))  # Remplacez par les valeurs de gui.constant
clock = pg.time.Clock()
pg.display.set_caption("Roguelike")


# Créer un logger
console = log.Logger("out.log", "Start processus")
open("out.log", "w").write("")


if __name__ == "__main__":
    func.main(screen, clock)
