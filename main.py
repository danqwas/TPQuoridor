import pygame
from queue import PriorityQueue
import time
# Dimensiones de la  pantalla y titulo
DIMENSIONES = 600
VENTANA = pygame.display.set_mode((DIMENSIONES, DIMENSIONES))
pygame.display.set_caption("Trabajo Parcial - Complejidad Algoritimica")

# Colores por defecto (global)
filas = 50
MARRON = (128, 64, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (128, 0, 128)
NARANJA = (255, 165, 0)
GRIS = (128, 128, 128)
TURQUESA = (64, 224, 208)


class Nodo:
    def __init__(self, fila, columna, ancho, total_filas):
        self.fila = fila
        self.columna = columna
        self.x = fila * ancho
        self.y = columna * ancho
        self.color = MARRON
        self.vecinos = []
        self.ancho = ancho
        self.total_filas = total_filas

    def getPosicion(self):
        return self.fila, self.columna

    def is_closed(self):
        return self.color == ROJO

    def is_open(self):
        return self.color == VERDE

    def is_barrier(self):
        return self.color == NEGRO

    def is_inicio(self):
        return self.color == NARANJA

    def is_final(self):
        return self.color == TURQUESA

    def reset(self):
        self.color = BLANCO

    def setInicio(self):
        self.color = NARANJA

    def make_closed(self):
        self.color = ROJO

    def make_open(self):
        self.color = VERDE

    def make_barrier(self):
        self.color = NEGRO

    def make_final(self):
        self.color = TURQUESA

    def construirCamino(self):
        self.color = MORADO

    def draw(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizarVecinos(self, mapa):
        self.vecinos = []
        if self.fila < self.total_filas - 1 and not mapa[self.fila + 1][self.columna].is_barrier():  # ABAJO
            self.vecinos.append(mapa[self.fila + 1][self.columna])

        if self.fila > 0 and not mapa[self.fila - 1][self.columna].is_barrier():  # ARRIBA
            self.vecinos.append(mapa[self.fila - 1][self.columna])

        if self.columna < self.total_filas - 1 and not mapa[self.fila][self.columna + 1].is_barrier():  # DERECHA
            self.vecinos.append(mapa[self.fila][self.columna + 1])

        if self.columna > 0 and not mapa[self.fila][self.columna - 1].is_barrier():  # IZQUIERDA
            self.vecinos.append(mapa[self.fila][self.columna - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruirCamino(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.construirCamino()
        draw()


def AStarAlgoritmo(draw, mapa, inicio, final):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    came_from = {}
    g_score = {celda: float("inf") for fila in mapa for celda in fila}
    g_score[inicio] = 0
    f_score = {celda: float("inf") for fila in mapa for celda in fila}
    f_score[inicio] = h(inicio.getPosicion(), final.getPosicion())

    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == final:
            reconstruirCamino(came_from, final, draw)
            final.make_final()
            return True

        for neighbor in current.vecinos:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.getPosicion(), final.getPosicion())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != inicio:
            current.make_closed()

    return False


def mapaJuego(filas, ancho):
    mapa = []
    brecha = ancho // filas
    for i in range(filas):
        mapa.append([])
        for j in range(filas):
            celda = Nodo(i, j, brecha, filas)
            mapa[i].append(celda)

    return mapa


def dibujarMapa(ventana, filas, ancho):
    brecha = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * brecha), (ancho, i * brecha))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * brecha, 0), (j * brecha, ancho))


def draw(ventana, mapa, filas, ancho):
    ventana.fill(BLANCO)

    for fila in mapa:
        for celda in fila:
            celda.draw(ventana)

    dibujarMapa(ventana, filas, ancho)
    pygame.display.update()


def get_clicked_pos(pos, filas, ancho):
    brecha = ancho // filas
    y, x = pos

    fila = y // brecha
    columna = x // brecha

    return fila, columna
#por testear
def BFS(draw, mapa, inicio, final):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    came_from = {}
    g_score = {celda: float("inf") for fila in mapa for celda in fila}
    g_score[inicio] = 0
    f_score = {celda: float("inf") for fila in mapa for celda in fila}
    f_score[inicio] = h(inicio.getPosicion(), final.getPosicion())

    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == final:
            reconstruirCamino(came_from, final, draw)
            final.make_final()
            return True

        for neighbor in current.vecinos:
            temp_g_score = g_score[current]+3
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.getPosicion(), final.getPosicion())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != inicio:
            current.make_closed()

    return False

def main(ventana, ancho):

    mapa = mapaJuego(filas, ancho)

    inicio = None
    final = None

    run = True
    while run:
        draw(ventana, mapa, filas, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                fila, columna = get_clicked_pos(pos, filas, ancho)
                celda = mapa[fila][columna]
                if not inicio and celda != final:
                    inicio = celda
                    inicio.setInicio()

                elif not final and celda != inicio:
                    final = celda
                    final.make_final()

                elif celda != final and celda != inicio:
                    celda.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                fila, columna = get_clicked_pos(pos, filas, ancho)
                celda = mapa[fila][columna]
                celda.reset()
                if celda == inicio:
                    inicio = None
                elif celda == final:
                    final = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and final:
                    for fila in mapa:
                        for celda in fila:
                            celda.actualizarVecinos(mapa)

                    t0 = time.time()
                    AStarAlgoritmo(lambda: draw(ventana, mapa, filas, ancho), mapa, inicio, final)
                    print(time.time()-t0)
                    t1=time.time()
                    BFS(lambda: draw(ventana, mapa, filas, ancho), mapa, inicio, final)
                    print(time.time() - t1)
                if event.key == pygame.K_c:
                    inicio = None
                    final = None
                    mapa = mapaJuego(filas, ancho)

    pygame.quit()


main(VENTANA, DIMENSIONES)
