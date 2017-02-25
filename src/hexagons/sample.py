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
g = grid.HexagonGrid(600, size, coord.Axial(0, 0), hex_format='flat')
pygame.init()
display = pygame.display.set_mode((600, 600), pygame.HWSURFACE)
running = True
n = len(list(g.all_centers()))
colors = []
for i in range(n):
    colors.append(random_color())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(g.clicked_hex(pos))
    i = 0
    for c in g.hexagon_list():
        pygame.draw.polygon(display, colors[i], c)
        i += 1
    pygame.display.flip()

pygame.quit()
