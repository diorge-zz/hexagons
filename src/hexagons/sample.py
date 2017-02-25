import pygame
import grid
import coordinate as coord
import random


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return pygame.Color(r, g, b, 255)


size = 50
window = 600
center_hex = coord.Axial(0, 0)
hex_format = 'flat'

g = grid.HexagonGrid(window, size, center_hex, hex_format=hex_format)
pygame.init()
display = pygame.display.set_mode((window, window), pygame.HWSURFACE)
running = True

colors = {}
for pt in center_hex.to_cube().circle_around(g.size):
    colors[pt] = random_color()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clicked = g.clicked_hex(pos)
            if clicked is not None:
                colors[clicked.to_cube()] = random_color()
    i = 0
    for c in g.all_centers():
        cn = tuple(grid.flat_corners(c, g.hex_size))
        ax = g.clicked_hex(c)
        pygame.draw.polygon(display, colors[ax.to_cube()], cn)
        i += 1
    pygame.display.flip()

pygame.quit()
