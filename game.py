import pygame
import random

from unit import *


# Ajouter un nouveau type de classe pour gérer les cases
class Cell:
    def __init__(self, x, y, cell_type):
        """
        Initialise une case avec ses coordonnées et son type.

        Paramètres
        ----------
        x : int
            Coordonnée x sur la grille.
        y : int
            Coordonnée y sur la grille.
        cell_type : str
            Type de la case ("traversable", "non_traversable").
        """
        self.x = x
        self.y = y
        self.cell_type = cell_type

    def draw(self, screen):
        """
        Dessine la case sur l'écran avec des couleurs différentes en fonction de son type.
        """
        if self.cell_type == "traversable":
            color = (144, 238, 144)  # Vert clair
        elif self.cell_type == "non_traversable":
            color = (220, 20, 60)  # Rouge foncé
        else:
            color = (211, 211, 211)  # Gris clair (par défaut)

        # Dessiner la case
        pygame.draw.rect(
            screen,
            color,
            (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )


# Ajouter une grille au jeu
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.grid = [
            [Cell(x, y, "traversable" if random.random() > 0.2 else "non_traversable")
             for y in range(GRID_SIZE)]
            for x in range(GRID_SIZE)
        ]
        self.player_units = [Unit(0, 0, 10, 2, "player")]
        self.enemy_units = [Unit(6, 6, 8, 1, "enemy")]

    def flip_display(self):
        """
        Met à jour l'affichage du jeu, y compris la grille et les unités.
        """
        self.screen.fill(BLACK)

        # Afficher la grille
        for row in self.grid:
            for cell in row:
                cell.draw(self.screen)

        # Afficher les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):

        self.grid=[
            [Cell(x,y,"traversable" if random.random()>0.2 else "non_traversable")
             for y in range (GRID_SIZE)]
            for x in range(GRID_SIZE)
        ]
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy')]

    def handle_player_turn(self):
        """
        Gère le tour du joueur.
        Permet au joueur de déplacer une unité ou d'utiliser une compétence.
        """
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True

            # Position initiale du curseur
            cursor_x, cursor_y = selected_unit.x, selected_unit.y

            while not has_acted:
                # Afficher la grille et les unités
                self.flip_display()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches
                    if event.type == pygame.KEYDOWN:
                        # Déplacement du curseur
                        if event.key == pygame.K_LEFT and cursor_x > 0:
                            cursor_x -= 1
                        elif event.key == pygame.K_RIGHT and cursor_x < GRID_SIZE - 1:
                            cursor_x += 1
                        elif event.key == pygame.K_UP and cursor_y > 0:
                            cursor_y -= 1
                        elif event.key == pygame.K_DOWN and cursor_y < GRID_SIZE - 1:
                            cursor_y += 1

                        # Validation du déplacement
                        elif event.key == pygame.K_SPACE:
                            if (cursor_x, cursor_y) in self.get_accessible_cells(selected_unit):
                                self.move_unit(selected_unit, cursor_x, cursor_y)
                                has_acted = True  # Fin du tour
                                selected_unit.is_selected = False

                        # Gestion des compétences avec des lettres
                        elif event.key in [pygame.K_a, pygame.K_b, pygame.K_c]:
                            skill_index = {'a': 0, 'b': 1, 'c': 2}[pygame.key.name(event.key)]
                            if 0 <= skill_index < len(selected_unit.skills):
                                selected_skill = selected_unit.skills[skill_index]
                                self.target_with_skill(selected_unit, selected_skill)
                                has_acted = True  # Fin du tour
                                selected_unit.is_selected = False

                    # Dessiner le curseur
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 255),  # Bleu vif
                        (cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        3  # Épaisseur
                    )

                    pygame.display.flip()

    def target_with_skill(self, unit, skill):
        """
        Permet au joueur de cibler une case avec une compétence.

        Paramètres
        ----------
        unit : Unit
            L'unité qui utilise la compétence.
        skill : Skill
            La compétence utilisée.
        """
        targeting = True
        cursor_x, cursor_y = unit.x, unit.y

        # Calculer les cases ciblables
        targetable_cells = self.get_targetable_cells(unit, skill)

        while targeting:
            self.flip_display()

            # Afficher les cases ciblables en jaune
            for x, y in targetable_cells:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 0),  # Jaune
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    3  # Contour épais
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Déplacer le curseur
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and cursor_x > 0:
                        cursor_x -= 1
                    elif event.key == pygame.K_RIGHT and cursor_x < GRID_SIZE - 1:
                        cursor_x += 1
                    elif event.key == pygame.K_UP and cursor_y > 0:
                        cursor_y -= 1
                    elif event.key == pygame.K_DOWN and cursor_y < GRID_SIZE - 1:
                        cursor_y += 1

                    # Valider la cible
                    if event.key == pygame.K_SPACE:
                        if (cursor_x, cursor_y) in targetable_cells:
                            self.apply_skill_effect(unit, cursor_x, cursor_y, skill)
                            targeting = False

            # Dessiner le curseur en rouge
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),  # Rouge
                (cursor_x * CELL_SIZE, cursor_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3
            )
            pygame.display.flip()

    def draw_accessible_cells(self, accessible_cells):
        """
        Dessine une surbrillance sur les cases accessibles.

        Paramètres
        ----------
        accessible_cells : list[tuple[int, int]]
            Liste des coordonnées des cases accessibles.
        """
        for x, y in accessible_cells:
            pygame.draw.rect(
                self.screen,
                (30, 144, 255),  # Bleu clair pour les cases accessibles
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3  # Épaisseur du contour
            )

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)



    def get_accessible_cells(self, unit ,max_distance=3):
        accessible_cells =[]
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                x, y = unit.x + dx, unit.y + dy
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    cell = self.grid[x][y]
                    if cell.cell_type == "traversable":
                        accessible_cells.append((x, y))
        return accessible_cells

    def draw_accessible_cells(self, accessible_cells):
        """
        Dessine les cases accessibles sur la grille.

        Paramètres
        ----------
        accessible_cells : list[tuple[int, int]]
            Liste des coordonnées des cases accessibles.
        """
        for x, y in accessible_cells:
            pygame.draw.rect(
                self.screen,
                (173, 216, 230),  # Couleur bleu pâle
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    def move_unit(self, unit, target_x, target_y):
        """
        Déplace une unité vers une case cible si elle est accessible.

        Paramètres
        ----------
        unit : Unit
            L'unité à déplacer.
        target_x : int
            Coordonnée x de la case cible.
        target_y : int
            Coordonnée y de la case cible.
        """
        # Vérifier les cases accessibles autour de l'unité
        accessible_cells = self.get_accessible_cells(unit)
        if (target_x, target_y) in accessible_cells:
            self.animate_move(unit ,target_x,target_y)
            unit.x = target_x
            unit.y = target_y
            self.flip_display()

    def draw_skills(self, unit):
        """
        Affiche les compétences disponibles pour une unité.

        Paramètres
        ----------
        unit : Unit
            L'unité sélectionnée.
        """
        font = pygame.font.SysFont("monospace", 20)
        skill_keys = ['A', 'B', 'C']  # Lettres associées aux compétences
        for i, skill in enumerate(unit.skills):
            skill_text = f"{skill_keys[i]}: {skill.name} (Range: {skill.range_min}-{skill.range_max})"
            text_surface = font.render(skill_text, True, WHITE)
            self.screen.blit(text_surface, (10, 10 + i * 25))

    def flip_display(self):
        """
        Met à jour l'affichage du jeu, y compris la grille, les unités et les compétences.
        """
        # Remplir l'écran avec une couleur de fond (noir)
        self.screen.fill(BLACK)

        # Dessiner la grille
        for row in self.grid:
            for cell in row:
                cell.draw(self.screen)  # Assurez-vous que chaque case est dessinée avec ses propriétés (couleur).

        # Dessiner les unités


        if self.player_units:
            selected_unit = self.player_units[0]  # Exemple : première unité sélectionnée
            accessible_cells = self.get_accessible_cells(selected_unit)
            self.draw_accessible_cells(accessible_cells)
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Dessiner les compétences disponibles si une unité est sélectionnée

        if self.player_units:
            self.draw_skills(self.player_units[0])
        # Rafraîchir l'écran
        pygame.display.flip()

    def animate_move(self, unit, target_x, target_y):
        """
        Anime le déplacement d'une unité vers une case cible.

        Paramètres
        ----------
        unit : Unit
            L'unité à déplacer.
        target_x : int
            Coordonnée x cible (en cases).
        target_y : int
            Coordonnée y cible (en cases).
        """
        start_x, start_y = unit.x * CELL_SIZE, unit.y * CELL_SIZE
        end_x, end_y = target_x * CELL_SIZE, target_y * CELL_SIZE
        steps = 10  # Nombre de frames pour l'animation

        for step in range(steps):
            # Calculer la position intermédiaire
            current_x = start_x + (end_x - start_x) * (step + 1) / steps
            current_y = start_y + (end_y - start_y) * (step + 1) / steps

            # Redessiner la grille et l'unité
            self.flip_display()
            pygame.draw.circle(
                self.screen,
                (0, 255, 0),  # Vert clair pour l'unité en déplacement
                (int(current_x + CELL_SIZE // 2), int(current_y + CELL_SIZE // 2)),
                CELL_SIZE // 3
            )
            pygame.display.flip()
            pygame.time.delay(30)  # Délai entre les frames

        # Mettre à jour la position finale de l'unité
        unit.x = target_x
        unit.y = target_y

    def get_targetable_cells(self, unit, skill):
        """
        Retourne les cases ciblables pour une unité en fonction de la portée de la compétence.

        Paramètres
        ----------
        unit : Unit
            L'unité qui utilise la compétence.
        skill : Skill
            La compétence utilisée.

        Retourne
        --------
        list[tuple[int, int]]
            Liste des coordonnées des cases ciblables.
        """
        targetable_cells = []
        for dx in range(-skill.range_max, skill.range_max + 1):
            for dy in range(-skill.range_max, skill.range_max + 1):
                x, y = unit.x + dx, unit.y + dy
                distance = abs(dx) + abs(dy)  # Distance de Manhattan
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    if skill.range_min <= distance <= skill.range_max:
                        targetable_cells.append((x, y))
        return targetable_cells

    def apply_skill_effect(self, unit, target_x, target_y, skill):
        """
        Applique l'effet d'une compétence à la cible.

        Paramètres
        ----------
        unit : Unit
            L'unité qui utilise la compétence.
        target_x : int
            Coordonnée x de la cible.
        target_y : int
            Coordonnée y de la cible.
        skill : Skill
            La compétence utilisée.
        """
        for enemy in self.enemy_units:
            if enemy.x == target_x and enemy.y == target_y:
                enemy.health -= skill.power
                if enemy.health <= 0:
                    self.enemy_units.remove(enemy)  # Retirer l'ennemi s'il n'a plus de santé


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
