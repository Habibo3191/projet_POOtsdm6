import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.skills = [
            Skill("Pistol", 1, 3, "damage", 3),
            Skill("Rifle", 2, 5, "damage", 5),
            Skill("Grenade", 3, 7, "damage", 4)
        ]

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw_health_bar(self, screen):
        """
        Dessine une barre de vie au-dessus de l'unité.
        """
        health_ratio = self.health / 10  # Suppose que la santé max est 10
        pygame.draw.rect(screen, (255, 0, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE - 5, CELL_SIZE, 5))  # Rouge
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.x * CELL_SIZE, self.y * CELL_SIZE - 5, CELL_SIZE * health_ratio, 5))  # Vert

    def draw(self, screen):
        """
        Dessine l'unité sur l'écran.
        """
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 3)
        self.draw_health_bar(screen)

class Skill:
    """
    Classe pour représenter une compétence.

    Attributs
    ---------
    name : str
        Nom de la compétence (ex. : "Pistol", "Rifle").
    range_min : int
        Portée minimale de la compétence.
    range_max : int
        Portée maximale de la compétence.
    effect : str
        Type d'effet de la compétence (ex. : "damage", "heal").
    power : int
        Puissance de l'effet (ex. : dégâts infligés).
    """

    def __init__(self, name, range_min, range_max, effect, power):
        self.name = name
        self.range_min = range_min
        self.range_max = range_max
        self.effect = effect
        self.power = power
